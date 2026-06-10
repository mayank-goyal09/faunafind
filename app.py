import streamlit as st
import PIL.Image
from ultralytics import YOLO
import pandas as pd
from collections import Counter
import os

# --- 1. SETTING THE VIBE (Custom CSS & HUD Theme) ---
st.set_page_config(page_title="Safari Sight AI - Jungle Scanner", page_icon="🌿", layout="wide")

# Custom CSS for Premium Jungle HUD theme and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&display=swap');

    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #020c04 0%, #082110 50%, #010502 100%);
        color: #ecfdf5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Falling Leaves Container & Items */
    .leaves-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 99999;
        overflow: hidden;
    }
    
    .leaf {
        position: absolute;
        display: block;
        top: -50px;
        opacity: 0;
        pointer-events: none;
        animation: fall linear infinite;
        user-select: none;
    }
    
    @keyframes fall {
        0% {
            top: -50px;
            transform: translateX(0) rotate(0deg) scale(0.8);
            opacity: 0;
        }
        10% {
            opacity: 0.75;
        }
        90% {
            opacity: 0.75;
        }
        100% {
            top: 105vh;
            transform: translateX(100px) rotate(360deg) scale(1.1);
            opacity: 0;
        }
    }
    
    /* Leaf animations delay, duration and left positioning */
    .leaf-1  { left: 8%;   animation-duration: 14s; animation-delay: 0s;   font-size: 26px; }
    .leaf-2  { left: 22%;  animation-duration: 18s; animation-delay: 3s;   font-size: 20px; }
    .leaf-3  { left: 38%;  animation-duration: 12s; animation-delay: 1.5s; font-size: 30px; }
    .leaf-4  { left: 52%;  animation-duration: 16s; animation-delay: 5s;   font-size: 24px; }
    .leaf-5  { left: 68%;  animation-duration: 20s; animation-delay: 2.5s; font-size: 28px; }
    .leaf-6  { left: 84%;  animation-duration: 13s; animation-delay: 7s;   font-size: 22px; }
    .leaf-7  { left: 15%;  animation-duration: 15s; animation-delay: 9s;   font-size: 25px; }
    .leaf-8  { left: 32%;  animation-duration: 11s; animation-delay: 4.5s; font-size: 29px; }
    .leaf-9  { left: 48%;  animation-duration: 17s; animation-delay: 8s;   font-size: 21px; }
    .leaf-10 { left: 62%;  animation-duration: 13s; animation-delay: 10s;  font-size: 32px; }
    .leaf-11 { left: 78%;  animation-duration: 19s; animation-delay: 1.2s; font-size: 18px; }
    .leaf-12 { left: 93%;  animation-duration: 15s; animation-delay: 6.2s; font-size: 27px; }

    /* Headers */
    h1 { 
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        text-shadow: 0px 4px 15px rgba(16, 185, 129, 0.3);
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
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
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2rem;
        text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.6);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #010a03 !important;
        border-right: 1px solid rgba(16, 185, 129, 0.25) !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #a7f3d0;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #f59e0b !important;
    }
    
    /* Action Buttons */
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
        color: #020c04 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.5);
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Glassmorphic Cards */
    .hud-card {
        background: rgba(8, 33, 16, 0.4) !important;
        border-radius: 12px !important;
        padding: 22px !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 1.5rem;
    }
    
    /* Custom CSS to style st.metric container blocks */
    div[data-testid="metric-container"] {
        background: rgba(8, 33, 16, 0.35) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #10b981 !important;
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
    }

    /* Tabs Styling */
    div[data-testid="stTabBar"] {
        background-color: rgba(1, 10, 3, 0.7) !important;
        border-radius: 12px;
        padding: 6px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    button[data-testid="stTabBarTab"] {
        color: #a7f3d0 !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }
    
    button[data-testid="stTabBarTab"][aria-selected="true"] {
        background: rgba(16, 185, 129, 0.2) !important;
        color: #f59e0b !important;
        border-bottom: 2px solid #f59e0b !important;
    }
    
    /* Image Scanner Container */
    .jungle-hud-container {
        position: relative;
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 8px;
        background: rgba(1, 10, 3, 0.5);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.35);
        overflow: hidden;
        margin-bottom: 1rem;
    }
    
    .jungle-hud-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            linear-gradient(rgba(16, 185, 129, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16, 185, 129, 0.08) 1px, transparent 1px);
        background-size: 24px 24px;
        pointer-events: none;
        z-index: 2;
    }
    
    .jungle-hud-container::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #10b981, #f59e0b, #10b981, transparent);
        box-shadow: 0 0 20px 4px #10b981;
        z-index: 3;
        pointer-events: none;
        animation: scan-line 3.5s ease-in-out infinite;
    }
    
    @keyframes scan-line {
        0% { top: 0%; }
        50% { top: 100%; }
        100% { top: 0%; }
    }

    /* Tables */
    div[data-testid="stTable"] table { 
        color: #ecfdf5 !important; 
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    div[data-testid="stTable"] th { 
        background-color: rgba(16, 185, 129, 0.2) !important; 
        color: #f59e0b !important; 
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        border-bottom: 2px solid rgba(16, 185, 129, 0.4) !important;
    }
    
    div[data-testid="stTable"] td {
        background-color: rgba(1, 10, 3, 0.4) !important;
        border-bottom: 1px solid rgba(16, 185, 129, 0.15) !important;
    }
    
    /* File Uploader override */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(16, 185, 129, 0.6) !important;
        background-color: rgba(1, 10, 3, 0.8) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #f59e0b !important;
        background-color: rgba(8, 33, 16, 0.75) !important;
    }
    
    /* Custom glow highlights */
    .glow-green {
        color: #10b981;
        text-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
    }
    
    .glow-gold {
        color: #f59e0b;
        text-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INJECT LEAVES ANIMATION ---
def inject_leaves():
    leaves_html = """
    <div class="leaves-container">
        <div class="leaf leaf-1">🍃</div>
        <div class="leaf leaf-2">🌿</div>
        <div class="leaf leaf-3">🍂</div>
        <div class="leaf leaf-4">🍃</div>
        <div class="leaf leaf-5">🌿</div>
        <div class="leaf leaf-6">🍂</div>
        <div class="leaf leaf-7">🍁</div>
        <div class="leaf leaf-8">🍃</div>
        <div class="leaf leaf-9">🌿</div>
        <div class="leaf leaf-10">🍂</div>
        <div class="leaf leaf-11">🌿</div>
        <div class="leaf leaf-12">🍃</div>
    </div>
    """
    st.markdown(leaves_html, unsafe_allow_html=True)

inject_leaves()

# --- 3. THE MODEL LOADER ---
@st.cache_resource
def load_model():
    for path in ['best.pt', 'runs/detect/train2/weights/best.pt', 'runs/detect/train/weights/best.pt']:
        if os.path.exists(path):
            return YOLO(path)
    return None

model = load_model()

# --- 4. TOP TITLE HEADER ---
st.markdown("<h1 style='text-align: center;'>🌿 <span class='gradient-text'>Safari Sight AI</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Autonomous Wildlife Identification & Population Tracking</div>", unsafe_allow_html=True)

if model is None:
    st.error("🚨 **Model Not Found!** Could not locate your `best.pt` file. Please ensure your trained model is in the project folder.", icon="❌")
    st.stop()

# --- 5. TOP LEVEL Navigation ---
app_mode = st.radio(
    "Navigation Modes",
    ["🐾 Jungle AI Scanner", "📊 Reserve Census Dashboard"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br/>", unsafe_allow_html=True)

# Load CSV Census Data
@st.cache_data
def load_census_data():
    if os.path.exists("Wildlife_Population_Report.csv"):
        return pd.read_csv("Wildlife_Population_Report.csv")
    return pd.DataFrame(columns=["filename", "buffalo", "zebra", "elephant", "rhino"])

df_census = load_census_data()

# ----------------- VIEW 1: JUNGLE AI SCANNER -----------------
if app_mode == "🐾 Jungle AI Scanner":
    
    # Sidebar controls
    with st.sidebar:
        st.image("sidebar_jungle.png", use_container_width=True)
        st.header("⚙️ Scanner Settings")
        st.markdown("Adjust the sensitivity of the AI. Lower confidence detects more animals, but might make mistakes.")
        conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.35, 0.05)
        
        st.markdown("---")
        st.markdown("### 📸 Image Upload")
        uploaded_file = st.file_uploader("Drop a snapshot from the reserve", type=['jpg', 'jpeg', 'png'])

    # State management
    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None

    if uploaded_file is not None:
        st.session_state.selected_image = None

    img_source = None
    img_name = None

    if uploaded_file is not None:
        img_source = uploaded_file
        img_name = uploaded_file.name
    elif st.session_state.selected_image is not None:
        img_source = st.session_state.selected_image
        img_name = os.path.basename(st.session_state.selected_image)

    # Perform prediction
    if img_source is not None:
        img = PIL.Image.open(img_source)
        
        with st.spinner("Scanning the horizon... 🦒"):
            results = model.predict(img, conf=conf_threshold)
        
        # Display Columns
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            st.subheader("🔍 Satellite View")
            
            # Draw HUD grid and scanner laser
            st.markdown('<div class="jungle-hud-container">', unsafe_allow_html=True)
            annotated_img = results[0].plot()
            st.image(annotated_img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"📡 AI HUD Scanning Feed Active — {img_name}")
            
            if st.session_state.selected_image is not None:
                if st.button("🔄 Clear Scan & Choose Another Image", use_container_width=True):
                    st.session_state.selected_image = None
                    st.rerun()
            
        with col2:
            st.subheader("📊 Expedition Report")
            
            names = results[0].names
            classes = [names[int(c)] for c in results[0].boxes.cls]
            counts = Counter(classes)
            
            if counts:
                total_animals = sum(counts.values())
                st.success(f"✅ Successfully tracked {total_animals} animal{'s' if total_animals > 1 else ''}!")
                
                # Table details
                df = pd.DataFrame.from_dict(counts, orient='index', columns=['Count detected'])
                st.table(df)
                
                # Download CSV Report
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
        st.info("💡 **Awaiting Input:** Upload a photo in the sidebar, or select one of the reserve snapshots below to test the AI scanner.")
        
        st.markdown("### 🐾 Reserve Gallery")
        st.markdown("Choose a preloaded photo to analyze immediately:")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🐃 Buffalo", "🐘 Elephant", "🦏 Rhino", "🦓 Zebra"])
        
        samples = {
            "buffalo": [f"sample_images/buffalo_{i}.jpg" for i in range(1, 6)],
            "elephant": [f"sample_images/elephant_{i}.jpg" for i in range(1, 6)],
            "rhino": [f"sample_images/rhino_{i}.jpg" for i in range(1, 6)],
            "zebra": [f"sample_images/zebra_{i}.jpg" for i in range(1, 6)]
        }
        
        def render_gallery_tab(sample_list, key_prefix):
            cols = st.columns(5)
            for idx, img_path in enumerate(sample_list):
                with cols[idx]:
                    st.image(img_path, use_container_width=True, caption=f"Snapshot #{idx+1}")
                    if st.button(f"Scan #{idx+1}", key=f"{key_prefix}_{idx}", use_container_width=True):
                        st.session_state.selected_image = img_path
                        st.rerun()

        with tab1:
            render_gallery_tab(samples["buffalo"], "btn_buf")
        with tab2:
            render_gallery_tab(samples["elephant"], "btn_ele")
        with tab3:
            render_gallery_tab(samples["rhino"], "btn_rhi")
        with tab4:
            render_gallery_tab(samples["zebra"], "btn_zeb")

# ----------------- VIEW 2: RESERVE CENSUS DASHBOARD -----------------
else:
    st.markdown("<h2 style='text-align: center; margin-bottom:1.5rem;'>📊 Reserve Census & Population Analytics</h2>", unsafe_allow_html=True)
    
    if df_census.empty:
        st.warning("⚠️ No historical Census logbook found. Place your `Wildlife_Population_Report.csv` in the root folder.")
    else:
        # Calculate summary numbers
        total_buffalo = int(df_census['buffalo'].sum())
        total_zebra = int(df_census['zebra'].sum())
        total_elephant = int(df_census['elephant'].sum())
        total_rhino = int(df_census['rhino'].sum())
        total_wildlife = total_buffalo + total_zebra + total_elephant + total_rhino
        total_records = len(df_census)
        
        # Display key metrics in 4 columns
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Total Wildlife Counted", f"{total_wildlife:,}", help="Sum of all species detected historically.")
        with m_col2:
            st.metric("Active Camera Sectors", f"{total_records:,}", help="Total number of logged image reports.")
        with m_col3:
            st.metric("Average Herd Density", f"{round(total_wildlife / max(1, total_records), 2)}", help="Average animal count per photo.")
            
        # Species diversity / Shannon entropy approximation for fun
        counts_list = [total_buffalo, total_zebra, total_elephant, total_rhino]
        richness = sum(1 for c in counts_list if c > 0)
        with m_col4:
            st.metric("Species Richness Index", f"{richness} / 4", help="Distinct species classes identified in the reserve.")
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Dashboard charts and breakdowns
        c_col1, c_col2 = st.columns([1, 1], gap="large")
        
        with c_col1:
            st.subheader("🦒 Population Distribution by Species")
            species_df = pd.DataFrame({
                "Species": ["Buffalo 🐃", "Elephant 🐘", "Rhino 🦏", "Zebra 🦓"],
                "Total Counted": [total_buffalo, total_elephant, total_rhino, total_zebra]
            }).set_index("Species")
            
            st.bar_chart(species_df, color="#10b981")
            
        with c_col2:
            st.subheader("🔥 Species Hotspots (High Density Sectors)")
            # Find filename where each species count is maximized
            idx_buf = df_census['buffalo'].idxmax()
            idx_ele = df_census['elephant'].idxmax()
            idx_rhi = df_census['rhino'].idxmax()
            idx_zeb = df_census['zebra'].idxmax()
            
            hotspots = pd.DataFrame({
                "Species": ["Buffalo 🐃", "Elephant 🐘", "Rhino 🦏", "Zebra 🦓"],
                "Max Sector File": [
                    df_census.loc[idx_buf, 'filename'],
                    df_census.loc[idx_ele, 'filename'],
                    df_census.loc[idx_rhi, 'filename'],
                    df_census.loc[idx_zeb, 'filename']
                ],
                "Peak Herd Size": [
                    int(df_census.loc[idx_buf, 'buffalo']),
                    int(df_census.loc[idx_ele, 'elephant']),
                    int(df_census.loc[idx_rhi, 'rhino']),
                    int(df_census.loc[idx_zeb, 'zebra'])
                ]
            }).set_index("Species")
            
            st.table(hotspots)
            
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # Log search section
        st.subheader("📋 Search Census Registry Logs")
        search_query = st.text_input("🔍 Search logs by image file name (e.g. '1 (66).jpg' or '35'):", "")
        
        # Filtering logs based on query
        if search_query:
            filtered_df = df_census[df_census['filename'].astype(str).str.contains(search_query, case=False)]
        else:
            filtered_df = df_census
            
        st.markdown(f"Displaying **{len(filtered_df)}** of **{len(df_census)}** camera scans:")
        st.dataframe(
            filtered_df.style.format({
                "buffalo": "{:.0f}",
                "zebra": "{:.0f}",
                "elephant": "{:.0f}",
                "rhino": "{:.0f}"
            }), 
            use_container_width=True
        )
