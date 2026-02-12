import streamlit as st
from datetime import datetime, timedelta

def show_login(conn, cookie_manager):
    st.title("🔐 Login")
    
    # Form Login
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")
        
        if submit:
            try:
                # 1. Autentikasi via Supabase
                res = conn.client.auth.sign_in_with_password({"email": email, "password": password})
                
                if res.user:
                    # 2. Set Session State untuk akses instan
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = res.user.email
                    
                    # 3. Tulis Cookie Manual ke Browser
                    # Cookie ini akan bertahan selama 1 hari (bisa disesuaikan)
                    expiry = datetime.now() + timedelta(days=1)
                    
                    cookie_manager.set(
                        cookie="is_logged_in", 
                        value="true", 
                        expires_at=expiry
                    )
                    cookie_manager.set(
                        cookie="user_email", 
                        value=res.user.email, 
                        expires_at=expiry
                    )
                    
                    st.success("Login Berhasil! Mengalihkan...")
                    st.rerun()
                    
            except Exception:
                st.error("Login Gagal: Pastikan email dan password benar.")
