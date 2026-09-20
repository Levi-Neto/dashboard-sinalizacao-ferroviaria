import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Sinalização Ferroviária",
    page_icon="🚆",
    layout="wide"
)

# =========================
# ESTILO VISUAL
# =========================

st.markdown("""
<style>

/* Fonte geral */
html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

/* Título principal */
h1 {
    color: #A71930 !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

/* Subtítulos */
h2, h3 {
    color: #5A1A24 !important;
    font-weight: 600 !important;
}

/* Valores dos indicadores */
[data-testid="stMetricValue"] {
    color: #A71930;
    font-weight: 700;
}

/* Linha divisória */
hr {
    border-color: #A71930 !important;
}

/* Pequeno detalhe lateral */
[data-testid="stAppViewContainer"] {
    border-top: 6px solid #A71930;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CARREGAMENTO DOS DADOS
# =========================

df = pd.read_csv("dataset_sinalizacao_ferroviaria.csv")

# =========================
# CABEÇALHO
# =========================

st.title("🚈 Dashboard de Sinalização Ferroviária")

st.write(
    "Análise comparativa entre os sistemas **Bloco Fixo** e **CBTC**."
)

# =========================
# INDICADORES
# =========================

st.subheader("Visão Geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros",
    f"{len(df):,}".replace(",", ".")
)

col2.metric(
    "Trens",
    df["id_trem"].nunique()
)

col3.metric(
    "Blocos",
    df["id_bloco"].nunique()
)

col4.metric(
    "Headway médio",
    f'{df["headway_seg"].mean():.1f} s'
)

st.divider()

# =========================
# GRÁFICO 1
# =========================

st.subheader("Headway por Tipo de Sinalização")

fig_headway = px.box(
    df,
    x="tipo_sinalizacao",
    y="headway_seg",
    color="tipo_sinalizacao",

    color_discrete_map={
        "CBTC": "#A71930",
        "Bloco Fixo": "#D85A6A"
    },

    labels={
        "tipo_sinalizacao": "Tipo de Sinalização",
        "headway_seg": "Headway (segundos)"
    }
)

fig_headway.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

fig_headway.update_xaxes(
    showgrid=False
)

fig_headway.update_yaxes(
    gridcolor="#E5E5E5"
)

st.plotly_chart(
    fig_headway,
    use_container_width=True
)

st.caption(
    "O CBTC apresenta headways menores, permitindo que os trens "
    "operem com intervalos menores entre si."
)
# =========================
# GRÁFICO 2
# =========================

st.divider()

st.subheader("Aspectos dos Sinais por Tipo de Sinalização")

# Contagem dos sinais
contagem_sinais = (
    df.groupby(["tipo_sinalizacao", "aspecto_sinal"])
    .size()
    .reset_index(name="Quantidade")
)

fig_sinais = px.bar(
    contagem_sinais,
    x="tipo_sinalizacao",
    y="Quantidade",
    color="aspecto_sinal",
    barmode="group",

    color_discrete_map={
        "Verde": "#2E8B57",
        "Amarelo": "#E5B700",
        "Vermelho": "#C62828"
    },

    labels={
        "tipo_sinalizacao": "Tipo de Sinalização",
        "aspecto_sinal": "Aspecto do Sinal"
    },

    text="Quantidade"
)

fig_sinais.update_traces(
    textposition="outside"
)

fig_sinais.update_layout(
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend_title_text="Aspecto do Sinal"
)

fig_sinais.update_xaxes(
    showgrid=False
)

fig_sinais.update_yaxes(
    gridcolor="#E5E5E5",
    title="Quantidade de ocorrências"
)

st.plotly_chart(
    fig_sinais,
    use_container_width=True
)

st.caption(
    "O Bloco Fixo apresenta predominância de sinais verdes, enquanto "
    "o CBTC apresenta proporcionalmente mais ocorrências de sinais "
    "amarelos e vermelhos."
)

# =========================
# GRÁFICO 3
# =========================

st.divider()

st.subheader("Velocidade Permitida x Tempo de Ocupação")

fig_velocidade = px.scatter(
    df,
    x="velocidade_permitida_kmh",
    y="tempo_ocupacao_circuito_seg",
    color="tipo_sinalizacao",
    opacity=0.6,

    color_discrete_map={
        "CBTC": "#A71930",
        "Bloco Fixo": "#D85A6A"
    },

    labels={
        "velocidade_permitida_kmh": "Velocidade Permitida (km/h)",
        "tempo_ocupacao_circuito_seg": "Tempo de Ocupação (segundos)",
        "tipo_sinalizacao": "Tipo de Sinalização"
    }
)

fig_velocidade.update_layout(
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend_title_text="Tipo de Sinalização"
)

fig_velocidade.update_xaxes(
    gridcolor="#E5E5E5"
)

fig_velocidade.update_yaxes(
    gridcolor="#E5E5E5"
)

st.plotly_chart(
    fig_velocidade,
    use_container_width=True
)

st.caption(
    "O gráfico permite observar a relação entre a velocidade autorizada "
    "e o tempo que o trem permanece ocupando o circuito ferroviário."
)