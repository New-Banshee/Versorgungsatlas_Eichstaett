import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page configurations
st.set_page_config(
    page_title="Gesundheits- & Versorgungsatlas Stadt & Landkreis Eichstätt",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data helper
@st.cache_data
def load_data():
    return pd.read_csv("versorgungsatlas_eichstaett.csv")

try:
    df = load_data()
except Exception:
    # Fallback to local path if run locally
    df = pd.read_csv("versorgungsatlas_eichstaett.csv")

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .author-box {
        background-color: #F8FAFC;
        border-radius: 6px;
        padding: 10px 15px;
        border-left: 4px solid #0284C7;
        margin-bottom: 20px;
        font-size: 14px;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR: Context & Info
st.sidebar.image("https://img.icons8.com/clouds/150/hospital-room.png", width=100)
st.sidebar.title("Versorgungsatlas")
st.sidebar.markdown("**Stadt und Landkreis Eichstätt**")

st.sidebar.markdown("""
<div style="background-color:#EFF6FF; padding:12px; border-radius:5px; border-left:4px solid #3B82F6; margin-bottom:15px;">
    <strong>Strukturdaten:</strong><br>
    👥 Einwohner: 135.982 (31.12.2025)<br>
    🗺️ Fläche: 1.214 km²<br>
    🏡 Gemeinden: 30
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="background-color:#F8FAFC; padding:12px; border-radius:5px; border-left:4px solid #0284C7; margin-bottom:15px; font-size:13px;">
    <strong>🎓 Akademischer Rahmen:</strong><br>
    • <strong>Studium / Hochschule:</strong><br>Katholische Stiftungshochschule München (KSH München)<br><br>
    • <strong>Praktikumsstelle:</strong><br>Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)<br><br>
    • <strong>Autorinnen / Projektteam:</strong><br><em>[Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc.]</em>
</div>
""", unsafe_allow_html=True)

st.sidebar.subheader("📥 Downloads")

# CSV Download Button
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📊 Datenbank (CSV) herunterladen",
    data=csv,
    file_name="versorgungsatlas_eichstaett.csv",
    mime="text/csv"
)

# Excel Matrix Download Button if file exists
excel_path = "versorgungsatlas_eichstaett_original_matrix.xlsx"
if os.path.exists(excel_path):
    with open(excel_path, "rb") as f:
        excel_bytes = f.read()
    st.sidebar.download_button(
        label="📗 Original Excel-Matrix (.xlsx)",
        data=excel_bytes,
        file_name="versorgungsatlas_eichstaett_original_matrix.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# MAIN PAGE
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur in Stadt und Landkreis Eichstätt</div>', unsafe_allow_html=True)

# Author Header Box
st.markdown("""
<div class="author-box">
    <strong>🎓 Wissenschaftliches Projekt</strong> | 
    <strong>Hochschule (Studium):</strong> Katholische Stiftungshochschule München (KSH München) | 
    <strong>Praktikumsstelle:</strong> Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)<br>
    <strong>Autorinnen / Projektteam:</strong> <em>[Hier Eure Namen eintragen, z. B. Vorname Nachname, Vorname Nachname]</em>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Regionalvergleich", "🔍 Gemeinde-Steckbriefe", "📘 Recherchemanual & Methodik"])

with tab1:
    st.header("Regionaler Überblick & Verteilungsanalyse")
    
    # Aggregated stats
    tot_einwohner = int(df["Einwohner"].sum())
    tot_aerzte = int(df["Aerztliche_Fachgebietseintraege"].sum())
    tot_psych = int(df["Psychotherapie"].sum())
    tot_zahnaerzte = int(df["Zahnaerztliche_Personen"].sum())
    tot_apotheken = int(df["Oeffentliche_Apotheken"].sum())
    tot_heilmittel = int(df["Heilmittelpraxen"].sum())
    tot_pflege = int(df["Pflegeeinrichtungen_Dienste"].sum())
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("👥 Einwohner gesamt", f"{tot_einwohner:,}".replace(",", "."))
    col2.metric("🩺 Fachgebietseinträge", tot_aerzte)
    col3.metric("🧠 Psychotherapie", tot_psych)
    col4.metric("🦷 Zahnärztliche Personen", tot_zahnaerzte)
    col5.metric("💊 Apotheken", tot_apotheken)
    col6.metric("🏡 Pflegeeinrichtungen", tot_pflege)
    
    st.markdown("---")
    
    # Regional Benchmark Section
    st.subheader("📍 Regionaler Benchmark-Vergleich (Stadt & Landkreis Eichstätt vs. Bayern)")
    
    st.markdown("""
    **Methode:** Um eine methodisch saubere Gegenüberstellung ohne Durchmischung von Bundes- und Landesebene zu gewährleisten, 
    werden die Erfassungswerte von Stadt und Landkreis Eichstätt einheitlich dem Landesdurchschnitt Bayern (Angebote je 100.000 Einwohner) gegenübergestellt.
    """)
    
    # Benchmark Chart Image Display
    benchmark_img_path = "versorgungsatlas_regionaler_benchmark.png"
    if os.path.exists(benchmark_img_path):
        st.image(benchmark_img_path, caption="Regionaler Benchmark-Vergleich der 7 Versorgungssektoren (Angebote je 100.000 Einwohner)", use_container_width=True)
    
    # Detailed Source List
    st.markdown("""
    #### 📌 Offizielle Quellen und Stichtagsnachweis der Referenzdaten:
    * **Einwohnerzahl Stichtag (31.12.2025):** Bayerisches Landesamt für Statistik (LfStat Bayern). Homepage: [www.statistik.bayern.de](https://www.statistik.bayern.de) *(abgerufen am 13.09.2026)*.
    * **Hausärztliche & Ambulante Ärztliche Versorgung:** Kassenärztliche Vereinigung Bayerns (KVB Versorgungsatlas Hausärzte & KVB-Arztregister, Stand August 2026: 72,8 Hausärzt/innen je 100k Einw.). Homepage: [www.kvb.de/ueber-uns/versorgungsatlas/](https://www.kvb.de/ueber-uns/versorgungsatlas/) *(abgerufen am 13.09.2026)*.
    * **Psychotherapeutische Versorgung:** Kassenärztliche Vereinigung Bayerns (KVB Bedarfsplanungsdaten & 116117-Arztsuche). Homepage: [www.kvb.de](https://www.kvb.de) *(abgerufen am 13.09.2026)*.
    * **Zahnärztliche Versorgung:** Bayerische Landeszahnärztekammer (BLZK) & Bundeszahnärztekammer (BZÄK Zahnarztsuche / Mitgliederstatistik). Homepages: [www.blzk.de](https://www.blzk.de) & [www.bzaek.de](https://www.bzaek.de) *(abgerufen am 13.09.2026)*.
    * **Öffentliche Apotheken & Arzneimittelversorgung:** Bayerische Landesapothekerkammer (BLAK) & ABDA (Stand 2024/2025: 2.744 Apotheken in Bayern = 20,2 je 100k Einw.) sowie Statistisches Bundesamt (Destatis Pressemitteilung N034 2024: 4.819 Einw./Apotheke in DE vs. 6.475 Einw./Apotheke im LK Eichstätt). Homepages: [www.blak.de](https://www.blak.de), [www.abda.de](https://www.abda.de) & [www.destatis.de](https://www.destatis.de) *(abgerufen am 13.09.2026)*.
    * **Heilmittelpraxen:** GKV-Spitzenverband (GKV-Heilmittelerbringerverzeichnis) & Amtliche Gesundheitsberichterstattung des Bundes (GBE Bund). Homepages: [www.gkv-heilmittel.de](https://www.gkv-heilmittel.de) & [www.gbe-bund.de](https://www.gbe-bund.de) *(abgerufen am 13.09.2026)*.
    * **Pflegerische Versorgung:** Bayerisches Landesamt für Statistik (LfStat Bayern, Zweijährliche Pflegestatistik 12/2023) & Pflegefinder Bayern. Homepage: [www.statistik.bayern.de](https://www.statistik.bayern.de) *(abgerufen am 13.09.2026)*.
    * **Krankenhaus- & Rehabilitationsversorgung:** Bayerisches Staatsministerium für Gesundheit, Pflege und Prävention (StMGP Krankenhausplan Bayern) & Deutsches Krankenhausverzeichnis. Homepages: [www.stmgp.bayern.de](https://www.stmgp.bayern.de) & [www.deutsches-krankenhaus-verzeichnis.de](https://www.deutsches-krankenhaus-verzeichnis.de) *(abgerufen am 13.09.2026)*.
    """)
    
    st.markdown("---")
    
    # Selection of indicator for visual comparison across 30 municipalities
    st.subheader("Verteilungsanalyse der 30 Gemeinden nach Infrastrukturmerkmalen")
    
    indicator_mapping = {
        "Ärztliche Fachgebietseinträge": "Aerztliche_Fachgebietseintraege",
        "Einwohner": "Einwohner",
        "Psychotherapeutische Personen": "Psychotherapie",
        "Zahnärztliche Personen": "Zahnaerztliche_Personen",
        "Öffentliche Apotheken": "Oeffentliche_Apotheken",
        "Heilmittelpraxen": "Heilmittelpraxen",
        "Pflegeeinrichtungen / -dienste": "Pflegeeinrichtungen_Dienste"
    }
    
    selected_label = st.selectbox("Wählen Sie ein Merkmal für den Vergleich der 30 Gemeinden:", list(indicator_mapping.keys()))
    selected_col = indicator_mapping[selected_label]
    
    # Plotly bar chart
    df_sorted = df.sort_values(by=selected_col, ascending=False)
    
    fig = px.bar(
        df_sorted, 
        x="Gemeinde", 
        y=selected_col,
        title=f"Verteilung in den 30 Gemeinden: {selected_label}",
        labels={selected_col: selected_label, "Gemeinde": "Gemeinde"},
        color=selected_col,
        color_continuous_scale="Blues",
        height=500
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight box
    st.info("""
    ℹ️ **Interpretationshinweis:** Größere Zentren wie die **Stadt Eichstätt** oder **Kösching** weisen aufgrund ihrer zentralörtlichen Funktion, 
    Krankenhausstandorte und der ansässigen Facharztpraxen naturgemäß die höchsten quantitativen Werte auf. Das Umland wird überregional bzw. gemeindeübergreifend mitversorgt.
    """)

with tab2:
    st.header("Gemeindespezifische Versorgungs-Steckbriefe")
    
    selected_gemeinde = st.selectbox("Gemeinde auswählen:", sorted(df["Gemeinde"].unique()))
    
    g_data = df[df["Gemeinde"] == selected_gemeinde].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### Steckbrief **{selected_gemeinde}**")
        st.write(f"**Einwohnerzahl:** {int(g_data['Einwohner']):,} Einwohner".replace(",", "."))
        
        # Simple table
        st.markdown("#### Lokale Infrastruktur-Kennzahlen")
        metrics_df = pd.DataFrame({
            "Versorgungsbereich": [
                "Ärztliche Fachgebietseinträge",
                "Psychotherapie",
                "Zahnärztliche Personen",
                "Öffentliche Apotheken",
                "Heilmittelpraxen",
                "Pflegeeinrichtungen / -dienste",
                "Krankenhaus / Reha / Hospiz"
            ],
            "Anzahl (Vor Ort)": [
                int(g_data["Aerztliche_Fachgebietseintraege"]),
                int(g_data["Psychotherapie"]),
                int(g_data["Zahnaerztliche_Personen"]),
                int(g_data["Oeffentliche_Apotheken"]),
                int(g_data["Heilmittelpraxen"]),
                int(g_data["Pflegeeinrichtungen_Dienste"]),
                int(g_data["Krankenhaus_Reha_Hospiz"])
            ]
        })
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("### Lokale Versorgungsstruktur im Landkreis-Kontext")
        st.markdown("#### Abweichung vom Landkreis-Durchschnitt (pro Gemeinde)")
        
        comparison_data = []
        for label, col in indicator_mapping.items():
            g_val = g_data[col]
            avg_val = df[col].mean()
            pct_of_avg = (g_val / avg_val * 100) if avg_val > 0 else 0
            comparison_data.append({
                "Infrastruktur": label,
                "Lokaler Wert": int(g_val) if col != "Einwohner" else int(g_val),
                "Landkreis-Durchschnitt": round(avg_val, 2),
                "Anteil am Durchschnitt (%)": round(pct_of_avg, 1)
            })
            
        comp_df = pd.DataFrame(comparison_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
        
        # Special note about data variance (Opt-In problem)
        if selected_gemeinde == "Denkendorf":
            st.warning("""
            ⚠️ **Methodische Besonderheit für Denkendorf:**  
            Die offizielle Zahnarztsuche weist hier einen Wert von **0** aus, obwohl auf der Gemeindehomepage 1 Zahnarztpraxis gelistet ist. 
            Gemäß unserem wissenschaftlichen Recherchemanual wird zur Sicherung der Replizierbarkeit strikt der offizielle Registerwert der Landeszahnärztekammer (Opt-In-Verfahren) ausgewiesen.
            """)

with tab3:
    st.header("Wissenschaftliches Recherchemanual & Methodische Grundlagen")
    
    st.markdown("""
    <div style="background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #CBD5E1; margin-bottom:20px;">
        <h4>📖 Akademischer Rahmen der Studie</h4>
        <ul>
            <li><strong>Studie / Titel:</strong> <em>Quartiersmanagement aus interprofessioneller Perspektive: Versorgungsformen und -strukturen von Stadt und Landkreis Eichstätt – Eine explorative Mixed-Methods-Studie</em></li>
            <li><strong>Hochschule (Studium):</strong> Katholische Stiftungshochschule München (KSH München)</li>
            <li><strong>Praktikumsstelle / Praxispartner:</strong> Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)</li>
            <li><strong>Autorinnen / Projektteam:</strong> <em>[Hier Eure Namen eintragen, z. B. Vorname Nachname, Vorname Nachname]</em></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Zentrale Zählregeln & Datenquellen")
        st.markdown("""
        * **Ärztliche Versorgung (Fachgebietseinträge):** Erfasst über die *116117-Arztsuche/KVB*. Mehrfach qualifizierte Ärzte werden in jedem Fachgebiet gezählt, um das tatsächliche Spektrum abzubilden.
        * **Psychotherapie:** Erfasst über die *116117-Arztsuche/KVB*. Psychologische Psychotherapie und Kinder-/Jugendlichenpsychotherapie werden getrennt erhoben.
        * **Zahnärztliche Versorgung:** Erfasst über die *Bayerische Landeszahnärztekammer*.
        * **Öffentliche Apotheken:** Erfasst über die *Bayerische Landesapothekerkammer*. Jede örtliche Betriebsstätte zählt.
        * **Heilmittelpraxen:** Erfasst über das *GKV-Heilmittelerbringerverzeichnis* (Physiotherapie, Ergotherapie, Logopädie, Podologie, Ernährungstherapie).
        * **Pflegerische Versorgung:** Erfasst über den *Pflegefinder Bayern* (Ambulante Dienste, vollstationäre Pflege, Tages- und Kurzzeitpflege).
        """)
        
    with col_b:
        st.subheader("2. Methodische Abgrenzung & Rettungsdienst")
        st.markdown("""
        * **Regionale / Landkreisweite Versorgung:** Rettungsdienststrukturen (**Rettungswachen, Notarztstandorte, Integrierte Leitstelle**) werden logischerweise **nicht** einzelnen Gemeinden zugeordnet, da Rettungsdienstbereiche durch den *Zweckverband für Rettungsdienst und Feuerwehralarmierung (ZRF) Region Ingolstadt* überregional geplant und gesteuert werden.
        * **Limitation der Datenvalidität (Opt-In-Verfahren):** Quantitative Daten aus offiziellen Suchverzeichnissen weichen teilweise von der realen Vor-Ort-Versorgung ab. Das liegt am datenschutzrechtlichen Opt-In-Verfahren, bei dem die Veröffentlichung in Verbraucher-Suchmasken auf freiwilliger Einwilligung basiert (Underreporting). Zur methodischen Konsistency wird im Datensatz dennoch strikt der offizielle Registerwert geführt.
        * **Deskriptive Bestandsaufnahme:** Der Atlas untersucht ausschließlich das *Vorhandensein* (Bestand) von Strukturen und stellt keine Bedarfsplanung dar.
        """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Stadt und Landkreis Eichstätt | KSH München & KU Eichstätt-Ingolstadt | © 2026 Open Science Project</div>", unsafe_allow_html=True)
