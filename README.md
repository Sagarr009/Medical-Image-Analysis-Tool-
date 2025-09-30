# 🩺 Medical Image Analysis Tool 🔬

An **AI-powered web application** built with **Streamlit** that analyzes medical images (X-ray, MRI, CT, Ultrasound, etc.) and provides structured diagnostic insights, patient-friendly explanations, and references from recent medical literature.  

The app uses **Google Gemini AI** (via Agno Agent framework) and integrates **DuckDuckGo search** to provide contextual medical references.

---

## ✨ Features

- 📤 Upload medical images (JPG, JPEG, PNG, BMP, GIF).  
- 🔍 Automated AI analysis:
  - Detects **image modality** and anatomical region.  
  - Provides **systematic findings** with measurements.  
  - Suggests **primary & differential diagnoses** with confidence.  
  - Highlights **critical observations**.  
- 🧑‍⚕️ Patient-friendly explanation without heavy jargon.  
- 📚 Contextual references from **recent medical literature**.  
- 🎨 Modern UI with a responsive layout (Streamlit + custom CSS).  

---

## 🛠 Installation & Setup

### 1. Clone the repository
git clone https://github.com/Sagarr009/Medical-Image-Analysis-Tool-.git
cd Medical-Image-Analysis-Tool-

### 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

### 3. Create a requirements.txt file with:
streamlit
Pillow
agno

Then install:
pip install -r requirements.txt

### 5. You need a Google Gemini API key.
GOOGLE_API_KEY = "your_api_key_here"

** Running the App
** streamlit run app.py
 Open your browser at http://localhost:8501.



