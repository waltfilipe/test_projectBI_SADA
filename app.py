import streamlit as st
import plotly.graph_objects as go

# ──────────────────────────────────────────��───────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Scout Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# COLOR SYSTEM
# ──────────────────────────────────────────────────────────────────────────────
BG = "#071423"
DARK = "#04101D"
CARD = "#001A33"
CARD_2 = "#001529"
BORDER = "#174067"
CYAN = "#7EC8FF"
TEXT = "#EAF2FF"
MUTED = "#8FA7BF"
YELLOW = "#E7C53D"
YELLOW_2 = "#FFD44D"
GREEN = "#31E981"
RED = "#FE4A49"
LIGHT_PANEL = "#A8BCCB"

# ──────────────────────────────────────────────────────────────────────────────
# DATA (baseado na imagem enviada)
# ──────────────────────────────────────────────────────────────────────────────
PLAYER = {
    "name": "Adriano Martins",
    "position": "Zagueiro",
    "club": "Atlético GO",
    "year": 1998,
    "nat": "Brazil",
    "height": 193,
    "foot": "Destro",
    "minutes": 1955,
    "goals": 2,
    "assists": 0,

    # Perfil
    "profile": "Híbrido",
    "p_comb": 21,
    "p_cons": 41,
    "p_posi": 39,

    # Ratings
    "rtg": 6.4,
    "rnk": 52,
    "comb": 5.8,
    "r_comb": 71,
    "cons": 6.9,
    "r_cons": 39,
    "posi": 6.8,
    "r_posi": 48,

    # Aspectos
    "def_asp": [("Confrontos", "X"), ("Duelos Aéreos", "-"), ("Intervenções", "G")],
    "off_asp": [("Ball Security", "G"), ("Progressão", "S")],
    "con_asp": [("Passes Verticais", "-"), ("PCF*", "G"), ("Passes Longos", "X")],

    # Métricas
    "bars": [
        ("Construção", 43, "#FED766"),
        ("Ofensividade", 77, "#31E981"),
        ("1vs1 Defensivo", 5, "#FE4A49"),
        ("Contenção", 78, "#31E981"),
        ("Duelo Aéreo", 14, "#FE4A49"),
    ],
}

# ──────────────────────────────────────────────────────────��───────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(1200px 500px at -10% -10%, #0e2a45 0%, {BG} 55%),
            radial-gradient(800px 300px at 110% 120%, #0a2238 0%, {BG} 65%);
        color: {TEXT};
    }}

    section[data-testid="stSidebar"] {{
        background: {DARK};
        border-right: 1px solid rgba(126,200,255,0.18);
    }}

    .block-container {{
        padding-top: 0.6rem !important;
        padding-bottom: 1rem !important;
        max-width: 100%;
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    .card {{
        background: linear-gradient(180deg, {CARD} 0%, {CARD_2} 100%);
        border: 1px solid rgba(80,120,170,0.35);
        border-radius: 14px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def section_title(label: str) -> str:
    return (
        f'<div style="font-size:0.60rem;font-weight:700;letter-spacing:0.16em;'
        f'text-transform:uppercase;color:{CYAN};padding-bottom:0.2rem;'
        f'border-bottom:1px solid rgba(126,200,255,0.28);margin-bottom:0.45rem;">{label}</div>'
    )

def icon_html(k: str) -> str:
    if k == "X":
        return f'<span style="color:{RED};font-weight:900;font-size:0.88rem;">X</span>'
    if k == "G":
        return '<span style="font-size:0.95rem;">🥇</span>'
    if k == "S":
        return '<span style="font-size:0.95rem;">🥈</span>'
    return f'<span style="color:{MUTED};font-size:0.9rem;">-</span>'

def aspect_block(title: str, items):
    html = section_title(title)
    for item, status in items:
        html += (
            f'<div style="display:flex;align-items:center;gap:0.4rem;padding:0.22rem 0;'
            f'font-size:0.78rem;color:{TEXT};border-bottom:1px solid rgba(23,64,103,0.45);">'
            f'{icon_html(status)}<span>{item}</span></div>'
        )
    return html

def rating_color(v):
    v = float(v)
    if v <= 5:
        return "#A33A3A"
    if v <= 7:
        return "#D09B2E"
    if v <= 8:
        return "#4BAF67"
    return "#2D7EA8"

def rating_pill(label, value, rank):
    col = rating_color(value)
    return (
        f'<div style="background:{DARK};border:1px solid {BORDER};border-radius:9px;'
        f'padding:0.45rem 0.62rem;margin-bottom:0.35rem;">'
        f'<div style="font-size:0.54rem;font-weight:700;letter-spacing:0.11em;'
        f'text-transform:uppercase;color:{MUTED};">{label}</div>'
        f'<div style="display:flex;align-items:center;gap:0.45rem;margin-top:0.1rem;">'
        f'<div style="background:{col};color:#fff;border-radius:6px;padding:0.04rem 0.52rem;'
        f'font-size:1.15rem;font-weight:800;min-width:48px;text-align:center;">{value}</div>'
        f'<div style="font-size:0.78rem;font-weight:700;color:{MUTED};">#{rank}</div>'
        f'</div></div>'
    )

def metric_bar(label, value, color):
    pct = max(0, min(100, int(value)))
    return (
        f'<div style="margin-bottom:0.58rem;">'
        f'<div style="font-size:0.70rem;color:{MUTED};font-weight:600;margin-bottom:0.1rem;">{label}</div>'
        f'<div style="display:flex;align-items:center;gap:0.4rem;">'
        f'<div style="flex:1;height:8px;background:{DARK};border:1px solid rgba(23,64,103,0.6);'
        f'border-radius:4px;overflow:hidden;">'
        f'<div style="height:100%;width:{pct}%;background:{color};"></div></div>'
        f'<div style="font-size:0.72rem;font-weight:800;color:#fff;min-width:22px;text-align:right;">{value}</div>'
        f'</div></div>'
    )

# ──────────────────────────────────────────────────────────────────────────────
# RADAR (clean/elegante inspirado na imagem)
# ──────────────────────────────────────────────────────────────────────────────
def build_profile_radar(p):
    cats = ["Combativo", "Construtor", "Posicional"]
    vals = [p["p_comb"], p["p_cons"], p["p_posi"]]

    fig = go.Figure()

    # anéis triangulares
    for lv in [33, 66, 100]:
        fig.add_trace(go.Scatterpolar(
            r=[lv, lv, lv, lv],
            theta=[cats[0], cats[1], cats[2], cats[0]],
            mode="lines",
            line=dict(color="rgba(180,190,205,0.30)", width=1),
            hoverinfo="skip",
            showlegend=False
        ))

    # eixos
    for cat in cats:
        fig.add_trace(go.Scatterpolar(
            r=[0, 100],
            theta=[cat, cat],
            mode="lines",
            line=dict(color="rgba(180,190,205,0.35)", width=1),
            hoverinfo="skip",
            showlegend=False
        ))

    # base triangular externa sutil
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100],
        theta=[cats[0], cats[1], cats[2], cats[0]],
        mode="lines",
        fill="toself",
        fillcolor="rgba(170,185,210,0.22)",
        line=dict(color="rgba(120,140,180,0.32)", width=1.2),
        hoverinfo="skip",
        showlegend=False
    ))

    # polígono do atleta
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        mode="lines",
        fill="toself",
        fillcolor="rgba(231,197,61,0.22)",
        line=dict(color="#B9991F", width=2),
        hovertemplate="%{theta}: <b>%{r}%</b><extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(
                tickfont=dict(size=18, color="#EAF2FF", family="Inter"),
                rotation=90,
                direction="clockwise",
                gridcolor="rgba(0,0,0,0)",
                linecolor="rgba(0,0,0,0)",
            ),
        ),
        margin=dict(l=8, r=8, t=4, b=6),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center;padding:0.7rem 0 0.35rem;">
            <div style="font-size:1.85rem;">⚽</div>
            <div style="font-size:0.58rem;letter-spacing:0.22em;color:{CYAN};font-weight:700;text-transform:uppercase;">
                Scout Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    st.checkbox("Combativo", value=False)
    st.checkbox("Construtor", value=False)
    st.checkbox("Híbrido", value=True)
    st.checkbox("Posicional", value=False)
    st.divider()
    st.text_input("Buscar jogador", value="Adriano Martins")
    st.caption("Base: Brasileirão Série A 2025/26")

# ──────────────────────────────────────────────────────────────────────────────
# TOP BAR
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="background:{DARK};border:1px solid rgba(126,200,255,0.16);border-radius:10px;
                padding:0.38rem 0.6rem;display:flex;justify-content:space-between;align-items:center;
                margin-bottom:0.65rem;">
        <div style="display:flex;align-items:center;gap:0.45rem;">
            <span style="font-size:0.72rem;">⚽</span>
            <span style="font-size:0.58rem;letter-spacing:0.19em;color:{CYAN};font-weight:700;text-transform:uppercase;">
                Scout Intelligence Platform
            </span>
        </div>
        <div style="display:flex;align-items:center;gap:1rem;">
            <span style="font-size:0.58rem;color:{MUTED};">Temporada 2025/26</span>
            <span style="font-size:0.58rem;color:{MUTED};">Brasileirão Série A</span>
            <div style="width:7px;height:7px;border-radius:50%;background:{GREEN};box-shadow:0 0 8px {GREEN};"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ──────────────────────────────────────────────────────────────────────────────
# ROW 1
# ──────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([2.0, 1.5, 1.9, 1.9], gap="small")

# Card atleta (revisado no estilo da imagem 2)
with c1:
    athlete = f"""
    <div class="card" style="padding:0.9rem;">
        <div style="height:8px;"></div>
        <div style="text-align:center;margin:0.2rem 0 0.55rem;">
            <div style="font-size:2.05rem;font-weight:800;color:{YELLOW_2};line-height:1.08;">{PLAYER["name"]}</div>
            <div style="font-size:1.05rem;font-weight:600;color:{TEXT};line-height:1.25;">{PLAYER["position"]}</div>
            <div style="font-size:1.22rem;font-weight:700;color:{CYAN};line-height:1.2;">{PLAYER["club"]}</div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.42rem 0.7rem;margin:0.2rem 0 0.65rem;">
            <div style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:{YELLOW_2};line-height:1;">Ano</div>
                <div style="font-size:1.8rem;font-weight:700;color:{TEXT};line-height:1.15;">{PLAYER["year"]}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:{YELLOW_2};line-height:1;">Nacionalidade</div>
                <div style="font-size:1.8rem;font-weight:700;color:{TEXT};line-height:1.15;">{PLAYER["nat"]}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:{YELLOW_2};line-height:1;">Altura</div>
                <div style="font-size:1.8rem;font-weight:700;color:{TEXT};line-height:1.15;">{PLAYER["height"]}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:800;color:{YELLOW_2};line-height:1;">Pé dominante</div>
                <div style="font-size:1.8rem;font-weight:700;color:{TEXT};line-height:1.15;">{PLAYER["foot"]}</div>
            </div>
        </div>

        <div style="background:{LIGHT_PANEL};border-radius:12px;padding:0.5rem 0.6rem;">
            <div style="display:flex;justify-content:space-between;">
                <span style="font-size:1.45rem;font-weight:800;color:#142437;">Minutagem</span>
                <span style="font-size:1.45rem;font-weight:800;color:#142437;">Gols</span>
                <span style="font-size:1.45rem;font-weight:800;color:#142437;">Assist.</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:0.08rem;">
                <span style="font-size:2.7rem;font-weight:900;color:#313626;">{PLAYER["minutes"]}</span>
                <span style="font-size:2.7rem;font-weight:900;color:#2d2d2d;">{PLAYER["goals"]}</span>
                <span style="font-size:2.7rem;font-weight:900;color:#2d2d2d;">{PLAYER["assists"]}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(athlete, unsafe_allow_html=True)

# Ratings
with c2:
    html = f'<div class="card" style="padding:0.9rem;height:100%;">'
    html += section_title("Ratings")
    html += rating_pill("Rating Geral", PLAYER["rtg"], PLAYER["rnk"])
    html += rating_pill("Combativo", PLAYER["comb"], PLAYER["r_comb"])
    html += rating_pill("Construtor", PLAYER["cons"], PLAYER["r_cons"])
    html += rating_pill("Posicional", PLAYER["posi"], PLAYER["r_posi"])
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Aspectos Def + Construção
with c3:
    html = f'<div class="card" style="padding:0.85rem;height:100%;">'
    html += aspect_block("Aspectos Defensivos", PLAYER["def_asp"])
    html += '<div style="margin:0.5rem 0;border-top:1px solid rgba(23,64,103,0.6);"></div>'
    html += aspect_block("Aspectos de Construção", PLAYER["con_asp"])
    html += f'<div style="margin-top:0.3rem;font-size:0.54rem;color:{MUTED};">*Passes Construtores Finais</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Aspectos ofensivos
with c4:
    html = f'<div class="card" style="padding:0.85rem;height:100%;">'
    html += aspect_block("Aspectos Ofensivos", PLAYER["off_asp"])
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

st.markdown('<div style="height:0.45rem;"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ROW 2 — Perfil (bloco único elegante) + Métricas
# ──────────────────────────────────────────────────────────────────────────────
r2c1, r2c2 = st.columns([2.2, 5.2], gap="small")

with r2c1:
    # Header do bloco perfil no estilo da imagem 1
    st.markdown(
        f"""
        <div class="card" style="padding:0.82rem 0.95rem 0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div style="font-size:1.85rem;font-weight:800;color:{YELLOW_2};line-height:1;">Perfil</div>
                    <div style="font-size:2.1rem;font-weight:800;color:{TEXT};line-height:1.1;">{PLAYER["profile"]}</div>
                </div>
                <div style="text-align:left;margin-top:0.08rem;">
                    <div style="font-size:1.25rem;font-weight:800;color:{YELLOW_2};line-height:1.2;">Combativo {PLAYER["p_comb"]}%</div>
                    <div style="font-size:1.25rem;font-weight:800;color:{YELLOW_2};line-height:1.2;">Construtor {PLAYER["p_cons"]}%</div>
                    <div style="font-size:1.25rem;font-weight:800;color:{YELLOW_2};line-height:1.2;">Posicional {PLAYER["p_posi"]}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(build_profile_radar(PLAYER), use_container_width=True, config={"displayModeBar": False})

with r2c2:
    html = f'<div class="card" style="padding:0.88rem;height:100%;">'
    html += section_title("Métricas")
    html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.15rem 1.45rem;">'
    for lbl, val, col in PLAYER["bars"]:
        html += metric_bar(lbl, val, col)
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)
