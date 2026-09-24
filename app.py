import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io

# ==============================================================================
# 🎓 KONFIGURATION / PERSONALISIERUNG
# ==============================================================================
AUTORINNEN = "Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc."  # <-- DIESEN TEXT MIT EUREN NAMEN ERSETZEN
PROJEKTTEILNEHMER = AUTORINNEN

UNI_NAME = "Katholische Stiftungshochschule München (KSH München)"
PRAKTIKUM_NAME = "Katholische Universität Eichstätt-Ingolstadt (KU Eichstätt-Ingolstadt)"
STUDIENGANG = "Angewandte Versorgungsforschung"
SEMESTER = "Sommersemester 2026"
PROJEKTTITEL = (
    "Quartiersmanagement aus interprofessioneller Perspektive: "
    "Versorgungsformen und -strukturen von Stadt und Landkreis Eichstätt – "
    "Eine explorative Mixed-Methods-Studie"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

XLSX_FILENAME = os.path.join(BASE_DIR, "versorgungsatlas_eichstaett_original_matrix.xlsx")
CSV_DETAILED_FILENAME = os.path.join(BASE_DIR, "versorgungsatlas_eichstaett_detailliert.csv")
CSV_OVERVIEW_FILENAME = os.path.join(BASE_DIR, "versorgungsatlas_eichstaett_v2.csv")
CSV_SIMPLE_FILENAME = os.path.join(BASE_DIR, "versorgungsatlas_eichstaett.csv")
BENCHMARK_IMG_PATH = os.path.join(BASE_DIR, "versorgungsatlas_regionaler_benchmark.png")

# Set page configurations
st.set_page_config(
    page_title="Gesundheits- & Versorgungsatlas Eichstätt",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data helper
@st.cache_data
def load_data():
    # 1. Try Primary Excel Matrix
    if os.path.exists(XLSX_FILENAME):
        try:
            df_o = pd.read_excel(XLSX_FILENAME, sheet_name="Gemeindeübersicht", header=3)
            df_o = df_o[df_o['Gemeinde'].notna() & (~df_o['Gemeinde'].astype(str).str.contains('Gesamt'))]
            rename_map = {
                'Ärztliche Fachgebietseinträge': 'Aerztliche_Fachgebietseintraege',
                'Zahnärztliche Personen': 'Zahnaerztliche_Personen',
                'Öffentliche Apotheken': 'Oeffentliche_Apotheken',
                'Pflegeeinrichtungen / -dienste': 'Pflegeeinrichtungen_Dienste',
                'Krankenhaus / Reha / Hospiz': 'Krankenhaus_Reha_Hospiz'
            }
            df_o = df_o.rename(columns=rename_map)
            
            df_d = pd.read_excel(XLSX_FILENAME, sheet_name="Detailmatrix Gemeinden", header=3)
            df_d = df_d[df_d['Gemeinde'].notna() & (~df_d['Gemeinde'].astype(str).str.contains('Gesamt'))]
            return df_o.fillna(""), df_d.fillna("")
        except Exception:
            pass

    # 2. Try Detailed CSVs
    if os.path.exists(CSV_OVERVIEW_FILENAME) and os.path.exists(CSV_DETAILED_FILENAME):
        try:
            df_o = pd.read_csv(CSV_OVERVIEW_FILENAME)
            df_d = pd.read_csv(CSV_DETAILED_FILENAME)
            return df_o.fillna(""), df_d.fillna("")
        except Exception:
            pass

    # 3. Fallback Simple CSV
    if os.path.exists(CSV_SIMPLE_FILENAME):
        try:
            df_o = pd.read_csv(CSV_SIMPLE_FILENAME)
            return df_o.fillna(""), df_o.fillna("")
        except Exception:
            pass

    # 4. Empty Fallback
    empty_df = pd.DataFrame({"Gemeinde": ["Eichstätt"], "Einwohner": [135982]})
    return empty_df, empty_df

df_overview, df_detailed = load_data()

# Ensure numeric columns
num_cols = ["Einwohner", "Aerztliche_Fachgebietseintraege", "Psychotherapie", "Zahnaerztliche_Personen", 
            "Oeffentliche_Apotheken", "Heilmittelpraxen", "Pflegeeinrichtungen_Dienste", "Krankenhaus_Reha_Hospiz"]
for col in num_cols:
    if col in df_overview.columns:
        df_overview[col] = pd.to_numeric(df_overview[col], errors='coerce').fillna(0)

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
        font-size: 17px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR: Context & Info
st.sidebar.image("https://img.icons8.com/clouds/150/hospital-room.png", width=100)
st.sidebar.title("Versorgungsatlas")
st.sidebar.markdown("**Stadt und Landkreis Eichstätt**")

# Studentisches Infofeld in der Sidebar
st.sidebar.markdown(f"""
<div style="background-color:#F5F3FF; padding:12px; border-radius:5px; border-left:4px solid #7C3AED; margin-bottom:15px; font-size: 13px;">
    <strong>🎓 Wissenschaftliches Projekt:</strong><br>
    • <strong>Hochschule (Studium):</strong><br>{UNI_NAME}<br>
    • <strong>Praktikumsstelle:</strong><br>{PRAKTIKUM_NAME}<br>
    • <strong>Studiengang:</strong> {STUDIENGANG} ({SEMESTER})<br><br>
    <strong>Projekttitel:</strong><br>
    <em>{PROJEKTTITEL}</em><br><br>
    <strong>Autorinnen:</strong><br>
    <span style="font-weight:bold; color:#1E3A8A;">{AUTORINNEN}</span>
</div>
""", unsafe_allow_html=True)

# Structure Box
st.sidebar.markdown("""
<div style="background-color:#EFF6FF; padding:12px; border-radius:5px; border-left:4px solid #3B82F6; margin-bottom:15px; font-size: 13px;">
    <strong>📍 Steckbrief Landkreis Eichstätt:</strong><br>
    🏛️ <strong>Regierungsbezirk:</strong> Oberbayern<br>
    👥 <strong>Einwohner:</strong> 135.982<br>
    📅 <strong>Stichtag Einwohner:</strong> 31.12.2025<br>
    🗺️ <strong>Fläche:</strong> 1.214 km²<br>
    📐 <strong>Bevölkerungsdichte:</strong> 112,0 Einw./km²<br>
    🏡 <strong>Gemeinden:</strong> 30
</div>
""", unsafe_allow_html=True)

# SINGLE EXCEL DOWNLOAD BUTTON ONLY
st.sidebar.subheader("📥 Daten-Download")

if os.path.exists(XLSX_FILENAME):
    try:
        with open(XLSX_FILENAME, "rb") as fp:
            st.sidebar.download_button(
                label="📊 Original Excel-Matrix (.xlsx) herunterladen",
                data=fp,
                file_name="versorgungsatlas_eichstaett_original_matrix.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Enthält die vollständige Arbeitsmappe mit Steckbrief, Gemeindeübersicht, Detailmatrix & Recherchemanual"
            )
    except Exception:
        pass
else:
    # Offer dynamically generated Excel from current dataframe
    output_b = io.BytesIO()
    with pd.ExcelWriter(output_b, engine='openpyxl') as writer:
        df_overview.to_excel(writer, sheet_name='Gemeindeübersicht', index=False)
        df_detailed.to_excel(writer, sheet_name='Detailmatrix Gemeinden', index=False)
    st.sidebar.download_button(
        label="📊 Original Excel-Matrix (.xlsx) herunterladen",
        data=output_b.getvalue(),
        file_name="versorgungsatlas_eichstaett_original_matrix.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.sidebar.markdown("""
---
✉️ **Anfragen / Kontakt:**  
_Kontaktieren Sie das Autorenteam direkt am Poster oder per E-Mail._
""")

# MAIN PAGE
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur in Stadt und Landkreis Eichstätt</div>', unsafe_allow_html=True)

# Header info line for authors and institutions
st.markdown(f"""
<div style="background-color:#F1F5F9; padding:12px 16px; border-radius:6px; margin-bottom:20px; font-size:14px; color:#334155; border-left:4px solid #1E3A8A;">
    <strong>🎓 Wissenschaftliches Projekt der {UNI_NAME}</strong> | <strong>Praktikumsstelle: {PRAKTIKUM_NAME}</strong><br>
    <strong>Autorinnen / Projektteam:</strong> <span style="font-weight:bold; color:#1E3A8A;">{AUTORINNEN}</span>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Regionalvergleich", "🔍 Gemeinde-Steckbriefe (Detailansicht)", "📘 Recherchemanual & Methodik"])

with tab1:
    st.header("Landkreis-Steckbrief & Regionaler Überblick")
    
    col_sb1, col_sb2 = st.columns([1, 2])
    
    with col_sb1:
        st.markdown("""
        <div style="background-color:#F8FAFC; padding:18px; border-radius:8px; border:1px solid #CBD5E1;">
            <h4 style="margin-top:0; color:#1E3A8A;">📌 Steckbrief Stadt und Landkreis Eichstätt</h4>
            <table style="width:100%; font-size:14px; border-collapse:collapse;">
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Untersuchungsraum:</strong></td><td>Stadt und Landkreis Eichstätt</td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Regierungsbezirk:</strong></td><td>Oberbayern</td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Einwohner:</strong></td><td><strong>135.982</strong></td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Einwohner – Stichtag:</strong></td><td><span style="color:#2563EB; font-weight:bold;">31.12.2025</span></td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Fläche:</strong></td><td>1.214 km²</td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Bevölkerungsdichte:</strong></td><td>112,0 Einw. / km²</td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Anzahl Gemeinden:</strong></td><td>30 Gemeinden</td></tr>
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Gemeindeebene:</strong></td><td>Ortsgebundene Angebote</td></tr>
                <tr><td style="padding:6px 0;"><strong>Landkreisebene:</strong></td><td>Überregionale Versorgung</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    with col_sb2:
        def safe_sum(df, col):
            if col in df.columns:
                return int(pd.to_numeric(df[col], errors='coerce').fillna(0).sum())
            return 0

        tot_aerzte = safe_sum(df_overview, "Aerztliche_Fachgebietseintraege")
        tot_psych = safe_sum(df_overview, "Psychotherapie")
        tot_zahnaerzte = safe_sum(df_overview, "Zahnaerztliche_Personen")
        tot_apotheken = safe_sum(df_overview, "Oeffentliche_Apotheken")
        tot_heilmittel = safe_sum(df_overview, "Heilmittelpraxen")
        tot_pflege = safe_sum(df_overview, "Pflegeeinrichtungen_Dienste")
        
        st.markdown("#### 📊 Aggregierte Gesamtstruktur im Landkreis Eichstätt")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("🩺 Fachgebietseinträge gesamt", tot_aerzte)
        m_col2.metric("🧠 Psychotherapeuten gesamt", tot_psych)
        m_col3.metric("🦷 Zahnärztliche Personen", tot_zahnaerzte)
        
        m_col4, m_col5, m_col6 = st.columns(3)
        m_col4.metric("💊 Öffentliche Apotheken", tot_apotheken)
        m_col5.metric("💆 Heilmittelpraxen", tot_heilmittel)
        m_col6.metric("🏡 Pflegeeinrichtungen / Dienste", tot_pflege)
        
    st.markdown("---")
    
    st.subheader("Landkreisweite, regionale und koordinierende Versorgungsstrukturen")
    st.markdown("_Gemäß Erfassungsmethodik werden gemeindeübergreifend koordinierte Strukturen auf Landkreisebene geführt:_")
    
    landkreis_table = pd.DataFrame([
        {"Versorgungsbereich": "Öffentlicher Gesundheitsdienst", "Akteur / Angebot": "Gesundheitsamt Eichstätt", "Standort / Träger": "Landratsamt Eichstätt / Gesundheitsamt", "Funktion / Versorgungsform": "Öffentlicher Gesundheitsdienst", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Gesundheitsförderung & Koordination", "Akteur / Angebot": "Gesundheitsregionplus", "Standort / Träger": "Landkreis Eichstätt", "Funktion / Versorgungsform": "Koordination, Vernetzung & Prävention", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Landkreis Eichstätt"},
        {"Versorgungsbereich": "Schwangerschaft & Familie", "Akteur / Angebot": "Schwangerschaftsberatung", "Standort / Träger": "Gesundheitsamt / Träger", "Funktion / Versorgungsform": "Beratung & Unterstützung", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Sucht", "Akteur / Angebot": "Suchtberatung & Suchtprävention", "Standort / Träger": "Gesundheitsamt / Partner", "Funktion / Versorgungsform": "Beratung, Vermittlung & Prävention", "Räumlicher Bezug": "Landkreisweit / regional", "Standardquelle": "Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Psychosoziale Versorgung", "Akteur / Angebot": "Sozialpsychiatrischer Dienst / Krisendienst", "Standort / Träger": "Krisendienste Bayern", "Funktion / Versorgungsform": "Beratung, Unterstützung & Krisenintervention", "Räumlicher Bezug": "Landkreisweit / regional", "Standardquelle": "Krisendienste Bayern"},
        {"Versorgungsbereich": "Pflege", "Akteur / Angebot": "Pflegestützpunkt & Fachstelle f. Angehörige", "Standort / Träger": "Landkreis Eichstätt / Träger", "Funktion / Versorgungsform": "Pflegeberatung & Vernetzung", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Landkreis Eichstätt"},
        {"Versorgungsbereich": "Hebammenversorgung", "Akteur / Angebot": "Hebammen mit Versorgungsgebiet", "Standort / Träger": "Freiberufliche Hebammen", "Funktion / Versorgungsform": "Aufsuchende Hebammenversorgung", "Räumlicher Bezug": "Landkreisweit / PLZ", "Standardquelle": "Hebammensuche Bayern"},
        {"Versorgungsbereich": "Rettungsdienst", "Akteur / Angebot": "Rettungswachen & Notarztstandorte", "Standort / Träger": "ZRF Region 10 / ILS", "Funktion / Versorgungsform": "Notfallrettung & Notarztversorgung", "Räumlicher Bezug": "Rettungsdienstbereich Region 10", "Standardquelle": "ZRF Region Ingolstadt"},
        {"Versorgungsbereich": "Krankenhausversorgung", "Akteur / Angebot": "Klinik Eichstätt & Klinik Kösching", "Standort / Träger": "Kliniken im Naturpark Altmühltal", "Funktion / Versorgungsform": "Stationäre Grund- und Regelversorgung", "Räumlicher Bezug": "Standortbezogen & landkreisweit", "Standardquelle": "Deutsches Krankenhausverzeichnis"},
        {"Versorgungsbereich": "Rehabilitation", "Akteur / Angebot": "Klinik Kipfenberg (Neurolog. Zentrum)", "Standort / Träger": "Private / Freie Träger", "Funktion / Versorgungsform": "Stationäre & ambulante Rehabilitation", "Räumlicher Bezug": "Standortbezogen / regional", "Standardquelle": "GKV-Suchmaschinen / QS-Reha"}
    ]).fillna("")
    
    st.dataframe(landkreis_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("Verteilungsanalyse der 30 Gemeinden")
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
    
    if selected_col in df_overview.columns:
        df_sorted = df_overview.sort_values(by=selected_col, ascending=False)
        fig = px.bar(
            df_sorted, 
            x="Gemeinde", 
            y=selected_col,
            title=f"Verteilung von: {selected_label}",
            labels={selected_col: selected_label, "Gemeinde": "Gemeinde"},
            color=selected_col,
            color_continuous_scale="Viridis",
            height=480
        )
        fig.update_traces(
            marker_line_color='#1E293B', 
            marker_line_width=1.2,
            texttemplate='%{y}', 
            textposition='outside'
        )
        fig.update_layout(xaxis_tickangle=-45, plot_bgcolor='white', paper_bgcolor='white', yaxis=dict(gridcolor='#E2E8F0'))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # BENCHMARK GRAPHIC & SOURCES
    st.subheader("📍 Regionaler Benchmark-Vergleich (Landkreis Eichstätt vs. Bayern)")
    st.markdown("""
    _Methode: Um eine methodisch saubere Gegenüberstellung ohne Durchmischung von Bundes- und Landesebene zu gewährleisten, werden die Erfassungswerte des Landkreises Eichstätt einheitlich dem **Landesdurchschnitt Bayern** gegenübergestellt._
    """)

    # Render image if file exists, otherwise render Plotly chart directly!
    if os.path.exists(BENCHMARK_IMG_PATH):
        st.image(BENCHMARK_IMG_PATH, caption="Regionaler Benchmark-Vergleich (Landkreis Eichstätt vs. Bayern)", use_container_width=True)
    else:
        benchmark_df = pd.DataFrame([
            {"Versorgungsindikator": "Öffentliche Apotheken (je 100k Einw.)", "Landkreis Eichstätt": 15.4, "Bayern-Durchschnitt": 20.2},
            {"Versorgungsindikator": "Ambulante Ärzt/innen & Psych. (je 100k Einw.)", "Landkreis Eichstätt": 157.4, "Bayern-Durchschnitt": 198.4},
            {"Versorgungsindikator": "Zahnärztliche Personen (je 100k Einw.)", "Landkreis Eichstätt": 18.4, "Bayern-Durchschnitt": 87.2}
        ])

        fig_bench = px.bar(
            benchmark_df,
            x="Versorgungsindikator",
            y=["Landkreis Eichstätt", "Bayern-Durchschnitt"],
            barmode="group",
            title="Versorgungsdichte je 100.000 Einwohner im Vergleich zum Landesdurchschnitt Bayern",
            color_discrete_map={"Landkreis Eichstätt": "#2563EB", "Bayern-Durchschnitt": "#94A3B8"},
            height=380
        )
        fig_bench.update_traces(texttemplate='%{y}', textposition='outside')
        fig_bench.update_layout(plot_bgcolor='white', paper_bgcolor='white', yaxis=dict(gridcolor='#E2E8F0'), legend_title_text="")
        st.plotly_chart(fig_bench, use_container_width=True)

    # Methodological Sources Caption
    st.caption("""
    📌 **Quellen und Stichtagsnachweis der Referenzdaten:**
    * **Einwohnerzahl Stichtag:** 31.12.2025 (Bayerisches Landesamt für Statistik).
    * **Öffentliche Apotheken:** Bayerische Landesapothekerkammer (BLAK, Stand 2024/2025: 2.744 Apotheken in Bayern = 20,2 je 100k Einw.).
    * **Ambulante Ärztliche Versorgung:** Kassenärztliche Vereinigung Bayerns (KVB Versorgungsatlas, Stand 2024/2025: ca. 198,4 je 100k Einw.).
    * **Zahnärztliche Versorgung:** Bayerische Landeszahnärztekammer (BLZK, Stand 2024/2025: ca. 87,2 aktiv behandelnde Zahnärzt/innen je 100k Einw.). *Hinweis: Die Abweichung bei den Zahnärzten im Landkreis resultiert aus dem im Recherchemanual beschriebenen Opt-In-Verfahren der Kammerregister.*
    """)

with tab2:
    st.header("Gemeindespezifische Detail-Steckbriefe")
    
    if "Gemeinde" in df_detailed.columns:
        selected_gemeinde = st.selectbox("Gemeinde auswählen:", sorted(df_detailed["Gemeinde"].unique()))
        
        g_det_matches = df_detailed[df_detailed["Gemeinde"] == selected_gemeinde]
        if not g_det_matches.empty:
            g_det = g_det_matches.iloc[0]
            
            col_g1, col_g2 = st.columns([1, 2])
            
            with col_g1:
                st.markdown(f"### Gemeindesteckbrief: **{selected_gemeinde}**")
                
                def clean_v(key, default="-"):
                    val = g_det.get(key, default)
                    if pd.isna(val) or str(val).strip().lower() in ["nan", "none", ""]:
                        return default
                    return str(val).strip()

                einwohner_str = clean_v('Einwohner')
                try:
                    einwohner_val = f"{int(float(einwohner_str)):,}".replace(",", ".")
                except Exception:
                    einwohner_val = einwohner_str

                st.markdown(f"""
                <div style="background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #E2E8F0; font-size:13.5px;">
                    👥 <strong>Einwohnerzahl:</strong> {einwohner_val} Einwohner<br>
                    📐 <strong>Fläche:</strong> {clean_v('Flaeche_km2')} km² ({clean_v('Einwohner_je_km2')} Einw./km²)<br>
                    🏛️ <strong>Gemeindeart:</strong> {clean_v('Gemeindeart')}<br>
                    🏢 <strong>Verwaltungsgemeinschaft:</strong> {clean_v('Verwaltungsgemeinschaft')}<br>
                    🏛️ <strong>Rathaus:</strong> {clean_v('Rathaus')}<br>
                    🌐 <strong>Website:</strong> <a href="{clean_v('Website')}" target="_blank">{clean_v('Website')}</a>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### Ortsteile / Gemeindeteile")
                st.info(clean_v('Ortsteile'))
                
                bemerkung_val = clean_v('Bemerkung', default="")
                if bemerkung_val and bemerkung_val != "-":
                    st.warning(f"⚠️ **Besondere Bemerkung:** {bemerkung_val}")
                    
            with col_g2:
                st.markdown(f"### Detaillierte Fachkategorien: **{selected_gemeinde}**")
                
                def clean_int(key):
                    val = g_det.get(key, 0)
                    try:
                        if pd.isna(val) or str(val).strip().lower() in ["nan", "none", ""]:
                            return 0
                        return int(float(val))
                    except Exception:
                        return 0

                # 1. Ambulante Ärztliche Versorgung
                st.markdown("#### 🩺 Ambulante ärztliche Versorgung nach Fachgebieten")
                aerzte_df = pd.DataFrame({
                    "Fachgebiet / Arztgruppe": [
                        "Allgemeinmedizin", "Praktische Ärztinnen und Ärzte", "Innere Medizin",
                        "Kinder- und Jugendmedizin", "Frauenheilkunde und Geburtshilfe", "Hals-Nasen-Ohren-Heilkunde",
                        "Augenheilkunde", "Haut- und Geschlechtskrankheiten", "Orthopädie und Unfallchirurgie",
                        "Chirurgie", "Neurologie", "Psychiatrie und Psychotherapie", "Urologie",
                        "Anästhesiologie", "Radiologie", "Weitere Fachgebiete"
                    ],
                    "Anzahl (Vor Ort)": [
                        clean_int("Allgemeinmedizin"), clean_int("Praktische_Aerzte"), clean_int("Innere_Medizin"),
                        clean_int("Kinder_Jugendmedizin"), clean_int("Frauenheilkunde"), clean_int("HNO"),
                        clean_int("Augenheilkunde"), clean_int("Hautkrankheiten"), clean_int("Orthopaedie"),
                        clean_int("Chirurgie"), clean_int("Neurologie"), clean_int("Psychiatrie_Psychotherapie"),
                        clean_int("Urologie"), clean_int("Anaesthesiologie"), clean_int("Radiologie"), clean_int("Weitere_Fachgebiete")
                    ],
                    "Standardquelle": ["116117-Arztsuche / KVB"] * 16
                })
                st.dataframe(aerzte_df, use_container_width=True, hide_index=True)
                st.caption(f"**Summe Fachgebietseinträge:** {clean_int('Summe_Aerztliche_Fachgebietseintraege')}")
                
                st.markdown("---")
                
                # 2. Psychotherapie & Zahnärzte
                col_sub1, col_sub2 = st.columns(2)
                
                with col_sub1:
                    st.markdown("#### 🧠 Psychotherapie")
                    psych_df = pd.DataFrame({
                        "Kategorie": ["Psychologische Psychotherapie", "Kinder- & Jugendlichenpsychotherapie"],
                        "Anzahl": [clean_int("Psychologische_Psychotherapie"), clean_int("Kinder_Jugendlichenpsychotherapie")],
                        "Quelle": ["116117-Arztsuche"] * 2
                    })
                    st.dataframe(psych_df, use_container_width=True, hide_index=True)
                    
                    st.markdown("#### 🦷 Zahnärztliche Versorgung")
                    zahn_df = pd.DataFrame({
                        "Kategorie": ["Zahnärztinnen und Zahnärzte", "Kieferorthopädie"],
                        "Anzahl": [clean_int("Zahnaerzte"), clean_int("Kieferorthopaedie")],
                        "Quelle": ["Bayerische Landeszahnärztekammer"] * 2
                    })
                    st.dataframe(zahn_df, use_container_width=True, hide_index=True)
                    
                with col_sub2:
                    st.markdown("#### 💊 Arzneimittel- & Heilmittelversorgung")
                    heil_df = pd.DataFrame({
                        "Versorgungsbereich": [
                            "Öffentliche Apotheken", "Physiotherapie", "Ergotherapie",
                            "Logopädie / Sprachtherapie", "Podologie", "Ernährungstherapie"
                        ],
                        "Anzahl": [
                            clean_int("Oeffentliche_Apotheken"), clean_int("Physiotherapie"),
                            clean_int("Ergotherapie"), clean_int("Logopadie_Sprachtherapie"),
                            clean_int("Podologie"), clean_int("Ernaehrungstherapie")
                        ],
                        "Quelle": ["BLAK"] + ["GKV-Heilmittelerbringerverzeichnis"] * 5
                    })
                    st.dataframe(heil_df, use_container_width=True, hide_index=True)
                    
                st.markdown("---")
                
                # 3. Pflege & Krankenhaus
                col_sub3, col_sub4 = st.columns(2)
                
                with col_sub3:
                    st.markdown("#### 🏡 Pflegerische Versorgung")
                    pflege_df = pd.DataFrame({
                        "Angebotsform": ["Ambulante Pflegedienste", "Vollstationäre Pflege", "Tagespflege", "Kurzzeitpflege"],
                        "Anzahl": [clean_int("Ambulante_Pflegedienste"), clean_int("Vollstationaere_Pflege"), clean_int("Tagespflege"), clean_int("Kurzzeitpflege")],
                        "Quelle": ["Pflegefinder Bayern"] * 4
                    })
                    st.dataframe(pflege_df, use_container_width=True, hide_index=True)
                    
                with col_sub4:
                    st.markdown("#### 🏥 Krankenhaus / Reha / Hospiz")
                    kh_df = pd.DataFrame({
                        "Einrichtungstyp": ["Krankenhausstandorte", "Rehabilitationseinrichtungen", "Stationäre Hospize"],
                        "Anzahl": [clean_int("Krankenhausstandorte"), clean_int("Rehabilitationseinrichtungen"), clean_int("Stationaere_Hospize")],
                        "Quelle": ["Deutsches Krankenhausverzeichnis / QS-Reha"] * 3
                    })
                    st.dataframe(kh_df, use_container_width=True, hide_index=True)

with tab3:
    st.header("Wissenschaftlicher Hintergrund & Recherchemanual")
    
    st.markdown(f"""
    <div style="background-color:#F9FAFB; padding:15px; border-radius:8px; border:1px solid #E5E7EB; margin-bottom:25px;">
        <h4>🏫 Akademischer Rahmen des Projekts</h4>
        Dieses interaktive System und die zugrundeliegende Erfassung wurden im Rahmen des 
        <strong>Masterstudiengangs {STUDIENGANG}</strong> ({SEMESTER}) an der <strong>{UNI_NAME}</strong> erarbeitet.<br>
        <strong>Praktikumsstelle / Praxispartner:</strong> {PRAKTIKUM_NAME}<br><br>
        <strong>Interprofessioneller Ansatz:</strong><br>
        Die Erhebung ist in das Projektmodul <strong>"{PROJEKTTITEL}"</strong> eingebettet, 
        das aufzeigt, wie die verschiedenen Sektoren der Gesundheits- und Soziallandschaft (Ärzte, Zahnärzte, Heilmittelerbringer, Pflege- und Beratungsstrukturen) 
        integriert zusammenwirken können, um eine lückenlose Versorgung zu gewährleisten.<br><br>
        <em>Autorinnen / Projektteam: {AUTORINNEN}</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Dieses interaktive System basiert auf dem offiziellen **Recherchemanual und methodischen Regelbuch des Versorgungsatlasses des Landkreises Eichstätt**.
    Ein stabiles und logisches Regelwerk sichert die wissenschaftliche Replizierbarkeit und Validität der erhobenen Strukturen.
    """)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Zentrale Zählregeln & Datenquellen")
        st.markdown("""
        *   **Ärztliche Versorgung (Fachgebietseinträge):** Erfasst über die *116117-Arztsuche/KVB*. Mehrfach qualifizierte Ärzte werden in jedem Fachgebiet gezählt, um das tatsächliche Spektrum abzubilden. Praxis- und MVZ-Strukturen selbst werden nicht rekonstruiert.
        *   **Psychotherapie:** Erfasst über die *116117-Arztsuche/KVB*. Psychologische Psychotherapie und Kinder- und Jugendlichenpsychotherapeutinnen und -psychotherapeuten werden getrennt erhoben.
        *   **Zahnärztliche Versorgung:** Erfasst über die *Bayerische Landeszahnärztekammer*. Keine Rekonstruktion von Praxisorganisationen.
        *   **Öffentliche Apotheken:** Erfasst über die *Bayerische Landesapothekerkammer*. Jede örtliche Betriebsstätte zählt (einschließlich Filialen).
        *   **Heilmittelpraxen:** Erfasst über das *GKV-Heilmittelerbringerverzeichnis*. Zugelassene Betriebsstätten je Bereich (Physiotherapie, Ergotherapie, Logopädie, Podologie, Ernährung).
        *   **Pflegerische Versorgung:** Erfasst über den *Pflegefinder Bayern*. Ambulante Dienste, vollstationäre Einrichtungen, Tagespflege und Kurzzeitpflege werden getrennt gezählt.
        """)
        
    with col_b:
        st.subheader("2. Methodische Abgrenzung & Logik des Rettungsdienstes")
        st.markdown("""
        *   **Regionale / Landkreisweite Versorgung:** Rettungsdienststrukturen (**Rettungswachen, Notarztstandorte, Integrierte Leitstelle**) werden logischerweise **nicht** einzelnen Gemeinden zugeordnet, da dies zu Fehlinterpretationen führen würde. Rettungsdienstbereiche werden durch den *Zweckverband für Rettungsdienst und Feuerwehralarmierung (ZRF) Region Ingolstadt* überregional geplant und gesteuert. Sie sind daher als gemeindeübergreifende Angebote auf Landkreisebene angesiedelt.
        *   **Limitation der Datenvalidität (Opt-In-Verfahren):** Quantitative Daten aus offiziellen Suchverzeichnissen weichen teilweise von der realen Vor-Ort-Versorgung ab. Das liegt am datenschutzrechtlichen Opt-In-Verfahren, bei dem die Veröffentlichung in Verbraucher-Suchmasken auf freiwilliger Einwilligung basiert (Underreporting). Zur methodischen Konsistenz wird im Datensatz dennoch strikt der offizielle Registerwert geführt, Abweichungen werden in den Bemerkungen transparent gemacht.
        *   **Deskriptive Bestandsaufnahme:** Der Atlas untersucht ausschließlich das *Vorhandinsein* (Bestand) von Strukturen und ist keine Bedarfsplanung (keine Bedarfsdeckungs- oder Erreichbarkeitsanalyse).
        """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Landkreis Eichstätt | © 2026 Open Science Project</div>", unsafe_allow_html=True)
