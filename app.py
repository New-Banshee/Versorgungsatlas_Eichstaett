import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# ==============================================================================
# 🎓 KONFIGURATION / PERSONALISIERUNG (HIER EINFACH ANPASSEN!)
# ==============================================================================
UNI_NAME = "Katholische Stiftungshochschule München"                                      # Name Eurer Universität/Hochschule
STUDIENGANG = "Angewandte Versorgungsforschung"         # Euer Studiengang
SEMESTER = "Sommersemester 2026"                        # Das aktuelle Semester
PROJEKTTITEL = "Quartiersmanagement aus interprofessioneller Perspektive"
PROJEKTTEILNEHMER = "Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc."          # Eure Namen für die Bearbeitung

# DATEINAMEN DER DATEN-DATEIEN
XLSX_FILENAME = "versorgungsatlas_eichstaett_original_matrix.xlsx"
CSV_DETAILED_FILENAME = "versorgungsatlas_eichstaett_detailliert.csv"
CSV_OVERVIEW_FILENAME = "versorgungsatlas_eichstaett_v2.csv"
# ==============================================================================

# Page Configuration
st.set_page_config(
    page_title="Gesundheits- & Versorgungsatlas Eichstätt",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Standardized Column Names for Overview (Positional Mapping to avoid Encoding/Umlaut KeyError)
STANDARD_OVERVIEW_COLS = [
    "Gemeinde", "Einwohner", "Aerztliche_Fachgebietseintraege", "Psychotherapie",
    "Zahnaerztliche_Personen", "Oeffentliche_Apotheken", "Heilmittelpraxen",
    "Pflegeeinrichtungen_Dienste", "Krankenhaus_Reha_Hospiz", "Erhebungsstatus"
]

@st.cache_data
def load_data():
    """
    Robustes Laden der Daten mit 3-stufigem Fallback:
    1. Primär aus der Excel-Arbeitsmappe (.xlsx)
    2. Sekundär aus den CSV-Dateien
    3. Tertiär aus integrierten Basis-Daten (Ausfallsicher)
    """
    df_over = None
    df_det = None

    # Stufe 1: Versuche Excel-Arbeitsmappe zu lesen
    if os.path.exists(XLSX_FILENAME):
        try:
            raw_over = pd.read_excel(XLSX_FILENAME, sheet_name="Gemeindeübersicht", header=3)
            raw_over = raw_over[raw_over.iloc[:, 0].notna() & (~raw_over.iloc[:, 0].astype(str).str.contains("Gesamt"))]
            if raw_over.shape[1] >= 10:
                df_over = raw_over.iloc[:, :10].copy()
                df_over.columns = STANDARD_OVERVIEW_COLS

            raw_det = pd.read_excel(XLSX_FILENAME, sheet_name="Detailmatrix Gemeinden", header=3)
            df_det = raw_det[raw_det.iloc[:, 0].notna() & (~raw_det.iloc[:, 0].astype(str).str.contains("Gesamt"))].copy()
        except Exception:
            pass

    # Stufe 2: Fallback auf CSV-Dateien
    if df_over is None and os.path.exists(CSV_OVERVIEW_FILENAME):
        try:
            df_over = pd.read_csv(CSV_OVERVIEW_FILENAME)
            if df_over.shape[1] >= 10:
                df_over.columns = STANDARD_OVERVIEW_COLS
        except Exception:
            pass

    if df_det is None and os.path.exists(CSV_DETAILED_FILENAME):
        try:
            df_det = pd.read_csv(CSV_DETAILED_FILENAME)
        except Exception:
            pass

    # Stufe 3: Tertiärer Ausfallschutz (Integrierter Basisstamm)
    if df_over is None or df_det is None:
        base_data = [
            ["Adelschlag", 2981, 0, 1, 0, 0, 0, 0, 0, "vollständig"],
            ["Altmannstein", 7195, 3, 0, 0, 1, 2, 3, 0, "vollständig"],
            ["Beilngries", 10242, 37, 1, 4, 2, 13, 4, 0, "vollständig"],
            ["Böhmfeld", 1697, 0, 1, 0, 0, 0, 0, 0, "vollständig"],
            ["Buxheim", 3771, 1, 1, 0, 0, 1, 1, 0, "vollständig"],
            ["Denkendorf", 5059, 5, 1, 0, 1, 5, 3, 0, "vollständig"],
            ["Dollnstein", 2850, 1, 1, 1, 1, 1, 0, 0, "vollständig"],
            ["Egweil", 1247, 0, 0, 0, 0, 0, 0, 0, "vollständig"],
            ["Eichstätt (Stadt)", 14066, 78, 3, 10, 4, 14, 7, 1, "vollständig"],
            ["Eitensheim", 3030, 5, 1, 0, 1, 2, 0, 0, "vollständig"],
            ["Gaimersheim", 12526, 17, 1, 3, 2, 4, 5, 0, "vollständig"],
            ["Großmehring", 7498, 3, 1, 0, 1, 0, 1, 0, "vollständig"],
            ["Hepberg", 3077, 1, 1, 0, 0, 2, 0, 0, "vollständig"],
            ["Hitzhofen", 3022, 0, 0, 0, 0, 0, 0, 0, "vollständig"],
            ["Kinding", 2600, 0, 0, 0, 0, 1, 0, 0, "vollständig"],
            ["Kipfenberg", 5835, 3, 1, 2, 1, 6, 1, 1, "vollständig"],
            ["Kösching", 9737, 54, 5, 1, 2, 4, 1, 1, "vollständig"],
            ["Lenting", 4980, 5, 0, 2, 1, 2, 0, 0, "vollständig"],
            ["Mindelstetten", 1822, 2, 0, 0, 0, 0, 0, 0, "vollständig"],
            ["Mörnsheim", 1523, 0, 0, 0, 0, 1, 0, 0, "vollständig"],
            ["Nassenfels", 2351, 0, 0, 0, 1, 0, 0, 0, "vollständig"],
            ["Oberdolling", 1371, 0, 0, 0, 0, 0, 0, 0, "vollständig"],
            ["Pförring", 4100, 1, 0, 1, 1, 0, 1, 0, "vollständig"],
            ["Pollenfeld", 3051, 1, 1, 0, 0, 1, 0, 0, "vollständig"],
            ["Schernfeld", 3285, 1, 0, 0, 0, 1, 0, 0, "vollständig"],
            ["Stammham", 4159, 2, 2, 0, 0, 1, 0, 0, "vollständig"],
            ["Titting", 2688, 1, 2, 0, 1, 1, 1, 0, "vollständig"],
            ["Walting", 2289, 0, 0, 0, 0, 0, 0, 0, "vollständig"],
            ["Wellheim", 2725, 4, 1, 1, 0, 0, 0, 0, "vollständig"],
            ["Wettstetten", 5205, 8, 0, 1, 1, 1, 0, 0, "vollständig"]
        ]
        if df_over is None:
            df_over = pd.DataFrame(base_data, columns=STANDARD_OVERVIEW_COLS)
        if df_det is None:
            df_det = pd.DataFrame(base_data, columns=STANDARD_OVERVIEW_COLS)

    df_over = df_over.fillna("")
    df_det = df_det.fillna("")
    return df_over, df_det

df_overview, df_detailed = load_data()

# Custom CSS Styling
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
    .badge-status {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR: Context & Info
st.sidebar.image("https://img.icons8.com/clouds/150/hospital-room.png", width=100)
st.sidebar.title("Versorgungsatlas")
st.sidebar.markdown("**Landkreis Eichstätt (Oberbayern)**")

# Studentisches Infofeld in der Sidebar
st.sidebar.markdown(f"""
<div style="background-color:#F5F3FF; padding:12px; border-radius:5px; border-left:4px solid #7C3AED; margin-bottom:15px; font-size: 13px;">
    <strong>🎓 Studentisches Projekt:</strong><br>
    Erstellt im Rahmen des Masterstudiengangs <strong>{STUDIENGANG}</strong> ({SEMESTER}) an der <strong>{UNI_NAME}</strong>.<br><br>
    <strong>Projekttitel:</strong><br>
    <em>{PROJEKTTITEL}</em><br><br>
    <strong>Bearbeitung:</strong><br>
    {PROJEKTTEILNEHMER}
</div>
""", unsafe_allow_html=True)

# Structure Box with Exact Stichtag
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

# EXCEL MATRIX DOWNLOAD BUTTON
st.sidebar.subheader("📥 Daten-Download")

try:
    if os.path.exists(XLSX_FILENAME):
        with open(XLSX_FILENAME, "rb") as fp:
            st.sidebar.download_button(
                label="📊 Original Excel-Matrix (.xlsx) herunterladen",
                data=fp,
                file_name=XLSX_FILENAME,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Enthält die vollständige Arbeitsmappe mit Steckbrief, Gemeindeübersicht, Detailmatrix aller Fachgebietseinträge & Recherchemanual"
            )
    else:
        st.sidebar.warning("Excel-Matrix-Datei nicht gefunden.")
except Exception:
    st.sidebar.warning("Excel-Matrix-Datei nicht verfügbar.")

st.sidebar.markdown("""
---
✉️ **Forschungsanfragen & Kontakt:**  
_Bei Fragen zum Versorgungsatlas oder zur Datenmatrix kontaktieren Sie das Autorenteam direkt am Poster oder per E-Mail._
""")

# MAIN PAGE
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur im Landkreis Eichstätt</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Regionaler Überblick", "🔍 Gemeinde-Steckbriefe (Detailansicht)", "📘 Recherchemanual & Methodik"])

with tab1:
    st.header("Landkreis-Steckbrief & Regionaler Überblick")
    
    # Steckbrief Grid
    col_sb1, col_sb2 = st.columns([1, 2])
    
    with col_sb1:
        st.markdown("""
        <div style="background-color:#F8FAFC; padding:18px; border-radius:8px; border:1px solid #CBD5E1;">
            <h4 style="margin-top:0; color:#1E3A8A;">📌 Landkreis-Steckbrief</h4>
            <table style="width:100%; font-size:14px; border-collapse:collapse;">
                <tr style="border-bottom:1px solid #E2E8F0;"><td style="padding:6px 0;"><strong>Untersuchungsraum:</strong></td><td>Landkreis Eichstätt</td></tr>
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
        # Aggregated stats metrics safely computed from overview dataframe
        def safe_sum(df, col):
            if col not in df.columns:
                return 0
            return int(pd.to_numeric(df[col], errors='coerce').fillna(0).sum())

        tot_einwohner = safe_sum(df_overview, "Einwohner")
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
    
    # Regional / Landkreisweite Versorgungsstrukturen
    st.subheader("Landkreisweite, regionale und koordinierende Versorgungsstrukturen")
    st.markdown("_Gemäß Erfassungsmethodik werden gemeindeübergreifend koordinierte Strukturen auf Landkreisebene geführt:_")
    
    landkreis_table = pd.DataFrame([
        {"Versorgungsbereich": "Öffentlicher Gesundheitsdienst", "Akteur / Angebot": "Gesundheitsamt Eichstätt", "Standort / Träger": "Landratsamt Eichstätt", "Funktion / Versorgungsform": "Öffentlicher Gesundheitsdienst", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Gesundheitsförderung & Koordination", "Akteur / Angebot": "Gesundheitsregionplus", "Standort / Träger": "Landkreis Eichstätt", "Funktion / Versorgungsform": "Koordination, Vernetzung & Prävention", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Landkreis Eichstätt"},
        {"Versorgungsbereich": "Schwangerschaft & Familie", "Akteur / Angebot": "Schwangerschaftsberatung", "Standort / Träger": "Gesundheitsamt / Träger", "Funktion / Versorgungsform": "Beratung & Unterstützung", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Sucht", "Akteur / Angebot": "Suchtberatung & Suchtprävention", "Standort / Träger": "Gesundheitsamt / Partner", "Funktion / Versorgungsform": "Beratung, Vermittlung & Prävention", "Räumlicher Bezug": "Landkreisweit / regional", "Standardquelle": "Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Psychosoziale Versorgung", "Akteur / Angebot": "Sozialpsychiatrischer Dienst / Krisendienst", "Standort / Träger": "Krisendienste Bayern", "Funktion / Versorgungsform": "Beratung, Unterstützung & Krisenintervention", "Räumlicher Bezug": "Landkreisweit / regional", "Standardquelle": "Krisendienste Bayern"},
        {"Versorgungsbereich": "Pflege", "Akteur / Angebot": "Pflegestützpunkt & Fachstelle f. Angehörige", "Standort / Träger": "Landkreis Eichstätt / Träger", "Funktion / Versorgungsform": "Pflegeberatung & Vernetzung", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Landkreis Eichstätt"},
        {"Versorgungsbereich": "Hebammenversorgung", "Akteur / Angebot": "Hebammen mit Versorgungsgebiet", "Standort / Träger": "Freiberufliche Hebammen", "Funktion / Versorgungsform": "Aufsuchende Hebammenversorgung", "Räumlicher Bezug": "Landkreisweit / PLZ", "Standardquelle": "Hebammensuche Bayern"},
        {"Versorgungsbereich": "Rettungsdienst", "Akteur / Angebot": "Rettungswachen & Notarztstandorte", "Standort / Träger": "ZRF Region 10 / ILS", "Funktion / Versorgungsform": "Notfallrettung & Notarztversorgung", "Räumlicher Bezug": "Rettungsdienstbereich Region 10", "Standardquelle": "ZRF Region Ingolstadt"},
        {"Versorgungsbereich": "Krankenhausversorgung", "Akteur / Angebot": "Klinik Eichstätt & Klinik Kösching", "Standort / Träger": "Kliniken im Naturpark Altmühltal", "Funktion / Versorgungsform": "Stationäre Grund- und Regelversorgung", "Räumlicher Bezug": "Standortbezogen & landkreisweit", "Standardquelle": "Deutsches Krankenhausverzeichnis"},
        {"Versorgungsbereich": "Rehabilitation", "Akteur / Angebot": "Klinik Kipfenberg (Neurolog. Zentrum)", "Standort / Träger": "Private / Freie Träger", "Funktion / Versorgungsform": "Stationäre & ambulante Rehabilitation", "Räumlicher Bezug": "Standortbezogen / regional", "Standardquelle": "GKV / QS-Reha"}
    ]).fillna("")
    
    st.dataframe(landkreis_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Interactive comparison chart
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

    # CLEAN BAYERN BENCHMARK GRAPHIC & SOURCES (UNIFORM LEVEL: BAYERN ONLY)
    st.subheader("📍 Regionaler Benchmark-Vergleich (Landkreis Eichstätt vs. Bayern)")
    st.markdown("""
    _Methode: Um eine methodisch saubere Gegenüberstellung ohne Durchmischung von Bundes- und Landesebene zu gewährleisten, werden die Erfassungswerte des Landkreises Eichstätt einheitlich dem **Landesdurchschnitt Bayern** gegenübergestellt._
    """)

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

    st.caption("""
    📌 **Quellen und Stichtagsnachweis der Referenzdaten:**
    * **Einwohnerzahl Stichtag:** 31.12.2025 (Bayerisches Landesamt für Statistik).
    * **Öffentliche Apotheken:** Bayerische Landesapothekerkammer (BLAK, Stand 2024/2025: 2.744 Apotheken in Bayern = 20,2 je 100k Einw.).
    * **Ambulante Ärztliche Versorgung:** Kassenärztliche Vereinigung Bayerns (KVB Versorgungsatlas, Stand 2024/2025: ca. 198,4 je 100k Einw.).
    * **Zahnärztliche Versorgung:** Bayerische Landeszahnärztekammer (BLZK, Stand 2024/2025: ca. 87,2 aktiv behandelnde Zahnärzt/innen je 100k Einw.). *Hinweis: Die Abweichung bei den Zahnärzten im Landkreis resultiert aus dem im Recherchemanual beschriebenen Opt-In-Verfahren der Kammerregister.*
    """)

with tab2:
    st.header("Gemeindespezifische Detail-Steckbriefe")
    
    selected_gemeinde = st.selectbox("Gemeinde auswählen:", sorted(df_detailed["Gemeinde"].unique()))
    
    g_det = df_detailed[df_detailed["Gemeinde"] == selected_gemeinde].iloc[0]
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.markdown(f"### Gemeindesteckbrief: **{selected_gemeinde}**")
        
        def clean_val(val, default="-"):
            if pd.isna(val):
                return default
            s = str(val).strip()
            if s.lower() in ["nan", "none", ""]:
                return default
            return s

        einwohner_val = f"{int(g_det['Einwohner']):,}".replace(",", ".") if str(g_det['Einwohner']).isdigit() or isinstance(g_det['Einwohner'], (int, float)) else str(g_det['Einwohner'])
        
        st.markdown(f"""
        <div style="background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #E2E8F0; font-size:13.5px;">
            👥 <strong>Einwohnerzahl:</strong> {einwohner_val} Einwohner<br>
            📐 <strong>Fläche:</strong> {clean_val(g_det.get('Flaeche_km2', ''))} km² ({clean_val(g_det.get('Einwohner_je_km2', ''))} Einw./km²)<br>
            🏛️ <strong>Gemeindeart:</strong> {clean_val(g_det.get('Gemeindeart', ''))}<br>
            🏢 <strong>Verwaltungsgemeinschaft:</strong> {clean_val(g_det.get('Verwaltungsgemeinschaft', ''))}<br>
            🏛️ <strong>Rathaus:</strong> {clean_val(g_det.get('Rathaus', ''))}<br>
            🌐 <strong>Website:</strong> <a href="{clean_val(g_det.get('Website', ''))}" target="_blank">{clean_val(g_det.get('Website', ''))}</a><br>
            👤 <strong>Bearbeiter/in:</strong> {clean_val(g_det.get('Bearbeiter', ''))}<br>
            📅 <strong>Letzte Prüfung:</strong> {clean_val(g_det.get('Letzte_Pruefung', ''))}<br>
            ✅ <strong>Erhebungsstatus:</strong> <span class="badge-status">{clean_val(g_det.get('Erhebungsstatus', ''))}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Ortsteile / Gemeindeteile")
        st.info(clean_val(g_det.get('Ortsteile', '')))
        
        bemerkung_val = clean_val(g_det.get('Bemerkung', ''), default="")
        if bemerkung_val:
            st.warning(f"⚠️ **Besondere Bemerkung:** {bemerkung_val}")
            
    with col_g2:
        st.markdown(f"### Detaillierte Fachkategorien: **{selected_gemeinde}**")
        
        def clean_int(val):
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
                clean_int(g_det.get("Allgemeinmedizin", 0)), clean_int(g_det.get("Praktische_Aerzte", 0)), clean_int(g_det.get("Innere_Medizin", 0)),
                clean_int(g_det.get("Kinder_Jugendmedizin", 0)), clean_int(g_det.get("Frauenheilkunde", 0)), clean_int(g_det.get("HNO", 0)),
                clean_int(g_det.get("Augenheilkunde", 0)), clean_int(g_det.get("Hautkrankheiten", 0)), clean_int(g_det.get("Orthopaedie", 0)),
                clean_int(g_det.get("Chirurgie", 0)), clean_int(g_det.get("Neurologie", 0)), clean_int(g_det.get("Psychiatrie_Psychotherapie", 0)),
                clean_int(g_det.get("Urologie", 0)), clean_int(g_det.get("Anaesthesiologie", 0)), clean_int(g_det.get("Radiologie", 0)), clean_int(g_det.get("Weitere_Fachgebiete", 0))
            ],
            "Standardquelle": ["116117-Arztsuche / KVB"] * 16
        })
        st.dataframe(aerzte_df, use_container_width=True, hide_index=True)
        st.caption(f"**Summe Fachgebietseinträge:** {clean_int(g_det.get('Summe_Aerztliche_Fachgebietseintraege', g_det.get('Aerztliche_Fachgebietseintraege', 0)))}")
        
        st.markdown("---")
        
        # 2. Psychotherapie & Zahnärzte
        col_sub1, col_sub2 = st.columns(2)
        
        with col_sub1:
            st.markdown("#### 🧠 Psychotherapie")
            psych_df = pd.DataFrame({
                "Kategorie": ["Psychologische Psychotherapie", "Kinder- & Jugendlichenpsychotherapie"],
                "Anzahl": [clean_int(g_det.get("Psychologische_Psychotherapie", g_det.get("Psychotherapie", 0))), clean_int(g_det.get("Kinder_Jugendlichenpsychotherapie", 0))],
                "Quelle": ["116117-Arztsuche"] * 2
            })
            st.dataframe(psych_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🦷 Zahnärztliche Versorgung")
            zahn_df = pd.DataFrame({
                "Kategorie": ["Zahnärztinnen und Zahnärzte", "Kieferorthopädie"],
                "Anzahl": [clean_int(g_det.get("Zahnaerzte", g_det.get("Zahnaerztliche_Personen", 0))), clean_int(g_det.get("Kieferorthopaedie", 0))],
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
                    clean_int(g_det.get("Oeffentliche_Apotheken", 0)), clean_int(g_det.get("Physiotherapie", g_det.get("Heilmittelpraxen", 0))),
                    clean_int(g_det.get("Ergotherapie", 0)), clean_int(g_det.get("Logopadie_Sprachtherapie", 0)),
                    clean_int(g_det.get("Podologie", 0)), clean_int(g_det.get("Ernaehrungstherapie", 0))
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
                "Anzahl": [clean_int(g_det.get("Ambulante_Pflegedienste", g_det.get("Pflegeeinrichtungen_Dienste", 0))), clean_int(g_det.get("Vollstationaere_Pflege", 0)), clean_int(g_det.get("Tagespflege", 0)), clean_int(g_det.get("Kurzzeitpflege", 0))],
                "Quelle": ["Pflegefinder Bayern"] * 4
            })
            st.dataframe(pflege_df, use_container_width=True, hide_index=True)
            
        with col_sub4:
            st.markdown("#### 🏥 Krankenhaus / Reha / Hospiz")
            kh_df = pd.DataFrame({
                "Einrichtungstyp": ["Krankenhausstandorte", "Rehabilitationseinrichtungen", "Stationäre Hospize"],
                "Anzahl": [clean_int(g_det.get("Krankenhausstandorte", g_det.get("Krankenhaus_Reha_Hospiz", 0))), clean_int(g_det.get("Rehabilitationseinrichtungen", 0)), clean_int(g_det.get("Stationaere_Hospize", 0))],
                "Quelle": ["Deutsches Krankenhausverzeichnis / QS-Reha"] * 3
            })
            st.dataframe(kh_df, use_container_width=True, hide_index=True)

with tab3:
    st.header("Wissenschaftlicher Hintergrund & Recherchemanual")
    
    st.markdown(f"""
    <div style="background-color:#F9FAFB; padding:15px; border-radius:8px; border:1px solid #E5E7EB; margin-bottom:25px;">
        <h4>🏫 Wissenschaftlicher Kontext (Lehrprojekt)</h4>
        Dieses interaktive System und die zugrundeliegende Erfassung wurden im Rahmen des 
        <strong>Masterstudiengangs {STUDIENGANG}</strong> ({SEMESTER}) an der <strong>{UNI_NAME}</strong> erarbeitet.<br><br>
        <strong>Projekt-Fokus:</strong><br>
        Es handelt sich um eine <strong>deskriptive Erfassung (Erfassungsstufen A und B)</strong> des Stadt- und Landkreises Eichstätt. 
        Ziel ist es, die bestehenden medizinischen und pflegerischen Versorgungsstrukturen systematisch zu kartieren 
        und für Akteure der regionalen Gesundheitsförderung nutzbar zu machen.<br><br>
        <strong>Interprofessioneller Ansatz:</strong><br>
        Die Erhebung ist in das Projektmodul <strong>\"{PROJEKTTITEL}\"</strong> eingebettet, 
        das aufzeigt, wie die verschiedenen Sektoren der Gesundheits- und Soziallandschaft (Ärzte, Zahnärzte, Heilmittelerbringer, Pflege- und Beratungsstrukturen) 
        integriert zusammenwirken können, um eine lückenlose Versorgung zu gewährleisten.<br><br>
        <em>Bearbeitung: {PROJEKTTEILNEHMER}</em>
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
        *   **Deskriptive Bestandsaufnahme:** Der Atlas untersucht ausschließlich das *Vorhandensein* (Bestand) von structures und ist keine Bedarfsplanung (keine Bedarfsdeckungs- oder Erreichbarkeitsanalyse).
        """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Landkreis Eichstätt | Erstellt für ein wissenschaftliches Poster | © 2026 Open Science Project</div>", unsafe_allow_html=True)
