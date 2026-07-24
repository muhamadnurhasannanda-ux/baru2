import streamlit as st
import pandas as pd
import io
import os
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Simulasi Ekonomi Sumber Daya Air", 
    layout="wide"
)
st.markdown("""
<style>

.stApp{
    background: linear-gradient(
135deg,
rgb(235,248,255),
rgb(220,242,255),
rgb(245,252,255)
);

[data-testid="stSidebar"]{
    [data-testid="stSidebar"]{
    background-color: rgb(0,91,150);
}

[data-testid="stSidebar"] *{
    color:white;
}

[data-testid="metric-container"]{
background-color:white;
border-left:8px solid rgb(0,153,204);
border-radius:12px;
padding:20px;
box-shadow:0px 5px 12px rgba(0,0,0,0.15);
}


h1{
    color:rgb(0,91,150);
}

h2{
    color:rgb(0,153,204);
}

h3{
    color:rgb(0,102,102);
}

</style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([1.5, 8.5])

# Menentukan jalur pasti (absolute path) ke folder script ini berada
# Menentukan jalur folder tempat app.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo_unisba.png")

with col1:
    # Mengecek apakah file logo_unisba.png ada di folder app.py
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        # Jika file belum ditemukan, tampilkan info lokasi pencarian
        st.warning("⚠️ Logo belum ditemukan.")
        st.caption(f"Pastikan file logo_unisba.png ada di:\n`{LOGO_PATH}`")

with col2:
    st.markdown("#  Simulasi Ekonomi Sumber Daya Air")
    
    sub_col1, sub_col2 = st.columns([1, 1])
    with sub_col1:
        st.markdown("### Ekonomi Pembangunan")
    with sub_col2:
        st.markdown("Dosen Pengampu: Yuhka Sundaya")
    
    st.markdown("Dikembangkan Oleh: Muhamad Nurhasan Nanda (10090219131)")

st.divider()
# ==========================================
# 3. PENJELASAN TEORI & DATA DUMMY
# ==========================================
st.title("💧 Simulasi Ekonomi Sumber Daya Air")

st.markdown("""
Aplikasi ini mensimulasikan konsep **Ekonomi Sumber Daya Air**
berdasarkan **Bab 9 - Environmental and Natural Resource Economics
(Tietenberg & Lewis)**.

Dalam ekonomi sumber daya air, tujuan utama adalah mencapai
alokasi air yang efisien sehingga kebutuhan masyarakat dapat
dipenuhi tanpa mengurangi keberlanjutan sumber daya air.

Simulasi ini menggunakan konsep:

- Water Demand (Permintaan Air)
- Water Supply (Ketersediaan Air)
- Water Scarcity Index (WSI)
- Net Social Benefit
""")



data_daerah = {
    "Daerah": [
        "Kabupaten A",
        "Kabupaten B"
    ],
    "Permintaan Air (m³)": [
        8500,
        9600
    ],
    "Ketersediaan Air (m³)": [
        10000,
        11000
    ]
}

df_daerah = pd.DataFrame(data_daerah)



st.sidebar.header("💧 Parameter Simulasi")

jumlah_penduduk = st.sidebar.slider(
    "Jumlah Penduduk",
    1000,
    50000,
    12000,
    500
)

kebutuhan_perkapita = st.sidebar.slider(
    "Kebutuhan Air per Kapita (m³)",
    50,
    300,
    150,
    10
)

ketersediaan_air = st.sidebar.slider(
    "Ketersediaan Air (m³)",
    500000,
    5000000,
    2500000,
    50000
)

biaya_pengelolaan = st.sidebar.slider(
    "Biaya Pengelolaan Air (Rp)",
    1000000,
    100000000,
    25000000,
    1000000
)

nilai_manfaat = st.sidebar.slider(
    "Nilai Manfaat Ekonomi Air (Rp)",
    5000000,
    300000000,
    120000000,
    5000000
)



water_demand = jumlah_penduduk * kebutuhan_perkapita

water_supply = ketersediaan_air

water_scarcity = water_demand / water_supply

net_social_benefit = nilai_manfaat - biaya_pengelolaan



col1, col2 = st.columns(2)

with col1:

    st.subheader("📘 Persamaan Ekonomi Sumber Daya Air")

    st.markdown("""
Konsep dasar simulasi menggunakan persamaan berikut.
""")

    st.latex(r"WD=P\times q")

    st.markdown("""
Keterangan

P = Jumlah Penduduk

q = Kebutuhan Air per Kapita
""")

    st.latex(r"WSI=\frac{WD}{WS}")

    st.markdown("""
WSI menunjukkan tingkat kelangkaan air.

Semakin besar nilai WSI maka semakin tinggi tekanan terhadap
ketersediaan sumber daya air.
""")

    st.latex(r"NSB=B-C")

    st.markdown("""
B = Manfaat Ekonomi Air

C = Biaya Pengelolaan
""")

with col2:

    st.subheader("📊 Dashboard Indikator")

    c1, c2 = st.columns(2)

    c1.metric(
        "Water Demand",
        f"{water_demand:,.0f} m³"
    )

    c2.metric(
        "Water Supply",
        f"{water_supply:,.0f} m³"
    )

    c3, c4 = st.columns(2)

    c3.metric(
        "WSI",
        f"{water_scarcity:.2f}"
    )

    c4.metric(
        "Net Social Benefit",
        f"Rp {net_social_benefit:,.0f}"
    )

    st.divider()

    if water_scarcity < 0.8:

        st.success("""
🟢 Kondisi sumber daya air masih aman.

Ketersediaan air mampu memenuhi kebutuhan masyarakat.
""")

    elif water_scarcity < 1:

        st.warning("""
🟡 Daerah mulai mengalami tekanan terhadap sumber daya air.

Perlu dilakukan konservasi serta efisiensi penggunaan air.
""")

    else:

        st.error("""
🔴 Terjadi Water Scarcity.

Permintaan air lebih besar dibandingkan ketersediaan air.

Pemerintah perlu meningkatkan konservasi,
pembangunan waduk,
serta efisiensi distribusi air.
""")


st.divider()

st.subheader("📈 Grafik Hubungan Permintaan dan Ketersediaan Air")

rentang_penduduk = np.linspace(1000, 50000, 100)

demand_simulasi = rentang_penduduk * kebutuhan_perkapita

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    rentang_penduduk,
    demand_simulasi,
    color="blue",
    linewidth=3,
    label="Permintaan Air"
)

ax.axhline(
    water_supply,
    color="green",
    linestyle="--",
    linewidth=2,
    label="Ketersediaan Air"
)

warna = "green"

if water_demand > water_supply:
    warna = "red"

ax.scatter(
    jumlah_penduduk,
    water_demand,
    s=180,
    color=warna,
    zorder=5,
    label="Kondisi Saat Ini"
)

ax.fill_between(
    rentang_penduduk,
    demand_simulasi,
    water_supply,
    where=demand_simulasi <= water_supply,
    alpha=0.25,
    color="lightblue"
)

ax.fill_between(
    rentang_penduduk,
    demand_simulasi,
    water_supply,
    where=demand_simulasi > water_supply,
    alpha=0.30,
    color="lightcoral"
)

ax.set_title("Permintaan Air vs Ketersediaan Air")
ax.set_xlabel("Jumlah Penduduk")
ax.set_ylabel("Volume Air (m³)")
ax.grid(True, linestyle=":")
ax.legend()

st.pyplot(fig)


st.divider()

st.subheader("💧 Analisis Water Scarcity Index")

col_a, col_b, col_c = st.columns(3)

col_a.metric(
    "Permintaan Air",
    f"{water_demand:,.0f} m³"
)

col_b.metric(
    "Ketersediaan Air",
    f"{water_supply:,.0f} m³"
)

col_c.metric(
    "WSI",
    f"{water_scarcity:.2f}"
)

st.progress(min(water_scarcity,1.0))

if water_scarcity < 0.6:

    st.success("""
### Kondisi Aman

Ketersediaan air masih mencukupi kebutuhan masyarakat.

Pengelolaan air tetap perlu dilakukan agar keberlanjutan sumber daya air terjaga.
""")

elif water_scarcity < 1:

    st.warning("""
### Kondisi Waspada

Permintaan air mulai mendekati kapasitas sumber daya air.

Perlu dilakukan konservasi serta peningkatan efisiensi penggunaan air.
""")

else:

    st.error("""
### Water Scarcity

Permintaan air telah melebihi ketersediaan air.

Rekomendasi:

- Efisiensi penggunaan air
- Pembangunan waduk
- Konservasi daerah resapan
- Pengelolaan irigasi
""")


st.divider()

st.subheader("📊 Data Simulasi Indonesia")

csv_data = """
Tahun,Kebutuhan_Air,Ketersediaan_Air
2020,7800,10000
2021,8200,9950
2022,8600,9800
2023,9050,9600
2024,9500,9400
2025,10100,9200
"""

df = pd.read_csv(io.StringIO(csv_data))

st.dataframe(df, use_container_width=True)

col1,col2 = st.columns(2)

with col1:

    st.markdown("#### Tren Permintaan Air")

    st.line_chart(
        df.set_index("Tahun")["Kebutuhan_Air"]
    )

with col2:

    st.markdown("#### Tren Ketersediaan Air")

    st.line_chart(
        df.set_index("Tahun")["Ketersediaan_Air"]
    )


st.divider()

with st.expander("📚 Referensi"):

    st.markdown("""
1. Tietenberg, T. H., & Lewis, L. (2024). *Environmental and Natural Resource Economics.*

2. BPS Indonesia.

3. Kementerian PUPR.

4. FAO AQUASTAT.

5. World Bank Water Resources.
""")

st.sidebar.markdown("---")
st.sidebar.caption("FEB Universitas Islam Bandung")
st.sidebar.caption("Ekonomi Sumber Daya Alam")

st.markdown("---")

st.markdown(
"""
<div style="text-align:center">

### Water Resource Economics Simulator

Environmental and Natural Resource Economics

Bab 9 – Water Resources

Universitas Islam Bandung

2026

</div>
""",
unsafe_allow_html=True
)
