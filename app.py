import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 🎓 KONFIGURATION / PERSONALISIERUNG
# ==============================================================================
UNI_NAME = "Katholischen Stiftungshochschule München"                                      # Name Eurer Universität/Hochschule
STUDIENGANG = "Angewandte Versorgungsforschung"         # Euer Studiengang
SEMESTER = "Sommersemester 2026"                        # Das aktuelle Semester
PROJEKTTITEL = "Quartiersmanagement aus interprofessioneller Perspektive: Versorgungsformen und -strukturen von Stadt und Landkreis Eichstätt - eine explorative Mixed-Methods-Studie"
AUTORINNEN = "Christina Papacek-Zimmermann B.Sc., Jennifer Zimmermann B.Sc."                # Eure Namen für die Bearbeitung

# DATEINAMEN DER DATEN-DATEIEN & GRAFIKEN
XLSX_FILENAME = "versorgungsatlas_eichstaett_original_matrix.xlsx"
BENCHMARK_IMG = "versorgungsatlas_regionaler_benchmark.png"
# ==============================================================================

# Set page configurations
st.set_page_config(
    page_title="Gesundheits- & Versorgungsatlas Eichstätt",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data helper - Reads directly from the Excel Matrix!
@st.cache_data
def load_data():
    try:
        # Sheet 1: Gemeindeübersicht (Index 1)
        df_over = pd.read_excel(XLSX_FILENAME, sheet_name=1, header=3)
        df_over = df_over[df_over.iloc[:, 0].notna() & (~df_over.iloc[:, 0].astype(str).str.contains('Gesamt', case=False))]
        
        # Rename standard columns by position to avoid encoding errors
        df_over.columns.values[0] = 'Gemeinde'
        df_over.columns.values[1] = 'Einwohner'
        df_over.columns.values[2] = 'Aerztliche_Fachgebietseintraege'
        df_over.columns.values[3] = 'Psychotherapie'
        df_over.columns.values[4] = 'Zahnaerztliche_Personen'
        df_over.columns.values[5] = 'Oeffentliche_Apotheken'
        df_over.columns.values[6] = 'Heilmittelpraxen'
        df_over.columns.values[7] = 'Pflegeeinrichtungen_Dienste'
        df_over.columns.values[8] = 'Krankenhaus_Reha_Hospiz'
        df_over.columns.values[9] = 'Erhebungsstatus'
        
        # Sheet 2: Detailmatrix Gemeinden (Index 2)
        df_det = pd.read_excel(XLSX_FILENAME, sheet_name=2, header=3)
        df_det = df_det[df_det.iloc[:, 0].notna() & (~df_det.iloc[:, 0].astype(str).str.contains('Gesamt', case=False))]
        df_det.columns.values[0] = 'Gemeinde'
    except Exception as e:
        # Fallback to CSV if present
        try:
            df_over = pd.read_csv("versorgungsatlas_eichstaett_v2.csv")
            df_det = pd.read_csv("versorgungsatlas_eichstaett_detailliert.csv")
        except Exception:
            st.error(f"🚨 **Fehler beim Laden der Daten:** {e}")
            st.stop()
        
    df_over = df_over.fillna("")
    df_det = df_det.fillna("")
    return df_over, df_det

try:
    df_overview, df_detailed = load_data()
except Exception as e:
    st.error(f"🚨 **Fehler beim Laden der Excel-Matrix:** {e}")
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
    </style>
""", unsafe_allowed_html=True)

# SIDEBAR: Context & Info
st.sidebar.image("https://img.icons8.com/clouds/150/hospital-room.png", width=100)
st.sidebar.title("Versorgungsatlas")
st.sidebar.markdown("**Stadt und Landkreis Eichstätt (Oberbayern)**")

# Studentisches Infofeld in der Sidebar
st.sidebar.markdown(f"""
<div style="background-color:#F5F3FF; padding:12px; border-radius:5px; border-left:4px solid #7C3AED; margin-bottom:15px; font-size: 13px;">
    <strong>🎓 Wissenschaftliches Projekt:</strong><br>
    Erstellt im Rahmen des Masterstudiengangs <strong>{STUDIENGANG}</strong> ({SEMESTER}) an der <strong>{UNI_NAME}</strong>.<br><br>
    <strong>Projekttitel:</strong><br>
    <em>{PROJEKTTITEL}</em><br><br>
    <strong>Autorinnen:</strong><br>
    {AUTORINNEN}
</div>
""", unsafe_allowed_html=True)

# Structure Box with Exact Stichtag
st.sidebar.markdown("""
<div style="background-color:#EFF6FF; padding:12px; border-radius:5px; border-left:4px solid #3B82F6; margin-bottom:15px; font-size: 13px;">
    <strong>📍 Steckbrief Stadt und Landkreis Eichstätt:</strong><br>
    🏛️ <strong>Regierungsbezirk:</strong> Oberbayern<br>
    👥 <strong>Einwohner:</strong> 135.982<br>
    📅 <strong>Stichtag Einwohner:</strong> 31.12.2025<br>
    🗺️ <strong>Fläche:</strong> 1.214 km²<br>
    📐 <strong>Bevölkerungsdichte:</strong> 112,0 Einw./km²<br>
    🏡 <strong>Gemeinden:</strong> 30
</div>
""", unsafe_allowed_html=True)

# SINGLE EXCEL DOWNLOAD BUTTON
st.sidebar.subheader("📥 Daten-Download")

try:
    with open(XLSX_FILENAME, "rb") as fp:
        st.sidebar.download_button(
            label="📊 Original Excel-Matrix (.xlsx) herunterladen",
            data=fp,
            file_name=XLSX_FILENAME,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Enthält die vollständige Arbeitsmappe mit Steckbrief, Gemeindeübersicht, Detailmatrix aller Fachgebietseinträge & Recherchemanual"
        )
except Exception:
    st.sidebar.warning("Excel-Matrix-Datei nicht im Repository gefunden.")

st.sidebar.markdown("""
---
✉️ **Forschungsanfragen / Original-Datensatz:**  
_Kontaktieren Sie die Autorinnen direkt per E-Mail oder am Poster._
""")

# MAIN PAGE
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allowed_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur in Stadt und Landkreis Eichstätt</div>', unsafe_allowed_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Regionalvergleich", "🔍 Gemeinde-Steckbriefe (Detailansicht)", "📘 Recherchemanual & Methodik"])

with tab1:
    st.header("Überblick über alle erfassten Angebote (Summe aller 30 Gemeinden)")
    
    # Aggregated stats metrics
    def safe_sum(df, col):
        return int(pd.to_numeric(df[col], errors='coerce').fillna(0).sum())

    tot_einwohner = safe_sum(df_overview, "Einwohner")
    tot_aerzte = safe_sum(df_overview, "Aerztliche_Fachgebietseintraege")
    tot_psych = safe_sum(df_overview, "Psychotherapie")
    tot_zahnaerzte = safe_sum(df_overview, "Zahnaerztliche_Personen")
    tot_apotheken = safe_sum(df_overview, "Oeffentliche_Apotheken")
    tot_heilmittel = safe_sum(df_overview, "Heilmittelpraxen")
    tot_pflege = safe_sum(df_overview, "Pflegeeinrichtungen_Dienste")
    tot_kh = safe_sum(df_overview, "Krankenhaus_Reha_Hospiz")
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("👥 Einwohner gesamt", "135.982")
    m_col2.metric("🩺 Ärztliche Fachgebietseinträge", tot_aerzte)
    m_col3.metric("🧠 Psychotherapie", tot_psych)
    m_col4.metric("🦷 Zahnärztliche Personen", tot_zahnaerzte)
    
    m_col5, m_col6, m_col7, m_col8 = st.columns(4)
    m_col5.metric("💊 Öffentliche Apotheken", tot_apotheken)
    m_col6.metric("💆 Heilmittelpraxen", tot_heilmittel)
    m_col7.metric("🏡 Pflegeeinrichtungen / Dienste", tot_pflege)
    m_col8.metric("🏥 Krankenhaus / Reha / Hospiz", tot_kh)
    
    st.markdown("---")
    
    # REGIONAL BENCHMARK COMPARISON GRAPHIC & DETAILED SOURCES
    st.subheader("📍 Regionaler Benchmark-Vergleich (Stadt und Landkreis Eichstätt vs. Bayern)")
    st.markdown("""
    _Methode: Um eine methodisch saubere Gegenüberstellung ohne Durchmischung von Bundes- und Landesebene zu gewährleisten, werden die Erfassungswerte von Stadt und Landkreis Eichstätt einheitlich dem **Landesdurchschnitt Bayern** gegenübergestellt._
    """)

    # Display Benchmark Graphic
    if os.path.exists(BENCHMARK_IMG):
        st.image(BENCHMARK_IMG, caption="Abbildung: Regionaler Benchmark-Vergleich aller 7 Versorgungssektoren (Stadt und Landkreis Eichstätt vs. Bayern Ø)", use_container_width=True)
    else:
        st.info("Hinweis: Grafik `versorgungsatlas_regionaler_benchmark.png` wird geladen.")

    st.markdown("""
    📌 **Quellen und Stichtagsnachweis der Referenzdaten:**
    * **Einwohnerzahl Stichtag:** 31.12.2025 – Bayerisches Landesamt für Statistik (LfStat Bayern). Homepage: [www.statistik.bayern.de](https://www.statistik.bayern.de) *(abgerufen am 13.09.2026)*.
    * **Ambulante Ärztliche Versorgung:** Kassenärztliche Vereinigung Bayerns (KVB Versorgungsatlas Hausärzte & KVB-Arztregister, Stand August 2026: 72,8 Hausärzt/innen je 100k Einw.). Homepage: [www.kvb.de/ueber-uns/versorgungsatlas/](https://www.kvb.de/ueber-uns/versorgungsatlas/) *(abgerufen am 13.09.2026)*.
    * **Psychotherapeutische Versorgung:** Kassenärztliche Vereinigung Bayerns (KVB Bedarfsplanungsdaten & 116117-Arztsuche). Homepage: [www.kvb.de](https://www.kvb.de) *(abgerufen am 13.09.2026)*.
    * **Zahnärztliche Versorgung:** Bayerische Landeszahnärztekammer (BLZK) & Bundeszahnärztekammer (BZÄK Zahnarztsuche / Mitgliederstatistik). Homepages: [www.blzk.de](https://www.blzk.de) & [www.bzaek.de](https://www.bzaek.de) *(abgerufen am 13.09.2026)*.
    * **Öffentliche Apotheken & Arzneimittelversorgung:** Bayerische Landesapothekerkammer (BLAK) & ABDA (Stand 2024/2025: 2.744 Apotheken in Bayern = 20,2 je 100k Einw.) sowie Statistisches Bundesamt (Destatis Pressemitteilung N034 2024). Homepages: [www.blak.de](https://www.blak.de), [www.abda.de](https://www.abda.de) & [www.destatis.de](https://www.destatis.de) *(abgerufen am 13.09.2026)*.
    * **Heilmittelpraxen:** GKV-Spitzenverband (GKV-Heilmittelerbringerverzeichnis) & Amtliche Gesundheitsberichterstattung des Bundes (GBE Bund). Homepages: [www.gkv-heilmittel.de](https://www.gkv-heilmittel.de) & [www.gbe-bund.de](https://www.gbe-bund.de) *(abgerufen am 13.09.2026)*.
    * **Pflegerische Versorgung:** Bayerisches Landesamt für Statistik (LfStat Bayern, Zweijährliche Pflegestatistik 12/2023) & Pflegefinder Bayern. Homepage: [www.statistik.bayern.de](https://www.statistik.bayern.de) *(abgerufen am 13.09.2026)*.
    * **Krankenhaus- & Rehabilitationsversorgung:** Bayerisches Staatsministerium für Gesundheit, Pflege und Prävention (StMGP Krankenhausplan Bayern) & Deutsches Krankenhausverzeichnis. Homepages: [www.stmgp.bayern.de](https://www.stmgp.bayern.de) & [www.deutsches-krankenhaus-verzeichnis.de](https://www.deutsches-krankenhaus-verzeichnis.de) *(abgerufen am 13.09.2026)*.
    """)

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

        einwohner_val = f"{int(g_det['Einwohner']):,}".replace(",", ".") if str(g_det['Einwohner']).isdigit() else str(g_det['Einwohner'])
        
        st.markdown(f"""
        <div style="background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #E2E8F0; font-size:13.5px;">
            👥 <strong>Einwohnerzahl:</strong> {einwohner_val} Einwohner<br>
            📐 <strong>Fläche:</strong> {clean_val(g_det['Flaeche_km2'])} km² ({clean_val(g_det['Einwohner_je_km2'])} Einw./km²)<br>
            🏛️ <strong>Gemeindeart:</strong> {clean_val(g_det['Gemeindeart'])}<br>
            🏢 <strong>Verwaltungsgemeinschaft:</strong> {clean_val(g_det['Verwaltungsgemeinschaft'])}<br>
            🏛️ <strong>Rathaus:</strong> {clean_val(g_det['Rathaus'])}<br>
            🌐 <strong>Website:</strong> <a href="{clean_val(g_det['Website'])}" target="_blank">{clean_val(g_det['Website'])}</a>
        </div>
        """, unsafe_allowed_html=True)
        
        st.markdown("#### Ortsteile / Gemeindeteile")
        st.info(clean_val(g_det['Ortsteile']))
        
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
                clean_int(g_det["Allgemeinmedizin"]), clean_int(g_det["Praktische_Aerzte"]), clean_int(g_det["Innere_Medizin"]),
                clean_int(g_det["Kinder_Jugendmedizin"]), clean_int(g_det["Frauenheilkunde"]), clean_int(g_det["HNO"]),
                clean_int(g_det["Augenheilkunde"]), clean_int(g_det["Hautkrankheiten"]), clean_int(g_det["Orthopaedie"]),
                clean_int(g_det["Chirurgie"]), clean_int(g_det["Neurologie"]), clean_int(g_det["Psychiatrie_Psychotherapie"]),
                clean_int(g_det["Urologie"]), clean_int(g_det["Anaesthesiologie"]), clean_int(g_det["Radiologie"]), clean_int(g_det["Weitere_Fachgebiete"])
            ],
            "Standardquelle": ["116117-Arztsuche / KVB"] * 16
        })
        st.dataframe(aerzte_df, use_container_width=True, hide_index=True)
        st.caption(f"**Summe Fachgebietseinträge:** {clean_int(g_det['Summe_Aerztliche_Fachgebietseintraege'])}")
        
        st.markdown("---")
        
        # 2. Psychotherapie & Zahnärzte
        col_sub1, col_sub2 = st.columns(2)
        
        with col_sub1:
            st.markdown("#### 🧠 Psychotherapie")
            psych_df = pd.DataFrame({
                "Kategorie": ["Psychologische Psychotherapie", "Kinder- & Jugendlichenpsychotherapie"],
                "Anzahl": [clean_int(g_det["Psychologische_Psychotherapie"]), clean_int(g_det["Kinder_Jugendlichenpsychotherapie"])],
                "Quelle": ["116117-Arztsuche"] * 2
            })
            st.dataframe(psych_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🦷 Zahnärztliche Versorgung")
            zahn_df = pd.DataFrame({
                "Kategorie": ["Zahnärztinnen und Zahnärzte", "Kieferorthopädie"],
                "Anzahl": [clean_int(g_det["Zahnaerzte"]), clean_int(g_det["Kieferorthopaedie"])],
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
                    clean_int(g_det["Oeffentliche_Apotheken"]), clean_int(g_det["Physiotherapie"]),
                    clean_int(g_det["Ergotherapie"]), clean_int(g_det["Logopadie_Sprachtherapie"]),
                    clean_int(g_det["Podologie"]), clean_int(g_det["Ernaehrungstherapie"])
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
                "Anzahl": [clean_int(g_det["Ambulante_Pflegedienste"]), clean_int(g_det["Vollstationaere_Pflege"]), clean_int(g_det["Tagespflege"]), clean_int(g_det["Kurzzeitpflege"])],
                "Quelle": ["Pflegefinder Bayern"] * 4
            })
            st.dataframe(pflege_df, use_container_width=True, hide_index=True)
            
        with col_sub4:
            st.markdown("#### 🏥 Krankenhaus / Reha / Hospiz")
            kh_df = pd.DataFrame({
                "Einrichtungstyp": ["Krankenhausstandorte", "Rehabilitationseinrichtungen", "Stationäre Hospize"],
                "Anzahl": [clean_int(g_det["Krankenhausstandorte"]), clean_int(g_det["Rehabilitationseinrichtungen"]), clean_int(g_det["Stationaere_Hospize"])],
                "Quelle": ["Deutsches Krankenhausverzeichnis / QS-Reha"] * 3
            })
            st.dataframe(kh_df, use_container_width=True, hide_index=True)

with tab3:
    st.header("Wissenschaftlicher Hintergrund & Recherchemanual")
    
    st.markdown(f"""
    <div style="background-color:#F9FAFB; padding:15px; border-radius:8px; border:1px solid #E5E7EB; margin-bottom:25px;">
        <h4>🏫 Wissenschaftlicher Kontext</h4>
        Dieses interaktive System und die zugrundeliegende Erfassung wurden im Rahmen des 
        <strong>Masterstudiengangs {STUDIENGANG}</strong> ({SEMESTER}) an der <strong>{UNI_NAME}</strong> erarbeitet.<br><br>
        <strong>Interprofessioneller Ansatz:</strong><br>
        Die Erhebung ist in das Projekt <strong>"{PROJEKTTITEL}"</strong> eingebettet, 
        das aufzeigt, wie die verschiedenen Sektoren der Gesundheits- und Soziallandschaft (Ärzte, Zahnärzte, Heilmittelerbringer, Pflege- und Beratungsstrukturen) 
        integriert zusammenwirken können, um eine lückenlose Versorgung zu gewährleisten.<br><br>
        <em>Autorinnen: {AUTORINNEN}</em>
    </div>
    """, unsafe_allowed_html=True)
    
    st.markdown("""
    Dieses interaktive System basiert auf dem offiziellen **Recherchemanual und methodischen Regelbuch des Versorgungsatlasses von Stadt und Landkreis Eichstätt**.
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
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Stadt und Landkreis Eichstätt | Erstellt für ein wissenschaftliches Poster | © 2026 Open Science Project</div>", unsafe_allowed_html=True)
