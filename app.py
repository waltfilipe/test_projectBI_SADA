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
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {{
  font-family: 'Inter', sans-serif !important;
  box-sizing: border-box;
}}

/* ── App background ── */
.stApp {{
  background-color: {BG};
  color: {TEXT};
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
  background: {DARK} !important;
  border-right: 1px solid {CYAN}22;
}}
section[data-testid="stSidebar"] > div {{
  padding-top: 0 !important;
}}

/* ── Main layout ── */
.block-container {{
  padding: 0.5rem 1rem 1rem !important;
  max-width: 100% !important;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── Buttons ── */
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
}}
.stButton > button:hover {{
  background: {CYAN}16;
  border-color: {CYAN};
  color: {CYAN};
  box-shadow: 0 0 10px {CYAN}20;
}}

/* ── Checkboxes ── */
div[data-testid="stCheckbox"] {{
  margin-bottom: -0.15rem;
}}
div[data-testid="stCheckbox"] label span {{
  color: {MUTED} !important;
  font-size: 0.82rem !important;
}}
div[data-testid="stCheckbox"] svg {{
  fill: {CYAN} !important;
}}

/* ── Text input ── */
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

/* ── Select box ── */
div[data-testid="stSelectbox"] > div > div {{
  background: {DARK} !important;
  border-color: {BORDER} !important;
  color: {TEXT} !important;
  border-radius: 7px !important;
  font-size: 0.82rem !important;
}}

/* ── Divider ── */
hr {{
  border-color: {BORDER};
  opacity: 0.45;
  margin: 0.4rem 0;
}}

/* ── Plotly chart container ── */
div[data-testid="stPlotlyChart"] {{
  border-radius: 12px;
  overflow: hidden;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {DARK}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 10px; }}

/* ── Reusable card ── */
.sc-card {{
  background: {CARD};
  border: 1px solid {BORDER};
  border-radius: 12px;
  padding: 0.9rem 1rem;
  height: 100%;
}}

/* ── Section title ── */
.sec-ttl {{
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: {CYAN};
  padding-bottom: 0.22rem;
  border-bottom: 1px solid {CYAN}28;
  margin-bottom: 0.4rem;
}}

/* ── Aspect row ── */
.asp {{
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.25rem 0;
  font-size: 0.77rem;
  color: {TEXT};
  border-bottom: 1px solid {BORDER}40;
}}

/* ── Bar chart ── */
.bar-lbl {{
  font-size: 0.7rem;
  color: {MUTED};
  margin-bottom: 0.14rem;
  font-weight: 500;
}}
.bar-row {{
  display: flex;
  align-items: center;
  gap: 0.45rem;
  margin-bottom: 0.7rem;
}}
.bar-track {{
  flex: 1;
  height: 7px;
  background: {DARK};
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid {BORDER}60;
}}
.bar-num {{
  font-size: 0.7rem;
  font-weight: 700;
  color: #fff;
  min-width: 22px;
  text-align: right;
}}

/* ── Sidebar label ── */
.sb-lbl {{
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: {CYAN};
  margin-bottom: 0.2rem;
  margin-top: 0.1rem;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLAYER DATA
# ─────────────────────────────────────────────────────────────────────────────
PLAYERS = {
    "Adriano Martins (Atlético GO)": {
        "name": "Adriano Martins", "position": "Zagueiro", "club": "Atlético GO",
        "year": 1998, "nat": "Brazil", "height": 193, "foot": "Destro",
        "min": 1955, "goals": 2, "ast": 0,
        "rtg": 6.4, "rnk": 52,
        "comb": 5.8, "r_comb": 71,
        "cons": 6.9, "r_cons": 39,
        "posi": 6.8, "r_posi": 48,
        "profile": "Híbrido",
        "p_comb": 21, "p_cons": 41, "p_posi": 39,
        "def_asp":  [("Confrontos", "X"), ("Duelos Aéreos", "–"), ("Intervenções", "G")],
        "off_asp":  [("Ball Security", "G"), ("Progressão", "S")],
        "con_asp":  [("Passes Verticais", "–"), ("PCF*", "G"), ("Passes Longos", "X")],
        "bars": [
            ("Construção",      43, YELLOW),
            ("Ofensividade",    77, GREEN),
            ("1vs1 – Defensivo", 5, RED),
            ("Contenção",       78, GREEN),
            ("Duelo Aéreo",     14, RED),
        ],
    },
    "Lucas Henrique (Botafogo)": {
        "name": "Lucas Henrique", "position": "Volante", "club": "Botafogo",
        "year": 1997, "nat": "Brazil", "height": 182, "foot": "Destro",
        "min": 2210, "goals": 0, "ast": 2,
        "rtg": 7.2, "rnk": 11,
        "comb": 7.0, "r_comb": 18,
        "cons": 6.8, "r_cons": 22,
        "posi": 7.4, "r_posi":  9,
        "profile": "Posicional",
        "p_comb": 25, "p_cons": 30, "p_posi": 45,
        "def_asp":  [("Confrontos", "G"), ("Duelos Aéreos", "S"), ("Intervenções", "G")],
        "off_asp":  [("Ball Security", "S"), ("Progressão", "G")],
        "con_asp":  [("Passes Verticais", "G"), ("PCF*", "S"), ("Passes Longos", "–")],
        "bars": [
            ("Construção",      65, YELLOW),
            ("Ofensividade",    55, GREEN),
            ("1vs1 – Defensivo",72, GREEN),
            ("Contenção",       80, GREEN),
            ("Duelo Aéreo",     60, YELLOW),
        ],
    },
    "Gustavo Nunes (Grêmio)": {
        "name": "Gustavo Nunes", "position": "Extremo Direito", "club": "Grêmio",
        "year": 2003, "nat": "Brazil", "height": 175, "foot": "Esquerdo",
        "min": 1840, "goals": 6, "ast": 5,
        "rtg": 7.5, "rnk": 7,
        "comb": 6.9, "r_comb": 20,
        "cons": 7.0, "r_cons": 15,
        "posi": 7.8, "r_posi":  4,
        "profile": "Combativo",
        "p_comb": 48, "p_cons": 28, "p_posi": 24,
        "def_asp":  [("Confrontos", "S"), ("Duelos Aéreos", "–"), ("Intervenções", "–")],
        "off_asp":  [("Ball Security", "G"), ("Progressão", "G")],
        "con_asp":  [("Passes Verticais", "G"), ("PCF*", "–"), ("Passes Longos", "S")],
        "bars": [
            ("Construção",      55, YELLOW),
            ("Ofensividade",    91, GREEN),
            ("1vs1 – Defensivo",38, YELLOW),
            ("Contenção",       42, YELLOW),
            ("Duelo Aéreo",     31, RED),
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def icon_html(k: str) -> str:
    if k == "X":  return f'<span style="color:{RED};font-weight:800;font-size:0.82rem;">✕</span>'
    if k == "G":  return '<span style="font-size:0.88rem;">🥇</span>'
    if k == "S":  return '<span style="font-size:0.88rem;">🥈</span>'
    return f'<span style="color:{BORDER};font-size:0.88rem;">─</span>'

def rating_block(label: str, value, rank: int, bg: str, fg: str = "#fff") -> str:
    return f"""
    <div style="background:{DARK};border:1px solid {BORDER};border-radius:8px;
         padding:0.46rem 0.7rem;margin-bottom:0.42rem;">
      <div style="font-size:0.58rem;font-weight:600;letter-spacing:0.13em;
                  text-transform:uppercase;color:{MUTED};">{label}</div>
      <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.16rem;">
        <div style="background:{bg};color:{fg};border-radius:5px;padding:0.07rem 0.55rem;
             font-size:1.18rem;font-weight:800;letter-spacing:-0.01em;">{value}</div>
        <div style="font-size:0.85rem;font-weight:700;color:{MUTED};">#{rank}</div>
      </div>
    </div>"""

def aspect_section(title: str, items: list) -> str:
    rows = "".join(f'<div class="asp">{icon_html(v)}<span>{k}</span></div>' for k, v in items)
    return f'<div class="sec-ttl">{title}</div>{rows}'

def bar_block(label: str, value: int, color: str) -> str:
    pct = min(max(value, 0), 100)
    return f"""
    <div>
      <div class="bar-lbl">{label}</div>
      <div class="bar-row">
        <div class="bar-track">
          <div style="height:100%;width:{pct}%;background:{color};border-radius:3px;
               box-shadow:0 0 6px {color}55;"></div>
        </div>
        <div class="bar-num">{value}</div>
      </div>
    </div>"""

def build_radar(p: dict) -> go.Figure:
    cats   = ["Combativo", "Construtor", "Posicional"]
    vals   = [p["p_comb"], p["p_cons"], p["p_posi"]]
    colors = [RED, GREEN, CYAN]

    fig = go.Figure()

    # Concentric triangle grid
    for ring in [20, 40, 60, 80, 100]:
        fig.add_trace(go.Scatterpolar(
            r=[ring] * 3 + [ring],
            theta=cats + [cats[0]],
            mode="lines",
            line=dict(color=BORDER, width=0.75),
            fill=None, showlegend=False, hoverinfo="skip",
        ))

    # Axis lines from center
    for cat in cats:
        fig.add_trace(go.Scatterpolar(
            r=[0, 100], theta=[cat, cat],
            mode="lines",
            line=dict(color=BORDER, width=1),
            showlegend=False, hoverinfo="skip",
        ))

    # Individual axis dots (max value markers)
    for cat, col in zip(cats, colors):
        fig.add_trace(go.Scatterpolar(
            r=[100], theta=[cat],
            mode="markers",
            marker=dict(size=5, color=col, opacity=0.6),
            showlegend=False, hoverinfo="skip",
        ))

    # Player polygon
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        fill="toself",
        fillcolor=YELLOW + "28",
        line=dict(color=YELLOW, width=2.2),
        mode="lines+markers",
        marker=dict(
            size=7, color=YELLOW,
            line=dict(color=BG, width=1.5),
        ),
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
        margin=dict(l=40, r=40, t=20, b=20),
        height=255,
        showlegend=False,
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:0.9rem 0 0.5rem;">
      <div style="font-size:2rem;line-height:1;">⚽</div>
      <div style="font-size:0.56rem;letter-spacing:0.26em;color:{CYAN};
                  font-weight:700;text-transform:uppercase;margin-top:0.25rem;">
        Scout Intelligence
      </div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown(f'<div class="sb-lbl">Perfil</div>', unsafe_allow_html=True)
    st.checkbox("Combativo",  key="f_comb",  value=False)
    st.checkbox("Construtor", key="f_cons",  value=False)
    st.checkbox("Híbrido",    key="f_hibr",  value=True)
    st.checkbox("Posicional", key="f_posi",  value=False)
    st.divider()

    st.markdown(f'<div class="sb-lbl">Jogadores</div>', unsafe_allow_html=True)
    st.text_input("", placeholder="🔍  Buscar jogador...",
                  label_visibility="collapsed", key="search")
    player_key = st.selectbox("", list(PLAYERS.keys()),
                               label_visibility="collapsed", key="player_sel")
    st.divider()

    st.markdown(f'<div class="sb-lbl">Navegação</div>', unsafe_allow_html=True)
    for pos in ["Zagueiros", "Laterais", "Meio-campistas",
                "Extremos", "Meias Ofensivos", "Atacantes"]:
        st.button(pos, key=f"nav_{pos}")

    st.divider()
    st.markdown(f"""
    <div style="display:flex;justify-content:space-around;padding:0.25rem 0;font-size:1.1rem;">
      <span title="Início" style="cursor:pointer;opacity:0.8;">🏠</span>
      <span title="Ajuda"  style="cursor:pointer;opacity:0.8;">❓</span>
      <span title="Busca"  style="cursor:pointer;opacity:0.8;">🔍</span>
      <span title="Stats"  style="cursor:pointer;opacity:0.8;">📊</span>
    </div>
    <div style="margin-top:0.9rem;text-align:center;font-size:0.6rem;color:{MUTED};">
      Jogadores Analisados &nbsp;
      <span style="color:{CYAN};font-weight:700;font-size:0.7rem;">78</span>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD SELECTED PLAYER
# ─────────────────────────────────────────────────────────────────────────────
p = PLAYERS[player_key]

# ─────────────────────────────────────────────────────────────────────────────
# HEADER BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{DARK};border-bottom:1px solid {CYAN}18;
     padding:0.38rem 0.2rem;display:flex;justify-content:space-between;
     align-items:center;margin-bottom:0.75rem;">
  <div style="display:flex;align-items:center;gap:0.5rem;">
    <span style="font-size:0.72rem;">⚽</span>
    <span style="font-size:0.58rem;letter-spacing:0.2em;color:{CYAN};
                 font-weight:700;text-transform:uppercase;">Scout Intelligence Platform</span>
  </div>
  <div style="display:flex;align-items:center;gap:1.2rem;">
    <span style="font-size:0.58rem;color:{MUTED};">Temporada 2025/26</span>
    <span style="font-size:0.58rem;color:{MUTED};">Brasileirão Série A</span>
    <div style="width:6px;height:6px;border-radius:50%;background:{GREEN};
         box-shadow:0 0 6px {GREEN};"></div>
  </div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN COLUMNS
# ─────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([2.05, 1.55, 2.1, 1.75, 2.0], gap="small")

# ═══════════════════════════════════════
# C1 — PLAYER CARD
# ═══════════════════════════════════════
with c1:
    st.markdown(f"""
    <div class="sc-card">

      <!-- Avatar placeholder -->
      <div style="text-align:center;margin-bottom:0.75rem;">
        <div style="display:inline-flex;align-items:center;justify-content:center;
             width:74px;height:74px;border*
