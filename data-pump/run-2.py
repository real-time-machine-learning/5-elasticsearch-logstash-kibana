
## 该程序会将文本数据上传到RabbitMQ消息交换中心，后面我们将会利用
## ELK 集群进行分析。

import csv
import pika 
import pandas as pd 
from datetime import datetime

## 建立和RabbitMQ的连接

exchange_name = "stock_price"

connection_parameters = pika.ConnectionParameters(host = "rabbitmq",
                                                  connection_attempts = 10, 
                                                  retry_delay = 20)
connection = pika.BlockingConnection(connection_parameters) 

channel = connection.channel()

channel.exchange_declare(exchange = exchange_name, 
                         type = "fanout")

## 读取数据并发布到RabbitMQ中

read_date_list = ["20150803", "20150804"] 
read_stock_list = ["aapl", "intc", "goog", "googl", "fb"] 

UNIX_EPOCH = datetime(1970, 1, 1, 0, 0)
def ConvertTime(timestamp_raw, date):
    """ 该函数会将原始的时间转化为所需的datetime格式 """
    delta = datetime.utcfromtimestamp(timestamp_raw) - UNIX_EPOCH
    return (date + delta).isoformat()

for date in read_date_list:
    date_converted = datetime.strptime(date, 
                                                "%Y%m%d")
    for symbol in read_stock_list:
        data = pd.read_csv("fin/"+ date+"/"+symbol+".csv",
                           names = ["timestamp_raw","Open","High",
                                    "Low","Close","Volume"],
                           index_col = False)
        data["timestamp"] = list(map(lambda x: ConvertTime(x, date_converted),
                                     data["timestamp_raw"]/1000))
        data = data.drop("timestamp_raw",1)
        data["symbol"] = symbol 

        for index, row in data.iterrows():
            channel.basic_publish(exchange = exchange_name,
                                  routing_key = "",
                                  body = row.to_json())
                            
connection.close() 
