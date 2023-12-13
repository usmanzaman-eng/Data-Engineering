import boto3
from datetime import datetime 
import pandas as pd
import io
from pymongo import MongoClient
from user_agents import parse
from apscheduler.schedulers.blocking import BlockingScheduler


def loop():   
    year=datetime.now().year
    month=datetime.now().month
    day=datetime.now().day
    hour=datetime.now().hour
    path = f"year={year:04d}/month={month:02d}/day={day:02d}/hour={hour:02d}/"
    prefix =path
    dataframe_collector(prefix)


def dataframe_collector(prefix):
    all_csv_files = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    collect_dataframes = []
    for csv_file in all_csv_files['Contents']:
        if csv_file['Key'].endswith('.csv'):
            csv_file_data = s3.get_object(Bucket=bucket, Key=csv_file['Key'])['Body'].read().decode('utf-8')
            tmp_df = pd.read_csv(io.StringIO(csv_file_data))
            collect_dataframes.append(tmp_df)
    final_dataframe = pd.concat(collect_dataframes, ignore_index=True)
    data = final_dataframe.to_dict('records')
    collection_page_data.insert_many(data)
    parser_function(final_dataframe)


def parser_function(dataframe):
    dataframe['browser'] = dataframe['user_agent'].apply(lambda x: parse(x).browser.family)
    dataframe['device'] = dataframe['user_agent'].apply(lambda x: parse(x).device.family)
    transformer(dataframe)


def transformer(dataframe):
    dataframe=dataframe.drop(['user_agent','Unnamed: 0'],axis=1)
    dataframe['page_views'] = 1
    dataframe = dataframe.groupby(['site', 'device', 'browser']).agg({'page_views': 'sum', 'user_cookie': 'nunique'})
    store_records(dataframe)


def store_records(dataframe):
    data = dataframe.to_dict('records')
    collection_usertraffic.insert_many(data)


if __name__=="__main__":
    bucket = "test-bucket"
    s3 = boto3.client(
    "s3",
    endpoint_url="http://minio-server:9000",
    aws_access_key_id= "usmanadmin",
    aws_secret_access_key= "usmanadmin"
    )
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["UserActivityDatabase"]
    collection_usertraffic = db["userstraffic"]
    collection_page_data=db["pagedata"]
    scheduler = BlockingScheduler()
    scheduler.add_job(loop, 'interval', hours=1)
    scheduler.start()
