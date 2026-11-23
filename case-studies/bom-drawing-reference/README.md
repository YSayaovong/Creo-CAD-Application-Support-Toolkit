# Incorrect drawing reference in a BOM

This simulated CAD support case uses fictional CSV exports. The exercise can be reproduced without Creo.

## Reported issue

The BOM for a sample mounting assembly lists bracket part `PT-210` with drawing `DWG-220`. The drawing index associates that drawing with spacer part `PT-220`.

## Diagnose and correct

1. Open [the reported BOM](bom-before.csv) and [the drawing index](drawing-index.csv).
2. Look up the affected row by its part number, `PT-210`, in the drawing index. The matching record identifies `DWG-210` as the bracket drawing.
3. Check the original drawing reference against the same index. `DWG-220` belongs to `PT-220`, confirming the bracket row points to the spacer drawing.
4. Change only the bracket row's drawing reference from `DWG-220` to `DWG-210`. Compare the result with [the corrected BOM](bom-after.csv).

## Verify the correction

Check every BOM row against the drawing index using the part number as the lookup key. After the correction, all three drawing references match. The part numbers, item numbers, descriptions and quantities are identical in the two BOM exports.

If a real drawing index returns multiple records for the same part, confirm the applicable revision or release record before editing the BOM.
