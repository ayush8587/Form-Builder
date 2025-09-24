from flask import Flask, request, jsonify
from function import create_form_from_name
from flask import send_from_directory



app = Flask(__name__)

# Keep the existing create_form_from_name function as is.
# It already contains the logic for API calls and error handling.
# from previous_code import create_form_from_name # Assuming create_form_from_name is in a separate file

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

@app.route('/create_form', methods=['POST'])
def handle_create_form_request():
    """
    Handles the form creation request from the frontend via a POST request.
    Expects a JSON body with a 'form_name' key.
    """
    data = request.get_json()
    if not data or 'form_name' not in data:
        return jsonify({"status": "failure", "error": "Missing 'form_name' in request body"}), 400

    form_name = data['form_name']
    print(f"Received form creation request for name: {form_name}")

    result = create_form_from_name(form_name)

    if isinstance(result, str):
        # Success: result is the form preview URL
        print(f"Form created successfully. URL: {result}")
        return jsonify({"status": "success", "form_url": result}), 200
    elif isinstance(result, dict) and 'error' in result:
        # Failure: result is an error dictionary
        print(f"Form creation failed: {result['error']}")
        # Determine appropriate HTTP status code based on the error type if possible
        return jsonify({"status": "failure", "error": result['error']}), 500 # Internal Server Error for API issues
    else:
        # Unexpected return type from create_form_from_name
        print(f"Unexpected result from create_form_from_name: {result}")
        return jsonify({"status": "failure", "error": "An unexpected error occurred during form creation."}), 500

if __name__ == '__main__':
    app.run(port=5000)