-- Filename: bitcoin_rate_queries.sql

-- Schema Information Metadata
-- Retrieve the names and SQL statements of all tables in the database
SELECT name, sql
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

-- Retrieve all rows from the 'bitcoin_rates' table where the chart name is 'Bitcoin' and the timestamp is within the last 1440 minutes (24 hours)
SELECT *
FROM bitcoin_rates
WHERE chart_name = 'Bitcoin'
    AND datetime(timestamp) >= datetime('now', '-1440 minutes');

-- Retrieve the first row from the 'bitcoin_rates' table
SELECT *
FROM bitcoin_rates
LIMIT 1;

-- Retrieve the latest row from the 'bitcoin_rates' table based on the 'unique_number' column
SELECT *
FROM bitcoin_rates
ORDER BY unique_number DESC
LIMIT 1;

-- Retrieve all rows from the 'bitcoin_rates' table where the chart name is 'Bitcoin' and the timestamp is within the last 5 minutes from a specified datetime
SELECT *
FROM bitcoin_rates
WHERE chart_name = 'Bitcoin'
    AND datetime(timestamp) >= datetime('2023-06-15T17:15:00+00:00', '-5 minutes');

-- Retrieve the maximum timestamp value from the 'bitcoin_rates' table and subtract 5 minutes from it
SELECT datetime(max(timestamp), '-5 minutes')
FROM bitcoin_rates;

-- Retrieve all rows from the 'bitcoin_rates' table where the chart name is 'Bitcoin' and the timestamp is within 5 minutes of the maximum timestamp in the table
SELECT *
FROM bitcoin_rates
WHERE chart_name = 'Bitcoin'
    AND datetime(timestamp) >= (SELECT datetime(max(timestamp), '-5 minutes') FROM bitcoin_rates);

-- ------------------------------

SELECT DISTINCT
    t2.timestamp, t2.chart_name, t2.usd_rate, t2.gbp_rate, t2.eur_rate, t2.previous_timestamp, t2.flag
        , COUNT(t2.unique_number) OVER () AS total_affected_records
FROM (
    SELECT t1.*, strftime('%s', t1.timestamp) - strftime('%s', t1.previous_timestamp) AS flag
    FROM (
        SELECT *,
            LAG(timestamp) OVER (ORDER BY timestamp ASC) AS previous_timestamp
        FROM bitcoin_rates
        WHERE chart_name = 'Bitcoin'
    ) t1
) t2
WHERE t2.flag IS NOT NULL AND t2.flag > 60;
-- -----------------DISCONTINUOUS TIMESTAMP
-- This could either be due to delay by the client in fetching the JSON payload before it is refreshed, 
-- or due to the data at the "missing timestamp" not being available on the API's server. 
-- But this is minimal, as only 29 out of 2861 records were affected by this. 


SELECT 
    COUNT(1) 
FROM bitcoin_rates;
-- 2861

SELECT 
    COUNT(DISTINCT t1.timestamp) 
FROM bitcoin_rates t1;
-- 2852; 9 duplicates as of the 3,924th entry or as at 2023-06-16T12:54:00+00:00

SELECT t1.*
    , COUNT(t1.unique_number) OVER () AS total_affected_records
FROM (
    SELECT *,
        COUNT(unique_number) OVER (PARTITION BY timestamp ORDER BY unique_number ASC) AS flag
    FROM bitcoin_rates
    WHERE chart_name = 'Bitcoin'
) t1
WHERE t1.flag > 1;
-- -----------------DUPLICATES
-- This is due to a delay in update of the JSON payload at the CoinDesk API, so we have to use an UPSERT clause
-- OR UNIQUE constraint and ON CONFLICT clause on the timestamp field to prevent conflicting records being inserted



