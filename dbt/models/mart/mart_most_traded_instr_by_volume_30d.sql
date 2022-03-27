
{{ config(materialized='table') }}

WITH
  daily_sec_vol AS (
  SELECT
    securityid
    , description
    , date
    , SUM(open * tradedvolume) / 1e6 AS tradeamountmm
  FROM
    {{ ref('raw_xetra') }}
  WHERE
    currency = 'EUR'
  GROUP BY
    securityid
    , description
    , date ),
  daily_max AS (
  SELECT
    date
    , MAX(tradeamountmm) AS maxamount
  FROM
    daily_sec_vol
  GROUP BY
    date)
SELECT
  dm.date
  , dsv.securityid
  , dsv.description
  , dsv.tradeamountmm
FROM
  daily_max AS dm
LEFT JOIN
  daily_sec_vol AS dsv
ON
  dsv.tradeamountmm = dm.maxamount
  AND dsv.date = dm.date
WHERE
  dm.date >= CURRENT_DATE - 30
ORDER BY
  dsv.date DESC,
  dm.maxamount DESC