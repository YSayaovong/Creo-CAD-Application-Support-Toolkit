# Creo CAD Configuration Validation Toolkit

**Engineering Configuration Analysis | CAD Metadata Quality | Revision Integrity | Configuration-Control Readiness**

A Python-based **offline portfolio demonstration** for reviewing synthetic Creo-like CAD metadata exports. The toolkit identifies inconsistencies that a configuration analyst would investigate before accepting engineering model information as reliable for a controlled product baseline.

The focus is on **configuration data integrity**, not CAD modeling or live application administration. The tool applies repeatable checks and produces a JSON exception report to support human review, follow-up, and documentation.

## Configuration analysis scenario

An Engineering Configuration Analyst receives a structured export representing a set of CAD models and their relationships. Before the information can be used in downstream engineering or configuration-control processes, the analyst checks that:

- Each model has a unique, nonblank identifier.
- Required metadata fields are present and correctly formatted.
- Required `MATERIAL` and revision (`REV`) parameters exist.
- Referenced model IDs are included in the supplied export.
- Regeneration status does not indicate a warning or failure requiring investigation.

These checks help surface potential configuration-record exceptions early. **A flagged exception is not proof of a defective released configuration.** For example, an unresolved reference may simply mean the supplied export is incomplete.

## Implemented checks

| Control area | Validation | Reported result |
|---|---|---|
| Record integrity | Required CSV columns, nonblank model IDs, duplicate model IDs | Invalid input raises a validation error |
| Parameter integrity | Malformed or duplicate `KEY=VALUE` parameters | `INVALID_PARAMETER_FORMAT` |
| Required metadata | Missing `MATERIAL` or `REV` | `MISSING_PARAMETER` |
| Model relationships | Referenced model ID absent from the current export | `UNRESOLVED_REFERENCE` |
| Model health indicator | Regeneration status is `WARNING` or `FAILED` | `REGENERATION_WARNING` or `REGENERATION_FAILURE` |
| Status consistency | Status other than `OK`, `WARNING`, or `FAILED` | `UNKNOWN_REGEN_STATUS` |

The tool writes each finding with model ID, issue code, severity, details, and a suggested next investigation step. Its automated tests cover several normal and exception scenarios.

## Example synthetic dataset

The included `data/cad_models.csv` intentionally contains:
- An assembly with relationships to part records.
- A part missing `MATERIAL` and referencing a model not in the export.
- A model marked with failed regeneration.
- A model marked with a regeneration warning.

This permits repeatable demonstration of configuration data checks without using real engineering or employer information.

## How to run

Requires Python and the packages in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python src/diagnose.py --input data/cad_models.csv --output reports/cad_diagnostics.json
pytest -q
```

Input columns:

```text
model_id,model_type,parameters,references,regeneration_status
```

`parameters` uses semicolon-delimited `KEY=VALUE` entries; `references` uses semicolon-delimited model IDs.

## Engineering Configuration Analyst workflow

1. **Collect** a controlled, authorized metadata export and confirm its intended scope.
2. **Validate** record uniqueness, required attributes, revision presence, dependencies, and status fields.
3. **Classify** exceptions by severity and distinguish incomplete export data from possible engineering issues.
4. **Investigate** flagged items against the authoritative engineering system and applicable processes.
5. **Document** findings, responsible owners, decisions, and closure evidence in a separate controlled workflow.
6. **Confirm** the approved baseline only in the organization's authorized PLM/PDM or change-control system.

**Steps 1–3 are illustrated by the offline program; steps 4–6 describe a real-world analyst workflow and are not automated by this repository.**

## Scope and limitations

- This is **not** a Creo plugin and does not read native Creo model files or execute regeneration.
- It does **not** connect to Windchill, SAP, other PLM/PDM systems, or production engineering environments.
- Presence of `REV` is checked; the program does **not** compare revisions against approved baselines, effectivity records, or engineering change orders.
- The program does **not** manage ECO/ECN approvals, release gates, audit trails, configuration status accounting, or manufacturing BOM reconciliation.
- Model references are checked only against the records provided in the CSV.
- All provided sample data is synthetic; no confidential employer data is used.

## Skills demonstrated

**Configuration data validation · Engineering record integrity · Revision metadata checks · Dependency analysis · Exception reporting · Risk-based review · Python automation · Automated testing · Engineering documentation**

## Potential next enhancements (not implemented)

1. Approved baseline vs. candidate revision comparison.
2. Synthetic engineering change requests with approval and release statuses.
3. Engineering BOM reconciliation and missing/extra component identification.
4. Configuration audit history and exception closure tracking.
5. CSV-based configuration status accounting dashboard.

## Related project

[Engineering Change & Revision Tracker](https://github.com/YSayaovong/Engineering-Change-Revision-Tracker) — a separate portfolio project for engineering change and revision workflows.

---

**Portfolio positioning:** A controlled-data quality and exception-analysis exercise relevant to **Engineering Configuration Analyst**, **Configuration Management Analyst**, and **Engineering Change Analyst** roles. It demonstrates transferable analysis practices without suggesting live PLM administration or production release authority.
