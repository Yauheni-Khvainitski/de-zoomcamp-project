
{{ config(materialized='table') }}

SELECT
  securityid
  , description
  , AVG((high - low) / low) AS implied_vol
FROM
  {{ ref('raw_xetra') }}
WHERE 
  date >= CURRENT_DATE - 7
GROUP BY
  securityid
  , description
ORDER BY
  implied_vol DESC

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}