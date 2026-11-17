import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from diagnose import diagnose,load_models,parse_parameters

def test_sample_findings():
    root=Path(__file__).resolve().parents[1]
    findings=diagnose(load_models(root/"data/cad_models.csv"))
    codes={f["code"] for f in findings}
    assert "UNRESOLVED_REFERENCE" in codes
    assert "MISSING_PARAMETER" in codes
    assert "REGENERATION_FAILURE" in codes
    assert "REGENERATION_WARNING" in codes

def test_clean_model():
    rows=[{"model_id":"P-1","model_type":"part","parameters":"MATERIAL=STEEL;REV=A","references":"","regeneration_status":"OK"}]
    assert diagnose(rows)==[]

def test_bad_parameter():
    with pytest.raises(ValueError):parse_parameters("INVALID")

def test_duplicate_ids(tmp_path):
    p=tmp_path/"dupes.csv"
    p.write_text("model_id,model_type,parameters,references,regeneration_status\nX,part,MATERIAL=STEEL;REV=A,,OK\nX,part,MATERIAL=STEEL;REV=A,,OK\n")
    with pytest.raises(ValueError):load_models(p)


def test_cli_generates_report(tmp_path):
    """The runnable entry point works even outside the repository directory."""
    import json
    import subprocess

    project_root = Path(__file__).resolve().parents[1]
    report_file = tmp_path / "report.json"
    result = subprocess.run(
        [sys.executable, str(project_root / "main.py"), "--output", str(report_file)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert report["count"] == 4
    assert "UNRESOLVED_REFERENCE" in {f["code"] for f in report["findings"]}


def test_cli_invalid_input_exits_cleanly(tmp_path):
    """Missing input produces a readable error and a nonzero exit code."""
    import subprocess

    project_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, str(project_root / "main.py"), "--input", str(tmp_path / "absent.csv")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "CAD diagnostic error:" in result.stderr
