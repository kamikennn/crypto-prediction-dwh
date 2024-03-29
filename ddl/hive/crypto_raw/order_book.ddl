DROP TABLE crypto_raw.order_book;

CREATE TABLE IF NOT EXISTS crypto_raw.order_book (
    id string COMMENT 'id of the crypto currency',
    seqid bigint COMMENT 'id of the record/order (SeqId)',
    order_type string COMMENT 'order type, which can be bid(buy) or ask(sell)',
    quote_price float COMMENT 'quote price of the order, such as 25,000$ for 1 BTC',
    base_amount float COMMENT 'base amount of the order, such as 0.001 BTC',
    order_rank int COMMENT 'rank of the order at the moment. If buy order, higher price is higher rank. If sell order, lower price is higher rank.',
    createTime bigint COMMENT 'time the record was created in the Poloniex system',
    ts_send bigint COMMENT 'unix timestamp when the record was created in UTC time',
    dt_create_utc date COMMENT 'date when the record was created in a trading system (based on createTime)',
    ts_create_utc timestamp COMMENT 'timestamp when the record was created in a trading system (based on createTime)',
    ts_insert_utc timestamp COMMENT 'timestamp when data was inserted to cassandra table',
    minute smallint COMMENT 'minute at the order data was created (based on createTime)',
    second smallint COMMENT 'second at the order data was created (based on createTime)'
)
COMMENT 'crypto candles data for each minute'
PARTITIONED BY(year smallint COMMENT 'year at the order data was created (based on createTime)',
    month smallint COMMENT 'month at the order data was created (based on createTime)',
    day smallint COMMENT 'day at the order data was created (based on createTime)',
    hour smallint COMMENT 'hour at the order data was created (based on createTime)')
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");
