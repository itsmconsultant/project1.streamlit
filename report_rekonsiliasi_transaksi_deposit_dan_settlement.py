import streamlit as st
import pandas as pd
from sqlalchemy import text

def show_report_rekonsiliasi_transaksi_deposit_dan_settlement():
    st.title("📊 Rekonsiliasi Transaksi Deposit dan Settlement")
    st.divider()

    # 1. Input Parameter Tanggal
    col1, col2 = st.columns([1, 2])
    with col1:
        default_date = st.session_state.get('last_date', date.today())
        selected_date = st.date_input("Pilih Tanggal:", default_date)
    
    # Simpan tanggal terakhir ke session state agar tidak reset
    st.session_state['last_date'] = selected_date

    # 2. Tombol Cari
    if st.button("Tampilkan Data", use_container_width=True):
        # Inisialisasi koneksi SQL dari secrets [connections.postgresql]
        db_sql = st.connection("postgresql", type="sql")
        
        tanggal_str = selected_date.strftime("%Y-%m-%d")
        
        with st.spinner(f"Mengambil data untuk tanggal {tanggal_str}..."):
            try:
                # 3. Eksekusi Query SELECT
                # Ganti 'nama_tabel_anda' dan 'nama_kolom_tanggal' sesuai database Anda
                query = text("""
                    SELECT merchant,tanggal_proses,keterangan,jumlah_transaksi,jumlah_transaksi_sesuai_rate,penambahan_rupiah,pengurangan_rupiah,rekonsiliasi_jumlah_transaksi,rekonsiliasi_rupiah,rekonsiliasi_tambah_kurang,saldo_rekonsiliasi_rupiah
                    FROM project1.summary_deposit
                    WHERE tanggal_proses::date = :tgl
                    ORDER BY urutan ASC
                """)
                
                # Menggunakan parameter binding untuk keamanan (mencegah SQL Injection)
                df = db_sql.query(query, params={"tgl": tanggal_str})

                # 4. Menampilkan Hasil
                if not df.empty:
                    st.success(f"Ditemukan {len(df)} baris data.")
                    
                    # Fitur Download Excel/CSV
                    col_dl1, col_dl2 = st.columns(2)
                    with col_dl1:
                        st.download_button(
                            label="📥 Download CSV",
                            data=df.to_csv(index=False),
                            file_name=f"report_{tanggal_str}.csv",
                            mime="text/csv"
                        )
                    
                    # Tampilkan Tabel
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning("Tidak ada data ditemukan untuk tanggal tersebut.")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat mengambil data: {e}")

    # Tombol Kembali
    if st.sidebar.button("⬅️ Kembali ke Menu Utama"):
        st.session_state["current_page"] = "menu"
        st.rerun()
