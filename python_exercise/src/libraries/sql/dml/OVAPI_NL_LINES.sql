
MERGE bbc_case_study.ovapi_nl_lines TARGET
USING bbc_case_study_staging.ext_ovapi_nl_lines SOURCE
ON SOURCE.Line = TARGET.LineID
WHEN MATCHED AND (TARGET.LineWheelchairAccessible <> SOURCE.LineWheelchairAccessible OR
    TARGET.TransportType <> SOURCE.TransportType OR
    TARGET.DestinationName50 <> SOURCE.DestinationName50 OR
    TARGET.DestinationCode <> SOURCE.DestinationCode OR
    TARGET.LinePublicNumber <> SOURCE.LinePublicNumber OR
    TARGET.LineName <> SOURCE.LineName)
THEN
  UPDATE SET 
    LineWheelchairAccessible = SOURCE.LineWheelchairAccessible,
    TransportType = SOURCE.TransportType,
    DestinationName50 = SOURCE.DestinationName50,
    DestinationCode = SOURCE.DestinationCode,
    LinePublicNumber = SOURCE.LinePublicNumber,
    LineName = SOURCE.LineName,
    TimeUpdatedUTC = CURRENT_DATETIME('UTC')
WHEN NOT MATCHED THEN
  INSERT (
LineID,	
LineWheelchairAccessible,
TransportType,
DestinationName50,
DataOwnerCode,
DestinationCode,
LinePublicNumber,
LinePlanningNumber,	
LineName,
LineDirection,
TimeInsertedUTC
)
VALUES(Line,	
LineWheelchairAccessible,
TransportType,
DestinationName50,
DataOwnerCode,
DestinationCode,
LinePublicNumber,
LinePlanningNumber,	
LineName,
CAST(LineDirection AS STRING),
CURRENT_DATETIME('UTC'))


