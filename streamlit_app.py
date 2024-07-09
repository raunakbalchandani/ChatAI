import streamlit as st
import requests

st.title("Travel Agent Chatbot")

question = st.text_input("Ask your travel question:")

if st.button("Ask"):
    try:
        response = requests.post('http://localhost:5000/api/ask', json={'question': question})
        response.raise_for_status()  # Raise an error for bad status codes
        answer = response.json().get('answer')
        st.write(f"Answer: {answer}")
    except requests.exceptions.RequestException as e:
        st.write("Error: Could not connect to the backend or received an invalid response.")
        st.write(f"Details: {e}")
    except ValueError as e:
        st.write("Error: Invalid response from the backend.")
        st.write(f"Details: {e}")

