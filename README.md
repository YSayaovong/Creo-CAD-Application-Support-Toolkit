# Creo CAD Application Support Toolkit

**Engineering systems support | Technical triage | CAD metadata validation**

A Python **offline simulator** that analyzes synthetic Creo-like model metadata exports. It demonstrates structured troubleshooting of engineering application issues without requiring Creo installation or access to company systems.

## Support scenario
An engineering application support analyst receives model metadata indicating missing parameters, broken references or regeneration warnings. The analyst needs a consistent triage report and investigation checklist.

## Implemented checks
- Input schema and duplicate model IDs
- Required `MATERIAL` and `REV` parameters
- References to model IDs absent from the provided export
- Regeneration states: `OK`, `WARNING`, `FAILED`
- JSON report with suggested next investigation steps
- Automated tests and synthetic sample data

## Run the demonstration
```bash
python -m pip install -r requirements.txt
python src/diagnose.py --input data/cad_models.csv --output reports/cad_diagnostics.json
pytest -q
```

## Input contract
```text
model_id,model_type,parameters,references,regeneration_status
```
Parameters use semicolon-separated `KEY=VALUE` pairs; references are semicolon-separated model IDs.

## How to interpret the report
Treat findings as **triage leads**, not confirmed root causes. For example, a missing referenced model might indicate an incomplete export rather than a broken assembly. A real support investigation would confirm the issue in an authorized engineering environment and document the resolution.

## Boundaries
**Not a Creo plugin.** The tool does not read native Creo files, invoke regeneration, call Creo APIs, access Windchill/SAP/TDMS or diagnose live production models. All inputs are synthetic and contain no employer data.

**Relevant roles:** Engineering Systems Support Analyst, CAD Application Support Analyst, PLM Support Analyst.

[Related engineering change tracker](https://github.com/YSayaovong/Engineering-Change-Revision-Tracker) · [Portfolio website repository](https://github.com/YSayaovong/operations-analytics-portfolio)
