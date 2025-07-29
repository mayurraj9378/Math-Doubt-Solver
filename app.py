import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Function to extract text from image using Gemini API
def extract_text_from_image(image_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = "Extract the mathematical problem text from the provided image accurately."
    # Pass the image dictionary directly, not as a list
    response = model.generate_content([prompt, image_data])
    return response.text

# Function to generate step-by-step solution using Gemini API
def generate_solution(problem_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an expert mathematician. Solve the following math problem step by step in a clear and concise manner. 
    Ensure each step is numbered and explained briefly. Provide the final answer at the end.
    Problem: {problem_text}
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit app configuration
st.set_page_config(page_title="Math Doubt Solver", page_icon="🧮")
st.title("Math Doubt Solver 🧮")
st.write("Upload an image of a math problem or enter it as text, and get a step-by-step solution!")

# Input options
input_method = st.radio("Choose input method:", ("Upload Image", "Enter Text"))

# Initialize problem text
problem_text = ""

# Handle image upload
if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image of the math problem (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Math Problem", use_container_width=True)
        
        # Prepare image data for Gemini API
        bytes_data = uploaded_file.getvalue()
        image_data = {"mime_type": uploaded_file.type, "data": bytes_data}
        
        # Extract text from image
        with st.spinner("Extracting text from image..."):
            problem_text = extract_text_from_image(image_data)
        st.subheader("Extracted Problem")
        st.write(problem_text)

# Handle text input
elif input_method == "Enter Text":
    problem_text = st.text_area("Enter the math problem:", placeholder="e.g., Solve the equation: 2x + 3 = 7")

# Generate solution button
if st.button("Solve Problem") and problem_text:
    with st.spinner("Generating step-by-step solution..."):
        solution = generate_solution(problem_text)
    st.subheader("Step-by-Step Solution")
    st.markdown(solution)

# Instructions for setup
st.sidebar.header("Setup Instructions")
st.sidebar.write("""
1. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the project directory with the following content:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install required libraries: `pip install streamlit google-generativeai pillow python-dotenv`.
4. Run the app: `streamlit run app.py`.
""")