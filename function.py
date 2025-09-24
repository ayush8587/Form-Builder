import os

def create_form_from_name(form_name):
    """
    Generates an API payload with a static schema, makes an API call
    to create a form, and extracts the form preview URL.

    Args:
        form_name: The name of the form to be created.

    Returns:
        A string containing the form preview URL on success, or a dictionary
        with an 'error' key on failure.
    """
    # Retrieve the API authorization token from an environment variable
    api_auth_token = os.environ.get('API_AUTH_TOKEN')

    if not api_auth_token:
        print("Error: API_AUTH_TOKEN environment variable not set.")
        return {"error": "API authorization token is not configured."}


    # Use a static JSON schema with UUIDs
    import uuid # Ensure uuid is imported if not already

    # Construct the API payload
    payload = {
        "name": form_name,
        "schema": {
        "pages": [
            [
                {
                    "id": str(uuid.uuid4()), # Use uuid.uuid4() for unique ID
                    "type": "heading",
                    "label": "Heading",
                    "data": {"text": "Static Form: " + form_name}
                },
                {
                    "id": str(uuid.uuid4()), # Use uuid.uuid4() for unique ID
                    "type": "short-text",
                    "label": "Short Text",
                    "data": {"label": "Enter your feedback:", "required": False}
                },
                 {
                    "id": str(uuid.uuid4()), # Use uuid.uuid4() for unique ID
                    "type": "short-text",
                    "label": "Short Text",
                    "data": {"label": "Click the button", "required": False}
                }
            ]
        ]
    },
        "settings": {},
        "teamBotId": "6e3050c0-bb1c-11ea-8d89-1b3a4a22a978" # Use the same teamBotId as before
    }

    # Define the API URL and headers, using the token from the environment variable
    api_url = "https://formapi.emitrr.com/forms"
    headers = {
        "Authorization": f"Bearer {api_auth_token}" # Use f-string for Bearer token
    }


    print(f"Attempting to create form via API: {form_name}")
    try:
        # Make the API call
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        response_data = response.json()

        # Extract the form ID
        if isinstance(response_data, dict) and '_id' in response_data:
            form_id = response_data['_id']
            # Construct the form preview URL
            form_preview_url = f"https://accounts.emitrr.com/emitrr/forms/preview/form/{form_id}"
            print(f"Successfully created form via API. Preview URL: {form_preview_url}")
            return form_preview_url
        else:
            print("API call successful, but could not find '_id' in the response.")
            return {"error": "Could not extract form ID from API response."}

    except requests.exceptions.RequestException as e:
        print(f"Error sending API request for form '{form_name}': {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        print("Error decoding JSON from API response.")
        return {"error": "Invalid JSON response from API."}
    except Exception as e:
        print(f"An unexpected error occurred during form creation API call: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

# Add instructions for setting the environment variable:
# In a production environment like Google App Engine, you would set the environment variable
# 'API_AUTH_TOKEN' with the value of your bearer token. This is typically done in the
# app.yaml file or through the cloud console.

# For example, in app.yaml:
# env_variables:
#   API_AUTH_TOKEN: "YOUR_BEARER_TOKEN_HERE"

# In a local development environment, you can set it using:
# export API_AUTH_TOKEN="YOUR_BEARER_TOKEN_HERE"
# or by creating a .env file and using a library like python-dotenv.
