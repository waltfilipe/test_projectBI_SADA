import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Scout Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# COLOR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────────
# PLAYER DATA
# ─────────────────────────────────────────────────────────────────────────────
PLAYERS = {
    "Adriano Martins (Atlético GO)": {
        "name": "Adriano Martins", "position": "Zagueiro", "club": "Atlético GO",
        "year": 1998, "nat": "Brazil", "height": 193, "foot": "Destro",
        "min": 1955, "goals": 2, "ast": 0,
        "rtg": 6.4, "rnk": 52, "comb": 5.8, "r_comb": 71,
        "cons": 6.9, "r_cons": 39, "posi": 6.8, "r_posi": 48,
        "profile": "Híbrido", "p_comb": 21, "p_cons": 41, "p_posi": 39,
        "def_asp": [("Confrontos","X"),("Duelos Aéreos","–"),("Intervenções","G")],
        "off_asp": [("Ball Security","G"),("Progressão","S")],
        "con_asp": [("Passes Verticais","–"),("PCF*","G"),("Passes Longos","X")],
        "bars": [
            ("Construção", 43, "#FED766"), ("Ofensividade", 77, "#31E981"),
            ("1vs1 – Defensivo", 5, "#FE4A49"), ("Contenção", 78, "#31E981"),
            ("Duelo Aéreo", 14, "#FE4A49"),
        ],
    },
    "Lucas Henrique (Botafogo)": {
        "name": "Lucas Henrique", "position": "Volante", "club": "Botafogo",
        "year": 1997, "nat": "Brazil", "height": 182, "foot": "Destro",
        "min": 2210, "goals": 0, "ast": 2,
        "rtg": 7.2, "rnk": 11, "comb": 7.0, "r_comb": 18,
        "cons": 6.8, "r_cons": 22, "posi": 7.4, "r_posi": 9,
        "profile": "Posicional", "p_comb": 25, "p_cons": 30, "p_posi": 45,
        "def_asp": [("Confrontos","G"),("Duelos Aéreos","S"),("Intervenções","G")],
        "off_asp": [("Ball Security","S"),("Progressão","G")],
        "con_asp": [("Passes Verticais","G"),("PCF*","S"),("Passes Longos","–")],
        "bars": [
            ("Construção", 65, "#FED766"), ("Ofensividade", 55, "#31E981"),
            ("1vs1 – Defensivo", 72, "#31E981"), ("Contenção", 80, "#31E981"),
            ("Duelo Aéreo", 60, "#FED766"),
        ],
    },
    "Gustavo Nunes (Grêmio)": {
        "name": "Gustavo Nunes", "position": "Extremo Direito", "club": "Grêmio",
        "year": 2003, "nat": "Brazil", "height": 175, "foot": "Esquerdo",
        "min": 1840, "goals": 6, "ast": 5,
        "rtg": 7.5, "rnk": 7, "comb": 6.9, "r_comb": 20,
        "cons": 7.0, "r_cons": 15, "posi": 7.8, "r_posi": 4,
        "profile": "Combativo", "p_comb": 48, "p_cons": 28, "p_posi": 24,
        "def_asp": [("Confrontos","S"),("Duelos Aéreos","–"),("Intervenções","–")],
        "off_asp": [("Ball Security","G"),("Progressão","G")],
        "con_asp": [("Passes Verticais","G"),("PCF*","–"),("Passes Longos","S")],
        "bars": [
            ("Construção", 55, "#FED766"), ("Ofensividade", 91, "#31E981"),
            ("1vs1 – Defensivo", 38, "#FED766"), ("Contenção", 42, "#FED766"),
            ("Duelo Aéreo", 31, "#FE4A49"),
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  — ALL css braces are doubled {{ }}
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {{
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}}

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    background: {DARK} !important;
    border-right: 1px solid {CYAN}22;
}}

section[data-testid="stSidebar"] > div {{
    padding-top: 0 !important;
}}

.block-container {{
    padding: 0.5rem 1rem 1rem !important;
    max-width: 100% !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.stButton > button {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 7px;
    width: 100%;
    font-size: 0.79rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    padding: 0.38rem;
    transition: all 0.15s ease;
    margin-bottom: 2px;
}}

.stButton > button:hover {{
    background: {CYAN}16;
    border-color: {CYAN};
    color: {CYAN};
    box-shadow: 0 0 10px {CYAN}20;
}}

div[data-testid="stCheckbox"] label span {{
    color: {MUTED} !important;
    font-size: 0.82rem !important;
}}

div[data-testid="stTextInput"] input {{
    background: {DARK} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 7px !important;
    font-size: 0.82rem !important;
}}

div[data-testid="stTextInput"] input:focus {{
    border-color: {CYAN} !important;
    box-shadow: 0 0 0 2px {CYAN}22 !important;
}}

div[data-testid="stSelectbox"] > div > div {{
    background: {DARK} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 7px !important;
    font-size: 0.82rem !important;
}}

hr {{
    border-color: {BORDER};
    opacity: 0.45;
    margin: 0.4rem 0;
}}

::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {DARK}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 10px; }}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def icon_html(k: str) -> str:
    if k == "X":
        return f'<span style="color:{RED};font-weight:800;font-size:0.85rem;">✕</span>'
    if k == "G":
        return '<span style="font-size:0.9rem;">🥇</span>'
    if k == "S":
        return '<span style="font-size:0.9rem;">🥈</span>'
    return f'<span style="color:{BORDER};font-size:0.88rem;">─</span>'


def rating_pill(label: str, value, rank: int, pill_color: str) -> str:
    return (
        f'<div style="background:{DARK};border:1px solid {BORDER};border-radius:8px;'
        f'padding:0.42rem 0.65rem;margin-bottom:0.38rem;">'
        f'<div style="font-size:0.56rem;font-weight:600;letter-spacing:0.13em;'
        f'text-transform:uppercase;color:{MUTED};">{label}</div>'
        f'<div style="display:flex;align-items:center;gap:0.45rem;margin-top:0.14rem;">'
        f'<div style="background:{pill_color};color:#fff;border-radius:5px;'
        f'padding:0.05rem 0.5rem;font-size:1.15rem;font-weight:800;">{value}</div>'
        f'<div style="font-size:0.8rem;font-weight:700;color:{MUTED};">#{rank}</div>'
        f'</div></div>'
    )


def asp_section_html(title: str, items: list) -> str:
    header = (
        f'<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
        f'text-transform:uppercase;color:{CYAN};padding-bottom:0.2rem;'
        f'border-bottom:1px solid {CYAN}28;margin-bottom:0.35rem;">{title}</div>'
    )
    rows = ""
    for name_, ico in items:
        rows += (
            f'<div style="display:flex;align-items:center;gap:0.4rem;padding:0.22rem 0;'
            f'font-size:0.76rem;color:{TEXT};border-bottom:1px solid {BORDER}30;">'
            f'{icon_html(ico)}<span>{name_}</span></div>'
        )
    return header + rows


def bar_html(label: str, value: int, color: str) -> str:
    pct = min(max(value, 0), 100)
    return (
        f'<div style="margin-bottom:0.62rem;">'
        f'<div style="font-size:0.68rem;color:{MUTED};font-weight:500;margin-bottom:0.12rem;">{label}</div>'
        f'<div style="display:flex;align-items:center;gap:0.42rem;">'
        f'<div style="flex:1;height:7px;background:{DARK};border-radius:3px;'
        f'overflow:hidden;border:1px solid {BORDER}55;">'
        f'<div style="height:100%;width:{pct}%;background:{color};border-radius:3px;'
        f'box-shadow:0 0 6px {color}55;"></div>'
        f'</div>'
        f'<div style="font-size:0.68rem;font-weight:700;color:#fff;min-width:20px;'
        f'text-align:right;">{value}</div>'
        f'</div></div>'
    )


def build_radar(p: dict) -> go.Figure:
    cats = ["Combativo", "Construtor", "Posicional"]
    vals = [p["p_comb"], p["p_cons"], p["p_posi"]]

    fig = go.Figure()

    # Grid rings
    for ring in [20, 40, 60, 80, 100]:
        fig.add_trace(go.Scatterpolar(
            r=[ring, ring, ring, ring],
            theta=[cats[0], cats[1], cats[2], cats[0]],
            mode="lines",
            line=dict(color=BORDER, width=0.7),
            showlegend=False, hoverinfo="skip",
        ))

    # Axis spokes
    for cat in cats:
        fig.add_trace(go.Scatterpolar(
            r=[0, 100], theta=[cat, cat],
            mode="lines",
            line=dict(color=BORDER, width=1),
            showlegend=False, hoverinfo="skip",
        ))

    # Player polygon
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        fill="toself",
        fillcolor=YELLOW + "30",
        line=dict(color=YELLOW, width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color=YELLOW, line=dict(color=BG, width=1.5)),
        showlegend=False,
        hovertemplate="%{theta}: <b>%{r}%</b><extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(
                tickfont=dict(size=10, color="#8ca0b8", family="Inter"),
                gridcolor=BORDER,
                linecolor=BORDER,
                rotation=90,
                direction="counterclockwise",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=38, r=38, t=18, b=18),
        height=250,
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="text-align:center;padding:0.85rem 0 0.45rem;">'
        f'<div style="font-size:2rem;line-height:1;">⚽</div>'
        f'<div style="font-size:0.55rem;letter-spacing:0.26em;color:{CYAN};'
        f'font-weight:700;text-transform:uppercase;margin-top:0.22rem;">'
        f'Scout Intelligence</div></div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        f'<div style="font-size:0.57rem;font-weight:700;letter-spacing:0.18em;'
        f'text-transform:uppercase;color:{CYAN};margin-bottom:0.15rem;">Perfil</div>',
        unsafe_allow_html=True,
    )
    st.checkbox("Combativo",  key="f_comb", value=False)
    st.checkbox("Construtor", key="f_cons", value=False)
    st.checkbox("Híbrido",    key="f_hibr", value=True)
    st.checkbox("Posicional", key="f_posi", value=False)
    st.divider()

    st.markdown(
        f'<div style="font-size:0.57rem;font-weight:700;letter-spacing:0.18em;'
        f'text-transform:uppercase;color:{CYAN};margin-bottom:0.15rem;">Jogadores</div>',
        unsafe_allow_html=True,
    )
    st.text_input("", placeholder="🔍  Buscar jogador...",
                  label_visibility="collapsed", key="search")
    player_key = st.selectbox(
        "", list(PLAYERS.keys()),
        label_visibility="collapsed", key="player_sel",
    )
    st.divider()

    st.markdown(
        f'<div style="font-size:0.57rem;font-weight:700;letter-spacing:0.18em;'
        f'text-transform:uppercase;color:{CYAN};margin-bottom:0.2rem;">Navegação</div>',
        unsafe_allow_html=True,
    )
    for pos in ["Zagueiros", "Laterais", "Meio-campistas",
                "Extremos", "Meias Ofensivos", "Atacantes"]:
        st.button(pos, key=f"nav_{pos}")

    st.divider()
    st.markdown(
        f'<div style="display:flex;justify-content:space-around;'
        f'padding:0.2rem 0;font-size:1.05rem;">'
        f'<span title="Início" style="cursor:pointer;opacity:0.75;">🏠</span>'
        f'<span title="Ajuda"  style="cursor:pointer;opacity:0.75;">❓</span>'
        f'<span title="Busca"  style="cursor:pointer;opacity:0.75;">🔍</span>'
        f'<span title="Stats"  style="cursor:pointer;opacity:0.75;">📊</span>'
        f'</div>'
        f'<div style="margin-top:0.85rem;text-align:center;font-size:0.58rem;color:{MUTED};">'
        f'Jogadores Analisados &nbsp;'
        f'<span style="color:{CYAN};font-weight:700;font-size:0.68rem;">78</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# LOAD SELECTED PLAYER
# ─────────────────────────────────────────────────────────────────────────────
p = PLAYERS[player_key]

# ─────────────────────────────────────────────────────────────────────────────
# TOP HEADER BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="background:{DARK};border-bottom:1px solid {CYAN}18;'
    f'padding:0.35rem 0.2rem;display:flex;justify-content:space-between;'
    f'align-items:center;margin-bottom:0.7rem;">'
    f'<div style="display:flex;align-items:center;gap:0.45rem;">'
    f'<span style="font-size:0.72rem;">⚽</span>'
    f'<span style="font-size:0.57rem;letter-spacing:0.2em;color:{CYAN};'
    f'font-weight:700;text-transform:uppercase;">Scout Intelligence Platform</span>'
    f'</div>'
    f'<div style="display:flex;align-items:center;gap:1.1rem;">'
    f'<span style="font-size:0.57rem;color:{MUTED};">Temporada 2025/26</span>'
    f'<span style="font-size:0.57rem;color:{MUTED};">Brasileirão Série A</span>'
    f'<div style="width:6px;height:6px;border-radius:50%;background:{GREEN};'
    f'box-shadow:0 0 6px {GREEN};"></div>'
    f'</div></div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN GRID
# ─────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([2.0, 1.5, 2.1, 1.75, 2.0], gap="small")

# ──────────────────────── C1 — PLAYER CARD ────────────────────────
with c1:
    card = (
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:1rem;height:100%;">'

        # Avatar
        f'<div style="text-align:center;margin-bottom:0.7rem;">'
        f'<div style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:72px;height:72px;border-radius:50%;'
        f'background:linear-gradient(135deg,{BORDER},{DARK});'
        f'border:2px solid {CYAN}44;font-size:2.4rem;line-height:1;">👤</div>'
        f'</div>'

        # Name
        f'<div style="text-align:center;margin-bottom:0.8rem;">'
        f'<div style="font-size:1.32rem;font-weight:800;color:#fff;'
        f'letter-spacing:-0.01em;line-height:1.15;">{p["name"]}</div>'
        f'<div style="font-size:0.75rem;color:{MUTED};margin-top:0.18rem;">{p["position"]}</div>'
        f'<div style="font-size:0.8rem;font-weight:600;color:{CYAN};margin-top:0.1rem;">{p["club"]}</div>'
        f'</div>'

        # Bio grid
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.35rem;'
        f'margin-bottom:0.75rem;">'
        f'<div style="background:{DARK};border:1px solid {BORDER}50;border-radius:6px;'
        f'padding:0.3rem 0.45rem;">'
        f'<div style="font-size:0.55rem;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Ano</div>'
        f'<div style="font-size:0.88rem;font-weight:700;color:#fff;">{p["year"]}</div>'
        f'</div>'
        f'<div style="background:{DARK};border:1px solid {BORDER}50;border-radius:6px;'
        f'padding:0.3rem 0.45rem;">'
        f'<div style="font-size:0.55rem;color:{CYAN};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Nacionalidade</div>'
        f'<div style="font-size:0.88rem;font-weight:700;color:#fff;">{p["nat"]}</div>'
        f'</div>'
        f'<div style="background:{DARK};border:1px solid {BORDER}50;border-radius:6px;'
        f'padding:0.3rem 0.45rem;">'
        f'<div style="font-size:0.55rem;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Altura</div>'
        f'<div style="font-size:0.88rem;font-weight:700;color:#fff;">{p["height"]} cm</div>'
        f'</div>'
        f'<div style="background:{DARK};border:1px solid {BORDER}50;border-radius:6px;'
        f'padding:0.3rem 0.45rem;">'
        f'<div style="font-size:0.55rem;color:{CYAN};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Pé dominante</div>'
        f'<div style="font-size:0.88rem;font-weight:700;color:#fff;">{p["foot"]}</div>'
        f'</div>'
        f'</div>'

        # Stats strip
        f'<div style="background:{DARK};border:1px solid {BORDER};border-radius:8px;'
        f'padding:0.55rem 0.6rem;">'
        f'<div style="display:flex;justify-content:space-between;'
        f'margin-bottom:0.28rem;">'
        f'<span style="font-size:0.55rem;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Minutagem</span>'
        f'<span style="font-size:0.55rem;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Gols</span>'
        f'<span style="font-size:0.55rem;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;">Assist.</span>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;">'
        f'<span style="font-size:1.55rem;font-weight:900;color:#fff;">{p["min"]}</span>'
        f'<span style="font-size:1.55rem;font-weight:900;color:#fff;">{p["goals"]}</span>'
        f'<span style="font-size:1.55rem;font-weight:900;color:#fff;">{p["ast"]}</span>'
        f'</div>'
        f'</div>'

        f'</div>'
    )
    st.markdown(card, unsafe_allow_html=True)

# ──────────────────────── C2 — RATINGS ────────────────────────
with c2:
    rtg_html = (
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:0.9rem;height:100%;">'
        f'<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
        f'text-transform:uppercase;color:{CYAN};padding-bottom:0.2rem;'
        f'border-bottom:1px solid {CYAN}28;margin-bottom:0.55rem;">Ratings</div>'
    )

    # Rating Geral — larger
    rtg_html += (
        f'<div style="background:{DARK};border:1px solid {BORDER};border-radius:8px;'
        f'padding:0.48rem 0.65rem;margin-bottom:0.42rem;">'
        f'<div style="font-size:0.56rem;font-weight:600;letter-spacing:0.13em;'
        f'text-transform:uppercase;color:{MUTED};">Rating Geral'
        f'<span style="color:{CYAN};font-size:0.48rem;"> (Rank)</span></div>'
        f'<div style="display:flex;align-items:center;gap:0.45rem;margin-top:0.14rem;">'
        f'<div style="background:{RED};color:#fff;border-radius:5px;'
        f'padding:0.05rem 0.55rem;font-size:1.45rem;font-weight:800;">{p["rtg"]}</div>'
        f'<div style="font-size:0.9rem;font-weight:700;color:{MUTED};">#{p["rnk"]}</div>'
        f'</div></div>'
    )

    rtg_html += rating_pill("Combativo",  p["comb"], p["r_comb"], PURPLE)
    rtg_html += rating_pill("Construtor", p["cons"], p["r_cons"], "#1a4a6e")
    rtg_html += rating_pill("Posicional", p["posi"], p["r_posi"], "#1a4a3e")
    rtg_html += "</div>"

    st.markdown(rtg_html, unsafe_allow_html=True)

# ──────────────────────── C3 — RADAR ────────────────────────
with c3:
    radar_card_top = (
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:0.75rem 0.9rem 0.2rem;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
        f'<div>'
        f'<div style="font-size:0.58rem;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:0.14em;font-weight:600;">Perfil</div>'
        f'<div style="font-size:1.45rem;font-weight:800;color:#fff;'
        f'letter-spacing:-0.01em;">{p["profile"]}</div>'
        f'</div>'
        f'<div style="text-align:right;">'
        f'<div style="font-size:0.73rem;font-weight:700;color:{RED};">'
        f'Combativo {p["p_comb"]}%</div>'
        f'<div style="font-size:0.73rem;font-weight:700;color:{GREEN};">'
        f'Construtor {p["p_cons"]}% 🔍</div>'
        f'<div style="font-size:0.73rem;font-weight:700;color:{CYAN};">'
        f'Posicional {p["p_posi"]}%</div>'
        f'</div></div>'
        f'</div>'
    )
    st.markdown(radar_card_top, unsafe_allow_html=True)
    st.plotly_chart(build_radar(p), use_container_width=True, config={"displayModeBar": False})

# ──────────────────────── C4 — ASPECTOS ────────────────────────
with c4:
    asp_html = (
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:0.85rem;height:100%;">'
        + asp_section_html("Aspectos Defensivos", p["def_asp"])
        + f'<div style="margin:0.55rem 0;border-top:1px solid {BORDER}40;"></div>'
        + asp_section_html("Aspectos de Construção", p["con_asp"])
        + f'<div style="margin-top:0.3rem;font-size:0.55rem;color:{MUTED};">'
        f'*Passes Construtores Finais</div>'
        f'</div>'
    )
    st.markdown(asp_html, unsafe_allow_html=True)

# ──────────────────────── C5 — OFENSIVOS + BARS ────────────────────────
with c5:
    off_html = (
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:0.85rem;">'
        + asp_section_html("Aspectos Ofensivos", p["off_asp"])
        + f'</div>'
        f'<div style="margin:0.45rem 0;"></div>'
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:0.85rem;">'
        f'<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
        f'text-transform:uppercase;color:{CYAN};padding-bottom:0.2rem;'
        f'border-bottom:1px solid {CYAN}28;margin-bottom:0.55rem;">Métricas</div>'
    )
    for lbl, val, col in p["bars"]:
        off_html += bar_html(lbl, val, col)
    off_html += "</div>"

    st.markdown(off_html, unsafe_allow_html=True)
