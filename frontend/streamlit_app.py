import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuração da página para visual premium
st.set_page_config(
    page_title="ShopeeAds Manager | Dashboard",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System e Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8f9fa;
    }
    
    /* Estilização dos Cards de Métrica */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ff4b2b;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;
    }

    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3);
        transform: translateY(-1px);
    }

    /* Estilização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# Lógica de URL da API
API_URL = os.getenv("API_URL", "http://backend:8000")
if API_URL and not API_URL.startswith("http"):
    API_URL = f"https://{API_URL}"

# --- Funções de Dados ---
def get_mock_data():
    dates = [datetime.now() - timedelta(days=x) for x in range(7)]
    data = {
        "Data": dates[::-1],
        "Vendas": [1200, 1500, 1100, 1800, 2200, 2100, 2500],
        "Pedidos": [12, 15, 11, 18, 22, 21, 25]
    }
    return pd.DataFrame(data)

# --- Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Shopee-logo.svg/2560px-Shopee-logo.svg.png", width=120)
    st.title("Manager")
    st.markdown("---")
    page = st.sidebar.radio("Navegação", ["📈 Dashboard", "🔗 Integrações", "⚙️ Configurações"])
    
    st.markdown("---")
    st.markdown("### Status do Sistema")
    try:
        res = requests.get(f"{API_URL}/health", timeout=2)
        if res.status_code == 200:
            st.success("API Online")
        else:
            st.error("API com Erro")
    except:
        st.warning("Conectando à API...")

# --- Dashboard Principal ---
if page == "📈 Dashboard":
    st.title("📈 Resumo de Performance")
    
    # KPIs Superiores
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Receita Total (Mês)", "R$ 12.450", "+12%")
    with col2:
        st.metric("Pedidos Totais", "124", "+5%")
    with col3:
        st.metric("Comissão Estimada", "R$ 1.867", "+8%")
    with col4:
        st.metric("Conversão", "3.2%", "-0.5%")

    st.markdown("---")
    
    # Gráficos de Tendência
    df = get_mock_data()
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📊 Tendência de Vendas (7 dias)")
        fig = px.area(df, x="Data", y="Vendas", line_shape="spline", 
                      color_discrete_sequence=['#ff4b2b'])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### 🛒 Pedidos por Dia")
        fig2 = px.bar(df, x="Data", y="Pedidos", color_discrete_sequence=['#363636'])
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
        st.plotly_chart(fig2, use_container_width=True)

elif page == "🔗 Integrações":
    st.header("🔗 Conectar Marketplace")
    st.info("Conecte sua conta de afiliado para automatizar a coleta de dados.")
    
    card_col = st.columns(3)[0]
    with card_col:
        st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #eee; text-align: center;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Shopee-logo.svg/2560px-Shopee-logo.svg.png" width="100">
                <h4>Shopee Affiliate</h4>
                <p style="color: #666; font-size: 0.9rem;">Sincronize pedidos, cliques e comissões automaticamente.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Conectar Shopee", use_container_width=True):
            try:
                res = requests.get(f"{API_URL}/api/auth/login")
                if res.status_code == 200:
                    auth_url = res.json().get("url")
                    st.link_button("Ir para Autenticação", auth_url)
                else:
                    st.error("Erro ao gerar link de conexão.")
            except:
                st.error("Serviço de autenticação indisponível.")

elif page == "⚙️ Configurações":
    st.header("⚙️ Configurações da Conta")
    st.text_input("Nome da Loja", value="Minha Loja Afiliada")
    st.text_input("Email para Notificações", value="admin@exemplo.com")
    st.checkbox("Receber relatórios diários por email", value=True)
    st.button("Salvar Configurações")
