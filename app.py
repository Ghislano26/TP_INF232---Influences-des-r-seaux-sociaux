import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration de la page
st.set_page_config(page_title="Collecte de Données Académiques", layout="wide")

# Fichier de stockage des données
DATA_FILE = "data_etudiants.csv"

# Fonction pour charger les données
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Nom", "Heures_Etude", "Heures_Sommeil", "Presence_Cours", "Social_Media", "GPA"])

# Titre de l'application
st.title("📊 Collecte & Analyse de la Performance Académique")
st.markdown("""
Cette application collecte des données sur les habitudes des étudiants pour analyser leur impact sur la réussite scolaire.
*Réalisé pour le cours INF 232.*
""")

# --- SECTION 1 : COLLECTE DES DONNÉES ---
st.sidebar.header("📝 Formulaire de Saisie")
with st.sidebar.form("survey_form", clear_on_submit=True):
    nom = st.text_input("Nom ou ID Étudiant")
    etude = st.slider("Heures d'étude / jour", 0, 15, 5)
    sommeil = st.slider("Heures de sommeil / nuit", 3, 12, 7)
    presence = st.number_input("Taux de présence (%)", 0, 100, 80)
    reseaux = st.slider("Temps Réseaux Sociaux (h/jour)", 0, 10, 2)
    note = st.number_input("Moyenne Académique (GPA / 20)", 0.0, 20.0, 12.0)
    
    submit = st.form_submit_button("Enregistrer les données")

if submit:
    new_data = pd.DataFrame([[nom, etude, sommeil, presence, reseaux, note]], 
                            columns=["Nom", "Heures_Etude", "Heures_Sommeil", "Presence_Cours", "Social_Media", "GPA"])
    
    # Sauvegarde
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success("Données enregistrées avec succès !")

# --- SECTION 2 : ANALYSE DESCRIPTIVE ---
df = load_data()

if not df.empty:
    st.header("📈 Analyse Descriptive des Données")
    
    # Métriques clés
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de répondants", len(df))
    col2.metric("Moyenne GPA", round(df["GPA"].mean(), 2))
    col3.metric("Moyenne Étude (h)", round(df["Heures_Etude"].mean(), 1))

    # Visualisations
    tab1, tab2 = st.tabs(["Distributions", "Corrélations"])
    
    with tab1:
        fig_hist = px.histogram(df, x="GPA", title="Distribution des Notes", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with tab2:
        fig_scatter = px.scatter(df, x="Heures_Etude", y="GPA", 
                                 size="Social_Media", hover_name="Nom",
                                 title="Lien entre Étude et Performance (Taille = Temps Réseaux Sociaux)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Affichage du tableau de données
    with st.expander("Voir les données brutes"):
        st.dataframe(df)
else:
    st.info("Aucune donnée collectée pour le moment. Utilisez le formulaire à gauche.")

# --- FOOTER ---
st.markdown("---")
st.caption("Application développée pour l'EC2 du module INF 232 - Analyse de données.")