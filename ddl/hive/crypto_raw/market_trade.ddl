DROP TABLE crypto_raw.market_trade;

CREATE TABLE IF NOT EXISTS crypto_raw.market_trade (
    id string COMMENT 'id of the crypto currency',
    trade_id bigint COMMENT 'trade id',
    takerSide string COMMENT 'trade side (buy, sell)',
    amount float COMMENT 'quote units traded',
    quantity float COMMENT 'base units traded',
    price float COMMENT 'trade price',
    createTime bigint COMMENT 'time the trade was created',
    ts_send bigint COMMENT 'time the record was pushed',
    dt_create_utc date COMMENT 'date when the record was created in a trading system (based on createTime)',
    ts_create_utc timestamp COMMENT 'timestamp when the record was created in a trading system (based on createTime)',
    ts_insert_utc timestamp COMMENT 'timestamp when data was inserted to cassandra table',
    minute smallint COMMENT 'minute at the trade data was created (based on createTime)',
    second smallint COMMENT 'second at the trade data was created (based on createTime)'
)
COMMENT 'crypto candles data for each minute'
PARTITIONED BY(year smallint COMMENT 'year at the trade data was created (based on createTime)',
    month smallint COMMENT 'month at the trade data was created (based on createTime)',
    day smallint COMMENT 'day at the trade data was created (based on createTime)',
    hour smallint COMMENT 'hour at the trade data was created (based on createTime)')
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");
