# Creo CAD Configuration Validation Toolkit

**CAD configuration data validation · Revision metadata · Model dependency checks · Exception reporting**

## Project overview

The Creo CAD Configuration Validation Toolkit is a Python command-line utility that evaluates structured, synthetic CAD metadata exports for record integrity and potential configuration discrepancies.

Engineering configuration records depend on consistent model identifiers, required attributes, revision metadata, and traceable relationships between parts and assemblies. Incomplete or inconsistent data can complicate downstream engineering reviews. This project demonstrates how repeatable validation rules can identify records that require further investigation before the information is relied upon.

The utility reads a CSV export, evaluates each model against a defined set of checks, and writes a machine-readable JSON findings report. It operates independently of Creo and enterprise PLM systems.

## Validation process

1. **Load the export.** Verify that required columns exist and that model identifiers are populated and unique.
2. **Parse model parameters.** Interpret semicolon-delimited `KEY=VALUE` attributes and identify malformed or duplicate entries.
3. **Check required attributes.** Identify records missing `MATERIAL` or `REV` parameters.
4. **Evaluate model references.** Compare referenced model identifiers with the identifiers included in the supplied export.
5. **Review regeneration indicators.** Flag `WARNING`, `FAILED`, or unrecognized regeneration statuses reported by the input data.
6. **Generate an exception report.** Record the affected model, issue code, severity, explanation, and recommended investigation step.

## Validation rules and outputs

| Area | Check | Behavior |
|---|---|---|
| Input schema | Required CSV columns | Rejects an export with missing columns |
| Record identity | Blank or duplicate `model_id` | Rejects invalid input |
| Parameter format | Invalid or duplicate parameter entries | Reports `INVALID_PARAMETER_FORMAT` |
| Required metadata | Missing `MATERIAL` or `REV` | Reports `MISSING_PARAMETER` |
| Model dependencies | Reference absent from supplied export | Reports `UNRESOLVED_REFERENCE` |
| Regeneration indicator | `FAILED` | Reports `REGENERATION_FAILURE` |
| Regeneration indicator | `WARNING` | Reports `REGENERATION_WARNING` |
| Status consistency | Unrecognized regeneration status | Reports `UNKNOWN_REGEN_STATUS` |

Each finding includes a severity level and a recommended follow-up. Input-level failures, such as duplicate model IDs, raise validation errors instead of producing ordinary findings.

## Example dataset

The included `data/cad_models.csv` contains synthetic assembly and part records. It intentionally includes missing material metadata, a reference to a model outside the export, and regeneration warning/failure indicators.

These records demonstrate how the validation process distinguishes normal model metadata from items requiring investigation. An unresolved reference, for example, can indicate an incomplete export rather than a missing component in the authoritative engineering system.

## Repository structure

```text
data/cad_models.csv       Synthetic CAD metadata input
src/diagnose.py           CSV validation and diagnostic rules
tests/test_diagnose.py    Automated validation tests
requirements.txt          Python dependencies
README.md                 Project documentation
```

## Running the utility

```bash
python -m pip install -r requirements.txt
python src/diagnose.py --input data/cad_models.csv --output reports/cad_diagnostics.json
pytest -q
```

Expected input columns:

```text
model_id,model_type,parameters,references,regeneration_status
```

The `parameters` field contains semicolon-separated `KEY=VALUE` pairs. The `references` field contains semicolon-separated model IDs.

The generated JSON report contains a `findings` array and a total `count`. Each finding identifies the affected model, issue code, severity, details, and a recommended investigation action.

## Engineering configuration relevance

The validation approach supports several foundational configuration-management activities:

- **Configuration identification:** Checking that model records have unique identifiers and required descriptive attributes.
- **Revision metadata completeness:** Identifying records without a revision designation.
- **Relationship consistency:** Checking whether referenced components are represented in the provided dataset.
- **Exception management:** Producing consistent, reviewable findings instead of relying solely on manual inspection.
- **Data quality review:** Separating potentially incomplete engineering information from records that satisfy the implemented checks.

These are preliminary data-quality controls. They do not establish whether a configuration is approved, released, or compliant with a specific engineering baseline.

## Technical boundaries

This project is an offline simulator, not a Creo extension or production configuration-management system.

- It does not open native Creo files, execute regeneration, or invoke Creo APIs.
- It does not connect to Windchill, SAP, or other PLM/PDM systems.
- It checks whether a `REV` parameter exists but does not verify revision correctness against an approved baseline.
- It does not implement engineering change orders, approval routing, release management, effectivity, or configuration status accounting.
- It does not reconcile engineering or manufacturing bills of materials.
- Dependency checks are limited to the models present in the supplied CSV.
- All sample data is synthetic and contains no employer information.

## Future development opportunities

The existing validation rules provide a foundation for additional configuration-control simulations:

- Comparing candidate model revisions with an approved baseline.
- Evaluating synthetic engineering change records and release statuses.
- Reconciling component lists across engineering BOM revisions.
- Tracking exception ownership, disposition, and closure.
- Summarizing configuration discrepancies across multiple datasets.

These capabilities are proposed extensions and are not included in the current implementation.

## Related project

[Engineering Change & Revision Tracker](https://github.com/YSayaovong/Engineering-Change-Revision-Tracker)
