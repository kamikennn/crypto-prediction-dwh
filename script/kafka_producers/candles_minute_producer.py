import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from confluent_kafka import Producer
import json
import time
import datetime
import logging
from pprint import pprint
from poloniex_apis import get_request

polo_operator = get_request.PoloniexOperator()

###################
# Set logging env #
###################

args = sys.argv
curr_date = args[1]
curr_timestamp = args[2]
print(curr_date,curr_timestamp)

logdir = f'/home/kamiken/kafka/log/{curr_date}'
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=f'{logdir}/candles_minute_producer_{curr_timestamp}.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(20)


###################
# Set Kafka config #
###################
kafka_conf = {
    'bootstrap.servers':"172.29.0.6:9092"
    }

# set a producer
p=Producer(kafka_conf)
logger.info('Kafka Producer has been initiated...')

def receipt(err,msg):
    if err is not None:
        logger.error('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))


########
# Main #
########
def main():
    # Set parameters for crypto data
    assets = ['BTC_USDT',
              'ETH_USDT',
              'BNB_USDT',
              'XRP_USDT',
              'ADA_USDT',
              'DOGE_USDT',
              'SOL_USDT',
              'TRX_USDD',
              'UNI_USDT',
              'ATOM_USDT',
              'GMX_USDT',
              'SHIB_USDT',
              'MKR_USDT'
              ]
    
    interval = 'MINUTE_1'
    period = 5 # minute
    
    target_topic = "crypto.candles_minute"
    
    retry_count = 0
    max_retry_count = 5
    while(True):
        # get_candles
        for asset in assets:
            try:
                raw_candle_data = polo_operator.get_candles(asset,interval,period)
                retry_count = 0
            except:
                retry_count+=1
                logger.warning('API ERROR: Could not get candle data')
                logger.warning(f'Retry Requst: {retry_count}')
                if retry_count == max_retry_count:
                    sys.exit(1)
                time.sleep(10)
                
            candle_data = {"data":[
                {
                    'id':asset,
                    'low':data[0],
                    'high':data[1],
                    'open':data[2],
                    'close':data[3],
                    'amount':data[4],
                    'quantity':data[5],
                    'buyTakerAmount':data[6],
                    'buyTakerQuantity':data[7],
                    'tradeCount':data[8],
                    'ts':data[9],
                    'weightedAverage':data[10],
                    'interval':data[11],
                    'startTime':data[12],
                    'closeTime':data[13],
                    'dt':datetime.date.today().strftime("%Y-%m-%d")
                } for data in raw_candle_data
                ]
                        }
                
            m=json.dumps(candle_data)
            p.produce(target_topic, m.encode('utf-8'),callback=receipt)
            time.sleep(10)
            
if __name__ == '__main__':
    main()