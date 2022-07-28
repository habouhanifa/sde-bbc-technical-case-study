CREATE OR REPLACE TABLE bbc_case_study.ovapi_nl_lines(
    LineID STRING NOT NULL,
    LineWheelchairAccessible STRING,
    TransportType STRING,
    DestinationName50 STRING,
    DataOwnerCode STRING NOT NULL,
    DestinationCode STRING,
    LinePublicNumber STRING,
    LinePlanningNumber STRING NOT NULL,
    LineName STRING,
    LineDirection STRING NOT NULL,
    TimeInsertedUTC DATETIME NOT NULL,
    TimeUpdatedUTC DATETIME
)
PARTITION BY DATETIME_TRUNC(TimeInsertedUTC, MONTH)
CLUSTER BY DataOwnerCode;
