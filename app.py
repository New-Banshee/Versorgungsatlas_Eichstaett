import streamlit as st
import pandas as pd
import plotly.express as px

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
    return pd.read_csv("versorgungsatlas_eichstaett.csv")

try:
    df = load_data()
except Exception as e:
    # Fallback to local path if run locally
    df = pd.read_csv("versorgungsatlas_eichstaett.csv")

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #2563EB;
    }
    </style>
""", unsafe_allowed_html=True)

# SIDEBAR: Context & Info
st.sidebar.image("https://img.icons8.com/clouds/150/hospital-room.png", width=100)
st.sidebar.title("Versorgungsatlas")
st.sidebar.markdown("**Landkreis Eichstätt (Oberbayern)**")

st.sidebar.markdown("""
<div style="background-color:#EFF6FF; padding:12px; border-radius:5px; border-left:4px solid #3B82F6; margin-bottom:15px;">
    <strong>Strukturdaten Landkreis:</strong><br>
    👥 Einwohner: 135.982 (31.12.2025)<br>
    🗺️ Fläche: 1.214 km²<br>
    🏡 Gemeinden: 30
</div>
""", unsafe_allowed_html=True)

st.sidebar.subheader("📥 Downloads & Anfragen")
# CSV Download Button
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📊 Original-Datenbank (CSV) herunterladen",
    data=csv,
    file_name="versorgungsatlas_eichstaett.csv",
    mime="text/csv"
)

# PDF Placeholder info
st.sidebar.markdown("""
---
📄 **Gedruckter Versorgungsatlas (PDF):**  
Den vollständigen Atlas mit allen 30 Detailblättern können Sie über den QR-Code auf unserem Poster herunterladen.

✉️ **Forschungsanfragen / Original Excel:**  
Die voll funktionsfähige Excel-Matrix mit allen Erfassungsstufen ist für wissenschaftliche Zwecke auf Anfrage erhältlich.  
_Kontaktieren Sie den Autor direkt am Poster oder per E-Mail._
""")

# MAIN PAGE
st.markdown('<div class="main-title">Gesundheits- & Versorgungsatlas</div>', unsafe_allowed_html=True)
st.markdown('<div class="subtitle">Interaktives Informationssystem zur medizinischen und pflegerischen Infrastruktur im Landkreis Eichstätt</div>', unsafe_allowed_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Regionalvergleich", "🔍 Gemeinde-Steckbriefe", "📘 Recherchemanual & Methodik"])

with tab1:
    st.header("Regionaler Überblick & Verteilungsanalyse")
    
    # Aggregated stats
    tot_einwohner = df["Einwohner"].sum()
    tot_aerzte = df["Aerztliche_Fachgebietseintraege"].sum()
    tot_psych = df["Psychotherapie"].sum()
    tot_zahnaerzte = df["Zahnaerztliche_Personen"].sum()
    tot_apotheken = df["Oeffentliche_Apotheken"].sum()
    tot_heilmittel = df["Heilmittelpraxen"].sum()
    tot_pflege = df["Pflegeeinrichtungen_Dienste"].sum()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("👥 Einwohner gesamt", f"{tot_einwohner:,}".replace(",", "."))
    col2.metric("🩺 Fachgebietseinträge", tot_aerzte)
    col3.metric("🧠 Psychotherapie", tot_psych)
    col4.metric("🦷 Zahnärztliche Personen", tot_zahnaerzte)
    col5.metric("💊 Apotheken", tot_apotheken)
    col6.metric("🏡 Pflegeeinrichtungen", tot_pflege)
    
    st.markdown("---")
    
    # Selection of indicator for visual comparison
    st.subheader("Verteilungsanalyse nach Infrastrukturmerkmalen")
    
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
        title=f"Verteilung von: {selected_label}",
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
        st.write(f"**Einwohnerzahl:** {g_data['Einwohner']:,} Einwohner".replace(",", "."))
        st.write(f"**Erhebungsstatus:** {g_data['Erhebungsstatus'].capitalize()} ✅")
        
        # Simple table
        st.markdown("#### Infrastruktur-Kennzahlen")
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
                g_data["Aerztliche_Fachgebietseintraege"],
                g_data["Psychotherapie"],
                g_data["Zahnaerztliche_Personen"],
                g_data["Oeffentliche_Apotheken"],
                g_data["Heilmittelpraxen"],
                g_data["Pflegeeinrichtungen_Dienste"],
                g_data["Krankenhaus_Reha_Hospiz"]
            ]
        })
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("### Lokale Versorgungsstruktur im Kontext")
        # Visualizing where this municipality stands compared to average
        avg_einwohner = df["Einwohner"].mean()
        avg_indicator = df[selected_col].mean()
        
        # Let's show a radar-style comparison or horizontal bars
        st.markdown("#### Lokale Abweichung vom Landkreis-Mittelwert")
        
        comparison_data = []
        for label, col in indicator_mapping.items():
            g_val = g_data[col]
            avg_val = df[col].mean()
            pct_of_avg = (g_val / avg_val * 100) if avg_val > 0 else 0
            comparison_data.append({
                "Infrastruktur": label,
                "Lokaler Wert": g_val,
                "Landkreis-Durchschnitt (pro Gemeinde)": round(avg_val, 2),
                "Prozent des Durchschnitts (%)": round(pct_of_avg, 1)
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
    st.header("Wissenschaftliches Recherchemanual & Zählregeln")
    
    st.markdown("""
    Dieses interaktive System basiert auf dem offiziellen **Recherchemanual und methodischen Regelbuch des Versorgungsatlasses des Landkreises Eichstätt**.
    Ein stabiles und logisches Regelwerk sichert die wissenschaftliche Replizierbarkeit und Validität der erhobenen Strukturen.
    """)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Zentrale Zählregeln & Datenquellen")
        st.markdown("""
        *   **Ärztliche Versorgung (Fachgebietseinträge):** Erfasst über die *116117-Arztsuche/KVB*. Mehrfach qualifizierte Ärzte werden in jedem Fachgebiet gezählt, um das tatsächliche Spektrum abzubilden. Praxis- und MVZ-Strukturen selbst werden nicht rekonstruiert.
        *   **Psychotherapie:** Erfasst über die *116117-Arztsuche/KVB*. Psychologische Psychotherapie und Kinder-/Jugendlichenpsychotherapie werden getrennt erhoben.
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
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Kommunaler Gesundheits- und Versorgungsatlas Landkreis Eichstätt | Erstellt für ein wissenschaftliches Poster | © 2026 Open Science Project</div>", unsafe_allowed_html=True)
