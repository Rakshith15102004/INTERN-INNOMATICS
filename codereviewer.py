import openai
import streamlit as st
import json

# OpenAI API Key (Replace with your own key)
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to review code using OpenAI API
def review_code(code, category):
    prompt = f"Analyze the following {category} Python code for bugs, improvements, and best practices. Provide fixed code snippets and explanations:\n\n{code}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 for better results
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("AI Code Reviewer")
st.write("Submit your Python code to receive bug fixes and optimizations.")

# Code input
code = st.text_area("Enter your Python code:", height=200)
category = st.selectbox("Select Code Category:", ["General", "Machine Learning", "Web Scraping", "Data Processing"])

if st.button("Review Code"):
    if code:
        with st.spinner("Analyzing code..."):
            result = review_code(code, category)
            st.subheader("AI Suggestions and Fixes:")
            st.text_area("Output:", result, height=300)
            
            # Provide download option
            json_data = json.dumps({"original_code": code, "review": result}, indent=4)
            st.download_button("Download Report", json_data, "code_review.json", "application/json")
    else:
        st.warning("Please enter some code to analyze.")
