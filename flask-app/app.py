import os
from flask import Flask, render_template, send_file
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set the Matplotlib backend to Agg
plt.switch_backend('Agg')

app = Flask(__name__)

# Retrieve the database URL from environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')  # Ensure this is 'postgres' in Docker
db_port = os.getenv('DB_PORT')

# Create SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

@app.route('/')
def index():
    # Fetch number of records and column info
    record_count_query = "SELECT COUNT(*) FROM weather;"
    record_count = pd.read_sql(record_count_query, engine).iloc[0, 0]
    
    column_info_query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'weather';"
    columns_info = pd.read_sql(column_info_query, engine)

    # Fetch some records for the table
    data_query = "SELECT * FROM weather LIMIT 10;"
    df = pd.read_sql(data_query, engine)
    data = df.to_html(classes='table table-striped')

    # Calculate summary statistics
    summary_stats_query = """
    SELECT 
        ROUND(AVG("TEMP")::numeric, 1) as avg_temp,
        ROUND(MAX("TEMP")::numeric, 1) as max_temp,
        ROUND(MIN("TEMP")::numeric, 1) as min_temp,
        COUNT(DISTINCT "STATION") as location_count
    FROM weather;
    """
    stats_df = pd.read_sql(summary_stats_query, engine)

    
    summary_stats = {
        'avg_temp': stats_df.iloc[0]['avg_temp'],
        'max_temp': stats_df.iloc[0]['max_temp'],
        'min_temp': stats_df.iloc[0]['min_temp'],
        'location_count': stats_df.iloc[0]['location_count']
    }

    # Prepare additional information to pass to the template
    dataset_info = {
        "source": "noaa-gsod-pds",
        "record_count": record_count,
        "columns_info": columns_info.to_html(classes='table table-sm table-bordered'),
    }
    
    return render_template('index.html', table=data, dataset_info=dataset_info, summary_stats=summary_stats)

@app.route('/plot.png')
def plot():
    # Fetch temperature data
    temp_query = """SELECT "TEMP" FROM weather;"""
    df = pd.read_sql(temp_query, engine)
    
    # Create the histogram plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df['TEMP'], bins=30, kde=True)
    plt.title('Temperature Distribution')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)