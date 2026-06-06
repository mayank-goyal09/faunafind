import streamlit as st
import PIL.Image
from ultralytics import YOLO
import pandas as pd
from collections import Counter
import os

# --- 1. SETTING THE VIBE (Custom CSS) ---
st.set_page_config(page_title="Safari Sight AI", page_icon="🦁", layout="wide")

st.markdown("""
    <style>
    /* Main Background & Text */
    .stApp {
        background: linear-gradient(135deg, #1A1A1D 0%, #2A2A35 100%);
        color: #E2DFD2;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Headers */
    h1 { 
        color: #F9A826; 
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        text-align: center;
        margin-bottom: 0.5rem;
    }
    h2, h3 { color: #F9A826; }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #A0AAB2;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton>button { 
        background: linear-gradient(90deg, #F9A826 0%, #F07025 100%);
        color: white; 
        border-radius: 8px; 
        border: none; 
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(249, 168, 38, 0.4);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1E1E24;
        border-right: 1px solid #333;
    }
    
    /* Cards/Containers */
    .css-1r6slb0, .css-12oz5g7 {
         background-color: rgba(255, 255, 255, 0.05);
         border-radius: 10px;
         padding: 15px;
         border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Tables */
    table { color: #E2DFD2 !important; }
    th { background-color: rgba(249, 168, 38, 0.2) !important; color: #F9A826 !important; }
    
    /* File Uploader override */
    [data-testid="stFileUploadDropzone"] {
        border-color: #F9A826;
        background-color: rgba(24, 24, 29, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN LOADER ---
@st.cache_resource
def load_model():
    # Attempt to load the model from common local paths
    for path in ['best.pt', 'runs/detect/train2/weights/best.pt', 'runs/detect/train/weights/best.pt']:
        if os.path.exists(path):
            return YOLO(path)
    return None

model = load_model()

# --- 3. THE UI LAYOUT ---
st.title("🦁 Safari Sight AI")
st.markdown("<div class='subtitle'>Autonomous Wildlife Identification & Population Tracking</div>", unsafe_allow_html=True)

if model is None:
    st.error("🚨 **Model Not Found!** Could not locate your `best.pt` file. Please ensure your trained model is in the project folder.", icon="❌")
    st.stop()

# Sidebar for controls
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1547471080-7fc2caa81f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)
    st.header("⚙️ Scanner Settings")
    st.markdown("Adjust the sensitivity of the AI. Lower confidence detects more animals, but might make mistakes.")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.35, 0.05)
    
    st.markdown("---")
    st.markdown("### 📸 Image Upload")
    uploaded_file = st.file_uploader("Drop a snapshot from the reserve", type=['jpg', 'jpeg', 'png'])

# --- 4. THE ACTION ---
if uploaded_file:
    # Open image
    img = PIL.Image.open(uploaded_file)
    
    with st.spinner("Scanning the horizon... 🦒"):
        # Run AI Inference
        # We use standard inference. Streamlit will display the visual overlay.
        results = model.predict(img, conf=conf_threshold)
    
    # Layout: Image on left, Stats on right
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.subheader("🔍 Satellite View")
        # Plot boxes on image
        annotated_img = results[0].plot()
        st.image(annotated_img, caption="AI Vision Feed Active", use_container_width=True)
        
    with col2:
        st.subheader("📊 Expedition Report")
        
        # Extract names and count them
        names = results[0].names
        classes = [names[int(c)] for c in results[0].boxes.cls]
        counts = Counter(classes)
        
        if counts:
            # Show a fun success message
            total_animals = sum(counts.values())
            st.success(f"✅ Successfully tracked {total_animals} animal{'s' if total_animals > 1 else ''}!")
            
            # Create a nice looking table
            df = pd.DataFrame.from_dict(counts, orient='index', columns=['Count detected'])
            st.table(df)
            
            # Download button for the micro-report
            csv_data = df.to_csv()
            st.download_button(
                label="📥 Download Mission Log",
                data=csv_data,
                file_name=f"safari_scan_{uploaded_file.name}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        else:
            st.warning("🌵 No wildlife detected in this sector at the current threshold. Try lowering the sensitivity.")

else:
    # Landing page state
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("💡 **Awaiting Input:** Open the sidebar menu on the left to upload a photo of a Zebra, Elephant, Buffalo, or Rhino to begin tracking.")
        # Show a placeholder image
        st.image("https://images.unsplash.com/photo-1516426122078-c23e76319801?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", caption="Awaiting deployment...", use_container_width=True)
