import requests
import streamlit as st
from dotenv import load_dotenv 
import os

load_dotenv()


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "47be4459-abd0-4038-84ee-be66a726a1dd"
FLOW_ID = "67f25f1b-ecb1-43e4-955f-cf74fa839970"

APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "Customer_FAQ"  # The endpoint name of the flow


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    # Streamlit's built-in CSS styling for cleaner appearance
    st.set_page_config(page_title="Chat Interface", layout="centered")

    # Title
    st.markdown("<h1 style='text-align: center; color: #1e88e5;'>Customer Support RAG</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5c6bc0;'>Ask your questions and get answers instantly!</p>", unsafe_allow_html=True)
    
    # Create two columns for the message box and response display
    col1, col2 = st.columns([3, 1])

    with col1:
        # Message input with placeholder and background color
        message = st.text_area("Type your question here", placeholder="Ask something...", height=150, key="message", label_visibility="collapsed", max_chars=500)

    with col2:
        # Display a stylish "Run Flow" button
        run_button = st.button("Send", key="run_button", use_container_width=True)

    # Handling button click action
    if run_button:
        if not message.strip():
            st.error("Please enter a message!", icon="🚨")
            return
        
        try:
            with st.spinner("Processing your request..."):
                response = run_flow(message)
            
            # Extract the response and display it
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(f"<div style='background-color: #f1f8e9; padding: 10px; border-radius: 5px; font-size: 16px; color: #388e3c;'>{response_text}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error occurred: {str(e)}", icon="⚠️")

    # Sidebar styling
    st.sidebar.title("About")
    st.sidebar.markdown("""
        This is a customer service chatbot that can answer questions related to your account and services.
        
        - **Endpoint:** Customer Information
        - **Powered by Langflow and Astra**
    """)

    # Custom Footer
    st.markdown("""
    <footer style='text-align: center; font-size: 14px; color: #b0bec5; padding: 10px;'>
        Developed by Simonetti Francesco &copy; 2024
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
