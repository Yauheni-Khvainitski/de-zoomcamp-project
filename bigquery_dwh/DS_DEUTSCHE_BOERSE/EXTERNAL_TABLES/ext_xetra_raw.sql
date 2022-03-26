CREATE OR REPLACE EXTERNAL TABLE deutsche_boerse.ext_raw_xetra 
(
    ISIN STRING
    , Mnemonic STRING
    , SecurityDesc STRING
    , SecurityType STRING
    , Currency STRING
    , SecurityID BIGINT
    , Date DATE
    , Time STRING
    , StartPrice FLOAT64
    , MaxPrice FLOAT64
    , MinPrice FLOAT64
    , EndPrice FLOAT64
    , TradedVolume FLOAT64
    , NumberOfTrades BIGINT
)
-- WITH PARTITION COLUMNS
-- (
--     Date DATE
-- )
OPTIONS 
(
    format = 'CSV',
    field_delimiter = ',',
    skip_leading_rows = 1,
    -- hive_partition_uri_prefix = 'gs://deutsche-boerse/xetra_raw',
    uris = ['gs://deutsche-boerse/xetra_raw/*']
);