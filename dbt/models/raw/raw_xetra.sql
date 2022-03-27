{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date"
    },
    )
}}

SELECT
  {{ dbt_utils.surrogate_key(['SecurityID', 'Date', 'Time']) }} AS id
  , ISIN AS isin
  , Mnemonic AS mnemonic
  , SecurityDesc AS description
  , SecurityType AS security_type
  , Currency AS currency
  , SecurityID AS securityid
  , Date AS date
  , Time AS time
  , StartPrice AS open
  , MaxPrice AS high
  , MinPrice AS low
  , EndPrice AS close
  , TradedVolume AS tradedvolume
  , NumberOfTrades AS trades_num
FROM
    {{ source('raw', 'ext_raw_xetra') }}

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}