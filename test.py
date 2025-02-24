import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langflow.load import run_flow_from_json
# Import the utility to load and resolve JSON
from Utilities import load_and_resolve_json

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)  # Load from .env by default
# This loads environment variables into the app

app = Flask(__name__)

# Tweaks (can be modified based on your flow)
TWEAKS = {
    "ChatOutput-te5Z1": {},
    "AzureOpenAIModel-Qh5EO": {},
    "ChatInput-6hCeH": {}
}

# Path to your LangFlow JSON file
# FLOW_FILE = "demo_test.json"
FLOW_FILE = "Azureopenaiflow.json"


@app.route('/')
def home():
    return "LangFlow API is running! Go to /chat to interact."


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # Accept JSON request

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    print(f"User Input: {user_input}")

    try:
        # Load and resolve the LangFlow JSON (with environment variables replaced)
        flow_data = load_and_resolve_json(FLOW_FILE)

        # Run LangFlow with the provided input and the resolved JSON
        result = run_flow_from_json(flow=flow_data,  # Use the loaded flow_data
                                    input_value=user_input,  # Pass the actual user input
                                    session_id="",  # provide a session id if you want to use session state
                                    fallback_to_env_vars=True,  # False by default
                                    tweaks=TWEAKS)

        # Extract the response from LangFlow output
        if result and hasattr(result[0], "outputs") and result[0].outputs:
            output_data = result[0].outputs[0].results

            # If output_data is a list, take its first element
            if isinstance(output_data, list) and output_data:
                output_data = output_data[0]

            # Attempt to extract the text from the output_data
            if isinstance(output_data, dict) and "text" in output_data:
                answer = output_data["text"]
            else:
                answer = str(output_data)
        else:
            answer = "No response from model"

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)  # Run locally in debug mode
