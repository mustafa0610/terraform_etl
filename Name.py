Pastebin
Search...

Login Sign up
Advertisement

asmr420
cd1
asmr420
Feb 3rd, 2025
6
0
Never
Add comment
Not a member of Pastebin yet? Sign Up, it unlocks many cool features!
6.85 KB | None |  
  
import pandas as pd
from sqlalchemy import create_engine, text
from api.config import Config
from api.utils.common_functions import save_file_to_sharepoint
import os
import json
 
def etl_tensile_test_parameters(df_Parameters: pd.DataFrame, file_name: str, Sample_ID: int, Sample_SID: int, username: str) -> pd.DataFrame:
    try:
        df_Parameters = df_Parameters.dropna(how="all", axis=0).dropna(how="all", axis=1)
        df_Parameters = df_Parameters.transpose()
        df_Parameters = df_Parameters.set_axis(df_Parameters.iloc[0], axis=1).iloc[2:]
 
        rename_map = {
            "Project Nr.": "Project_Nr",
            "Order Nr.": "Order_Nr",
            "Test standard": "Test_Standard",
            "Description test sample": "Description_Test_Sample",
            "Specimen type": "Specimen_Type",
            "Pre-treatment": "Pre_Treatment",
            "Machinedata": "Machine_Data",
            "Type of test2": "Type_Of_Test",
            "Pre-load": "Pre_load",
            "Speed, tensile modulus": "Speed_Tensile_Modulus",
            "Test speed": "Test_Speed",
            "Grip to grip separation at the start position": "Grip_To_Grip_Separation_At_The_Start_Position",
            "Gage length, standard travel": "Gage_Length_Standard_Travel",
            "Begin of tensile modulus determination": "Begin_Of_Tensile_Modulus_Determination",
            "End of tensile modulus determination": "End_Of_Tensile_Modulus_Determination",
            "Type of tensile modulus determination": "Type_Of_Tensile_Modulus_Determination"
        }
 
        df_Parameters = df_Parameters.rename(columns=rename_map)
        df_Parameters['Sample_ID'] = Sample_ID
        df_Parameters['Sample_SID'] = Sample_SID
        df_Parameters['File_Path'] = file_name
        df_Parameters['Created_By'] = username
        df_Parameters = df_Parameters.fillna(value="").replace("", None).infer_objects()
 
        return df_Parameters
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error processing Parameters sheet: {str(e)}"})
 
def etl_tensile_test_results(df_Results: pd.DataFrame, Tensile_Test_ID: int) -> pd.DataFrame:
    try:
        df_Results.columns = df_Results.iloc[0]  # Set headers correctly
        df_Results = df_Results.iloc[1:]  # Remove unit row
        df_Results['Tensile_Test_ID'] = Tensile_Test_ID
        return df_Results
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error processing Results sheet: {str(e)}"})
 
def etl_tensile_test_statistics(df_Statistics: pd.DataFrame, Tensile_Test_ID: int) -> pd.DataFrame:
    try:
        df_Statistics.columns = df_Statistics.iloc[0]  # Set headers
        df_Statistics = df_Statistics.iloc[1:]  # Remove unit row
        df_Statistics['Tensile_Test_ID'] = Tensile_Test_ID
        return df_Statistics
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error processing Statistics sheet: {str(e)}"})
 
def etl_tensile_test_specimen(df_Specimen: pd.DataFrame, Tensile_Test_ID: int, sheet_name: str) -> pd.DataFrame:
    try:
        df_Specimen = df_Specimen.iloc[2:]  # Skip first two rows (headers + units)
        df_Specimen.columns = ['Strain', 'Standard_Force']
        df_Specimen['Specimen'] = sheet_name
        df_Specimen['Tensile_Test_ID'] = Tensile_Test_ID
        return df_Specimen
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error processing {sheet_name} sheet: {str(e)}"})
 
def etl_tensile_test(file_name: str, Sample_ID: int, Sample_SID: int, username: str):
    cstr = Config.cstr
    tensile_test_file_path = f"{os.environ.get('MEASUREMENT_FILE_PATH')}/tensile_test/{file_name}"
    engine = create_engine(cstr, future=True)
 
    try:
        print("Loading Excel file...")
        df = pd.ExcelFile(tensile_test_file_path)
 
        # Check for required sheets
        required_sheets = ['Parameters', 'Results', 'Statistics']
        missing_sheets = [sheet for sheet in required_sheets if sheet not in df.sheet_names]
        if missing_sheets:
            return json.dumps({"status": "error", "message": f"Missing sheets: {', '.join(missing_sheets)}"})
 
        df_Parameters = df.parse('Parameters')
        df_Results = df.parse('Results')
        df_Statistics = df.parse('Statistics')
 
        print("Running etl_tensile_test_parameters...")
        op_etl_tensile_test_parameters = etl_tensile_test_parameters(df_Parameters, file_name, Sample_ID, Sample_SID, username)
 
        print("Executing SQL insert for Tensile_Test_Measurements...")
        with engine.begin() as connection:
            result = connection.execute(text(qry), op_etl_tensile_test_parameters.to_dict('records')[0])
 
            print("Fetching inserted Tensile_Test_ID...")
            Tensile_Test_ID = next(iter(result), None)
            if Tensile_Test_ID is None:
                return json.dumps({"status": "error", "message": "Failed to retrieve Tensile_Test_ID from database"})
 
            print("Running etl_tensile_test_results...")
            op_etl_tensile_test_results = etl_tensile_test_results(df_Results, Tensile_Test_ID)
            op_etl_tensile_test_results.to_sql(name="Tensile_Test_Results", con=connection, if_exists='append', index=False)
 
            print("Running etl_tensile_test_statistics...")
            op_etl_tensile_test_statistics = etl_tensile_test_statistics(df_Statistics, Tensile_Test_ID)
            op_etl_tensile_test_statistics.to_sql(name="Tensile_Test_Statistics", con=connection, if_exists='append', index=False)
 
            print("Processing specimen sheets...")
            for sheet_name in df.sheet_names:
                if sheet_name not in required_sheets:
                    print(f"Processing {sheet_name}...")
                    df_Specimen = df.parse(sheet_name, header=1)
                    if df_Specimen.empty:
                        return json.dumps({"status": "error", "message": f"Sheet {sheet_name} is empty!"})
 
                    op_etl_tensile_test_specimen = etl_tensile_test_specimen(df_Specimen, Tensile_Test_ID, sheet_name)
                    op_etl_tensile_test_specimen.to_sql(name="Tensile_Test_Curves", con=connection, if_exists='append', index=False)
 
            print("Uploading file to SharePoint...")
            response = save_file_to_sharepoint(tensile_test_file_path, '/Exported_Files/tensile_test/', 'application/vnd.ms-excel')
 
            if response.status_code != 200:
                return json.dumps({"status": "error", "message": "Tensile Test file upload to SharePoint failed"})
 
            connection.commit()
            return json.dumps({"status": "success", "message": "ETL process completed successfully"})
 
    except Exception as e:
        return json.dumps({"status": "error", "message": f"An unexpected error occurred: {str(e)}"})
