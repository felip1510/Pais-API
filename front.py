import html
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
REST_COUNTRIES_API_KEY = os.getenv("REST_COUNTRIES_API_KEY")

st.set_page_config(page_title="Explorador de Países", page_icon="🌍", layout="centered")

# ---------- Estilo ----------
st.markdown(
    """
    <style>
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2.5rem; max-width: 780px; }

    /* Cabeçalho */
    .hero { text-align: center; margin-bottom: 1.5rem; }
    .hero .globe { font-size: 3rem; line-height: 1; }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0.4rem 0 0.3rem;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p { opacity: 0.65; margin: 0; font-size: 1.05rem; }

    /* Formulário */
    div[data-testid="stForm"] {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        background: rgba(128, 128, 128, 0.05);
    }
    div[data-testid="stForm"] button {
        border-radius: 12px;
        font-weight: 600;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        color: white;
        border: none;
    }
    div[data-testid="stForm"] button:hover { filter: brightness(1.1); color: white; }

    /* Banner do país */
    .banner {
        margin-top: 1.8rem;
        padding: 2.2rem 1.5rem;
        border-radius: 22px;
        text-align: center;
        color: white;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #06b6d4 100%);
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.35);
    }
    .banner .label {
        font-size: 0.8rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        opacity: 0.8;
    }
    .banner .name {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0.3rem 0 0.7rem;
    }
    .banner .code {
        display: inline-block;
        padding: 0.25rem 1rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.35);
        font-weight: 700;
        letter-spacing: 0.15em;
    }

    /* Cards de informação */
    .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1.2rem;
    }
    .card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.1rem 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        background: rgba(128, 128, 128, 0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12); }
    .card.wide { grid-column: span 2; }
    .icon {
        flex: 0 0 auto;
        width: 3rem;
        height: 3rem;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .c1 { background: rgba(99, 102, 241, 0.18); }
    .c2 { background: rgba(16, 185, 129, 0.18); }
    .c3 { background: rgba(245, 158, 11, 0.20); }
    .c4 { background: rgba(236, 72, 153, 0.18); }
    .c5 { background: rgba(6, 182, 212, 0.20); }
    .card .k {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.6;
    }
    .card .v { font-size: 1.2rem; font-weight: 700; margin-top: 0.1rem; }

    @media (max-width: 600px) {
        .grid { grid-template-columns: 1fr; }
        .card.wide { grid-column: span 1; }
        .banner .name { font-size: 2.1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="globe">🌍</div>
        <h1>Explorador de Países</h1>
        <p>Digite o nome de um país em inglês e descubra tudo sobre ele.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not REST_COUNTRIES_API_KEY:
    st.error("Chave `REST_COUNTRIES_API_KEY` não encontrada. Verifique seu arquivo .env.")
    st.stop()


# ---------- Funções auxiliares ----------
def card(icone, cor, rotulo, valor, wide=False):
    classe = "card wide" if wide else "card"
    return (
        f'<div class="{classe}">'
        f'<div class="icon {cor}">{icone}</div>'
        f'<div><div class="k">{rotulo}</div><div class="v">{html.escape(str(valor))}</div></div>'
        f"</div>"
    )


def formatar_numero(n):
    return f"{n:,}".replace(",", ".")


# ---------- Busca ----------
with st.form("busca_pais"):
    col_input, col_btn = st.columns([4, 1], vertical_alignment="bottom")
    pais_escolhido = col_input.text_input(
        "País (em inglês)", placeholder="Ex: Brazil, Japan, France..."
    )
    buscar = col_btn.form_submit_button("🔎 Buscar", use_container_width=True)

if buscar:
    pais_escolhido = pais_escolhido.strip().lower()

    if not pais_escolhido:
        st.warning("Digite o nome de um país.")
        st.stop()

    url = f"https://api.restcountries.com/countries/v5/names.common/{pais_escolhido}"
    headers = {"Authorization": f"Bearer {REST_COUNTRIES_API_KEY}"}

    try:
        with st.spinner("Buscando..."):
            response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as erro:
        st.error(f"Erro de conexão com a API: {erro}")
        st.stop()

    if response.status_code != 200:
        st.error(f"Não foi possível encontrar o país (status {response.status_code}).")
        st.stop()

    try:
        dados = response.json()
        pais = dados["data"]["objects"][0]
        nome = pais["names"]["common"]
        sigla = pais["codes"]["alpha_2"]
    except (KeyError, IndexError, ValueError):
        st.error("Resposta inesperada da API ou país não encontrado.")
        st.stop()

    capitais = pais.get("capitals") or []
    regiao = pais.get("subregion") or "—"
    linguas = pais.get("languages") or []
    populacao = pais.get("population")
    moedas = pais.get("currencies") or []

    capital_txt = capitais[0]["name"] if capitais else "Não cadastrada"
    linguas_txt = ", ".join(l["name"] for l in linguas) if linguas else "—"
    populacao_txt = formatar_numero(populacao) if isinstance(populacao, int) else "—"
    moedas_txt = (
        ", ".join(f'{m["code"]} ({m.get("symbol", "")})' for m in moedas)
        if moedas
        else "—"
    )

    # ---------- Resultado ----------
    st.markdown(
        f"""
        <div class="banner">
            <div class="label">País</div>
            <div class="name">{html.escape(nome)}</div>
            <span class="code">{html.escape(sigla)}</span>
        </div>
        <div class="grid">
            {card("🏛️", "c1", "Capital", capital_txt)}
            {card("🗺️", "c2", "Região", regiao)}
            {card("👥", "c3", "População", populacao_txt)}
            {card("💰", "c4", "Moeda local", moedas_txt)}
            {card("🗣️", "c5", "Línguas", linguas_txt, wide=True)}
        </div>
        """,
        unsafe_allow_html=True,
    )