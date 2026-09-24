import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configurations
st.set_page_config(
    page_title="Gesundheits- & Versorgungsatlas Stadt und Landkreis Eichstätt",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Data Loader Helper with robust path fallback
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "versorgungsatlas_eichstaett.csv")
    xlsx_path = os.path.join(base_dir, "versorgungsatlas_eichstaett_original_matrix.xlsx")
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    elif os.path.exists("versorgungsatlas_eichstaett.csv"):
        return pd.read_csv("versorgungsatlas_eichstaett.csv")
    elif os.path.exists(xlsx_path):
        return pd.read_excel(xlsx_path, sheet_name="Gemeindeübersicht", skiprows=2)
    elif os.path.exists("versorgungsatlas_eichstaett_original_matrix.xlsx"):
        return pd.read_excel("versorgungsatlas_eichstaett_original_matrix.xlsx", sheet_name="Gemeindeübersicht", skiprows=2)
    else:
        raise FileNotFoundError("Weder 'versorgungsatlas_eichstaett.csv' noch 'versorgungsatlas_eichstaett_original_matrix.xlsx' wurden im App-Verzeichnis gefunden.")

try:
    df = load_data()
    # Clean column names if needed
    if "Gemeinde" not in df.columns and "Gemeinde " in df.columns:
        df.rename(columns={"Gemeinde ": "Gemeinde"}, inplace=True)
except Exception as e:
    st.error(f"⚠️ **Fehler beim Laden der Datengrundlage:** {e}")
    st.info("Bitte stellen Sie sicher, dass die Datei `versorgungsatlas_eichstaett.csv` oder `versorgungsatlas_eichstaett_original_matrix.xlsx` im selben GitHub-Ordner liegt wie `app.py`.")
    st.stop()

# 3. Custom CSS Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 17px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .academic-header {
        background-color: #F0F9FF;
        border-left: 5px solid #0284C7;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 20px;
        font-size: 14px;
        color: #0369A1;
    }
    .source-box {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        padding: 15px;
        border-radius: 8px;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. SIDEBAR
st.sidebar.image("https://img.icons8.com/clouds/150/hospital-room.png", width=100)
st.sidebar.title("Versorgungsatlas")
st.sidebar.markdown("**Stadt und Landkreis Eichstätt**")

st.sidebar.markdown("""
<div style="background-color:#EFF6FF; padding:12px; border-radius:6px; border-left:4px solid #3B82F6; margin-bottom:15px; font-size:13px;">
    <strong>Strukturdaten der Region:</strong><br>
    👥 Einwohner: 135.982 (Stichtag 31.12.2025)<br>
    🗺️ Fläche: 1.214 km²<br>
    🏡 Gemeinden: 30 (Stadt & Landkreis)
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="background-color:#F8FAFC; padding:12px; border-radius:6px; border:1px solid #E2E8F0; margin-bottom:15px; font-size:12px; line-height:1.5;">
    <strong>🎓 Akademischer Rahmen:</strong><br>
    • <strong>Studium / Hochschule:</strong> Katholische Stiftungshochschule München (KSH München)<br>
    • <strong>Praktikumsstelle:</strong> Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)<br>
    • <strong>Autorinnen / Projektteam:</strong> <code>[Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc.]</code>
</div>
""", unsafe_allow_html=True)

st.sidebar.subheader("📥 Daten-Download")
csv_data = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📊 Original-Datenbank (CSV) herunterladen",
    data=csv_data,
    file_name="versorgungsatlas_eichstaett.csv",
    mime="text/csv"
)

st.sidebar.markdown("""
---
✉️ **Forschungsanfragen / Original Excel:**  
Die vollständige Excel-Matrix mit allen Teildatenblättern ist für wissenschaftliche Zwecke auf Anfrage erhältlich.
""")

# 5. MAIN HEADER
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur in Stadt und Landkreis Eichstätt</div>', unsafe_allow_html=True)

st.markdown("""
<div class="academic-header">
    <strong>🎓 Wissenschaftliches Forschungsprojekt</strong><br>
    <strong>Hochschule (Studium):</strong> Katholische Stiftungshochschule München (KSH München) &nbsp;|&nbsp; 
    <strong>Praktikumsstelle / Praxispartner:</strong> Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)<br>
    <strong>Autorinnen / Projektteam:</strong> <code>[Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc.]</code>
</div>
""", unsafe_allow_html=True)

# 6. TABS
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Regionalvergleich", "🔍 Gemeinde-Steckbriefe", "📘 Recherchemanual & Methodik"])

# TAB 1
with tab1:
    st.header("Regionaler Überblick & Verteilungsanalyse")
    
    # Aggregated stats
    tot_einwohner = int(df["Einwohner"].sum()) if "Einwohner" in df.columns else 135982
    tot_aerzte = int(df["Aerztliche_Fachgebietseintraege"].sum()) if "Aerztliche_Fachgebietseintraege" in df.columns else 233
    tot_psych = int(df["Psychotherapie"].sum()) if "Psychotherapie" in df.columns else 25
    tot_zahnaerzte = int(df["Zahnaerztliche_Personen"].sum()) if "Zahnaerztliche_Personen" in df.columns else 26
    tot_apotheken = int(df["Oeffentliche_Apotheken"].sum()) if "Oeffentliche_Apotheken" in df.columns else 21
    tot_heilmittel = int(df["Heilmittelpraxen"].sum()) if "Heilmittelpraxen" in df.columns else 63
    tot_pflege = int(df["Pflegeeinrichtungen_Dienste"].sum()) if "Pflegeeinrichtungen_Dienste" in df.columns else 28
    
    st.subheader("Überblick über alle erfassten Angebote (Summe aller 30 Gemeinden)")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("👥 Einwohner gesamt", f"{tot_einwohner:,}".replace(",", "."))
    c2.metric("🩺 Ärztl. Fachgebiete", tot_aerzte)
    c3.metric("🧠 Psychotherapie", tot_psych)
    c4.metric("🦷 Zahnärztl. Personen", tot_zahnaerzte)
    c5.metric("💊 Öffentl. Apotheken", tot_apotheken)
    c6.metric("🏡 Pflegeangebote", tot_pflege)
    
    st.markdown("---")
    
    # Selection of indicator for visual comparison
    st.subheader("Interaktiver Vergleich der 30 Gemeinden")
    
    indicator_mapping = {
        "Ärztliche Fachgebietseinträge": "Aerztliche_Fachgebietseintraege",
        "Einwohnerzahl": "Einwohner",
        "Psychotherapeutische Personen": "Psychotherapie",
        "Zahnärztliche Personen": "Zahnaerztliche_Personen",
        "Öffentliche Apotheken": "Oeffentliche_Apotheken",
        "Heilmittelpraxen": "Heilmittelpraxen",
        "Pflegeeinrichtungen / -dienste": "Pflegeeinrichtungen_Dienste"
    }
    
    selected_label = st.selectbox("Wählen Sie eine Kennzahl für die Gemeinde-Gegenüberstellung:", list(indicator_mapping.keys()))
    selected_col = indicator_mapping[selected_label]
    
    if selected_col in df.columns:
        df_sorted = df.sort_values(by=selected_col, ascending=False)
        
        fig = px.bar(
            df_sorted, 
            x="Gemeinde", 
            y=selected_col,
            title=f"Verteilung im Landkreis: {selected_label}",
            labels={selected_col: selected_label, "Gemeinde": "Gemeinde"},
            color=selected_col,
            color_continuous_scale="Blues",
            height=480
        )
        fig.update_layout(xaxis_tickangle=-45, margin=dict(l=20, r=20, t=40, b=100))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Regional Benchmark Section
    st.subheader("📍 Regionaler Benchmark-Vergleich (Stadt und Landkreis Eichstätt vs. Bayern)")
    st.write("Methode: Um eine methodisch saubere Gegenüberstellung ohne Durchmischung von Bundes- und Landesebene zu gewährleisten, werden die Erfassungswerte des Landkreises Eichstätt einheitlich dem bayerischen Landesdurchschnitt gegenübergestellt.")
    
    if os.path.exists("versorgungsatlas_regionaler_benchmark.png"):
        st.image("versorgungsatlas_regionaler_benchmark.png", caption="Abbildung: Regionaler Benchmark-Vergleich aller 7 Versorgungssektoren (Angebote je 100.000 Einwohner) im Vergleich zum Landesdurchschnitt Bayern", use_container_width=True)
    elif os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "versorgungsatlas_regionaler_benchmark.png")):
        st.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "versorgungsatlas_regionaler_benchmark.png"), caption="Abbildung: Regionaler Benchmark-Vergleich der Versorgungsdichten", use_container_width=True)
    
    # Official Source documentation box
    st.markdown("""
    <div class="source-box">
        <strong>📌 Offizielle Quellen und Stichtagsnachweis der Referenzdaten (Bayern-Gegenüberstellung):</strong>
        <ul>
            <li><strong>Einwohnerzahl (Stichtag 31.12.2025):</strong> Bayerisches Landesamt für Statistik (LfStat Bayern). Homepage: <a href="https://www.statistik.bayern.de" target="_blank">www.statistik.bayern.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Ambulante Ärztliche Versorgung:</strong> Kassenärztliche Vereinigung Bayerns (KVB Versorgungsatlas Hausärzte & KVB-Arztregister, Stand August 2026: 72,8 Hausärzt/innen je 100k Einw.). Homepage: <a href="https://www.kvb.de/ueber-uns/versorgungsatlas/" target="_blank">www.kvb.de/ueber-uns/versorgungsatlas/</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Psychotherapeutische Versorgung:</strong> Kassenärztliche Vereinigung Bayerns (KVB Bedarfsplanungsdaten & 116117-Arztsuche). Homepage: <a href="https://www.kvb.de" target="_blank">www.kvb.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Zahnärztliche Versorgung:</strong> Bayerische Landeszahnärztekammer (BLZK) & Bundeszahnärztekammer (BZÄK Zahnarztsuche / Mitgliederstatistik). Homepages: <a href="https://www.blzk.de" target="_blank">www.blzk.de</a> & <a href="https://www.bzaek.de" target="_blank">www.bzaek.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Öffentliche Apotheken & Arzneimittelversorgung:</strong> Bayerische Landesapothekerkammer (BLAK) & ABDA (Stand 2024/2025: 2.744 Apotheken in Bayern = 20,2 je 100k Einw.) sowie Statistisches Bundesamt (Destatis Pressemitteilung N034 2024). Homepages: <a href="https://www.blak.de" target="_blank">www.blak.de</a>, <a href="https://www.abda.de" target="_blank">www.abda.de</a> & <a href="https://www.destatis.de" target="_blank">www.destatis.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Heilmittelpraxen:</strong> GKV-Spitzenverband (GKV-Heilmittelerbringerverzeichnis) & Amtliche Gesundheitsberichterstattung des Bundes (GBE Bund). Homepages: <a href="https://www.gkv-heilmittel.de" target="_blank">www.gkv-heilmittel.de</a> & <a href="https://www.gbe-bund.de" target="_blank">www.gbe-bund.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Pflegerische Versorgung:</strong> Bayerisches Landesamt für Statistik (LfStat Bayern, Zweijährliche Pflegestatistik 12/2023) & Pflegefinder Bayern. Homepage: <a href="https://www.statistik.bayern.de" target="_blank">www.statistik.bayern.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
            <li><strong>Krankenhaus- & Rehabilitationsversorgung:</strong> Bayerisches Staatsministerium für Gesundheit, Pflege und Prävention (StMGP Krankenhausplan Bayern) & Deutsches Krankenhausverzeichnis. Homepages: <a href="https://www.stmgp.bayern.de" target="_blank">www.stmgp.bayern.de</a> & <a href="https://www.deutsches-krankenhaus-verzeichnis.de" target="_blank">www.deutsches-krankenhaus-verzeichnis.de</a> <em>(abgerufen am 13.09.2026)</em>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# TAB 2
with tab2:
    st.header("Gemeindespezifische Versorgungs-Steckbriefe")
    
    gemeinden_list = sorted(df["Gemeinde"].unique()) if "Gemeinde" in df.columns else []
    
    if gemeinden_list:
        selected_gemeinde = st.selectbox("Gemeinde für Detaileinsicht auswählen:", gemeinden_list)
        g_data = df[df["Gemeinde"] == selected_gemeinde].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"### Steckbrief **{selected_gemeinde}**")
            einw_val = int(g_data['Einwohner']) if 'Einwohner' in g_data and pd.notnull(g_data['Einwohner']) else 0
            st.write(f"**Einwohnerzahl:** {einw_val:,} Einwohner".replace(",", "."))
            
            # Additional municipal info if available in dataframe
            if 'Flaeche_km2' in g_data and pd.notnull(g_data['Flaeche_km2']):
                st.write(f"**Fläche:** {g_data['Flaeche_km2']} km²")
            if 'Gemeindeart' in g_data and pd.notnull(g_data['Gemeindeart']):
                st.write(f"**Gemeindeart:** {g_data['Gemeindeart']}")
            if 'Verwaltungsgemeinschaft' in g_data and pd.notnull(g_data['Verwaltungsgemeinschaft']):
                st.write(f"**Verwaltungsgemeinschaft:** {g_data['Verwaltungsgemeinschaft']}")
            if 'Website' in g_data and pd.notnull(g_data['Website']):
                st.write(f"**Homepage:** [{g_data['Website']}](https://{g_data['Website']})")
                
            st.markdown("#### Lokale Infrastruktur-Angebote")
            
            metrics_list = []
            labels_map = {
                "Aerztliche_Fachgebietseintraege": "Ärztliche Fachgebietseinträge",
                "Psychotherapie": "Psychotherapeutische Sitze",
                "Zahnaerztliche_Personen": "Zahnärztliche Personen",
                "Oeffentliche_Apotheken": "Öffentliche Apotheken",
                "Heilmittelpraxen": "Heilmittelpraxen",
                "Pflegeeinrichtungen_Dienste": "Pflegeangebote (amb. & stat.)",
                "Krankenhaus_Reha_Hospiz": "Krankenhaus / Reha / Hospiz"
            }
            
            for col_key, col_label in labels_map.items():
                if col_key in g_data:
                    val = int(g_data[col_key]) if pd.notnull(g_data[col_key]) else 0
                    metrics_list.append({"Versorgungsbereich": col_label, "Anzahl (vor Ort)": val})
            
            if metrics_list:
                st.dataframe(pd.DataFrame(metrics_list), use_container_width=True, hide_index=True)
                
        with col2:
            st.markdown("### Lokale Versorgungsstruktur im Landkreis-Kontext")
            st.markdown("#### Abweichung vom Landkreis-Durchschnitt je Gemeinde")
            
            comparison_data = []
            for label, col in indicator_mapping.items():
                if col in df.columns:
                    g_val = float(g_data[col]) if pd.notnull(g_data[col]) else 0.0
                    avg_val = float(df[col].mean())
                    pct_of_avg = (g_val / avg_val * 100) if avg_val > 0 else 0.0
                    comparison_data.append({
                        "Infrastrukturmerkmal": label,
                        "Lokaler Wert": int(g_val),
                        "Landkreis-Schnitt pro Gemeinde": round(avg_val, 2),
                        "Prozent des Schnitts (%)": round(pct_of_avg, 1)
                    })
                    
            if comparison_data:
                st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
                
            # Methodical note for Denkendorf (Opt-In registry phenomenon)
            if selected_gemeinde == "Denkendorf":
                st.warning("""
                ⚠️ **Methodische Besonderheit für Denkendorf:**  
                Die offizielle Zahnarztsuche weist hier einen Registerwert von **0** aus, obwohl vor Ort eine Praxis existiert. 
                Gemäß unserem wissenschaftlichen Recherchemanual wird zur Sicherung der Replizierbarkeit strikt der offizielle Registerwert der Landeszahnärztekammer (Opt-In-Verfahren) geführt.
                """)

# TAB 3
with tab3:
    st.header("Wissenschaftliches Recherchemanual & Methodik")
    
    st.markdown("""
    <div style="background-color:#F8FAFC; padding:16px; border-radius:8px; border:1px solid #CBD5E1; margin-bottom:20px; font-size:14px; line-height:1.6;">
        <strong>📖 Akademischer Rahmen der Studie:</strong><br>
        • <strong>Vollständiger Studientitel:</strong> <em>Quartiersmanagement aus interprofessioneller Perspektive: Versorgungsformen und -strukturen von Stadt und Landkreis Eichstätt – Eine explorative Mixed-Methods-Studie</em><br>
        • <strong>Hochschule (Studium):</strong> Katholische Stiftungshochschule München (KSH München)<br>
        • <strong>Praktikumsstelle / Praxispartner:</strong> Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)<br>
        • <strong>Autorinnen / Projektteam:</strong> <code>[Hier Eure Namen eintragen]</code>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Zentrale Zählregeln & Primärregister")
        st.markdown("""
        *   **Ärztliche Versorgung (Fachgebietseinträge):** Erfasst über die *116117-Arztsuche/KVB*. Mehrfach qualifizierte Ärzt/innen werden in jedem Fachgebiet gezählt, um das tatsächliche Spektrum abzubilden.
        *   **Psychotherapie:** Erfasst über die *116117-Arztsuche/KVB*. Psychologische Psychotherapie und Kinder-/Jugendlichenpsychotherapie werden getrennt erhoben.
        *   **Zahnärztliche Versorgung:** Erfasst über die *Bayerische Landeszahnärztekammer (BLZK)*.
        *   **Öffentliche Apotheken:** Erfasst über die *Bayerische Landesapothekerkammer (BLAK)*. Jede örtliche Betriebsstätte zählt.
        *   **Heilmittelpraxen:** Erfasst über das *GKV-Heilmittelerbringerverzeichnis* (Physiotherapie, Ergotherapie, Logopädie, Podologie, Ernährung).
        *   **Pflegerische Versorgung:** Erfasst über den *Pflegefinder Bayern* (ambulante Dienste, vollstationäre Pflege, Tages- und Kurzzeitpflege).
        """)
        
    with col_b:
        st.subheader("2. Methodische Abgrenzung & Logik des Rettungsdienstes")
        st.markdown("""
        *   **Gemeindeübergreifende Versorgung:** Rettungsdienststrukturen (**Rettungswachen, Notarztstandorte, Integrierte Leitstelle**) werden logischerweise **nicht** einzelnen Gemeinden zugeordnet, da Rettungsdienstbereiche überregional vom *ZRF Region Ingolstadt* geplant und gesteuert werden.
        *   **Limitation der Datenvalidität (Opt-In-Verfahren):** Quantitative Daten aus offiziellen Suchverzeichnissen weichen teilweise von der realen Vor-Ort-Versorgung ab. Das liegt am datenschutzrechtlichen Opt-In-Verfahren der Kammern (Underreporting). Zur methodischen Konsistenz wird strikt der offizielle Registerwert geführt.
        *   **Deskriptive Bestandsaufnahme:** Der Atlas untersucht das *Vorhandensein* (Bestand) von Strukturen und ist keine Bedarfsdeckungs- oder Erreichbarkeitsanalyse.
        """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Stadt und Landkreis Eichstätt | KSH München & KU Eichstätt-Ingolstadt | © 2026 Open Science Project</div>", unsafe_allow_html=True)
