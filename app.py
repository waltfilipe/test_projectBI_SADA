import math
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import altair as alt

# PAGE CONFIG
st.set_page_config(
    page_title="Scout Intelligence",
    page_icon="soccer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# COLOR PALETTE
BG     = "#0D1B2A"
RED    = "#FE4A49"
CYAN   = "#1BE7FF"
GREEN  = "#31E981"
YELLOW = "#FED766"
PURPLE = "#8980F5"
CARD   = "#0e2038"
BORDER = "#1a3a5c"
MUTED  = "#5a7a9a"
TEXT   = "#c8d8e8"
DARK   = "#070e18"

YELLOW_FILL = "rgba(254,215,102,0.18)"


# RATING → gradient color
def rating_color(val):
    try:
        v = float(val)
    except Exception:
        return "#3a3a5a"
    if v <= 5.0:
        t = v / 5.0
        r = int(120 + (200 - 120) * (1 - t))
        g = int(20  + (60  - 20)  * t)
        b = int(20  + (20  - 20)  * t)
        return f"rgb({r},{g},{b})"
    elif v <= 8.0:
        t = (v - 5.0) / 3.0
        r = int(200 - (200 - 20)  * t)
        g = int(60  + (130 - 60)  * t)
        b = int(20  + (60  - 20)  * t)
        return f"rgb({r},{g},{b})"
    else:
        t = (v - 8.0) / 2.0
        r = int(20  - (20  - 10)  * t)
        g = int(130 - (130 - 60)  * t)
        b = int(60  + (160 - 60)  * t)
        return f"rgb({r},{g},{b})"


# PLAYER DATA
PLAYERS = {
    "Adriano Martins (Atletico GO)": {
        "name": "Adriano Martins", "position": "Zagueiro", "club": "Atletico GO",
        "year": 1998, "nat": "Brazil", "height": 193, "foot": "Destro",
        "min": 1955, "goals": 2, "ast": 0,
        "rtg": 6.4, "rnk": 52, "comb": 5.8, "r_comb": 71,
        "cons": 6.9, "r_cons": 39, "posi": 6.8, "r_posi": 48,
        "profile": "Hibrido", "p_comb": 21, "p_cons": 41, "p_posi": 39,
        "def_asp": [("Confrontos", "X"), ("Duelos Aereos", "-"), ("Intervencoes", "G")],
        "off_asp": [("Ball Security", "G"), ("Progressao", "S")],
        "con_asp": [("Passes Verticais", "-"), ("PCF*", "G"), ("Passes Longos", "X")],
        "bars": [
            ("Construcao", 43, "#FED766"), ("Ofensividade", 77, "#31E981"),
            ("1vs1 Defensivo", 5, "#FE4A49"), ("Contencao", 78, "#31E981"),
            ("Duelo Aereo", 14, "#FE4A49"),
        ],
    },
    "Lucas Henrique (Botafogo)": {
        "name": "Lucas Henrique", "position": "Volante", "club": "Botafogo",
        "year": 1997, "nat": "Brazil", "height": 182, "foot": "Destro",
        "min": 2210, "goals": 0, "ast": 2,
        "rtg": 7.2, "rnk": 11, "comb": 7.0, "r_comb": 18,
        "cons": 6.8, "r_cons": 22, "posi": 7.4, "r_posi": 9,
        "profile": "Posicional", "p_comb": 25, "p_cons": 30, "p_posi": 45,
        "def_asp": [("Confrontos", "G"), ("Duelos Aereos", "S"), ("Intervencoes", "G")],
        "off_asp": [("Ball Security", "S"), ("Progressao", "G")],
        "con_asp": [("Passes Verticais", "G"), ("PCF*", "S"), ("Passes Longos", "-")],
        "bars": [
            ("Construcao", 65, "#FED766"), ("Ofensividade", 55, "#31E981"),
            ("1vs1 Defensivo", 72, "#31E981"), ("Contencao", 80, "#31E981"),
            ("Duelo Aereo", 60, "#FED766"),
        ],
    },
    "Gustavo Nunes (Gremio)": {
        "name": "Gustavo Nunes", "position": "Extremo Direito", "club": "Gremio",
        "year": 2003, "nat": "Brazil", "height": 175, "foot": "Esquerdo",
        "min": 1840, "goals": 6, "ast": 5,
        "rtg": 7.5, "rnk": 7, "comb": 6.9, "r_comb": 20,
        "cons": 7.0, "r_cons": 15, "posi": 7.8, "r_posi": 4,
        "profile": "Combativo", "p_comb": 48, "p_cons": 28, "p_posi": 24,
        "def_asp": [("Confrontos", "S"), ("Duelos Aereos", "-"), ("Intervencoes", "-")],
        "off_asp": [("Ball Security", "G"), ("Progressao", "G")],
        "con_asp": [("Passes Verticais", "G"), ("PCF*", "-"), ("Passes Longos", "S")],
        "bars": [
            ("Construcao", 55, "#FED766"), ("Ofensividade", 91, "#31E981"),
            ("1vs1 Defensivo", 38, "#FED766"), ("Contencao", 42, "#FED766"),
            ("Duelo Aereo", 31, "#FE4A49"),
        ],
    },
}

# CSS
CSS_TEMPLATE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background-color: BG_COLOR; color: TEXT_COLOR; }
section[data-testid="stSidebar"] { background: DARK_COLOR !important; border-right: 1px solid rgba(27,231,255,0.13); }
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
.block-container { padding: 0.4rem 1rem 1rem !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stSidebar"] .stButton > button {
    background: CARD_COLOR; color: TEXT_COLOR; border: 1px solid BORDER_COLOR; border-radius: 7px;
    width: 100%; font-size: 0.79rem; font-weight: 500; letter-spacing: 0.04em; padding: 0.38rem 0.2rem;
    transition: all 0.15s ease; margin-bottom: 2px; text-align: center !important; justify-content: center !important;
    display: flex !important; align-items: center !important;
}
div[data-testid="stSidebar"] .stButton > button:hover { background: rgba(27,231,255,0.07); border-color: CYAN_COLOR; color: CYAN_COLOR; }
div[data-testid="stCheckbox"] label span { color: MUTED_COLOR !important; font-size: 0.82rem !important; }
div[data-testid="stTextInput"] input {
    background: DARK_COLOR !important; border: 1px solid BORDER_COLOR !important; color: TEXT_COLOR !important;
    border-radius: 7px !important; font-size: 0.82rem !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: DARK_COLOR !important; border-color: BORDER_COLOR !important; color: TEXT_COLOR !important;
    border-radius: 7px !important; font-size: 0.82rem !important;
}
hr { border-color: BORDER_COLOR; opacity: 0.45; margin: 0.4rem 0; }
</style>
"""
css = (
    CSS_TEMPLATE
    .replace("BG_COLOR", BG)
    .replace("TEXT_COLOR", TEXT)
    .replace("DARK_COLOR", DARK)
    .replace("CYAN_COLOR", CYAN)
    .replace("CARD_COLOR", CARD)
    .replace("BORDER_COLOR", BORDER)
    .replace("MUTED_COLOR", MUTED)
)
st.markdown(css, unsafe_allow_html=True)


# HELPERS
def icon_html(k):
    if k == "X":
        return f'<span style="color:{RED};font-weight:800;font-size:0.85rem;">X</span>'
    if k == "G":
        return '<span style="font-size:0.9rem;">&#x1F947;</span>'
    if k == "S":
        return '<span style="font-size:0.9rem;">&#x1F948;</span>'
    return f'<span style="color:{BORDER};font-size:0.88rem;">-</span>'


def section_title(label):
    return (
        f'<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
        f'text-transform:uppercase;color:{CYAN};padding-bottom:0.2rem;'
        f'border-bottom:1px solid rgba(27,231,255,0.25);margin-bottom:0.4rem;">{label}</div>'
    )


def rating_pill(label, value, rank):
    col = rating_color(value)
    return (
        f'<div style="background:{DARK};border:1px solid {BORDER};border-radius:8px;'
        f'padding:0.38rem 0.6rem;margin-bottom:0.32rem;">'
        f'<div style="font-size:0.54rem;font-weight:600;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:{MUTED};">{label}</div>'
        f'<div style="display:flex;align-items:center;gap:0.4rem;margin-top:0.1rem;">'
        f'<div style="background:{col};color:#fff;border-radius:5px;'
        f'padding:0.04rem 0.5rem;font-size:1.1rem;font-weight:800;min-width:46px;text-align:center;">{value}</div>'
        f'<div style="font-size:0.75rem;font-weight:700;color:{MUTED};">#{rank}</div>'
        f'</div></div>'
    )


def asp_section_html(title, items):
    h = section_title(title)
    for name_, ico in items:
        h += (
            f'<div style="display:flex;align-items:center;gap:0.4rem;padding:0.2rem 0;'
            f'font-size:0.76rem;color:{TEXT};border-bottom:1px solid rgba(26,58,92,0.45);">'
            f'{icon_html(ico)}<span>{name_}</span></div>'
        )
    return h


def bar_html(label, value, color):
    pct = min(max(int(value), 0), 100)
    return (
        f'<div style="margin-bottom:0.58rem;">'
        f'<div style="font-size:0.67rem;color:{MUTED};font-weight:500;margin-bottom:0.1rem;">{label}</div>'
        f'<div style="display:flex;align-items:center;gap:0.4rem;">'
        f'<div style="flex:1;height:7px;background:{DARK};border-radius:3px;overflow:hidden;'
        f'border:1px solid rgba(26,58,92,0.6);">'
        f'<div style="height:100%;width:{pct}%;background:{color};border-radius:3px;"></div></div>'
        f'<div style="font-size:0.67rem;font-weight:700;color:#fff;min-width:22px;text-align:right;">{value}</div>'
        f'</div></div>'
    )


def build_clean_triangle_radar(p):
    cats = ["Combativo", "Construtor", "Posicional"]
    vals = [p["p_comb"], p["p_cons"], p["p_posi"]]

    fig = go.Figure()

    # Grid triangular (níveis)
    grid_levels = [33, 66, 100]
    for lv in grid_levels:
        fig.add_trace(go.Scatterpolar(
            r=[lv, lv, lv, lv],
            theta=[cats[0], cats[1], cats[2], cats[0]],
            mode="lines",
            line=dict(color="rgba(180,190,205,0.30)", width=1),
            hoverinfo="skip",
            showlegend=False
        ))

    # Eixos
    for cat in cats:
        fig.add_trace(go.Scatterpolar(
            r=[0, 100],
            theta=[cat, cat],
            mode="lines",
            line=dict(color="rgba(180,190,205,0.35)", width=1),
            hoverinfo="skip",
            showlegend=False
        ))

    # Área externa sutil (estética scout)
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100],
        theta=[cats[0], cats[1], cats[2], cats[0]],
        mode="lines",
        fill="toself",
        fillcolor="rgba(160,175,205,0.22)",
        line=dict(color="rgba(120,140,180,0.35)", width=1.2),
        hoverinfo="skip",
        showlegend=False
    ))

    # Polígono do jogador
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        mode="lines",
        fill="toself",
        fillcolor="rgba(254,215,102,0.20)",
        line=dict(color="#C9A400", width=2),
        hovertemplate="%{theta}: <b>%{r}%</b><extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=False,
                range=[0, 100]
            ),
            angularaxis=dict(
                tickfont=dict(size=18, color="#EAF2FF", family="Inter"),
                rotation=90,
                direction="clockwise",
                gridcolor="rgba(0,0,0,0)",
                linecolor="rgba(0,0,0,0)"
            ),
        ),
        margin=dict(l=16, r=16, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300
    )
    return fig


def render_profile_radar_card(p):
    st.markdown(f"""
    <div style="
        background: linear-gradient(180deg, #001a33 0%, #001529 100%);
        border: 1px solid rgba(80,120,170,0.35);
        border-radius: 14px;
        padding: 14px 16px 8px 16px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    ">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
            <div>
                <div style="font-size:34px;line-height:1.05;font-weight:700;color:#FFD34D;margin-bottom:2px;">Perfil</div>
                <div style="font-size:44px;line-height:1;font-weight:800;color:#EAF2FF;">{p["profile"]}</div>
            </div>
            <div style="text-align:left;margin-top:2px;">
                <div style="font-size:34px;line-height:1.15;font-weight:700;color:#FFD34D;">Combativo {p["p_comb"]}%</div>
                <div style="font-size:34px;line-height:1.15;font-weight:700;color:#FFD34D;">Construtor {p["p_cons"]}%</div>
                <div style="font-size:34px;line-height:1.15;font-weight:700;color:#FFD34D;">Posicional {p["p_posi"]}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig = build_clean_triangle_radar(p)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
# SIDEBAR
with st.sidebar:
    st.markdown(
        f'<div style="text-align:center;padding:0.85rem 0 0.45rem;">'
        f'<div style="font-size:2rem;line-height:1;">&#x26BD;</div>'
        f'<div style="font-size:0.55rem;letter-spacing:0.26em;color:{CYAN};font-weight:700;text-transform:uppercase;margin-top:0.22rem;">'
        f'Scout Intelligence</div></div>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.checkbox("Combativo",  key="f_comb", value=False)
    st.checkbox("Construtor", key="f_cons", value=False)
    st.checkbox("Hibrido",    key="f_hibr", value=True)
    st.checkbox("Posicional", key="f_posi", value=False)
    st.divider()
    st.text_input("", placeholder="Buscar jogador...", label_visibility="collapsed", key="search")
    player_key = st.selectbox("", list(PLAYERS.keys()), label_visibility="collapsed", key="player_sel")

p = PLAYERS[player_key]

# HEADER BAR
st.markdown(
    f'<div style="background:{DARK};border-bottom:1px solid rgba(27,231,255,0.13);'
    f'padding:0.35rem 0.2rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">'
    f'<div style="display:flex;align-items:center;gap:0.45rem;"><span style="font-size:0.72rem;">&#x26BD;</span>'
    f'<span style="font-size:0.57rem;letter-spacing:0.2em;color:{CYAN};font-weight:700;text-transform:uppercase;">Scout Intelligence Platform</span></div>'
    f'<div style="display:flex;align-items:center;gap:1.1rem;">'
    f'<span style="font-size:0.57rem;color:{MUTED};">Temporada 2025/26</span>'
    f'<span style="font-size:0.57rem;color:{MUTED};">Brasileirao Serie A</span>'
    f'<div style="width:6px;height:6px;border-radius:50%;background:{GREEN};box-shadow:0 0 6px {GREEN};"></div>'
    f'</div></div>',
    unsafe_allow_html=True
)

# ROW 1
r1c1, r1c2, r1c3, r1c4 = st.columns([2.0, 1.6, 1.9, 1.9], gap="small")
with r1c1:
    st.markdown(f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:0.9rem;">'
                f'<div style="text-align:center"><div style="font-size:1.22rem;font-weight:800;color:#fff;">{p["name"]}</div>'
                f'<div style="font-size:0.72rem;color:{MUTED};">{p["position"]}</div>'
                f'<div style="font-size:0.78rem;font-weight:600;color:{CYAN};">{p["club"]}</div></div></div>', unsafe_allow_html=True)

with r1c2:
    rtg = f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:0.9rem;height:100%;">'
    rtg += section_title("Ratings")
    rtg += rating_pill("Rating Geral", p["rtg"], p["rnk"])
    rtg += rating_pill("Combativo", p["comb"], p["r_comb"])
    rtg += rating_pill("Construtor", p["cons"], p["r_cons"])
    rtg += rating_pill("Posicional", p["posi"], p["r_posi"])
    rtg += "</div>"
    st.markdown(rtg, unsafe_allow_html=True)

with r1c3:
    asp = f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:0.85rem;height:100%;">'
    asp += asp_section_html("Aspectos Defensivos", p["def_asp"])
    asp += '<div style="margin:0.5rem 0;border-top:1px solid rgba(26,58,92,0.6);"></div>'
    asp += asp_section_html("Aspectos de Construcao", p["con_asp"])
    asp += f'<div style="margin-top:0.28rem;font-size:0.52rem;color:{MUTED};">*Passes Construtores Finais</div></div>'
    st.markdown(asp, unsafe_allow_html=True)

with r1c4:
    off = f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:0.85rem;height:100%;">'
    off += asp_section_html("Aspectos Ofensivos", p["off_asp"])
    off += '</div>'
    st.markdown(off, unsafe_allow_html=True)

st.markdown('<div style="height:0.45rem;"></div>', unsafe_allow_html=True)

# ROW 2
r2c1, r2c2 = st.columns([2.2, 5.2], gap="small")

with r2c1:
    st.markdown(
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:0.75rem 0.9rem 0.5rem;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
        f'<div><div style="font-size:0.55rem;color:{MUTED};text-transform:uppercase;letter-spacing:0.13em;font-weight:600;">Perfil</div>'
        f'<div style="font-size:1.3rem;font-weight:800;color:#fff;">{p["profile"]}</div></div>'
        f'</div></div>',
        unsafe_allow_html=True
    )
    radar = build_pro_radar_altair(p, size=350)
    st.altair_chart(radar, use_container_width=True)

with r2c2:
    met = f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:0.85rem;height:100%;">'
    met += section_title("Metricas")
    met += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.1rem 1.4rem;">'
    for lbl, val, col in p["bars"]:
        met += bar_html(lbl, val, col)
    met += '</div></div>'
    st.markdown(met, unsafe_allow_html=True)
