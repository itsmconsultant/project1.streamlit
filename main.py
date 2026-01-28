import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login
from upload_data import show_upload_dashboard
# Import file menu/halaman lain di sini nanti

st.set_page_config(page_title="Portal System", layout="wide")

# CSS untuk tampilan Grid Kotak Putih (Dashboard Style)
st.markdown("""
    <style>
    .main-button {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        color: black;
        font-weight: bold;
        display: block;
        margin-bottom: 20px;
        text-decoration: none;
    }
    .main-button:hover {
        background-color: #f0f2f6;
        border-color: #ff4b4b;
    }
""", unsafe_allow_html=True)

conn = st.connection("supabase", type=SupabaseConnection)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu" # Halaman awal setelah login

# --- LOGIKA NAVIGASI ---
if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # Sidebar Global
    st.sidebar.title("Informasi Akun")
    st.sidebar.write(f"Logged in as:\n{st.session_state['user_email']}")
    
    if st.sidebar.button("Home Menu"):
        st.session_state["current_page"] = "menu"
        st.rerun()
        
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    # Konten berdasarkan halaman yang dipilih
    if st.session_state["current_page"] == "menu":
        # TAMPILAN MENU UTAMA (GRID KOTAK PUTIH)
        st.title("Selamat Datang di Portal Utama")
        st.subheader("Pilih Layanan:")
        
        # Membuat Grid 4 kolom seperti di gambar Anda
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📤 Upload Data", use_container_width=True):
                st.session_state["current_page"] = "upload"
                st.rerun()
        
        with col2:
            if st.button("📊 Report Sales", use_container_width=True):
                st.info("Halaman ini sedang dikembangkan")
        
        # Tambahkan kotak lainnya di sini sesuai kebutuhan
        with col3: st.button("📦 Inventory", use_container_width=True)
        with col4: st.button("💰 Settlement", use_container_width=True)

    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
