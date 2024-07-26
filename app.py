import streamlit as st
import openai

# OpenAIModel class definition
class OpenAIModel:
    def __init__(self, api_key, parameters):
        self.api_key = api_key
        self.parameters = parameters
        openai.api_key = api_key
    
    def generate_text(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.parameters.get("model", "gpt-4"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.parameters.get("max_tokens", 1500),
                temperature=self.parameters.get("temperature", 0.2)
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"Error: {str(e)}"

# Set Streamlit page configuration
st.set_page_config(
    page_title="MCQ Generator",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS styles for Streamlit components
st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI components
st.title("MCQ Generator")
st.markdown("### Welcome to the MCQ Generator!")
st.markdown("Upload Your Topic and get Perfect Answers.")

# Input fields for API key, topic, and number of questions
api_key = st.text_input("Enter OpenAI API Key")
topic = st.text_input("Enter Topic")
question_limit = st.number_input("Enter number of MCQ questions", min_value=1, step=1)

# Process input if all fields are provided
if topic and api_key and question_limit:
    try:
        # Initialize OpenAIModel with provided API key and parameters
        open_ai_model = OpenAIModel(
            api_key=api_key,
            parameters={
                "model": "gpt-4",
                "temperature": 0.2,
                "max_tokens": 1500,
            },
        )

        # Define the prompt for generating MCQs
        prompt = (
            f"Generate {question_limit} multiple-choice questions (MCQs) about {topic} "
            f"and provide their answers."
        )

        # Generate MCQs using the OpenAI model
        response = open_ai_model.generate_text(prompt)

        # Display generated MCQs if response is available
        if response:
            st.markdown("## Generated MCQs")
            st.markdown(response)

    except Exception as e:
        # Display error message if generation fails
        st.error(f"Error generating MCQs: {e}")
