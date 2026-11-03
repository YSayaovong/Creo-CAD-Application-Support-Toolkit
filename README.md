# Creo CAD Application Support Toolkit

Offline diagnostics for **synthetic Creo-like model metadata exports**. Demonstrates how a CAD application support specialist can triage missing parameters, unresolved references, regeneration failures, and warnings.

## Features
- Validates CSV input schema and duplicate model IDs
- Checks required `MATERIAL` and `REV` parameters
- Flags unresolved model references
- Flags failed or warning regeneration status
- Writes a JSON report with suggested investigation steps
- Includes automated tests and synthetic sample data

## Run
```bash
pip install -r requirements.txt
python src/diagnose.py --input data/cad_models.csv --output reports/cad_diagnostics.json
pytest -q
```

## Input schema
`model_id,model_type,parameters,references,regeneration_status`

Parameters use semicolon-separated `KEY=VALUE` pairs. References are semicolon-separated model IDs. Regeneration status is `OK`, `WARNING`, or `FAILED`.

## Important scope limitations
This is a **portfolio simulator**, not a Creo Parametric plugin. It does **not** read Creo native files, execute Creo regeneration, call Creo APIs, connect to Windchill/SAP/TDMS, or diagnose live workplace models. Missing references may reflect an incomplete CSV export, not a broken CAD assembly. The sample is synthetic and contains no employer data.
