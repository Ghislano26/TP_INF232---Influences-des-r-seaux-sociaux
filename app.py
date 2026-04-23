import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration
st.set_page_config(page_title="Mobilité Urbaine Yaoundé", layout="wide")

# Fichier de stockage
DATA_FILE = "transport_yaounde.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Quartier_Origine", "Quartier_Destination", "Mode_Transport", "Duree_Min", "Prix_CFA", "Heure_Depart"])

# --- INTERFACE ---
st.title("🚗 Analyse de la Mobilité Urbaine à Yaoundé")
st.markdown("""
Cette application collecte des données sur les déplacements des citoyens à Yaoundé pour optimiser la compréhension du transport urbain.
*Module INF 232 - Analyse de données.*
""")

# --- SECTION 1 : COLLECTE (Sidebar) ---
st.sidebar.header("📍 Enregistrer un trajet")
with st.sidebar.form("transport_form", clear_on_submit=True):
    origine = st.text_input("Quartier d'origine (ex: Bastos, Mvan)")
    destination = st.text_input("Quartier de destination (ex: Poste Centrale)")
    
    mode = st.selectbox("Mode de transport", 
                        ["Taxi (Ramassage)", "Taxi (Course)", "Moto-Taxi", "Yango/Uber", "Bus Stecy", "Véhicule Personnel"])
    
    duree = st.number_input("Durée du trajet (en minutes)", min_value=1, max_value=300, value=30)
    prix = st.number_input("Coût du trajet (CFA)", min_value=0, step=50, value=250)
    
    heure = st.select_slider("Heure de départ", 
                             options=["Matin (5h-9h)", "Midi (10h-14h)", "Soir (15h-19h)", "Nuit (20h-00h)"])
    
    submit = st.form_submit_button("Enregistrer le trajet")

if submit:
    if origine and destination:
        new_entry = pd.DataFrame([[origine, destination, mode, duree, prix, heure]], 
                                columns=["Quartier_Origine", "Quartier_Destination", "Mode_Transport", "Duree_Min", "Prix_CFA", "Heure_Depart"])
        
        if os.path.exists(DATA_FILE):
            df_existing = pd.read_csv(DATA_FILE)
            df_updated = pd.concat([df_existing, new_entry], ignore_index=True)
        else:
            df_updated = new_entry
            
        df_updated.to_csv(DATA_FILE, index=False)
        st.sidebar.success("Trajet enregistré !")
    else:
        st.sidebar.error("Veuillez remplir les quartiers.")

# --- SECTION 2 : ANALYSE DESCRIPTIVE ---
df = load_data()

if not df.empty:
    st.header("📊 Tableau de bord des déplacements")
    
    # Métriques
    c1, c2, c3 = st.columns(3)
    c1.metric("Total trajets", len(df))
    c2.metric("Prix Moyen", f"{round(df['Prix_CFA'].mean(), 0)} CFA")
    c3.metric("Temps Moyen", f"{round(df['Duree_Min'].mean(), 0)} min")

    col_left, col_right = st.columns(2)

    with col_left:
        # Graphique 1 : Répartition des modes de transport
        fig_pie = px.pie(df, names='Mode_Transport', title="Modes de transport les plus utilisés",
                         hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # Graphique 2 : Prix vs Durée par mode
        fig_scatter = px.scatter(df, x="Duree_Min", y="Prix_CFA", color="Mode_Transport",
                                 title="Relation Prix / Durée du trajet",
                                 labels={"Duree_Min": "Durée (min)", "Prix_CFA": "Prix (FCFA)"})
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Analyse par heure
    st.subheader("Occupation par tranche horaire")
    fig_bar = px.bar(df, x="Heure_Depart", title="Nombre de déplacements par moment de la journée",
                     color_discrete_sequence=['#FFA500'])
    st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("Consulter la base de données brute"):
        st.write(df)
else:
    st.info("En attente de données... Remplissez le formulaire à gauche pour générer les graphiques.")