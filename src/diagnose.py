"""Offline CAD metadata diagnostics for a synthetic Creo-like export.

Does not connect to Creo or parse native Creo model files.
"""
import argparse
import csv
import json
from pathlib import Path

REQUIRED={"model_id","model_type","parameters","references","regeneration_status"}
NEEDED_PARAMS={"MATERIAL","REV"}

def load_models(path):
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError(f"Missing columns: {sorted(REQUIRED-set(reader.fieldnames or []))}")
        rows=list(reader)
    seen=set()
    for i,row in enumerate(rows,2):
        row["model_id"]=row["model_id"].strip()
        if not row["model_id"]:raise ValueError(f"Blank model_id at row {i}")
        if row["model_id"] in seen:raise ValueError(f"Duplicate model_id: {row['model_id']}")
        seen.add(row["model_id"])
    return rows

def parse_parameters(value):
    parameters={}
    for token in value.split(";"):
        token=token.strip()
        if not token:continue
        if "=" not in token:raise ValueError(f"Malformed parameter token: {token}")
        key,val=token.split("=",1)
        key=key.strip().upper();val=val.strip()
        if not key or not val:raise ValueError(f"Blank parameter name/value: {token}")
        if key in parameters:raise ValueError(f"Duplicate parameter: {key}")
        parameters[key]=val
    return parameters

def diagnose(rows):
    ids={row["model_id"] for row in rows}
    findings=[]
    def flag(model,code,severity,details,recommendation):
        findings.append({"model_id":model,"code":code,"severity":severity,"details":details,"recommendation":recommendation})
    for row in rows:
        model=row["model_id"]
        try:parameters=parse_parameters(row["parameters"])
        except ValueError as e:
            flag(model,"INVALID_PARAMETER_FORMAT","ERROR",str(e),"Correct the exported parameter format.")
            parameters={}
        for key in sorted(NEEDED_PARAMS-set(parameters)):
            flag(model,"MISSING_PARAMETER","WARNING",key,f"Review required {key} parameter in the source model.")
        for ref in (x.strip() for x in row["references"].split(";")):
            if ref and ref not in ids:
                flag(model,"UNRESOLVED_REFERENCE","ERROR",ref,"Confirm model dependencies and export completeness.")
        status=row["regeneration_status"].strip().upper()
        if status=="FAILED":
            flag(model,"REGENERATION_FAILURE","ERROR",status,"Inspect feature failures and dependent geometry in Creo.")
        elif status=="WARNING":
            flag(model,"REGENERATION_WARNING","WARNING",status,"Review Creo regeneration messages and feature health.")
        elif status!="OK":
            flag(model,"UNKNOWN_REGEN_STATUS","WARNING",status,"Verify the export's regeneration status.")
    return findings

def main():
    p=argparse.ArgumentParser(description="Check synthetic CAD metadata CSV");p.add_argument("--input",default="data/cad_models.csv");p.add_argument("--output",default="reports/cad_diagnostics.json");a=p.parse_args()
    findings=diagnose(load_models(a.input));out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"findings":findings,"count":len(findings)},indent=2)+"\n",encoding="utf-8")
    print(f"{len(findings)} findings written to {out}")
if __name__=="__main__":main()
