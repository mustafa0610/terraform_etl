# Simple ETL Pipeline with Terraform and Docker

This project demonstrates a simple Extract, Transform, Load (ETL) pipeline for reading data from a CSV file, transforming it, and loading it into a database. The infrastructure and ETL process are orchestrated using Terraform and Docker.

## Components

### 1. **`etl_pipeline.py`**  
   - The main ETL script.
   

### 2. **`csvreader.py`**  
   - Helps verify CSV content

### 3. **`Dockerfile`**  
   - Defines the Docker image used for running the ETL pipeline.
   - Installs dependencies from `requirements.txt` and sets up the ETL environment.

### 4. **`requirements.txt`**  
   - Lists the Python dependencies for the project:
     - `boto3`
     - `pandas`
     - `psycopg2-binary`

### Infrastructure with Terraform
Terraform is used to provision the cloud infrastructure required for the ETL pipeline. This includes:
   - An S3 bucket for storing raw data.
   - A Redshift cluster for storing processed data.
   - Necessary IAM roles and policies to manage access.


