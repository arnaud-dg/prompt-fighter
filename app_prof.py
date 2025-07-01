import streamlit as st
import boto3
import os
import datetime
import json
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
# from annotated_text import annotated_text
from openai import OpenAI

load_dotenv()

# Configuration AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(
    page_title="Dashboard Prof",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo dans la sidebar
logo = Image.open("assets/logo_disc_prof.png")
with st.sidebar:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(logo, width=250)

st.sidebar.markdown("---")

# Filtres : date et exercice
date_filter = st.sidebar.text_input("🗕️ Date du jour", datetime.datetime.now().strftime("%d/%m/%Y"))
exercice_filter = st.sidebar.selectbox("🎯 Choix de l'exercice", ["Exercice 1", "Exercice 2", "Exercice 3"])

st.sidebar.markdown("---")

# Tabs pour affichage par partie
tab1, tab2, tab3, tab4 = st.tabs(["Partie 1", "Partie 2", "Partie 3", "Analyse contexte vs tâche"])

# Fonction pour parser les fichiers logs S3
def get_logs_for_exercice(exercice, date):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    data = []
    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            if key.endswith(".json") and exercice.replace(" ", "_") in key:
                obj_data = s3.get_object(Bucket=BUCKET_NAME, Key=key)
                content = obj_data["Body"].read().decode("utf-8")
                parsed = json.loads(content)
                if parsed.get("jour") == date:
                    data.append(parsed)
    return data

# Fonction d'appel à l'API OpenAI pour extraction contexte / tâche
def call_llm(prompt_text):
    system_msg = "Tu es un expert en analyse de prompt. À partir d'un prompt utilisateur, identifie les parties de la phrase correspondant au CONTEXTE (le cadre ou la situation) et à la TÂCHE (ce que l’on attend de l’IA). Retourne ta réponse sous la forme d’une liste JSON avec les champs 'type' (valeurs possibles : 'contexte', 'tâche') et 'text'."
    user_msg = f"Prompt : {prompt_text}"
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )
    return completion.choices[0].message.content

# Fonction d'affichage dans chaque onglet
def afficher_resultats(tab, exercice):
    with tab:
        st.subheader(exercice)
        if st.button(f"📊 Visualiser les réponses", key=f"btn_{exercice}"):
            logs = get_logs_for_exercice(exercice, date_filter)
            if logs:
                df = pd.DataFrame(logs)

                df_display = df.drop(columns=["timestamp", "jour", "session_id", "exercice"], errors='ignore')

                st.data_editor(df_display, use_container_width=True, num_rows="dynamic")

                st.markdown("---")
                st.markdown("## 📄 Prompts détaillés permettant de lire l'entiereté des échanges")

                detail_df = df[["prompt", "reponse"]].copy()
                detail_df.columns = ["📝 Prompt", "💬 Réponse"]

                detail_rows = ""
                for _, row in detail_df.iterrows():
                    prompt_html = f"<td style='vertical-align:top; white-space:pre-wrap;'>{row['📝 Prompt']}</td>"
                    response_html = f"<td style='vertical-align:top; white-space:pre-wrap;'>{row['💬 Réponse']}</td>"
                    detail_rows += f"<tr>{prompt_html}{response_html}</tr>"

                st.markdown(f"""
                <table style='width:100%; border-collapse: collapse;'>
                  <thead>
                    <tr>
                      <th style='text-align:left; border-bottom: 2px solid #ccc;'>📝 Prompt</th>
                      <th style='text-align:left; border-bottom: 2px solid #ccc;'>💬 Réponse</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detail_rows}
                  </tbody>
                </table>
                """, unsafe_allow_html=True)
            else:
                st.info("Aucune donnée trouvée pour les filtres sélectionnés.")

# Affichage dans les 3 tabs classiques
afficher_resultats(tab1, "Exercice 1")
afficher_resultats(tab2, "Exercice 2")
afficher_resultats(tab3, "Exercice 3")