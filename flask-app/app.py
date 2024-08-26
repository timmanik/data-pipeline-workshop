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

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

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

    # Prepare additional information to pass to the template
    dataset_info = {
        "source": "noaa-gsod-pds",
        "record_count": record_count,
        "columns_info": columns_info.to_html(classes='table table-sm table-bordered'),
    }
    
    return render_template('index.html', table=data, dataset_info=dataset_info)

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
    app.run(host='0.0.0.0', port=5000)
