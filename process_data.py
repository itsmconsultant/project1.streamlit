import streamlit as st
from datetime import date

def show_run_procedure(conn):
    st.title("⚙️ Jalankan Store Procedure")
    st.write("Gunakan halaman ini untuk menjalankan prosedur `run_all_procedure` berdasarkan tanggal tertentu.")
    st.divider()

    # 1. Input Tanggal
    selected_date = st.date_input("Pilih Tanggal Parameter:", date.today())
    
    # Tombol eksekusi
    if st.button("Jalankan Prosedur", use_container_width=True):
        # Konversi tanggal ke string format ISO (YYYY-MM-DD) agar sesuai dengan PostgreSQL
        tanggal_str = selected_date.strftime("%Y-%m-%d")
        
        with st.spinner(f"Sedang menjalankan prosedur untuk tanggal {tanggal_str}..."):
            try:
                # 2. Memanggil RPC (Remote Procedure Call)
                # Nama fungsi harus sesuai dengan yang ada di database
                # Parameter dikirimkan dalam bentuk dictionary: {"nama_parameter": nilai}
                response = conn.client.schema("project1").rpc(
                    "run_all_procedure", 
                    {"vgetdate": tanggal_str}
                ).execute()
                
                # 3. Menampilkan Hasil
                st.success(f"Prosedur berhasil dijalankan untuk tanggal: {tanggal_str}")
                
                # Jika procedure mengembalikan data (misal log atau status), tampilkan di sini
                if response.data:
                    st.json(response.data)
                
            except Exception as e:
                st.error(f"Gagal menjalankan prosedur: {e}")
                st.info("Pastikan parameter 'tanggal' di database bertipe DATE atau TEXT.")

    # Tombol Kembali (Opsional jika tidak lewat sidebar)
    if st.button("Kembali ke Menu Utama"):
        st.session_state["current_page"] = "menu"
        st.rerun()
