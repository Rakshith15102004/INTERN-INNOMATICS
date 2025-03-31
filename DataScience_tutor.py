
import streamlit as st
import google.generativeai as genai

# Replace with your Gemini API key
API_KEY = "Enter your Gemini api key here"

def configure_gemini(api_key):
    """Configures the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)

def get_data_science_response(conversation):
    """Fetches a response from the AI tutor based on the conversation history."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")
        prompt = "You are a friendly and knowledgeable AI tutor for Data Science. Maintain a conversational flow and provide helpful responses.\n\n" + conversation
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="AI Data Science Tutor", layout="centered")
st.title("💬 AI Data Science Tutor 📊")
st.markdown("Chat with an AI tutor for Data Science! Ask questions and continue the conversation naturally.")

configure_gemini(API_KEY)

if "conversation" not in st.session_state:
    st.session_state.conversation = ""

user_input = st.text_input("You:", "", key="user_input")

if st.button("Send"):
    if user_input:
        st.session_state.conversation += f"User: {user_input}\n"
        with st.spinner("Thinking..."):
            ai_response = get_data_science_response(st.session_state.conversation)
        st.session_state.conversation += f"AI Tutor: {ai_response}\n"

# Display chat history
st.subheader("Chat History")
st.write(st.session_state.conversation.replace("\n", "\n\n"))
