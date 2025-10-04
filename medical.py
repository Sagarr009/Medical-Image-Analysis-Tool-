import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st

# Set page configuration with custom favicon
st.set_page_config(
    page_title="Medical Image Analysis",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main-title {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .report-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .stSpinner {
        text-align: center;
        color: #3498db;
    }
    </style>
""", unsafe_allow_html=True)

# Set your API Key (Replace with your actual key)
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Ensure API Key is provided
if not GOOGLE_API_KEY:
    raise ValueError("⚠️ Please set your Google API Key in GOOGLE_API_KEY")

# Initialize the Medical Agent
medical_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

# Medical Analysis Query
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the medical image and structure your response as follows:

### 1. Image Type & Region
- Identify imaging modality (X-ray/MRI/CT/Ultrasound/etc.).
- Specify anatomical region and positioning.
- Evaluate image quality and technical adequacy.

### 2. Key Findings
- Highlight primary observations systematically.
- Identify potential abnormalities with detailed descriptions.
- Include measurements and density where relevant.

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level.
- List differential diagnoses ranked by likelihood.
- Support each diagnosis with observed evidence.
- Highlight critical/urgent findings.

### 4. Patient-Friendly Explanation
- Simplify findings in clear, non-technical language.
- Avoid medical jargon or provide easy definitions.
- Include relatable visual analogies.

### 5. Research Context
- Use DuckDuckGo search to find recent medical literature.
- Search for standard treatment protocols.
- Provide 2-3 key references supporting the analysis.

Ensure a structured and medically accurate response using clear markdown formatting.
"""

# Function to analyze medical image
def analyze_medical_image(image_path):
    """Processes and analyzes a medical image using AI."""
    
    # Open and resize image
    image = PILImage.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    # Save resized image
    temp_path = "temp_resized_image.png"
    resized_image.save(temp_path)

    # Create AgnoImage object
    agno_image = AgnoImage(filepath=temp_path)

    # Run AI analysis
    try:
        response = medical_agent.run(query, images=[agno_image])
        return response.content
    except Exception as e:
        return f"⚠️ Analysis error: {e}"
    finally:
        # Clean up temporary file
        os.remove(temp_path)

# UI Layout
st.markdown('<h1 class="main-title">🩺 Medical Image Analysis Tool 🔬</h1>', unsafe_allow_html=True)
st.markdown(
    """
    Welcome to the **Medical Image Analysis Tool**! Upload a medical image (X-ray, MRI, CT, Ultrasound, etc.), 
    and our AI-powered system will provide a detailed analysis, including findings, diagnosis, and research insights.
    """
)

# Sidebar
with st.sidebar:
    st.header("📤 Upload Medical Image")
    st.markdown(
        """
        **Instructions**:
        1. Upload an image in JPG, JPEG, PNG, BMP, or GIF format.
        2. Click **Analyze Image** to start the analysis.
        3. View the detailed report in the main panel.
        """
    )
    uploaded_file = st.file_uploader(
        "Choose a medical image file",
        type=["jpg", "jpeg", "png", "bmp", "gif"],
        help="Supported formats: JPG, JPEG, PNG, BMP, GIF"
    )
    if uploaded_file:
        st.success("✅ Image uploaded successfully!")

# Main content
if uploaded_file is not None:
    # Display uploaded image
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(uploaded_file, caption="Uploaded Medical Image", use_column_width=True)
    
    # Analyze button
    if st.sidebar.button("Analyze Image"):
        with st.spinner("🔍 Analyzing the image... This may take a moment."):
            # Save the uploaded image to a temporary file
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Run analysis
            report = analyze_medical_image(image_path)
            
            # Display report in an expander
            with st.expander("📋 View Analysis Report", expanded=True):
                st.markdown('<div class="report-section">', unsafe_allow_html=True)
                st.markdown(report, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Clean up
            os.remove(image_path)
            st.success("✅ Analysis complete! Scroll to view the report.")
else:
    st.info("ℹ️ Please upload a medical image in the sidebar to begin analysis.")
