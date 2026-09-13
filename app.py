import streamlit as st
import pandas as pd
import plotly.express as px

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
    df_over = pd.read_csv(CSV_OVERVIEW_FILENAME)
    df_det = pd.read_csv(CSV_DETAILED_FILENAME)
    return df_over, df_det

try:
    df_overview, df_detailed = load_data()
except Exception as e:
    st.error(f"""
    🚨 **Fehler beim Laden der Daten!**  
    Eine der benötigten Dateien (`{CSV_OVERVIEW_FILENAME}` oder `{CSV_DETAILED_FILENAME}`) wurde im Repository nicht gefunden.  
    **Lösung:** Vergewissert Euch, dass Ihr alle erstellten Daten-Dateien in Euer GitHub-Repository hochgeladen habt.
    """)
    st.stop()

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
    .info-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
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

st.sidebar.subheader("📥 Downloads (Vollständige Daten)")

# 1. Download XLSX
try:
    with open(XLSX_FILENAME, "rb") as fp:
        st.sidebar.download_button(
            label="📊 Original Excel-Matrix (.xlsx) herunterladen",
            data=fp,
            file_name=XLSX_FILENAME,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Enthält alle 4 Tabellenblätter: Steckbrief, Gemeindeübersicht, Detailmatrix aller Fachgebietseinträge & Recherchemanual"
        )
except Exception:
    pass

# 2. Download Detailed CSV
csv_det_bytes = df_detailed.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📈 Detaillierte Fachkategorien (.csv) herunterladen",
    data=csv_det_bytes,
    file_name=CSV_DETAILED_FILENAME,
    mime="text/csv",
    help="Enthält alle Aufschlüsselungen nach Fachärzten, Psychotherapie, Zahnärzten, Heilmitteln und Pflege"
)

# 3. Download Overview CSV
csv_over_bytes = df_overview.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📋 Gemeindeübersicht (.csv) herunterladen",
    data=csv_over_bytes,
    file_name=CSV_OVERVIEW_FILENAME,
    mime="text/csv"
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
        """, unsafe_allowed_html=True)
        
    with col_sb2:
        # Aggregated stats metrics
        tot_einwohner = df_overview["Einwohner"].sum()
        tot_aerzte = df_overview["Aerztliche_Fachgebietseintraege"].sum()
        tot_psych = df_overview["Psychotherapie"].sum()
        tot_zahnaerzte = df_overview["Zahnaerztliche_Personen"].sum()
        tot_apotheken = df_overview["Oeffentliche_Apotheken"].sum()
        tot_heilmittel = df_overview["Heilmittelpraxen"].sum()
        tot_pflege = df_overview["Pflegeeinrichtungen_Dienste"].sum()
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("🩺 Fachgebietseinträge gesamt", tot_aerzte)
        m_col2.metric("🧠 Psychotherapeuten gesamt", tot_psych)
        m_col3.metric("🦷 Zahnärztliche Personen", tot_zahnaerzte)
        
        m_col4, m_col5, m_col6 = st.columns(3)
        m_col4.metric("💊 Öffentliche Apotheken", tot_apotheken)
        m_col5.metric("💆 Heilmittelpraxen", tot_heilmittel)
        m_col6.metric("🏡 Pflegeeinrichtungen / Dienste", tot_pflege)
        
        # Referenzwerte Kasten
        st.markdown("""
        <div style="background-color:#F0FDF4; padding:12px; border-radius:8px; border-left:5px solid #16A34A; margin-top:12px;">
            <strong style="color:#15803D;">📌 Offizielle Vergleichsstatistiken (Bayern & Deutschland):</strong><br>
            <span style="font-size:13px; color:#1F2937;">
            • <strong>Ambulante Ärztedichte:</strong> 170 – 200 Ärzt/innen je 100k Einw. in DE/BY (<em>Quellen: BÄK / KVB</em>)<br>
            • <strong>Zahnärztedichte:</strong> 85 – 88 aktiv behandelnde Zahnärzt/innen je 100k Einw. (<em>Quelle: BZÄK</em>)<br>
            • <strong>Apothekendichte:</strong> 2.744 Apotheken in Bayern (ca. 21 je 100k Einw.) (<em>Quelle: BLAK / ABDA</em>)
            </span>
        </div>
        """, unsafe_allowed_html=True)
        
    st.markdown("---")
    
    # Regional / Landkreisweite Versorgungsstrukturen
    st.subheader("Landkreisweite, regionale und koordinierende Versorgungsstrukturen")
    st.markdown("_Gemäß Erfassungsmethodik (Blatt 01) werden gemeindeübergreifend koordinierte Strukturen auf Landkreisebene geführt:_")
    
    landkreis_table = pd.DataFrame([
        {"Versorgungsbereich": "Öffentlicher Gesundheitsdienst", "Akteur / Angebot": "Gesundheitsamt Eichstätt", "Standort / Träger": "Landratsamt Eichstätt", "Funktion / Versorgungsform": "Öffentlicher Gesundheitsdienst", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Gesundheitsförderung & Koordination", "Akteur / Angebot": "Gesundheitsregionplus", "Standort / Träger": "Landkreis Eichstätt", "Funktion": "Koordination, Vernetzung & Prävention", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Landkreis Eichstätt"},
        {"Versorgungsbereich": "Schwangerschaft & Familie", "Akteur / Angebot": "Schwangerschaftsberatung", "Standort / Träger": "Gesundheitsamt / Träger", "Funktion": "Beratung & Unterstützung", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Sucht", "Akteur / Angebot": "Suchtberatung & Suchtprävention", "Standort / Träger": "Gesundheitsamt / Partner", "Funktion": "Beratung, Vermittlung & Prävention", "Räumlicher Bezug": "Landkreisweit / regional", "Standardquelle": "Gesundheitsamt Eichstätt"},
        {"Versorgungsbereich": "Psychosoziale Versorgung", "Akteur / Angebot": "Sozialpsychiatrischer Dienst / Krisendienst", "Standort / Träger": "Krisendienste Bayern", "Funktion": "Beratung, Unterstützung & Krisenintervention", "Räumlicher Bezug": "Landkreisweit / regional", "Standardquelle": "Krisendienste Bayern"},
        {"Versorgungsbereich": "Pflege", "Akteur / Angebot": "Pflegestützpunkt & Fachstelle f. Angehörige", "Standort / Träger": "Landkreis Eichstätt / Träger", "Funktion": "Pflegeberatung & Vernetzung", "Räumlicher Bezug": "Landkreisweit", "Standardquelle": "Website Landkreis Eichstätt"},
        {"Versorgungsbereich": "Hebammenversorgung", "Akteur / Angebot": "Hebammen mit Versorgungsgebiet", "Standort / Träger": "Freiberufliche Hebammen", "Funktion": "Aufsuchende Hebammenversorgung", "Räumlicher Bezug": "Landkreisweit / PLZ", "Standardquelle": "Hebammensuche Bayern"},
        {"Versorgungsbereich": "Rettungsdienst", "Akteur / Angebot": "Rettungswachen & Notarztstandorte", "Standort / Träger": "ZRF Region 10 / ILS", "Funktion": "Notfallrettung & Notarztversorgung", "Räumlicher Bezug": "Rettungsdienstbereich Region 10", "Standardquelle": "ZRF Region Ingolstadt"},
        {"Versorgungsbereich": "Krankenhausversorgung", "Akteur / Angebot": "Klinik Eichstätt & Klinik Kösching", "Standort / Träger": "Kliniken im Naturpark Altmühltal", "Funktion": "Stationäre Grund- und Regelversorgung", "Räumlicher Bezug": "Standortbezogen & landkreisweit", "Standardquelle": "Deutsches Krankenhausverzeichnis"},
        {"Versorgungsbereich": "Rehabilitation", "Akteur / Angebot": "Klinik Kipfenberg (Neurolog. Zentrum)", "Standort / Träger": "Private / Freie Träger", "Funktion": "Stationäre & ambulante Rehabilitation", "Räumlicher Bezug": "Standortbezogen / regional", "Standardquelle": "GKV / QS-Reha"}
    ])
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
        height=500
    )
    fig.update_traces(
        marker_line_color='#1E293B', 
        marker_line_width=1.2,
        texttemplate='%{y}', 
        textposition='outside'
    )
    fig.update_layout(xaxis_tickangle=-45, plot_bgcolor='white', paper_bgcolor='white', yaxis=dict(gridcolor='#E2E8F0'))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Gemeindespezifische Detail-Steckbriefe")
    
    selected_gemeinde = st.selectbox("Gemeinde auswählen:", sorted(df_detailed["Gemeinde"].unique()))
    
    g_det = df_detailed[df_detailed["Gemeinde"] == selected_gemeinde].iloc[0]
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.markdown(f"### Gemeindesteckbrief: **{selected_gemeinde}**")
        st.markdown(f"""
        <div style="background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #E2E8F0; font-size:13.5px;">
            👥 <strong>Einwohnerzahl:</strong> {g_det['Einwohner']:,} Einwohner<br>
            📐 <strong>Fläche:</strong> {g_det['Flaeche_km2']} km² ({g_det['Einwohner_je_km2']} Einw./km²)<br>
            🏛️ <strong>Gemeindeart:</strong> {g_det['Gemeindeart']}<br>
            🏢 <strong>Verwaltungsgemeinschaft:</strong> {g_det['Verwaltungsgemeinschaft']}<br>
            🏛️ <strong>Rathaus:</strong> {g_det['Rathaus']}<br>
            🌐 <strong>Website:</strong> <a href="{g_det['Website']}" target="_blank">{g_det['Website']}</a><br>
            👤 <strong>Bearbeiter/in:</strong> {g_det['Bearbeiter']}<br>
            📅 <strong>Letzte Prüfung:</strong> {g_det['Letzte_Pruefung']}<br>
            ✅ <strong>Erhebungsstatus:</strong> <span class="badge-status">{g_det['Erhebungsstatus']}</span>
        </div>
        """, unsafe_allowed_html=True)
        
        st.markdown("#### Ortsteile / Gemeindeteile")
        st.info(g_det['Ortsteile'])
        
        if g_det['Bemerkung']:
            st.warning(f"⚠️ **Besondere Bemerkung:** {g_det['Bemerkung']}")
            
    with col_g2:
        st.markdown(f"### Detaillierte Fachkategorien: **{selected_gemeinde}**")
        
        # Build category tables matching original template
        
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
                g_det["Allgemeinmedizin"], g_det["Praktische_Aerzte"], g_det["Innere_Medizin"],
                g_det["Kinder_Jugendmedizin"], g_det["Frauenheilkunde"], g_det["HNO"],
                g_det["Augenheilkunde"], g_det["Hautkrankheiten"], g_det["Orthopaedie"],
                g_det["Chirurgie"], g_det["Neurologie"], g_det["Psychiatrie_Psychotherapie"],
                g_det["Urologie"], g_det["Anaesthesiologie"], g_det["Radiologie"], g_det["Weitere_Fachgebiete"]
            ],
            "Standardquelle": ["116117-Arztsuche / KVB"] * 16
        })
        st.dataframe(aerzte_df, use_container_width=True, hide_index=True)
        st.caption(f"**Summe Fachgebietseinträge:** {g_det['Summe_Aerztliche_Fachgebietseintraege']}")
        
        st.markdown("---")
        
        # 2. Psychotherapie & Zahnärzte
        col_sub1, col_sub2 = st.columns(2)
        
        with col_sub1:
            st.markdown("#### 🧠 Psychotherapie")
            psych_df = pd.DataFrame({
                "Kategorie": ["Psychologische Psychotherapie", "Kinder- & Jugendlichenpsychotherapie"],
                "Anzahl": [g_det["Psychologische_Psychotherapie"], g_det["Kinder_Jugendlichenpsychotherapie"]],
                "Quelle": ["116117-Arztsuche"] * 2
            })
            st.dataframe(psych_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🦷 Zahnärztliche Versorgung")
            zahn_df = pd.DataFrame({
                "Kategorie": ["Zahnärztinnen und Zahnärzte", "Kieferorthopädie"],
                "Anzahl": [g_det["Zahnaerzte"], g_det["Kieferorthopaedie"]],
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
                    g_det["Oeffentliche_Apotheken"], g_det["Physiotherapie"],
                    g_det["Ergotherapie"], g_det["Logopadie_Sprachtherapie"],
                    g_det["Podologie"], g_det["Ernaehrungstherapie"]
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
                "Anzahl": [g_det["Ambulante_Pflegedienste"], g_det["Vollstationaere_Pflege"], g_det["Tagespflege"], g_det["Kurzzeitpflege"]],
                "Quelle": ["Pflegefinder Bayern"] * 4
            })
            st.dataframe(pflege_df, use_container_width=True, hide_index=True)
            
        with col_sub4:
            st.markdown("#### 🏥 Krankenhaus / Reha / Hospiz")
            kh_df = pd.DataFrame({
                "Einrichtungstyp": ["Krankenhausstandorte", "Rehabilitationseinrichtungen", "Stationäre Hospize"],
                "Anzahl": [g_det["Krankenhausstandorte"], g_det["Rehabilitationseinrichtungen"], g_det["Stationaere_Hospize"]],
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
    """, unsafe_allowed_html=True)
    
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
