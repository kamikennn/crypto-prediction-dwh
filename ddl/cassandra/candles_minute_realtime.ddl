CREATE TABLE IF NOT EXISTS candles_minute_realtime (
    id varchar,
    low float,
    high float,
    open float,
    close float,
    amount float,
    quantity float,
    buyTakerAmount float,
    buyTakerQuantity float,
    tradeCount int,
    ts bigint,
    weightedAverage float,
    interval varchar,
    startTime bigint,
    closeTime bigint,
    dt varchar,
    PRIMARY KEY ((id,dt),ts)
  );