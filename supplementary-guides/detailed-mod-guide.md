# Modularizing the Data Pipeline

To make this data pipeline more modular and adaptable, we can break it down into smaller components. These components can be customized or replaced independently without affecting the entire workflow. Here's a step-by-step breakdown:

## 1. Data Ingestion (Extract)

- **Script Component:** The `extract.py` script downloads data from an AWS S3 bucket using the `boto3` library.
- **Flexibility in Data Sources:** You can customize the script to support data sources like S3, APIs, or local files, the script can be modularized by creating different scripts for each source. This approach enables easy adjustments or replacements of individual scripts without impacting the rest of the pipeline.
    - For instance, if you want to switch from extracting data from an S3 bucket to an API, you can replace or modify the `extract.py` script to use a dedicated API data extraction approach. 
    - Similarly, if local file ingestion is required, simply swap the extraction script to handle local file paths and data parsing.
    
- **Example:** For S3 data extraction, the script might look like this:

    ```python
    import boto3

    def extract_from_s3(bucket_name, file_key):
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = response['Body'].read()
        return data
    ```

    For an API-based extraction, the researcher can replace it with something like:

    ```python
    import requests

    def extract_from_api(api_url):
        response = requests.get(api_url)
        data = response.json()  # assuming JSON format
        return data
    ```

    For local file extraction:

    ```python
    def extract_from_local(local_path):
        with open(local_path, 'r') as file:
            data = file.read()
        return data
    ```

### ELT to ETL Comment:
If transformations are required **before** loading into the database, the logic should be applied right after the extraction, depending on the source type, to follow the ETL pattern.

## 2. Data Loading (Load)

- **Script Component:** The `load.py` script loads extracted data into a PostgreSQL database.
- **Modularization:** This can be adapted to load data into different database types (e.g., MySQL, SQLite) by using SQLAlchemy to abstract database operations.
- **Example:**

    ```python
    from sqlalchemy import create_engine
    db_type = os.getenv('DB_TYPE', 'postgresql')
    engine = create_engine(f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    ```

## 3. Data Transformation (Transform)

- **Script Component:** The `transform.py` script processes and cleans the data.
- **Modularization:** Make the transformation logic modular by passing specific transformations (e.g., filtering, aggregating) as functions or loading a configuration file that specifies transformation steps.
- **Example:**

    ```python
    def apply_transformations(dataframe, transformations):
        for transformation in transformations:
            dataframe = transformation(dataframe)
        return dataframe
    ```

## 4. Orchestration (Docker and Shell Scripts)

The Docker Compose setup can modularize services (like database and ETL components) by creating a shared network and volumes. Shell scripts for each phase ensure stages are executed in sequence, but can be replaced with more advanced orchestrators like Apache Airflow if needed.

## Example Guide for Modularizing and Generalizing

### Step-by-Step Instructions for Researchers

1. **Prepare Environment:** Set up `.env` files with variables for different stages (e.g., source type, database credentials).
    - `DB_TYPE` for database type (Postgres, MySQL, etc.).
    - `SOURCE` for the data source (S3, API, LOCAL).

2. **Ingestion Customization:**
    - Modify the `extract.py` script to ingest data from your preferred source by adjusting the source type in the environment variable.
    - Example:

    ```bash
    SOURCE=S3
    S3_BUCKET=example-bucket
    ```

3. **Loading Customization:**
    - Change the database type by setting `DB_TYPE` in your `.env`.
    - Example:

    ```bash
    DB_TYPE=postgresql
    ```

4. **Transformation Customization:**
    - If you need different transformations, either modify the existing logic or pass a configuration file with steps.
    - Example:

    ```yaml
    transformations:
    - filter: "column_name > 50"
    - aggregate: "sum"
    ```

## Turning the Script into Different Types of Ingestion

### 1. Real-Time Data Ingestion

- **Modularize the Extract Step:** Add support for streaming data by integrating a tool like Apache Kafka or AWS Kinesis to handle real-time data streams. Alternatively, you can leverage **Apache NiFi** for real-time data ingestion and processing with a highly configurable, drag-and-drop interface for data flow management.
- **Code Snippet:**

    ```python
    def extract_real_time_data(stream_source):
        # Code to connect to a real-time stream and process data in batches
    ```

### 2. Scheduled Ingestion (Cron Jobs)

- Use a cron job inside a container or set up on the host system to trigger the `extract.py` script at regular intervals.
- **User-Friendly Process for Updating Frequency:**
    - Create a simple script that allows the user to update the cron schedule via a command-line argument or a configuration file.
    - Example:

    ```bash
    echo "Setting up cron job..."
    (crontab -l 2>/dev/null; echo "0 * * * * python /path/to/extract.py") | crontab -
    ```

### 3. Large-Scale Data Ingestion

- **Parallelize the Workflow:** Use tools like Spark or Dask for parallel data processing in the extraction and transformation stages.
- **Scale Docker Setup:** In a large-scale environment, scale the containerized solution using Kubernetes or a cloud platform like AWS with autoscaling enabled.
- **Example:**
    - Use Spark for distributed data processing:

    ```python
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName('LargeScaleETL').getOrCreate()
    ```

By modularizing each part of the pipeline, researchers can easily adapt it to various use cases, ranging from small-scale local projects to real-time, large-scale data processing setups.
