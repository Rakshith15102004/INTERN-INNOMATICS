import streamlit as st
import google.generativeai as genai

# Replace with your Gemini API key
API_KEY = "Enter your api here "

def configure_gemini(api_key):
    """Configures the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)

def get_travel_options(source, destination):
    """Fetches possible travel options between source and destination."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")
        prompt = (
            f"Suggest all possible travel options from {source} to {destination}. "
            "Include flights, trains, buses, and any other viable means of transport."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("✈️ AI Travel Planner 🏝️")
st.markdown("Plan your journey with AI-powered suggestions!")

configure_gemini(API_KEY)

source = st.text_input("Enter source location:")
destination = st.text_input("Enter destination location:")

if st.button("Get Travel Options"):
    if source and destination:
        with st.spinner("Fetching travel options..."):
            travel_options = get_travel_options(source, destination)
        st.subheader("Suggested Travel Options:")
        st.write(travel_options)
    else:
        st.warning("Please enter both source and destination.")
