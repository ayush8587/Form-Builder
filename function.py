import requests
import json
import time
import uuid


def create_form_from_name(form_name, team_bot_id, auth_key):
    """
    Generates an API payload with a static schema, makes an API call
    to create a form, and extracts the form preview URL.

    Args:
        form_name: The name of the form to be created.

    Returns:
        A string containing the form preview URL on success, or a dictionary
        with an 'error' key on failure.
    """
    payload = {
        "name": form_name,
        "schema": {
        "pages": [
            [
                {
                    "id": str(uuid.uuid4()),
                    "type": "heading",
                    "label": "Heading",
                    "data": {"text": "Static Form: " + form_name}
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "short-text",
                    "label": "Short Text",
                    "data": {"label": "Enter your feedback:", "required": False}
                },
                 {
                    "id": str(uuid.uuid4()),
                    "type": "short-text",
                    "label": "Short Text",
                    "data": {"label": "Click the button", "required": False}
                }
            ]
        ]
    },
        "settings": {},
        "teamBotId": f"{team_bot_id}"
    }
    api_url = "https://formapi.emitrr.com/forms"
    headers = {
        "Authorization": f"{auth_key}"}

    print(f"Attempting to create form via API: {form_name}")
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if isinstance(response_data, dict) and '_id' in response_data:
            form_id = response_data['_id']
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
# print(f"\nResult of creating '{test_form_name}': {preview_url}")
