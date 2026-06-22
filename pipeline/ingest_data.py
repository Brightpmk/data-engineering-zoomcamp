import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

PARSE_DATES = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'
    
    year = 2021
    month = 1
    
    TABLE_NAME = 'yellow_taxi_data'
    chunksize = 100000
    
    URL_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    DATA_URL = f'{URL_PREFIX}yellow_tripdata_{year}-{month:02d}.csv.gz'
    
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    df_schema = pd.read_csv(DATA_URL, nrows=100, dtype=DTYPE, parse_dates=PARSE_DATES)
    df_schema.head(0).to_sql(name=TABLE_NAME, con=engine, if_exists='replace', index=False)
    
    df_iter = pd.read_csv(
        DATA_URL,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=chunksize
    )

    print("\nStarting Data Ingestion:")
    
    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name=TABLE_NAME,
            con=engine,
            if_exists='append',
            index=False
        )

    print("Data ingestion completed successfully!")
    
if __name__ == '__main__':
    run()