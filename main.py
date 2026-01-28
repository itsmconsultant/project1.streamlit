import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login
from upload_data import show_upload_dashboard

# 1. SET WIDE MODE DEFAULT
st.set_page_config(
    page_title="Portal System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS KUSTOM (Target spesifik area Main Menu)
st.markdown("""
    <style>
    /* 2. PAKSA KOLOM MELEBAR */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 calc(25% - 1rem) !important; /* Untuk 4 kolom */
        min-width: 200px !important;
    }

    /* 3. STYLE CARD UTAMA (Sangat Agresif) */
    [data-testid="stMain"] [data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] div.stButton > button {
        background-color: #ffffff !important;
        color: #31333F !important;
        border: 1px solid #e6e9ef !important;
        border-radius: 15px !important;
        
        /* Lebar Mutlak */
        width: 100% !important;
        display: block !important;
        min-height: 220px !important;
        
        /* Bayangan dan Transisi */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }

    /* Efek Hover */
    [data-testid="stMain"] div.stButton > button:hover {
        border-color: #ff4b4b !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.15) !important;
        background-color: #ffffff !important;
    }

    /* 4. RESET SIDEBAR (Tetap Standar) */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] div.stButton > button {
        width: 100% !important;
        min-height: unset !important;
        padding: 5px !important;
        border-radius: 4px !important;
        background-color: transparent !important;
        border: 1px solid rgba(49, 51, 63, 0.2) !important;
        box-shadow: none !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. KONEKSI & NAVIGASI
conn = st.connection("supabase", type=SupabaseConnection)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # SIDEBAR
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        if st.button("Home Menu", key="side_home"):
            st.session_state["current_page"] = "menu"
            st.rerun()
        if st.button("Logout", key="side_logout"):
            conn.client.auth.sign_out()
            st.session_state["authenticated"] = False
            st.rerun()

    # KONTEN UTAMA
    # Baris 1
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        if st.button("📤\n\nUpload Data", key="c1"):
            st.session_state["current_page"] = "upload"
            st.rerun()
    with row1_col2:
        st.button("📊\n\nReport Sales", key="c2", disabled=True)
    
    # Baris 2
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.button("📦\n\nInventory", key="c3", disabled=True)
    with row2_col2:
        st.button("💰\n\nSettlement", key="c4", disabled=True)


    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
