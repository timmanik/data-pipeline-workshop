import pandas as pd
from sqlalchemy import create_engine, text
import os

def transform_and_load_final():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')  # Ensure this is 'postgres' in Docker
    db_port = os.getenv('DB_PORT')
    
    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    try:
        with engine.connect() as conn:
            with conn.begin():  # Starts a transaction
                conn.execute(text('''
                CREATE TABLE IF NOT EXISTS weather (
                    "STATION" BIGINT,
                    "DATE" TEXT,
                    "LATITUDE" DOUBLE PRECISION,
                    "LONGITUDE" DOUBLE PRECISION,
                    "ELEVATION" DOUBLE PRECISION,
                    "NAME" TEXT,
                    "TEMP" DOUBLE PRECISION,
                    "DEWP" DOUBLE PRECISION,
                    "SLP" DOUBLE PRECISION,
                    "STP" DOUBLE PRECISION,
                    "VISIB" DOUBLE PRECISION,
                    "WDSP" DOUBLE PRECISION,
                    "MXSPD" DOUBLE PRECISION,
                    "GUST" DOUBLE PRECISION,
                    "MAX" DOUBLE PRECISION,
                    "MIN" DOUBLE PRECISION,
                    "PRCP" DOUBLE PRECISION,
                    "SNDP" DOUBLE PRECISION,
                    "FRSHTT" BIGINT
                )
            '''))
            
            # Transform data: load from staging and remove specified columns
            conn.execute(text('''
                INSERT INTO "weather" ("STATION", "DATE", "LATITUDE", "LONGITUDE", "ELEVATION", "NAME", "TEMP", "DEWP", "SLP", "STP", "VISIB", "WDSP", "MXSPD", "GUST", "MAX", "MIN", "PRCP", "SNDP", "FRSHTT")
                SELECT "STATION", "DATE", "LATITUDE", "LONGITUDE", "ELEVATION", "NAME", "TEMP", "DEWP", "SLP", "STP", "VISIB", "WDSP", "MXSPD", "GUST", "MAX", "MIN", "PRCP", "SNDP", "FRSHTT"
                FROM "staging_weather"
            '''))
            print('Data transformed and loaded into weather table.')
        
                # Commit the changes
            conn.commit()
            conn.close()
        print('Data transformation and loading to final table completed.')

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Ensure the connection is closed
        engine.dispose()

if __name__ == '__main__':
    transform_and_load_final()