import requests
import pandas as pd
from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI()

# Helper function to fetch data from Rick and Morty API
def fetch_api_data(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API")

# Helper function to normalize nested JSON data
def normalize_data(data, sep='_'):
    # Flatten the JSON data using pandas json_normalize
    return pd.json_normalize(data, sep=sep)

# FastAPI route to fetch and normalize data from the Rick and Morty API
@app.get("/get_data/{table_name}")
async def get_data(table_name: str):
    # Define the API URLs based on the table name
    if table_name == 'characters':
        api_url = "https://rickandmortyapi.com/api/character/"
    elif table_name == 'episodes':
        api_url = "https://rickandmortyapi.com/api/episode/"
    else:
        raise HTTPException(status_code=400, detail="Invalid table name. Only 'characters' and 'episodes' are allowed.")
    
    # Fetch data from the API
    data = fetch_api_data(api_url)
    
    # Normalize the data using pandas json_normalize
    normalized_data = normalize_data(data['results'])
    
    # Convert the normalized data back to a list of dictionaries (for JSON response)
    result = normalized_data.to_dict(orient='records')
    
    # Return the normalized data as JSON
    return result
