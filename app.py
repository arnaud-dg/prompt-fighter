import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
import uuid
import datetime
import os
import json
import boto3
from contenu_promptfight import Theorie_1, Enonce_1, Theorie_2, Enonce_2, Theorie_3, Enonce_3
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Atelier Prompting",
    layout="wide"      # 👈 clé pour élargir la fenêtre
)

# Configuration des clés API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
S3_PATH = os.getenv("S3_PATH")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

client = OpenAI(api_key=OPENAI_API_KEY)

# Chargement logo et sidebar
logo = Image.open("assets/logo_disc.png")
with st.sidebar:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(logo, width=300)
st.sidebar.markdown("---")

# Saisie pseudo et modèle
pseudo = st.sidebar.text_input("Renseignez votre pseudo")
st.sidebar.markdown("---")

# Réglages des paramètres
modele = st.sidebar.selectbox("Choix du modèle LLM", ["Mistral", "OpenAI"])
temperature = st.sidebar.slider("Température", 0.0, 1.0, 0.7, step=0.1, help="Contrôle la créativité : plus elle est haute, plus les réponses sont variées.")
max_tokens = st.sidebar.slider("Max tokens", 10, 1024, 600, step=10, help="Définit la longueur maximale de la réponse générée.")
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 1.0, step=0.1, help="Limite la diversité : plus c'est bas, plus les réponses sont concentrées sur les options les plus probables.")

# Session unique pour différencier les logs
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Fonction d'appel LLM
def call_llm(prompt, model):
    if model == "OpenAI":
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )
        return response.choices[0].message.content.strip()

    elif model == "Mistral":
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "mistral-medium-latest",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        r = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)
        try:
            result = r.json()
            if "choices" in result:
                return result["choices"][0]["message"]["content"].strip()
            else:
                st.error(f"Erreur API Mistral : {result}")
                return "Erreur lors de l'appel à l'API Mistral (voir détails ci-dessus)"
        except Exception as e:
            st.error(f"Réponse invalide de l'API Mistral : {r.text}")
            return f"Exception: {e}"

def log_interaction(pseudo, exercice, prompt, response, model):
    timestamp = datetime.datetime.utcnow().isoformat().replace(":", "-")
    safe_exercice = exercice.replace(" ", "_")
    filename = f"log_{st.session_state.session_id}_{safe_exercice}_{timestamp}.json"

    log_data = {
        "timestamp": timestamp,
        "jour": datetime.datetime.now().strftime("%d/%m/%Y"),
        "session_id": st.session_state.session_id,
        "pseudo": pseudo,
        "exercice": exercice,
        "modele": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "prompt": prompt,
        "reponse": response
    }

    with open(filename, "w") as f:
        json.dump(log_data, f)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    s3.upload_file(Filename=filename, Bucket=BUCKET_NAME, Key=filename)
    os.remove(filename)

# Création des onglets d'exercice
tab1, tab2, tab3 = st.tabs(["Partie 1", "Partie 2", "Partie 3"])

#############################################################################
#############################      Partie 1     #############################
#############################################################################

with tab1:
    st.subheader(f"Partie 1 – Les bases du prompting")

    st.markdown("""🎯 Objectif pédagogique  
    Comprendre ce qui fait un bon prompt : clarté, contextualisation, spécificité.""")
    
    prompt_key = "prompt_1"
    response_key = "response_1"
    reset_key = "reset_1"

    # Initialisation
    if prompt_key not in st.session_state:
        st.session_state[prompt_key] = ""
    if response_key not in st.session_state:
        st.session_state[response_key] = ""
    if reset_key not in st.session_state:
        st.session_state[reset_key] = False

    # Si reset demandé
    if st.session_state[reset_key]:
        st.session_state[prompt_key] = ""
        st.session_state[response_key] = ""
        st.session_state[reset_key] = False
        st.rerun()

    # Contenu texte
    with st.expander("📚 Quelques rappels théoriques", expanded=False):
        st.markdown(Theorie_1, unsafe_allow_html=True)

    with st.container():
        st.markdown(Enonce_1, unsafe_allow_html=True)

    # Zone de saisie
    prompt = st.text_area("Pose ta question à l'IA", value=st.session_state[prompt_key], key=prompt_key)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Envoyer", key="btn_send_1"):
            if not pseudo:
                st.warning("Merci de renseigner un pseudo dans la barre latérale.")
            elif not prompt.strip():
                st.warning("Merci d'écrire une question.")
            else:
                with st.spinner("L'IA réfléchit..."):
                    reponse = call_llm(prompt, modele)
                    st.session_state[response_key] = reponse
                    log_interaction(pseudo, "Exercice 1", prompt, reponse, modele)

    with col2:
        if st.button("Réinitialiser", key="btn_reset_1"):
            st.session_state[reset_key] = True
            st.rerun()

    # Affichage réponse
    if st.session_state[response_key]:
        st.markdown("### Réponse de l'IA")
        st.markdown(
            f'<div style="background-color:#e6ffe6;padding:10px;border-radius:5px;">{st.session_state[response_key]}</div>',
            unsafe_allow_html=True
        )

#############################################################################
#############################      Partie 2     #############################
#############################################################################

with tab2:
    st.subheader(f"Partie 2 – Les formats de sortie")

    st.markdown("""🎯 Objectif pédagogique  
    Apprendre à structurer ses demandes pour obtenir des formats de réponse adaptés aux besoins professionnels.""")
    
    prompt_key = "prompt_2"
    response_key = "response_2"
    reset_key = "reset_2"

    # Initialisation
    if prompt_key not in st.session_state:
        st.session_state[prompt_key] = ""
    if response_key not in st.session_state:
        st.session_state[response_key] = ""
    if reset_key not in st.session_state:
        st.session_state[reset_key] = False

    # Si reset demandé
    if st.session_state[reset_key]:
        st.session_state[prompt_key] = ""
        st.session_state[response_key] = ""
        st.session_state[reset_key] = False
        st.rerun()

    # Contenu texte
    with st.expander("📚 Quelques rappels théoriques", expanded=False):
        st.markdown(Theorie_2, unsafe_allow_html=True)

    with st.container():
        st.markdown(Enonce_2, unsafe_allow_html=True)

    # Aide rapide avec exemples de formats
    with st.expander("💡 Exemples de prompts avec formats", expanded=False):
        st.markdown("""
        **Format Email :**  
        *"Présente le lancement de ZenFlow sous forme d'email interne avec objet, contexte, détails du produit et prochaines étapes pour l'équipe"*
        
        **Format Post LinkedIn :**  
        *"Rédige un post LinkedIn pour annoncer ZenFlow avec une accroche engageante, 3 bénéfices clés, un appel à l'action et des hashtags pertinents"*
        
        **Format Tableau :**  
        *"Crée une fiche produit pour ZenFlow sous forme de tableau avec colonnes : Fonctionnalité | Bénéfice | Public cible"*
        """)

    # Zone de saisie
    prompt = st.text_area("Testez différents formats de sortie", value=st.session_state[prompt_key], key=prompt_key, height=100)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Envoyer", key="btn_send_2"):
            if not pseudo:
                st.warning("Merci de renseigner un pseudo dans la barre latérale.")
            elif not prompt.strip():
                st.warning("Merci d'écrire une question.")
            else:
                with st.spinner("L'IA réfléchit..."):
                    reponse = call_llm(prompt, modele)
                    st.session_state[response_key] = reponse
                    log_interaction(pseudo, "Exercice 2", prompt, reponse, modele)

    with col2:
        if st.button("Réinitialiser", key="btn_reset_2"):
            st.session_state[reset_key] = True
            st.rerun()

    # Affichage réponse
    if st.session_state[response_key]:
        st.markdown("### Réponse de l'IA")
        st.markdown(
            f'<div style="background-color:#e6f3ff;padding:10px;border-radius:5px;">{st.session_state[response_key]}</div>',
            unsafe_allow_html=True
        )

#############################################################################
#############################      Partie 3     #############################
#############################################################################

with tab3:
    st.subheader(f"Partie 3 – Le Few-Shot Prompting")

    st.markdown("""🎯 Objectif pédagogique  
    Maîtriser l'art de donner des exemples pour obtenir des réponses cohérentes et dans le format souhaité.""")
    
    prompt_key = "prompt_3"
    response_key = "response_3"
    reset_key = "reset_3"

    # Initialisation
    if prompt_key not in st.session_state:
        st.session_state[prompt_key] = ""
    if response_key not in st.session_state:
        st.session_state[response_key] = ""
    if reset_key not in st.session_state:
        st.session_state[reset_key] = False

    # Si reset demandé
    if st.session_state[reset_key]:
        st.session_state[prompt_key] = ""
        st.session_state[response_key] = ""
        st.session_state[reset_key] = False
        st.rerun()

    # Contenu texte
    with st.expander("📚 Quelques rappels théoriques", expanded=False):
        st.markdown(Theorie_3, unsafe_allow_html=True)

    with st.container():
        st.markdown(Enonce_3, unsafe_allow_html=True)

    # Aide rapide avec template Few-Shot
    with st.expander("💡 Template Few-Shot à utiliser", expanded=False):
        st.markdown("""
        **Structure recommandée :**
        ```
        Écris un post dans le style décontracté de TechFlow (startup tech avec humour et références pop culture).

        Exemples :

        Sujet : Lancement nouvelle feature
        Post : "Plot twist ! 🎬 Notre nouvelle fonction 'AutoMagic' débarque demain et elle va révolutionner votre workflow comme Thanos a révolutionné l'univers Marvel (mais en mieux, promis) ✨ #TechLife #Innovation"

        Sujet : Bug résolu  
        Post : "Bug de ce matin = officiellement éliminé ! 🐛💥 Notre équipe de ninjas-développeurs a frappé plus vite que l'éclair ⚡ Merci pour votre patience, vous êtes les meilleurs ! ❤️ #TeamWork #FixItFast"

        Maintenant, écris pour le sujet : [VOTRE SUJET]
        ```
        """)

    # Suggestions de sujets à tester
    st.markdown("**💡 Sujets suggérés à tester :**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Recrutement stagiaire", key="sujet1"):
            st.session_state[prompt_key] = """Écris un post dans le style décontracté de TechFlow (startup tech avec humour et références pop culture).

Exemples :

Sujet : Lancement nouvelle feature
Post : "Plot twist ! 🎬 Notre nouvelle fonction 'AutoMagic' débarque demain et elle va révolutionner votre workflow comme Thanos a révolutionné l'univers Marvel (mais en mieux, promis) ✨ #TechLife #Innovation"

Sujet : Bug résolu  
Post : "Bug de ce matin = officiellement éliminé ! 🐛💥 Notre équipe de ninjas-développeurs a frappé plus vite que l'éclair ⚡ Merci pour votre patience, vous êtes les meilleurs ! ❤️ #TeamWork #FixItFast"

Maintenant, écris pour le sujet : Recrutement d'un stagiaire développeur"""

    with col2:
        if st.button("🔧 Maintenance serveur", key="sujet2"):
            st.session_state[prompt_key] = """Écris un post dans le style décontracté de TechFlow (startup tech avec humour et références pop culture).

Exemples :

Sujet : Lancement nouvelle feature
Post : "Plot twist ! 🎬 Notre nouvelle fonction 'AutoMagic' débarque demain et elle va révolutionner votre workflow comme Thanos a révolutionné l'univers Marvel (mais en mieux, promis) ✨ #TechLife #Innovation"

Sujet : Bug résolu  
Post : "Bug de ce matin = officiellement éliminé ! 🐛💥 Notre équipe de ninjas-développeurs a frappé plus vite que l'éclair ⚡ Merci pour votre patience, vous êtes les meilleurs ! ❤️ #TeamWork #FixItFast"

Maintenant, écris pour le sujet : Maintenance serveur prévue ce weekend"""

    with col3:
        if st.button("🤝 Nouveau partenariat", key="sujet3"):
            st.session_state[prompt_key] = """Écris un post dans le style décontracté de TechFlow (startup tech avec humeur et références pop culture).

Exemples :

Sujet : Lancement nouvelle feature
Post : "Plot twist ! 🎬 Notre nouvelle fonction 'AutoMagic' débarque demain et elle va révolutionner votre workflow comme Thanos a révolutionné l'univers Marvel (mais en mieux, promis) ✨ #TechLife #Innovation"

Sujet : Bug résolu  
Post : "Bug de ce matin = officiellement éliminé ! 🐛💥 Notre équipe de ninjas-développeurs a frappé plus vite que l'éclair ⚡ Merci pour votre patience, vous êtes les meilleurs ! ❤️ #TeamWork #FixItFast"

Maintenant, écris pour le sujet : Partenariat avec une startup de design"""

    # Zone de saisie
    prompt = st.text_area("Testez vos prompts Few-Shot", value=st.session_state[prompt_key], key=prompt_key, height=150)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Envoyer", key="btn_send_3"):
            if not pseudo:
                st.warning("Merci de renseigner un pseudo dans la barre latérale.")
            elif not prompt.strip():
                st.warning("Merci d'écrire une question.")
            else:
                with st.spinner("L'IA réfléchit..."):
                    reponse = call_llm(prompt, modele)
                    st.session_state[response_key] = reponse
                    log_interaction(pseudo, "Exercice 3", prompt, reponse, modele)

    with col2:
        if st.button("Réinitialiser", key="btn_reset_3"):
            st.session_state[reset_key] = True
            st.rerun()

    # Affichage réponse
    if st.session_state[response_key]:
        st.markdown("### Réponse de l'IA")
        st.markdown(
            f'<div style="background-color:#fff3e6;padding:10px;border-radius:5px;">{st.session_state[response_key]}</div>',
            unsafe_allow_html=True
        )


# Un opérateur 31 ans travaille sur machine de cryobroyage de plantes dans un laboratoire pharmaceutique. Il se trouve face à un dysfonctionnement de la machine. La vis sans fin de la cuve de précongélation est bloquée par un corps étranger dans le conduit d'évacuation. L'opérateur procède alors à l'ouverture des couvercles de la cuve ce qui provoqua l'arrêt du système d'entraînement et l'arrêt de l'injection d'azote liquide. Quelques heures plus tard, son corps a été découvert inanimé dans la cuve, les jambes et le bassin ainsi que les mains et les avant-bras gelés. Il paraît vraisemblable que l’opérateur a subi un choc thermique important et suffoqué en respirant un air glacé nettement inférieur à zéro degré et où la proportion d'oxygène issu de l'air ambiant était incertaine.

# La victime, un chercheur intérimaire de 40 ans, effectuait une mission d'animalier dans une société pharmaceutique et a été victime d'une détresse respiratoire aiguë et d'un arrêt cardiaque. Elle est décédée à l'hôpital 13 jours plus tard sans avoir repris connaissance.

# Un agent de conditionnement intérimaire de 52 ans travaille dans un laboratoire pharmaceutique. Il s'est rendu aux toilettes car il ne se sentait pas bien. Ne le voyant pas revenir, un collègue est allé le chercher. L'intérimaire avait perdu connaissance. Il avait déjà fait un malaise le matin en arrivant au travail. Il est mort en fin de matinée.