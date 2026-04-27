import streamlit as st
import plotly.graph_objects as go

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Scout Analytics ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PALETA DE CORES ─────────────────────────────────────────────────────────
# Blue-Black : #0D1B2A  │  Ciano Elétrico : #1BE7FF
# Vermelho   : #FE4A49  │  Verde          : #31E981
# Amarelo    : #FED766  │  Roxo           : #8980F5

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #0D1B2A !important;
    color: #e2e8f0 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #091420 !important;
    border-right: 2px solid #1BE7FF22 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #cbd5e1 !important; }

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* ── Cards ── */
.card {
    background: #112031;
    border: 1px solid #1BE7FF22;
    border-radius: 14px;
    padding: 18px 20px;
    height: 100%;
    box-sizing: border-box;
}

/* ── Player info ── */
.player-name { font-size: 26px; font-weight: 800; color: #1BE7FF; line-height: 1.2; }
.player-pos  { font-size: 13px; color: #8980F5; margin-top: 2px; font-weight:600; }
.player-club { font-size: 14px; color: #31E981; font-weight: 600; margin-top: 2px; }

.info-row  { display: flex; justify-content: space-between; margin-top: 10px; gap: 8px; }
.info-cell { flex: 1; background: #0D1B2A; border-radius: 8px; padding: 8px; text-align: center;
             border: 1px solid #1BE7FF11; }
.info-cell .ic-label { font-size: 10px; color: #8980F5; text-transform: uppercase; letter-spacing: .5px; }
.info-cell .ic-val   { font-size: 14px; font-weight: 700; color: #FED766; }

.stat-row { display: flex; gap: 8px; margin-top: 12px; }
.stat-box { flex: 1; background: #0D1B2A; border: 1px solid #1BE7FF22;
            border-radius: 10px; text-align: center; padding: 10px 6px; }
.stat-box .sv { font-size: 24px; font-weight: 800; color: #1BE7FF; }
.stat-box .sl { font-size: 10px; color: #8980F5; text-transform: uppercase;
                letter-spacing: .8px; margin-top: 2px; }

/* ── Ratings ── */
.r-label { font-size: 11px; color: #8980F5; text-transform: uppercase;
           letter-spacing: .8px; margin-bottom: 5px; }
.rating-row { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }

.r-badge      { color: #0D1B2A; font-size: 24px; font-weight: 900;
                border-radius: 8px; padding: 4px 14px;
                min-width: 64px; text-align: center; }
.r-badge.main { font-size: 30px; background: #1BE7FF; color: #0D1B2A; }
.r-badge.comb { background: #FE4A49; color: #fff; }
.r-badge.cons { background: #31E981; color: #0D1B2A; }
.r-badge.posi { background: #8980F5; color: #fff; }

.rank-tag { background: #0D1B2A; color: #1BE7FF; border: 1px solid #1BE7FF44;
            border-radius: 6px; padding: 3px 10px;
            font-size: 13px; font-weight: 700; }

/* ── Aspects ── */
.section-title { font-size: 11px; font-weight: 700; letter-spacing: 1px;
                 text-transform: uppercase; margin-bottom: 8px; }
.aspect-tag { display: inline-block; background: #0D1B2A;
              border: 1px solid #1BE7FF33;
              border-radius: 6px; padding: 4px 10px; font-size: 12px;
              color: #cbd5e1; margin: 3px 2px; }

/* ── Attribute bars ── */
.attr-wrap { margin-bottom: 13px; }
.attr-header { display: flex; justify-content: space-between; margin-bottom: 4px; }
.attr-name { font-size: 13px; color: #94a3b8; }
.attr-val  { font-size: 13px; font-weight: 700; }
.bar-bg   { background: #0D1B2A; border-radius: 6px; height: 10px; overflow: hidden;
            border: 1px solid #1BE7FF11; }
.bar-fill { height: 10px; border-radius: 6px; }

/* ── Profile ── */
.profile-card { display: flex; align-items: center; justify-content: space-between; }
.profile-label { font-size: 11px; color: #8980F5; text-transform: uppercase; letter-spacing: 1px; }
.profile-name  { font-size: 22px; font-weight: 800; }
.pct-item { font-size: 13px; margin-bottom: 4px; }

/* ── Page header ── */
.page-header { color: #1BE7FF; font-size: 20px; font-weight: 800;
               letter-spacing: 2px; margin-bottom: 14px;
               border-bottom: 2px solid #1BE7FF33;
               padding-bottom: 8px; }

/* ── Buttons ── */
.stButton > button {
    background: #0D1B2A !important; color: #1BE7FF !important;
    border: 1px solid #1BE7FF44 !important; border-radius: 8px !important;
    font-size: 13px !important; transition: all .2s !important;
}
.stButton > button:hover {
    background: #1BE7FF !important; color: #0D1B2A !important;
    border-color: #1BE7FF !important; font-weight: 700 !important;
}

/* ── Inputs ── */
.stSelectbox > div > div,
.stTextInput > div > div {
    background: #0D1B2A !important; border: 1px solid #1BE7FF33 !important;
    color: #cbd5e1 !important; border-radius: 8px !important;
}
.stCheckbox label { color: #cbd5e1 !important; }
hr { border-color: #1BE7FF22 !important; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D1B2A; }
::-webkit-scrollbar-thumb { background: #1BE7FF44; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── PLAYERS DATABASE ────────────────────────────────────────────────────────
PLAYERS = {
    "Adriano Martins": {
        "club": "Atlético GO",        "position": "Zagueiro",
        "year": 1998,                 "nationality": "🇧🇷 Brazil",
        "height": 193,                "foot": "Destro",
        "minutes": 1955,              "goals": 2,     "assists": 0,
        "rating": 6.4,  "rank": 52,
        "combativo": 5.8, "combativo_rank": 71,
        "construtor": 6.9, "construtor_rank": 39,
        "posicional": 6.8, "posicional_rank": 48,
        "profile": "Híbrido",
        "pct_combativo": 21, "pct_construtor": 41, "pct_posicional": 39,
        "construcao": 43, "ofensividade": 77, "um_vs_um": 5,
        "contencao": 78, "duelo_aereo": 14,
        "aspect_def":   ["❌ Confrontos", "Duelos Aéreos", "🥉 Intervenções"],
        "aspect_off":   ["🥉 Ball Security", "🥉 Progressão"],
        "aspect_const": ["Passes Verticais", "🥉 PCF*", "❌ Passes Longos"],
    },
    "Rafael Sousa": {
        "club": "Fluminense",         "position": "Zagueiro",
        "year": 1995,                 "nationality": "🇧🇷 Brazil",
        "height": 188,                "foot": "Destro",
        "minutes": 2340,              "goals": 1,     "assists": 2,
        "rating": 7.1,  "rank": 18,
        "combativo": 7.3, "combativo_rank": 12,
        "construtor": 6.8, "construtor_rank": 22,
        "posicional": 7.2, "posicional_rank": 15,
        "profile": "Combativo",
        "pct_combativo": 58, "pct_construtor": 22, "pct_posicional": 20,
        "construcao": 61, "ofensividade": 45, "um_vs_um": 82,
        "contencao": 88, "duelo_aereo": 79,
        "aspect_def":   ["✅ Confrontos", "✅ Duelos Aéreos", "Intervenções"],
        "aspect_off":   ["Ball Security", "Progressão"],
        "aspect_const": ["Passes Verticais", "PCF*", "Passes Longos"],
    },
    "Lucas Ferreira": {
        "club": "Grêmio",             "position": "Zagueiro",
        "year": 2000,                 "nationality": "🇧🇷 Brazil",
        "height": 185,                "foot": "Canhoto",
        "minutes": 1780,              "goals": 0,     "assists": 1,
        "rating": 6.7,  "rank": 35,
        "combativo": 6.2, "combativo_rank": 48,
        "construtor": 7.1, "construtor_rank": 20,
        "posicional": 6.5, "posicional_rank": 41,
        "profile": "Construtor",
        "pct_combativo": 20, "pct_construtor": 55, "pct_posicional": 25,
        "construcao": 82, "ofensividade": 65, "um_vs_um": 31,
        "contencao": 55, "duelo_aereo": 40,
        "aspect_def":   ["Confrontos", "Duelos Aéreos", "🥉 Intervenções"],
        "aspect_off":   ["🥉 Ball Security", "✅ Progressão"],
        "aspect_const": ["✅ Passes Verticais", "🥉 PCF*", "Passes Longos"],
    },
    "Marcos Oliveira": {
        "club": "Santos FC",          "position": "Zagueiro",
        "year": 1997,                 "nationality": "🇧🇷 Brazil",
        "height": 190,                "foot": "Destro",
        "minutes": 2100,              "goals": 3,     "assists": 0,
        "rating": 6.9,  "rank": 28,
        "combativo": 6.8, "combativo_rank": 30,
        "construtor": 6.5, "construtor_rank": 44,
        "posicional": 7.0, "posicional_rank": 25,
        "profile": "Posicional",
        "pct_combativo": 25, "pct_construtor": 30, "pct_posicional": 45,
        "construcao": 55, "ofensividade": 50, "um_vs_um": 60,
        "contencao": 70, "duelo_aereo": 65,
        "aspect_def":   ["Confrontos", "✅ Duelos Aéreos", "Intervenções"],
        "aspect_off":   ["Ball Security", "Progressão"],
        "aspect_const": ["Passes Verticais", "PCF*", "🥉 Passes Longos"],
    },
    "Pedro Alves": {
        "club": "Vasco da Gama",      "position": "Zagueiro",
        "year": 1996,                 "nationality": "🇧🇷 Brazil",
        "height": 186,                "foot": "Destro",
        "minutes": 1600,              "goals": 1,     "assists": 0,
        "rating": 6.2,  "rank": 61,
        "combativo": 5.5, "combativo_rank": 78,
        "construtor": 6.4, "construtor_rank": 50,
        "posicional": 6.5, "posicional_rank": 42,
        "profile": "Híbrido",
        "pct_combativo": 28, "pct_construtor": 38, "pct_posicional": 34,
        "construcao": 50, "ofensividade": 40, "um_vs_um": 22,
        "contencao": 60, "duelo_aereo": 35,
        "aspect_def":   ["❌ Confrontos", "Duelos Aéreos", "Intervenções"],
        "aspect_off":   ["Ball Security", "Progressão"],
        "aspect_const": ["Passes Verticais", "PCF*", "❌ Passes Longos"],
    },
    "Diego Nascimento": {
        "club": "Sport Recife",       "position": "Zagueiro",
        "year": 2001,                 "nationality": "🇧🇷 Brazil",
        "height": 182,                "foot": "Canhoto",
        "minutes": 1200,              "goals": 0,     "assists": 1,
        "rating": 6.0,  "rank": 68,
        "combativo": 5.7, "combativo_rank": 73,
        "construtor": 6.2, "construtor_rank": 59,
        "posicional": 6.0, "posicional_rank": 65,
        "profile": "Construtor",
        "pct_combativo": 18, "pct_construtor": 52, "pct_posicional": 30,
        "construcao": 75, "ofensividade": 60, "um_vs_um": 15,
        "contencao": 48, "duelo_aereo": 20,
        "aspect_def":   ["Confrontos", "❌ Duelos Aéreos", "Intervenções"],
        "aspect_off":   ["🥉 Ball Security", "🥉 Progressão"],
        "aspect_const": ["✅ Passes Verticais", "PCF*", "Passes Longos"],
    },
    "Thiago Campos": {
        "club": "Ceará SC",           "position": "Zagueiro",
        "year": 1999,                 "nationality": "🇧🇷 Brazil",
        "height": 191,                "foot": "Destro",
        "minutes": 2250,              "goals": 2,     "assists": 0,
        "rating": 6.6,  "rank": 40,
        "combativo": 6.5, "combativo_rank": 45,
        "construtor": 6.3, "construtor_rank": 55,
        "posicional": 6.8, "posicional_rank": 32,
        "profile": "Posicional",
        "pct_combativo": 30, "pct_construtor": 28, "pct_posicional": 42,
        "construcao": 48, "ofensividade": 52, "um_vs_um": 55,
        "contencao": 72, "duelo_aereo": 68,
        "aspect_def":   ["Confrontos", "✅ Duelos Aéreos", "🥉 Intervenções"],
        "aspect_off":   ["Ball Security", "Progressão"],
        "aspect_const": ["Passes Verticais", "🥉 PCF*", "Passes Longos"],
    },
    "Bruno Lima": {
        "club": "Fortaleza EC",       "position": "Zagueiro",
        "year": 1994,                 "nationality": "🇧🇷 Brazil",
        "height": 195,                "foot": "Destro",
        "minutes": 2700,              "goals": 4,     "assists": 1,
        "rating": 7.3,  "rank": 8,
        "combativo": 7.5, "combativo_rank": 5,
        "construtor": 6.9, "construtor_rank": 21,
        "posicional": 7.0, "posicional_rank": 22,
        "profile": "Combativo",
        "pct_combativo": 62, "pct_construtor": 20, "pct_posicional": 18,
        "construcao": 55, "ofensividade": 40, "um_vs_um": 90,
        "contencao": 92, "duelo_aereo": 88,
        "aspect_def":   ["✅ Confrontos", "✅ Duelos Aéreos", "✅ Intervenções"],
        "aspect_off":   ["Ball Security", "Progressão"],
        "aspect_const": ["Passes Verticais", "PCF*", "❌ Passes Longos"],
    },
    "Gustavo Pereira": {
        "club": "Botafogo",           "position": "Zagueiro",
        "year": 2002,                 "nationality": "🇧🇷 Brazil",
        "height": 184,                "foot": "Canhoto",
        "minutes": 900,               "goals": 0,     "assists": 0,
        "rating": 5.8,  "rank": 75,
        "combativo": 5.3, "combativo_rank": 76,
        "construtor": 6.0, "construtor_rank": 67,
        "posicional": 5.9, "posicional_rank": 71,
        "profile": "Híbrido",
        "pct_combativo": 33, "pct_construtor": 33, "pct_posicional": 34,
        "construcao": 40, "ofensividade": 35, "um_vs_um": 30,
        "contencao": 45, "duelo_aereo": 25,
        "aspect_def":   ["❌ Confrontos", "Duelos Aéreos", "Intervenções"],
        "aspect_off":   ["Ball Security", "Progressão"],
        "aspect_const": ["Passes Verticais", "❌ PCF*", "Passes Longos"],
    },
    "André Rocha": {
        "club": "Athletico-PR",       "position": "Zagueiro",
        "year": 1993,                 "nationality": "🇧🇷 Brazil",
        "height": 189,                "foot": "Destro",
        "minutes": 2500,              "goals": 1,     "assists": 3,
        "rating": 7.0,  "rank": 22,
        "combativo": 6.9, "combativo_rank": 25,
        "construtor": 7.3, "construtor_rank": 11,
        "posicional": 6.9, "posicional_rank": 28,
        "profile": "Construtor",
        "pct_combativo": 22, "pct_construtor": 58, "pct_posicional": 20,
        "construcao": 88, "ofensividade": 72, "um_vs_um": 45,
        "contencao": 65, "duelo_aereo": 50,
        "aspect_def":   ["Confrontos", "Duelos Aéreos", "🥉 Intervenções"],
        "aspect_off":   ["🥉 Ball Security", "✅ Progressão"],
        "aspect_const": ["✅ Passes Verticais", "✅ PCF*", "🥉 Passes Longos"],
    },
}

PROFILE_COLORS = {
    "Combativo": "#FE4A49",
    "Construtor": "#31E981",
    "Posicional": "#8980F5",
    "Híbrido":    "#FED766",
}

PROFILE_TEXT_DARK = {"Construtor", "Híbrido"}   # cores claras → texto escuro


# ─── SESSION STATE (fix index bug) ───────────────────────────────────────────
if "selected_player" not in st.session_state:
    st.session_state["selected_player"] = list(PLAYERS.keys())[0]


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p style="color:#1BE7FF;font-size:18px;font-weight:800;'
        'letter-spacing:2px;margin:0">⚽ SCOUT ANALYTICS</p>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        '<p style="color:#1BE7FF;font-size:11px;font-weight:700;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:6px">Filtrar Perfil</p>',
        unsafe_allow_html=True,
    )
    f_combativo  = st.checkbox("⚡ Combativo")
    f_construtor = st.checkbox("🔧 Construtor")
    f_hibrido    = st.checkbox("🔀 Híbrido")
    f_posicional = st.checkbox("📍 Posicional")

    st.divider()
    st.markdown(
        '<p style="color:#1BE7FF;font-size:11px;font-weight:700;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:6px">Jogadores</p>',
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "", placeholder="🔍 Buscar jogador...", label_visibility="collapsed"
    )

    # ── build filtered list ──────────────────────────────────────────────────
    all_names = list(PLAYERS.keys())

    active_profiles = (
        (["Combativo"]  if f_combativo  else []) +
        (["Construtor"] if f_construtor else []) +
        (["Híbrido"]    if f_hibrido    else []) +
        (["Posicional"] if f_posicional else [])
    )

    filtered = [
        n for n in all_names
        if (not search or search.lower() in n.lower()
                       or search.lower() in PLAYERS[n]["club"].lower())
        and (not active_profiles or PLAYERS[n]["profile"] in active_profiles)
    ]

    if not filtered:
        filtered = all_names   # fallback: never empty

    display_names = [f"{n} ({PLAYERS[n]['club']})" for n in filtered]

    # safe default index ──────────────────────────────────────────────────────
    cur = st.session_state["selected_player"]
    if cur in filtered:
        default_idx = filtered.index(cur)
    else:
        default_idx = 0

    chosen_disp = st.selectbox(
        "", display_names,
        index=default_idx,
        label_visibility="collapsed",
    )
    selected_player = filtered[display_names.index(chosen_disp)]
    st.session_state["selected_player"] = selected_player   # persist choice

    st.divider()
    st.markdown(
        '<p style="color:#1BE7FF;font-size:11px;font-weight:700;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:6px">Navegação</p>',
        unsafe_allow_html=True,
    )
    for nav in ["🛡️ Zagueiros", "🏃 Laterais", "⚙️ Meio-campistas",
                "💨 Extremos", "🎯 Meias Ofensivos", "⚡ Atacantes"]:
        st.button(nav, use_container_width=True, key=f"nav_{nav}")

    st.divider()
    st.markdown(
        '<p style="color:#475569;font-size:12px">👥 Jogadores Analisados: '
        '<span style="color:#1BE7FF;font-weight:700">78</span></p>',
        unsafe_allow_html=True,
    )


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def tags_html(items: list) -> str:
    return "".join(f'<span class="aspect-tag">{i}</span>' for i in items)


def attr_bar(label: str, value: int) -> str:
    if value >= 70:
        color = "#31E981"
    elif value >= 40:
        color = "#FED766"
    else:
        color = "#FE4A49"
    return f"""
    <div class="attr-wrap">
      <div class="attr-header">
        <span class="attr-name">{label}</span>
        <span class="attr-val" style="color:{color}">{value}</span>
      </div>
      <div class="bar-bg">
        <div class="bar-fill" style="background:{color};width:{value}%"></div>
      </div>
    </div>"""


# ─── MAIN CONTENT ────────────────────────────────────────────────────────────
p  = PLAYERS[selected_player]
pc = PROFILE_COLORS.get(p["profile"], "#1BE7FF")
text_color = "#0D1B2A" if p["profile"] in PROFILE_TEXT_DARK else "#fff"

st.markdown(
    f'<div class="page-header">📊 ANÁLISE DE JOGADORES — {p["position"].upper()}S</div>',
    unsafe_allow_html=True,
)

# ── ROW 1 ─────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 2, 3], gap="medium")

# ── Player card ────────────────────────────────────────────────────────────���──
with col1:
    st.markdown(f"""
    <div class="card">
      <div class="player-name">{selected_player}</div>
      <div class="player-pos">{p['position']}</div>
      <div class="player-club">{p['club']}</div>

      <div class="info-row">
        <div class="info-cell">
          <div class="ic-label">Ano</div>
          <div class="ic-val">{p['year']}</div>
        </div>
        <div class="info-cell">
          <div class="ic-label">Nac.</div>
          <div class="ic-val">{p['nationality']}</div>
        </div>
      </div>
      <div class="info-row">
        <div class="info-cell">
          <div class="ic-label">Altura</div>
          <div class="ic-val">{p['height']} cm</div>
        </div>
        <div class="info-cell">
          <div class="ic-label">Pé Dom.</div>
          <div class="ic-val">{p['foot']}</div>
        </div>
      </div>

      <div class="stat-row">
        <div class="stat-box" style="flex:2">
          <div class="sv">{p['minutes']}</div>
          <div class="sl">Minutagem</div>
        </div>
        <div class="stat-box">
          <div class="sv">{p['goals']}</div>
          <div class="sl">Gols</div>
        </div>
        <div class="stat-box">
          <div class="sv">{p['assists']}</div>
          <div class="sl">Assist.</div>
        </div>
      </div>

      <div style="margin-top:14px;text-align:center">
        <span style="background:{pc};color:{text_color};font-weight:800;font-size:13px;
                     border-radius:20px;padding:5px 20px;letter-spacing:1px">
          {p['profile']}
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Ratings card ──────────────────────────────────────────────────��───────────
with col2:
    st.markdown(f"""
    <div class="card">
      <div class="r-label">⭐ RATING GERAL <small style="color:#1BE7FF44">(Rank)</small></div>
      <div class="rating-row" style="margin-bottom:14px">
        <div class="r-badge main">{p['rating']}</div>
        <div class="rank-tag">#{p['rank']}</div>
      </div>

      <div style="background:#0D1B2A;border-radius:10px;padding:14px;
                  border:1px solid #1BE7FF11">
        <div class="r-label">⚡ COMBATIVO</div>
        <div class="rating-row" style="margin-bottom:12px">
          <div class="r-badge comb">{p['combativo']}</div>
          <div class="rank-tag">#{p['combativo_rank']}</div>
        </div>

        <div class="r-label">🔧 CONSTRUTOR</div>
        <div class="rating-row" style="margin-bottom:12px">
          <div class="r-badge cons">{p['construtor']}</div>
          <div class="rank-tag">#{p['construtor_rank']}</div>
        </div>

        <div class="r-label">📍 POSICIONAL</div>
        <div class="rating-row">
          <div class="r-badge posi">{p['posicional']}</div>
          <div class="rank-tag">#{p['posicional_rank']}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Aspects card ──────────────────────────────────────────────────────────────
with col3:
    st.markdown(f"""
    <div class="card">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px">
        <div>
          <div class="section-title" style="color:#FE4A49">⚔️ Aspectos Defensivos</div>
          {tags_html(p['aspect_def'])}
        </div>
        <div>
          <div class="section-title" style="color:#31E981">🚀 Aspectos Ofensivos</div>
          {tags_html(p['aspect_off'])}
        </div>
      </div>
      <div style="border-top:1px solid #1BE7FF22;padding-top:14px">
        <div class="section-title" style="color:#1BE7FF">🔧 Aspectos de Construção</div>
        {tags_html(p['aspect_const'])}
        <div style="font-size:10px;color:#475569;margin-top:8px">
          *PCF = Passes Construtores Finais
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── ROW 2 ───────��─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col4, col5 = st.columns([3, 2], gap="medium")

# ── Radar + profile ───────────────────────────────────────────────────────────
with col4:
    st.markdown(f"""
    <div class="card" style="margin-bottom:8px">
      <div class="profile-card">
        <div>
          <div class="profile-label">Perfil Identificado</div>
          <div class="profile-name" style="color:{pc}">{p['profile']}</div>
        </div>
        <div>
          <div class="pct-item" style="color:#FE4A49">
            ⚡ Combativo &nbsp;<b>{p['pct_combativo']}%</b>
          </div>
          <div class="pct-item" style="color:#31E981">
            🔧 Construtor &nbsp;<b>{p['pct_construtor']}%</b>
          </div>
          <div class="pct-item" style="color:#8980F5">
            📍 Posicional &nbsp;<b>{p['pct_posicional']}%</b>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cats = ["Combativo", "Construtor", "Posicional"]
    vals = [p["pct_combativo"], p["pct_construtor"], p["pct_posicional"]]

    fig = go.Figure()
    # Background fill layers for visual depth
    for level, alpha in [(75, 0.04), (50, 0.06), (25, 0.08)]:
        fig.add_trace(go.Scatterpolar(
            r=[level] * 4,
            theta=cats + [cats[0]],
            fill="toself",
            fillcolor=f"rgba(27,231,255,{alpha})",
            line=dict(color="rgba(27,231,255,0.1)", width=0.5),
            hoverinfo="skip", showlegend=False,
        ))

    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        fill="toself",
        fillcolor=f"rgba({int(pc[1:3],16)},{int(pc[3:5],16)},{int(pc[5:7],16)},0.18)",
        line=dict(color=pc, width=3),
        mode="lines+markers",
        marker=dict(size=8, color=pc, line=dict(color="#0D1B2A", width=2)),
        hovertemplate="<b>%{theta}</b>: %{r}%<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(13,27,42,0.95)",
            radialaxis=dict(
                visible=True, range=[0, 75],
                tickvals=[15, 30, 45, 60, 75],
                tickfont=dict(color="#1BE7FF66", size=9),
                gridcolor="#1BE7FF22", linecolor="#1BE7FF22",
            ),
            angularaxis=dict(
                tickfont=dict(color="#e2e8f0", size=14),
                gridcolor="#1BE7FF22", linecolor="#1BE7FF22",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=40, b=40, l=60, r=60),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Attribute bars ────────────────────────────────────────────────────────────
with col5:
    bars = (
        attr_bar("Construção",       p["construcao"])   +
        attr_bar("Ofensividade",     p["ofensividade"]) +
        attr_bar("1vs1 – Defensivo", p["um_vs_um"])     +
        attr_bar("Contenção",        p["contencao"])    +
        attr_bar("Duelo Aéreo",      p["duelo_aereo"])
    )
    st.markdown(f"""
    <div class="card">
      <div class="section-title"
           style="color:#1BE7FF;margin-bottom:18px;font-size:12px;letter-spacing:1px">
        📊 ATRIBUTOS FÍSICO-TÁTICOS
      </div>
      {bars}
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#1BE7FF33;font-size:12px;letter-spacing:1px">'
    '⚽ Scout Analytics · Dados da Temporada 2025 · 78 Jogadores Analisados'
    '</div>',
    unsafe_allow_html=True,
)
