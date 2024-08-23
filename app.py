import streamlit as st
import requests
import json

# Configuración de la API key
serper_api_key = st.secrets["SERPER_API_KEY"]

def search_google_scholar(topic, num_quotes):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "q": f"{topic} site:scholar.google.com",
        "num_results": num_quotes
    }
    response = requests.post(url, headers=headers, json=data)
    search_results = response.json()

    citations = []
    for result in search_results.get('organic', []):
        title = result.get('title', 'Título no disponible')
        snippet = result.get('snippet', 'Descripción no disponible')
        link = result.get('link', 'Enlace no disponible')
        citations.append(f"**{title}**\n\n{snippet}\n\n[Enlace al artículo]({link})\n\n")

    return citations

st.title("Citas Académicas desde Google Scholar")

quote_topic = st.text_input("Introduce el tema para buscar citas en Google Scholar:")
num_quotes = st.slider("Número de citas", 1, 5, 3)

if st.button("Buscar Citas", key="search_citations"):
    if quote_topic:
        with st.spinner("Buscando citas..."):
            citations = search_google_scholar(quote_topic, num_quotes)
            if citations:
                for citation in citations:
                    st.markdown(citation)
            else:
                st.warning("No se encontraron citas relevantes. Intenta con otro tema.")
    else:
        st.warning("Por favor, introduce un tema.")
