import pandas as pd
import glob
import os
from sqlalchemy import create_engine, text

def load_data_to_postgres(input_dir='/data'):
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')  # Ensure this is 'postgres' in Docker
    db_port = os.getenv('DB_PORT')
    
    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    try:
        # Ensure the 'staging_weather' table exists
        with engine.connect() as conn:
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS staging_weather (
                    station BIGINT,
                    date TEXT,
                    latitude DOUBLE PRECISION,
                    longitude DOUBLE PRECISION,
                    elevation DOUBLE PRECISION,
                    name TEXT,
                    temp DOUBLE PRECISION,
                    temp_attributes BIGINT,
                    dewp DOUBLE PRECISION,
                    dewp_attributes BIGINT,
                    slp DOUBLE PRECISION,
                    slp_attributes BIGINT,
                    stp DOUBLE PRECISION,
                    stp_attributes BIGINT,
                    visib DOUBLE PRECISION,
                    visib_attributes BIGINT,
                    wdsp DOUBLE PRECISION,
                    wdsp_attributes BIGINT,
                    mxspd DOUBLE PRECISION,
                    gust DOUBLE PRECISION,
                    max DOUBLE PRECISION,
                    max_attributes TEXT,
                    min DOUBLE PRECISION,
                    min_attributes TEXT,
                    prcp DOUBLE PRECISION,
                    prcp_attributes TEXT,
                    sndp DOUBLE PRECISION,
                    frshtt BIGINT
                )
                '''))
            print('Ensured staging_weather table exists.')

        # Process each CSV file in the input directory
        for file_path in glob.glob(f'{input_dir}/*.csv'):
            print(f'Processing {file_path}')
            df = pd.read_csv(file_path)
            
            # Insert data into PostgreSQL staging table
            df.to_sql('staging_weather', engine, if_exists='append', index=False)
            print(f'Loaded {file_path} into database')
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Ensure the connection is closed
        engine.dispose()


    print("Table created or already exists.")
if __name__ == '__main__':
    load_data_to_postgres()