import streamlit as st
from st_supabase_connection import SupabaseConnection
# Mengimpor fungsi dari file lokal
from login import show_login
from upload_data import show_upload_dashboard

# Konfigurasi halaman tunggal
st.set_page_config(page_title="Sistem Upload Data", layout="wide")

# Koneksi Global
conn = st.connection("supabase", type=SupabaseConnection)

# Inisialisasi status login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Navigasi
if not st.session_state["authenticated"]:
    show_login(conn)
else:
    show_upload_dashboard(conn)
