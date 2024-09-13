import os
from dotenv import load_dotenv

load_dotenv()

# The URL of your FastAPI application
API_URL = os.getenv("API_URL")

import requests
import json
import pandas as pd

def test_predict_endpoint():
    # Endpoint we want to test
    endpoint = f"{API_URL}/predict"

    # Sample message to send to the API
    message = "MAXI is an Electronics store which sells Televisions, Air Conditioners, Refrigerators and other basic Home Appliances. The target audience is Tech-enthusiasts and Home-Decor Experts. The Social Media platform is Instagram and the time period is September"

    # Prepare the payload
    payload = {
        "message": message
    }

    # Make the POST request
    response = requests.post(endpoint, json=payload)

    # Check if the request was successful
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Parse the JSON response
    response_data = response.json()

    # Check if the response contains the 'response' key
    assert 'response' in response_data, "Response does not contain 'response' key"

    # Print the response for inspection
    print("API Response:")
    print(json.dumps(response_data, indent=2))

    # Convert JSON to DataFrame
    df = pd.DataFrame(json.loads(response_data['response']))

    # Convert DataFrame to HTML table
    html_table = df.to_html(index=False)

    # Create a complete HTML document
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Content Calendar</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Content Calendar</h1>
        {html_table}
    </body>
    </html>
    """

    # Save HTML to file
    output_file = 'content_calendar.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Content calendar saved to {output_file}")

    # Display the table in console (optional)
    print("\nContent Calendar Table:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    test_predict_endpoint()
    print("Test completed successfully!")