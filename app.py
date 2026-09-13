import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import openpyxl
import io
import os

# ==============================================================================
# 🎓 KONFIGURATION / PERSONALISIERUNG (HIER EINFACH ANPASSEN!)
# ==============================================================================
UNI_NAME = "Katholische Stiftungshochschule München"                                      # Name Eurer Universität/Hochschule
STUDIENGANG = "Angewandte Versorgungsforschung"         # Euer Studiengang
SEMESTER = "Sommersemester 2026"                        # Das aktuelle Semester
PROJEKTTITEL = "Quartiersmanagement aus interprofessioneller Perspektive"
PROJEKTTEILNEHMER = "Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc."          # Eure Namen für die Bearbeitung

# DATEINAMEN
XLSX_FILENAME = "versorgungsatlas_eichstaett_original_matrix.xlsx"
CSV_DETAILED_FILENAME = "versorgungsatlas_eichstaett_detailliert.csv"
CSV_OVERVIEW_FILENAME = "versorgungsatlas_eichstaett_v2.csv"
# ==============================================================================

# Set page configurations
st.set_page_config(
    page_title="Gesundheits- & Versorgungsatlas Eichstätt",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hardcoded Fallback Data for All 30 Municipalities (Guarantees zero crashes)
FALLBACK_COMMUNITIES = [
    {"Gemeinde": "Adelschlag", "Einwohner": 2981, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Altmannstein", "Einwohner": 7195, "Aerztliche_Fachgebietseintraege": 3, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 2, "Pflegeeinrichtungen_Dienste": 3, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Beilngries", "Einwohner": 10242, "Aerztliche_Fachgebietseintraege": 37, "Psychotherapie": 1, "Zahnaerztliche_Personen": 4, "Oeffentliche_Apotheken": 2, "Heilmittelpraxen": 13, "Pflegeeinrichtungen_Dienste": 4, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Böhmfeld", "Einwohner": 1697, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Buxheim", "Einwohner": 3771, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 1, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Denkendorf", "Einwohner": 5059, "Aerztliche_Fachgebietseintraege": 5, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 5, "Pflegeeinrichtungen_Dienste": 3, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Dollnstein", "Einwohner": 2850, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 1, "Zahnaerztliche_Personen": 1, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Egweil", "Einwohner": 1247, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Eichstätt (Stadt)", "Einwohner": 14066, "Aerztliche_Fachgebietseintraege": 78, "Psychotherapie": 3, "Zahnaerztliche_Personen": 10, "Oeffentliche_Apotheken": 4, "Heilmittelpraxen": 14, "Pflegeeinrichtungen_Dienste": 7, "Krankenhaus_Reha_Hospiz": 1, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Eitensheim", "Einwohner": 3030, "Aerztliche_Fachgebietseintraege": 5, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 2, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Gaimersheim", "Einwohner": 12526, "Aerztliche_Fachgebietseintraege": 17, "Psychotherapie": 1, "Zahnaerztliche_Personen": 3, "Oeffentliche_Apotheken": 2, "Heilmittelpraxen": 4, "Pflegeeinrichtungen_Dienste": 5, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Großmehring", "Einwohner": 7498, "Aerztliche_Fachgebietseintraege": 3, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 1, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Hepberg", "Einwohner": 3077, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 2, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Hitzhofen", "Einwohner": 3022, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Kinding", "Einwohner": 2600, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Kipfenberg", "Einwohner": 5835, "Aerztliche_Fachgebietseintraege": 3, "Psychotherapie": 1, "Zahnaerztliche_Personen": 2, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 6, "Pflegeeinrichtungen_Dienste": 1, "Krankenhaus_Reha_Hospiz": 1, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Kösching", "Einwohner": 9737, "Aerztliche_Fachgebietseintraege": 54, "Psychotherapie": 5, "Zahnaerztliche_Personen": 1, "Oeffentliche_Apotheken": 2, "Heilmittelpraxen": 4, "Pflegeeinrichtungen_Dienste": 1, "Krankenhaus_Reha_Hospiz": 1, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Lenting", "Einwohner": 4980, "Aerztliche_Fachgebietseintraege": 5, "Psychotherapie": 0, "Zahnaerztliche_Personen": 2, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 2, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Mindelstetten", "Einwohner": 1822, "Aerztliche_Fachgebietseintraege": 2, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Mörnsheim", "Einwohner": 1523, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Nassenfels", "Einwohner": 2351, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Oberdolling", "Einwohner": 1371, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Pförring", "Einwohner": 4100, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 0, "Zahnaerztliche_Personen": 1, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 1, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Pollenfeld", "Einwohner": 3051, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 1, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Schernfeld", "Einwohner": 3285, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Stammham", "Einwohner": 4159, "Aerztliche_Fachgebietseintraege": 2, "Psychotherapie": 2, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Titting", "Einwohner": 2688, "Aerztliche_Fachgebietseintraege": 1, "Psychotherapie": 2, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 1, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Walting", "Einwohner": 2289, "Aerztliche_Fachgebietseintraege": 0, "Psychotherapie": 0, "Zahnaerztliche_Personen": 0, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Wellheim", "Einwohner": 2725, "Aerztliche_Fachgebietseintraege": 4, "Psychotherapie": 1, "Zahnaerztliche_Personen": 1, "Oeffentliche_Apotheken": 0, "Heilmittelpraxen": 0, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"},
    {"Gemeinde": "Wettstetten", "Einwohner": 5205, "Aerztliche_Fachgebietseintraege": 8, "Psychotherapie": 0, "Zahnaerztliche_Personen": 1, "Oeffentliche_Apotheken": 1, "Heilmittelpraxen": 1, "Pflegeeinrichtungen_Dienste": 0, "Krankenhaus_Reha_Hospiz": 0, "Erhebungsstatus": "vollständig"}
]

# Multi-level data loading helper
@st.cache_data
def load_data():
    # Level 1: Try reading Excel Matrix
    if os.path.exists(XLSX_FILENAME):
        try:
            xls = pd.ExcelFile(XLSX_FILENAME)
            sheet_over = "Gemeindeübersicht" if "Gemeindeübersicht" in xls.sheet_names else xls.sheet_names[1]
            sheet_det = "Detailmatrix Gemeinden" if "Detailmatrix Gemeinden" in xls.sheet_names else xls.sheet_names[2]
            
            df_raw_o = pd.read_excel(XLSX_FILENAME, sheet_name=sheet_over)
            hdr_o = 0
            for idx, r in df_raw_o.iterrows():
                if "Gemeinde" in r.values:
                    hdr_o = idx + 1
                    break
            df_o = pd.read_excel(XLSX_FILENAME, sheet_name=sheet_over, header=hdr_o)

            df_raw_d = pd.read_excel(XLSX_FILENAME, sheet_name=sheet_det)
            hdr_d = 0
            for idx, r in df_raw_d.iterrows():
                if "Gemeinde" in r.values:
                    hdr_d = idx + 1
                    break
            df_d = pd.read_excel(XLSX_FILENAME, sheet_name=sheet_det, header=hdr_d)

            df_o = df_o[df_o["Gemeinde"].astype(str).str.startswith("Gesamt") == False]
            return df_o.fillna(""), df_d.fillna("")
        except Exception:
            pass

    # Level 2: Try reading CSV files
    if os.path.exists(CSV_OVERVIEW_FILENAME) and os.path.exists(CSV_DETAILED_FILENAME):
        try:
            df_o = pd.read_csv(CSV_OVERVIEW_FILENAME)
            df_d = pd.read_csv(CSV_DETAILED_FILENAME)
            return df_o.fillna(""), df_d.fillna("")
        except Exception:
            pass

    # Level 3: Fallback to embedded DataFrame
    df_o = pd.DataFrame(FALLBACK_COMMUNITIES)
    df_d = pd.DataFrame(FALLBACK_COMMUNITIES)
    return df_o.fillna(""), df_d.fillna("")

df_overview, df_detailed = load_data()

# Ensure numeric types
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
    <strong>🎓 Studentisches Lehrprojekt:</strong><br>
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

st.sidebar.subheader("📥 Downloads")

# 1. Download XLSX
if os.path.exists(XLSX_FILENAME):
    try:
        with open(XLSX_FILENAME, "rb") as fp:
            st.sidebar.download_button(
                label="📊 Original Excel-Matrix (.xlsx) herunterladen",
                data=fp,
                file_name=XLSX_FILENAME,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Enthält alle Tabellenblätter: Steckbrief, Gemeindeübersicht, Detailmatrix & Recherchemanual"
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
        file_name=XLSX_FILENAME,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.sidebar.markdown("""
---
📄 **Gedruckter Versorgungsatlas (PDF):**  
Den vollständigen Atlas mit allen 30 Detailblättern können Sie über den QR-Code auf unserem Poster herunterladen.

✉️ **Forschungsanfragen / Original-Datensatz:**  
_Kontaktieren Sie das Autorenteam direkt am Poster oder per E-Mail._
""")

# MAIN PAGE
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur im Landkreis Eichstätt</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Landkreis-Steckbrief", "🔍 Gemeinde-Steckbriefe (Detailansicht)", "📘 Recherchemanual & Methodik"])

with tab1:
    st.header("Landkreis-Steckbrief (Blatt 01) & Regionaler Überblick")
    
    # Steckbrief Grid
    col_sb1, col_sb2 = st.columns([1, 2])
    
    with col_sb1:
        st.markdown("""
        <div style="background-color:#F8FAFC; padding:18px; border-radius:8px; border:1px solid #CBD5E1;">
            <h4 style="margin-top:0; color:#1E3A8A;">📌 Landkreis-Steckbrief (Blatt 01)</h4>
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
        # Aggregated stats metrics
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
    
    # Regional / Landkreisweite Versorgungsstrukturen
    st.subheader("Landkreisweite, regionale und koordinierende Versorgungsstrukturen")
    st.markdown("_Gemäß Erfassungsmethodik (Blatt 01) werden gemeindeübergreifend koordinierte Strukturen auf Landkreisebene geführt:_")
    
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
    
    selected_gemeinde = st.selectbox("Gemeinde auswählen:", sorted(df_detailed["Gemeinde"].unique()))
    
    g_det = df_detailed[df_detailed["Gemeinde"] == selected_gemeinde].iloc[0]
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.markdown(f"### Gemeindesteckbrief: **{selected_gemeinde}**")
        
        # Helper to format clean text without 'nan'
        def clean_val(val, default="-"):
            if pd.isna(val):
                return default
            s = str(val).strip()
            if s.lower() in ["nan", "none", ""]:
                return default
            return s

        einwohner_num = pd.to_numeric(g_det.get('Einwohner', 0), errors='coerce') or 0
        einwohner_val = f"{int(einwohner_num):,}".replace(",", ".")
        
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
        
        # Check remark carefully so 'nan' is NEVER displayed
        bemerkung_val = clean_val(g_det.get('Bemerkung', ''), default="")
        if bemerkung_val and bemerkung_val != "-":
            st.warning(f"⚠️ **Besondere Bemerkung:** {bemerkung_val}")
            
    with col_g2:
        st.markdown(f"### Detaillierte Fachkategorien: **{selected_gemeinde}**")
        
        # Helper to convert float counts to clean ints
        def clean_int(val):
            try:
                if pd.isna(val):
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
        st.caption(f"**Summe Fachgebietseinträge:** {clean_int(g_det.get('Summe_Aerztliche_Fachgebietseintraege', 0))}")
        
        st.markdown("---")
        
        # 2. Psychotherapie & Zahnärzte
        col_sub1, col_sub2 = st.columns(2)
        
        with col_sub1:
            st.markdown("#### 🧠 Psychotherapie")
            psych_df = pd.DataFrame({
                "Kategorie": ["Psychologische Psychotherapie", "Kinder- & Jugendlichenpsychotherapie"],
                "Anzahl": [clean_int(g_det.get("Psychologische_Psychotherapie", 0)), clean_int(g_det.get("Kinder_Jugendlichenpsychotherapie", 0))],
                "Quelle": ["116117-Arztsuche"] * 2
            })
            st.dataframe(psych_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🦷 Zahnärztliche Versorgung")
            zahn_df = pd.DataFrame({
                "Kategorie": ["Zahnärztinnen und Zahnärzte", "Kieferorthopädie"],
                "Anzahl": [clean_int(g_det.get("Zahnaerzte", 0)), clean_int(g_det.get("Kieferorthopaedie", 0))],
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
                    clean_int(g_det.get("Oeffentliche_Apotheken", 0)), clean_int(g_det.get("Physiotherapie", 0)),
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
                "Anzahl": [clean_int(g_det.get("Ambulante_Pflegedienste", 0)), clean_int(g_det.get("Vollstationaere_Pflege", 0)), clean_int(g_det.get("Tagespflege", 0)), clean_int(g_det.get("Kurzzeitpflege", 0))],
                "Quelle": ["Pflegefinder Bayern"] * 4
            })
            st.dataframe(pflege_df, use_container_width=True, hide_index=True)
            
        with col_sub4:
            st.markdown("#### 🏥 Krankenhaus / Reha / Hospiz")
            kh_df = pd.DataFrame({
                "Einrichtungstyp": ["Krankenhausstandorte", "Rehabilitationseinrichtungen", "Stationäre Hospize"],
                "Anzahl": [clean_int(g_det.get("Krankenhausstandorte", 0)), clean_int(g_det.get("Rehabilitationseinrichtungen", 0)), clean_int(g_det.get("Stationaere_Hospize", 0))],
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
        *   **Deskriptive Bestandsaufnahme:** Der Atlas untersucht ausschließlich das *Vorhandensein* (Bestand) von Strukturen und ist keine Bedarfsplanung (keine Bedarfsdeckungs- oder Erreichbarkeitsanalyse).
        """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Landkreis Eichstätt | Erstellt für ein wissenschaftliches Poster | © 2026 Open Science Project</div>", unsafe_allow_html=True)
