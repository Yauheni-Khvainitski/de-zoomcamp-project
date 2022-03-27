{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date"
    },
    )
}}

SELECT
    *
FROM
    {{ source('raw', 'ext_raw_xetra') }}
LIMIT 10