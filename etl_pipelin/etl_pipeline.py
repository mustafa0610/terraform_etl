import boto3
import pandas as pd
import psycopg2
from io import StringIO

# AWS configurations
s3 = boto3.client('s3')
bucket_name = 'etl-pipeline-data-bucket'  # Your S3 bucket name
s3_file_key = 'laptop_price - dataset.csv'  # The file name/key in S3 (update if necessary)

# Redshift configurations
redshift_host = 'redshift-cluster-1.cscxzn6p5gvj.us-east-1.redshift.amazonaws.com'  # Your Redshift endpoint
redshift_db = 'etl_db'  # Your Redshift database name
redshift_user = 'masteruser'  # Your Redshift username
redshift_password = 'SuperSecurePassword123!'  # Your Redshift password
redshift_port = 5439  # Default Redshift port

# Step 1: List files in S3 bucket (Debugging)
def list_s3_files(bucket):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)
    if 'Contents' in response:
        print("Files in S3 bucket:")
        for obj in response['Contents']:
            print(obj['Key'])

# Step 2: Download the CSV file from S3
def download_s3_file(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except s3.exceptions.NoSuchKey:
        print(f"Error: The specified key '{key}' does not exist in bucket '{bucket}'.")
        raise

# Step 3: Process the data (simple transformation)
def process_data(data):
    # Read CSV from S3
    df = pd.read_csv(StringIO(data))
    
    # Example transformation: creating a new column (double the value of 'Price (Euro)')
    df['Price_Doubled'] = df['Price (Euro)'] * 2

    return df

# Step 4: Load data into Redshift
def load_data_to_redshift(df):
    # Connect to Redshift
    conn = psycopg2.connect(
        dbname=redshift_db,
        user=redshift_user,
        password=redshift_password,
        host=redshift_host,
        port=redshift_port
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist in Redshift
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laptop_prices (
        Manufacturer VARCHAR(255),
        Product VARCHAR(255),
        TypeName VARCHAR(255),
        Inches FLOAT,
        ScreenResolution VARCHAR(255),
        CPU_Company VARCHAR(255),
        CPU_Type VARCHAR(255),
        CPU_Frequency_GHz FLOAT,
        RAM_GB INT,
        Memory VARCHAR(255),
        GPU_Company VARCHAR(255),
        GPU_Type VARCHAR(255),
        OpSys VARCHAR(255),
        Weight_kg FLOAT,
        Price_Euro FLOAT,
        Price_Doubled FLOAT
    );
    """)

    # Insert data into the Redshift table
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO laptop_prices (
                Manufacturer, Product, TypeName, Inches, ScreenResolution, CPU_Company, 
                CPU_Type, CPU_Frequency_GHz, RAM_GB, Memory, GPU_Company, GPU_Type, OpSys, 
                Weight_kg, Price_Euro, Price_Doubled
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row['Company'], row['Product'], row['TypeName'], row['Inches'], row['ScreenResolution'],
                row['CPU_Company'], row['CPU_Type'], row['CPU_Frequency (GHz)'], row['RAM (GB)'], row['Memory'],
                row['GPU_Company'], row['GPU_Type'], row['OpSys'], row['Weight (kg)'], row['Price (Euro)'], row['Price_Doubled']
            )
        )

    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Main function to run the ETL pipeline
def main():
    # Step 1: List files in the S3 bucket (for debugging)
    print("Listing files in S3 bucket:")
    list_s3_files(bucket_name)

    # Step 2: Download the file from S3
    raw_data = download_s3_file(bucket_name, s3_file_key)

    # Step 3: Process the data
    processed_df = process_data(raw_data)

    # Step 4: Load the data into Redshift
    load_data_to_redshift(processed_df)

if __name__ == '__main__':
    main()
