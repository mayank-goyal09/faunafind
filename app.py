import streamlit as st
import PIL.Image
from ultralytics import YOLO
import pandas as pd
from collections import Counter
import os

# --- 1. SETTING THE VIBE (Custom CSS) ---
st.set_page_config(page_title="Safari Sight AI - Jungle Scanner", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&display=swap');

    /* Main Background & Text */
    .stApp {
        background: linear-gradient(135deg, #041208 0%, #0d2914 50%, #030804 100%);
        color: #ecfdf5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers with gradient text */
    h1 { 
        background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        text-shadow: 0px 4px 12px rgba(16, 185, 129, 0.15);
        text-align: center;
        margin-bottom: 0.5rem;
    }
    h2, h3, h4, h5, h6 { 
        color: #f59e0b !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #a7f3d0;
        font-size: 1.25rem;
        font-weight: 300;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
        text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #030a04 !important;
        border-right: 1px solid rgba(16, 185, 129, 0.15) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #a7f3d0;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #f59e0b !important;
        -webkit-text-fill-color: #f59e0b !important;
    }
    
    /* Buttons */
    .stButton>button { 
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: #ffffff !important; 
        border-radius: 10px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        padding: 0.6rem 1.8rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.75px;
        width: 100%;
    }
    
    .stButton>button:hover { 
        background: linear-gradient(90deg, #059669 0%, #f59e0b 100%);
        color: #041208 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Cards/Containers & Metric Blocks */
    div[data-testid="stVerticalBlockBorderWrapper"], 
    div[data-testid="element-container"] .css-1r6slb0,
    div[data-testid="element-container"] .css-12oz5g7 {
         background: rgba(13, 41, 20, 0.45) !important;
         border-radius: 12px !important;
         padding: 20px !important;
         border: 1px solid rgba(16, 185, 129, 0.2) !important;
         backdrop-filter: blur(12px);
         box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    
    /* Tabs custom styling */
    div[data-testid="stTabBar"] {
        background-color: rgba(4, 18, 8, 0.6) !important;
        border-radius: 12px;
        padding: 6px;
        border: 1px solid rgba(16, 185, 129, 0.15);
    }
    
    button[data-testid="stTabBarTab"] {
        color: #a7f3d0 !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }
    
    button[data-testid="stTabBarTab"][aria-selected="true"] {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #f59e0b !important;
        border-bottom: 2px solid #f59e0b !important;
    }
    
    /* Tables */
    div[data-testid="stTable"] table { 
        color: #ecfdf5 !important; 
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    div[data-testid="stTable"] th { 
        background-color: rgba(16, 185, 129, 0.15) !important; 
        color: #f59e0b !important; 
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        border-bottom: 2px solid rgba(16, 185, 129, 0.3) !important;
    }
    
    div[data-testid="stTable"] td {
        background-color: rgba(4, 18, 8, 0.3) !important;
        border-bottom: 1px solid rgba(16, 185, 129, 0.1) !important;
    }
    
    /* File Uploader override */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(16, 185, 129, 0.5) !important;
        background-color: rgba(4, 18, 8, 0.7) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #f59e0b !important;
        background-color: rgba(13, 41, 20, 0.6) !important;
    }

    [data-testid="stFileUploadDropzone"] [data-testid="stMarkdownContainer"] {
        color: #ecfdf5 !important;
    }
    
    /* Info/Success/Warning boxes styling overrides */
    div[data-testid="stAlert"] {
        background-color: rgba(4, 18, 8, 0.75) !important;
        border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
    }
    
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
        color: #ecfdf5 !important;
    }
    
    /* Slider custom aesthetics */
    div[data-testid="stSlider"] [class^="st-"] {
        color: #10b981;
    }
    
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #f59e0b !important;
        border: 2px solid #10b981 !important;
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
    st.image("sidebar_jungle.png", use_container_width=True)
    st.header("⚙️ Scanner Settings")
    st.markdown("Adjust the sensitivity of the AI. Lower confidence detects more animals, but might make mistakes.")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.35, 0.05)
    
    st.markdown("---")
    st.markdown("### 📸 Image Upload")
    uploaded_file = st.file_uploader("Drop a snapshot from the reserve", type=['jpg', 'jpeg', 'png'])

# --- 4. DATA HANDLING & STATE ---
# Initialize session state for selected sample image
if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None

# If user uploads a file, reset the sample selection so the uploaded file takes precedence
if uploaded_file is not None:
    st.session_state.selected_image = None

# Determine which image source to use
img_source = None
img_name = None

if uploaded_file is not None:
    img_source = uploaded_file
    img_name = uploaded_file.name
elif st.session_state.selected_image is not None:
    img_source = st.session_state.selected_image
    img_name = os.path.basename(st.session_state.selected_image)

# --- 4. THE ACTION ---
if img_source is not None:
    # Open image
    img = PIL.Image.open(img_source)
    
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
        st.image(annotated_img, caption=f"AI Vision Feed Active - {img_name}", use_container_width=True)
        
        # Add a reset button if it's a sample image
        if st.session_state.selected_image is not None:
            if st.button("🔄 Clear Scan & Choose Another Image", use_container_width=True):
                st.session_state.selected_image = None
                st.rerun()
        
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
                file_name=f"safari_scan_{img_name}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        else:
            st.warning("🌵 No wildlife detected in this sector at the current threshold. Try lowering the sensitivity.")

else:
    # Landing page state
    st.info("💡 **Awaiting Input:** Upload a photo in the sidebar, or select one of the reserve snapshots below to test the AI scanner.")
    
    st.markdown("### 🐾 Reserve Gallery")
    st.markdown("Choose a preloaded photo to analyze immediately:")
    
    # Tabs for different species
    tab1, tab2, tab3, tab4 = st.tabs(["🐃 Buffalo", "🐘 Elephant", "🦏 Rhino", "🦓 Zebra"])
    
    # Local sample paths
    samples = {
        "buffalo": [
            "sample_images/buffalo_1.jpg",
            "sample_images/buffalo_2.jpg",
            "sample_images/buffalo_3.jpg",
        ],
        "elephant": [
            "sample_images/elephant_1.jpg",
            "sample_images/elephant_2.jpg",
            "sample_images/elephant_3.jpg",
        ],
        "rhino": [
            "sample_images/rhino_1.jpg",
            "sample_images/rhino_2.jpg",
            "sample_images/rhino_3.jpg",
        ],
        "zebra": [
            "sample_images/zebra_1.jpg",
            "sample_images/zebra_2.jpg",
            "sample_images/zebra_3.jpg",
        ]
    }
    
    with tab1:
        cols = st.columns(3)
        for idx, img_path in enumerate(samples["buffalo"]):
            with cols[idx]:
                st.image(img_path, use_container_width=True, caption=f"Buffalo Snapshot #{idx+1}")
                if st.button(f"Scan Buffalo #{idx+1}", key=f"btn_buf_{idx}", use_container_width=True):
                    st.session_state.selected_image = img_path
                    st.rerun()
                    
    with tab2:
        cols = st.columns(3)
        for idx, img_path in enumerate(samples["elephant"]):
            with cols[idx]:
                st.image(img_path, use_container_width=True, caption=f"Elephant Snapshot #{idx+1}")
                if st.button(f"Scan Elephant #{idx+1}", key=f"btn_ele_{idx}", use_container_width=True):
                    st.session_state.selected_image = img_path
                    st.rerun()
                    
    with tab3:
        cols = st.columns(3)
        for idx, img_path in enumerate(samples["rhino"]):
            with cols[idx]:
                st.image(img_path, use_container_width=True, caption=f"Rhino Snapshot #{idx+1}")
                if st.button(f"Scan Rhino #{idx+1}", key=f"btn_rhi_{idx}", use_container_width=True):
                    st.session_state.selected_image = img_path
                    st.rerun()
                    
    with tab4:
        cols = st.columns(3)
        for idx, img_path in enumerate(samples["zebra"]):
            with cols[idx]:
                st.image(img_path, use_container_width=True, caption=f"Zebra Snapshot #{idx+1}")
                if st.button(f"Scan Zebra #{idx+1}", key=f"btn_zeb_{idx}", use_container_width=True):
                    st.session_state.selected_image = img_path
                    st.rerun()
