import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Fungsi untuk menghasilkan data pemilih dan menghitung suara
def generate_data():
    # Jumlah Pemilih 
    n_pemilih = 32_034

    # Jumlah kecamatan, kelurahan, dan TPS
    n_kecamatan = 5
    n_kelurahan = 8
    n_tps = 16

    # Daftar nama kecamatan, kelurahan, tdan TPS
    kecamatan = ['Kecamatan A', 'Kecamatan B', 'Kecamatan C', 'Kecamatan D', 'Kecamatan E']
    kelurahan = ['Kelurahan A', 'Kelurahan B', 'Kelurahan C', 'Kelurahan D', 'Kelurahan E', 'Kelurahan F', 'Kelurahan G', 'Kelurahan H']
    tps = [f'TPS {i:02d}' for i in range(1, n_tps + 1)]

    # Bangkitkan data jumlah pemilih
    jumlah_pemilih_kecamatan = [round(n_pemilih * random.uniform(0.02, 0.04)) for _ in range(n_kecamatan)]
    jumlah_pemilih_kelurahan = [round(jumlah_pemilih_kecamatan[i // n_kelurahan] * random.uniform(0.2, 0.4)) for i in range(n_kelurahan)]
    jumlah_pemilih_tps = [round(jumlah_pemilih_kelurahan[i // n_tps] * random.uniform(0.05, 0.20)) for i in range(n_tps)]

    # Buat DataFrame untuk TPS
    df_tps = pd.DataFrame({
        'TPS': tps,
        'Jumlah Pemilih': jumlah_pemilih_tps
    })

    # Simple random sampling
    sample_tps = df_tps.sample(n=5, random_state=1)

    # Hitung suara
    results = []
    for index, row in sample_tps.iterrows():
        total_pemilih = row['Jumlah Pemilih']
        
        # Tentukan batas untuk suara A dan B
        selisih = random.randint(20, 30)  # Selisih antara 20% dan 30%
        golput = round(total_pemilih * random.uniform(0.01, 0.07))  # Golput antara 1% dan 7%
        
        # Hitung suara A dan B berdasarkan selisih
        suara_a = round((total_pemilih - golput) * (50 + selisih / 2) / 100)  # 50% + selisih/2
        suara_b = total_pemilih - suara_a - golput  # sisa untuk Paslon B

        results.append({'TPS': row['TPS'], 'Suara A': suara_a, 'Suara B': suara_b, 'Golput': golput})
    
    return pd.DataFrame(results)

# Inisialisasi Streamlit
st.title("Quick Count Hasil Pemilihan")
st.write("Selamat datang di aplikasi Quick Count! Tekan tombol di bawah untuk menghasilkan data baru.")

# Tombol untuk menghasilkan data baru
if st.button("Generate Data"):
    hasil_suara = generate_data()

    # Menghitung total suara
    total_suara_a = hasil_suara['Suara A'].sum()
    total_suara_b = hasil_suara['Suara B'].sum()
    total_golput = hasil_suara['Golput'].sum()
    total_suara = total_suara_a + total_suara_b + total_golput

    persentase_a = (total_suara_a / total_suara) * 100
    persentase_b = (total_suara_b / total_suara) * 100
    persentase_golput = (total_golput / total_suara) * 100

    # Menampilkan hasil suara
    st.write("Hasil Suara dari Sampel:")
    st.dataframe(hasil_suara)

    st.write(f"**Persentase Suara Paslon A:** {persentase_a:.2f}%")
    st.write(f"**Persentase Suara Paslon B:** {persentase_b:.2f}%")
    st.write(f"**Persentase Golput:** {persentase_golput:.2f}%")

    # Membuat grafik hasil suara
    labels = ['Paslon A', 'Paslon B', 'Golput']
    sizes = [persentase_a, persentase_b, persentase_golput]
    colors = ['lightblue', 'lightcoral', 'lightgrey']

    # Diagram Batang
    plt.figure(figsize=(8, 5))
    plt.bar(labels, sizes, color=colors)
    plt.title('Persentase Suara Paslon A, Paslon B dan Golput')
    plt.ylabel('Persentase (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    st.pyplot(plt)

    # Diagram Donat
    plt.figure(figsize=(8, 5))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Distribusi Suara Paslon A, Paslon B dan Golput')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(plt)

# Menambahkan footer
st.markdown("---")
st.write("Aplikasi ini dikembangkan untuk tujuan edukasi. Terima kasih telah menggunakan aplikasi ini!")