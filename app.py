import streamlit as st
import plotly.graph_objects as go

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
# 0–5: dark red → orange
# 5–8: orange → dark green
# 8–10: dark green → dark blue
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
        return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
    elif v <= 8.0:
        t = (v - 5.0) / 3.0
        r = int(200 - (200 - 20)  * t)
        g = int(60  + (130 - 60)  * t)
        b = int(20  + (60  - 20)  * t)
        return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
    else:
        t = (v - 8.0) / 2.0
        r = int(20  - (20  - 10)  * t)
        g = int(130 - (130 - 60)  * t)
        b = int(60  + (160 - 60)  * t)
        return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"


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

*, *::before, *::after {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}
.stApp {
    background-color: BG_COLOR;
    color: TEXT_COLOR;
}
section[data-testid="stSidebar"] {
    background: DARK_COLOR !important;
    border-right: 1px solid rgba(27,231,255,0.13);
}
section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}
.block-container {
    padding: 0.4rem 1rem 1rem !important;
    max-width: 100% !important;
}
#MainMenu, footer, header {
    visibility: hidden;
}
/* Navigation buttons — centered */
div[data-testid="stSidebar"] .stButton > button {
    background: CARD_COLOR;
    color: TEXT_COLOR;
    border: 1px solid BORDER_COLOR;
    border-radius: 7px;
    width: 100%;
    font-size: 0.79rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    padding: 0.38rem 0.2rem;
    transition: all 0.15s ease;
    margin-bottom: 2px;
    text-align: center !important;
    justify-content: center !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(27,231,255,0.07);
    border-color: CYAN_COLOR;
    color: CYAN_COLOR;
}
div[data-testid="stCheckbox"] label span {
    color: MUTED_COLOR !important;
    font-size: 0.82rem !important;
}
div[data-testid="stTextInput"] input {
    background: DARK_COLOR !important;
    border: 1px solid BORDER_COLOR !important;
    color: TEXT_COLOR !important;
    border-radius: 7px !important;
    font-size: 0.82rem !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: DARK_COLOR !important;
    border-color: BORDER_COLOR !important;
    color: TEXT_COLOR !important;
    border-radius: 7px !important;
    font-size: 0.82rem !important;
}
hr {
    border-color: BORDER_COLOR;
    opacity: 0.45;
    margin: 0.4rem 0;
}
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: DARK_COLOR; }
::-webkit-scrollbar-thumb { background: BORDER_COLOR; border-radius: 10px; }
</style>
"""

css = CSS_TEMPLATE
css = css.replace("BG_COLOR",     BG)
css = css.replace("TEXT_COLOR",   TEXT)
css = css.replace("DARK_COLOR",   DARK)
css = css.replace("CYAN_COLOR",   CYAN)
css = css.replace("CARD_COLOR",   CARD)
css = css.replace("BORDER_COLOR", BORDER)
css = css.replace("MUTED_COLOR",  MUTED)
st.markdown(css, unsafe_allow_html=True)


# HELPERS

def icon_html(k):
    if k == "X":
        return '<span style="color:' + RED + ';font-weight:800;font-size:0.85rem;">X</span>'
    if k == "G":
        return '<span style="font-size:0.9rem;">&#x1F947;</span>'
    if k == "S":
        return '<span style="font-size:0.9rem;">&#x1F948;</span>'
    return '<span style="color:' + BORDER + ';font-size:0.88rem;">-</span>'


def section_title(label):
    h  = '<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
    h += 'text-transform:uppercase;color:' + CYAN + ';padding-bottom:0.2rem;'
    h += 'border-bottom:1px solid rgba(27,231,255,0.25);margin-bottom:0.4rem;">' + label + '</div>'
    return h


def rating_pill(label, value, rank):
    col = rating_color(value)
    h  = '<div style="background:' + DARK + ';border:1px solid ' + BORDER + ';border-radius:8px;'
    h += 'padding:0.38rem 0.6rem;margin-bottom:0.32rem;">'
    h += '<div style="font-size:0.54rem;font-weight:600;letter-spacing:0.12em;'
    h += 'text-transform:uppercase;color:' + MUTED + ';">' + str(label) + '</div>'
    h += '<div style="display:flex;align-items:center;gap:0.4rem;margin-top:0.1rem;">'
    h += '<div style="background:' + col + ';color:#fff;border-radius:5px;'
    h += 'padding:0.04rem 0.5rem;font-size:1.1rem;font-weight:800;'
    h += 'min-width:46px;text-align:center;">' + str(value) + '</div>'
    h += '<div style="font-size:0.75rem;font-weight:700;color:' + MUTED + ';">#' + str(rank) + '</div>'
    h += '</div></div>'
    return h


def asp_section_html(title, items):
    h  = section_title(title)
    for name_, ico in items:
        h += '<div style="display:flex;align-items:center;gap:0.4rem;padding:0.2rem 0;'
        h += 'font-size:0.76rem;color:' + TEXT + ';border-bottom:1px solid rgba(26,58,92,0.45);">'
        h += icon_html(ico) + '<span>' + name_ + '</span></div>'
    return h


def bar_html(label, value, color):
    pct = min(max(int(value), 0), 100)
    h  = '<div style="margin-bottom:0.58rem;">'
    h += '<div style="font-size:0.67rem;color:' + MUTED + ';font-weight:500;margin-bottom:0.1rem;">' + label + '</div>'
    h += '<div style="display:flex;align-items:center;gap:0.4rem;">'
    h += '<div style="flex:1;height:7px;background:' + DARK + ';border-radius:3px;overflow:hidden;'
    h += 'border:1px solid rgba(26,58,92,0.6);">'
    h += '<div style="height:100%;width:' + str(pct) + '%;background:' + color + ';border-radius:3px;"></div>'
    h += '</div>'
    h += '<div style="font-size:0.67rem;font-weight:700;color:#fff;min-width:22px;text-align:right;">' + str(value) + '</div>'
    h += '</div></div>'
    return h


def profile_pct_bar(label, pct, color):
    """Grey bar with colored fill — for profile breakdown."""
    h  = '<div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.28rem;">'
    h += '<div style="font-size:0.7rem;color:#8090a0;width:68px;font-weight:500;">' + label + '</div>'
    h += '<div style="flex:1;height:6px;background:#1a2a3a;border-radius:3px;overflow:hidden;">'
    h += '<div style="height:100%;width:' + str(pct) + '%;background:' + color + ';border-radius:3px;"></div>'
    h += '</div>'
    h += '<div style="font-size:0.7rem;font-weight:700;color:#8090a0;min-width:28px;text-align:right;">' + str(pct) + '%</div>'
    h += '</div>'
    return h


def build_radar(p):
    cats = ["Combativo", "Construtor", "Posicional"]
    vals = [p["p_comb"], p["p_cons"], p["p_posi"]]
    fig  = go.Figure()

    for ring in [20, 40, 60, 80, 100]:
        fig.add_trace(go.Scatterpolar(
            r=[ring, ring, ring, ring],
            theta=[cats[0], cats[1], cats[2], cats[0]],
            mode="lines",
            line=dict(color=BORDER, width=0.7),
            showlegend=False, hoverinfo="skip",
        ))
    for cat in cats:
        fig.add_trace(go.Scatterpolar(
            r=[0, 100], theta=[cat, cat],
            mode="lines",
            line=dict(color=BORDER, width=1),
            showlegend=False, hoverinfo="skip",
        ))
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        fill="toself",
        fillcolor=YELLOW_FILL,
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
                gridcolor=BORDER, linecolor=BORDER,
                rotation=90, direction="counterclockwise",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=38, r=38, t=10, b=10),
        height=220,
        showlegend=False,
    )
    return fig


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    h  = '<div style="text-align:center;padding:0.85rem 0 0.45rem;">'
    h += '<div style="font-size:2rem;line-height:1;">&#x26BD;</div>'
    h += '<div style="font-size:0.55rem;letter-spacing:0.26em;color:' + CYAN + ';'
    h += 'font-weight:700;text-transform:uppercase;margin-top:0.22rem;">'
    h += 'Scout Intelligence</div></div>'
    st.markdown(h, unsafe_allow_html=True)
    st.divider()

    lbl  = '<div style="font-size:0.57rem;font-weight:700;letter-spacing:0.18em;'
    lbl += 'text-transform:uppercase;color:' + CYAN + ';margin-bottom:0.15rem;">Perfil</div>'
    st.markdown(lbl, unsafe_allow_html=True)
    st.checkbox("Combativo",  key="f_comb", value=False)
    st.checkbox("Construtor", key="f_cons", value=False)
    st.checkbox("Hibrido",    key="f_hibr", value=True)
    st.checkbox("Posicional", key="f_posi", value=False)
    st.divider()

    lbl2  = '<div style="font-size:0.57rem;font-weight:700;letter-spacing:0.18em;'
    lbl2 += 'text-transform:uppercase;color:' + CYAN + ';margin-bottom:0.15rem;">Jogadores</div>'
    st.markdown(lbl2, unsafe_allow_html=True)
    st.text_input("", placeholder="Buscar jogador...", label_visibility="collapsed", key="search")
    player_key = st.selectbox("", list(PLAYERS.keys()), label_visibility="collapsed", key="player_sel")
    st.divider()

    lbl3  = '<div style="font-size:0.57rem;font-weight:700;letter-spacing:0.18em;'
    lbl3 += 'text-transform:uppercase;color:' + CYAN + ';margin-bottom:0.2rem;'
    lbl3 += 'text-align:center;">Navegacao</div>'
    st.markdown(lbl3, unsafe_allow_html=True)
    for pos in ["Zagueiros", "Laterais", "Meio-campistas", "Extremos", "Meias Ofensivos", "Atacantes"]:
        st.button(pos, key="nav_" + pos)

    st.divider()
    icons  = '<div style="display:flex;justify-content:space-around;padding:0.2rem 0;font-size:1.05rem;">'
    icons += '<span title="Inicio" style="cursor:pointer;opacity:0.75;">&#x1F3E0;</span>'
    icons += '<span title="Ajuda"  style="cursor:pointer;opacity:0.75;">&#x2753;</span>'
    icons += '<span title="Busca"  style="cursor:pointer;opacity:0.75;">&#x1F50D;</span>'
    icons += '<span title="Stats"  style="cursor:pointer;opacity:0.75;">&#x1F4CA;</span>'
    icons += '</div>'
    icons += '<div style="margin-top:0.85rem;text-align:center;font-size:0.58rem;color:' + MUTED + ';">'
    icons += 'Jogadores Analisados &nbsp;'
    icons += '<span style="color:' + CYAN + ';font-weight:700;font-size:0.68rem;">78</span>'
    icons += '</div>'
    st.markdown(icons, unsafe_allow_html=True)


# ─── LOAD PLAYER ─────────────────────────────────────────────────────────────
p = PLAYERS[player_key]


# ─── HEADER BAR ──────────────────────────────────────────────────────────────
hdr  = '<div style="background:' + DARK + ';border-bottom:1px solid rgba(27,231,255,0.13);'
hdr += 'padding:0.35rem 0.2rem;display:flex;justify-content:space-between;'
hdr += 'align-items:center;margin-bottom:0.6rem;">'
hdr += '<div style="display:flex;align-items:center;gap:0.45rem;">'
hdr += '<span style="font-size:0.72rem;">&#x26BD;</span>'
hdr += '<span style="font-size:0.57rem;letter-spacing:0.2em;color:' + CYAN + ';'
hdr += 'font-weight:700;text-transform:uppercase;">Scout Intelligence Platform</span>'
hdr += '</div>'
hdr += '<div style="display:flex;align-items:center;gap:1.1rem;">'
hdr += '<span style="font-size:0.57rem;color:' + MUTED + ';">Temporada 2025/26</span>'
hdr += '<span style="font-size:0.57rem;color:' + MUTED + ';">Brasileirao Serie A</span>'
hdr += '<div style="width:6px;height:6px;border-radius:50%;background:' + GREEN + ';'
hdr += 'box-shadow:0 0 6px ' + GREEN + ';"></div>'
hdr += '</div></div>'
st.markdown(hdr, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ROW 1 — Player card | Ratings | Aspectos Def/Cons | Aspectos Ofensivos
# ═══════════════════════════════════════════════════════════════════════════
r1c1, r1c2, r1c3, r1c4 = st.columns([2.0, 1.6, 1.9, 1.9], gap="small")

# ── R1C1: PLAYER CARD ──────────────────────────────────────────────────────
with r1c1:
    card  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.9rem;height:100%;">'

    card += '<div style="text-align:center;margin-bottom:0.6rem;">'
    card += '<div style="display:inline-flex;align-items:center;justify-content:center;'
    card += 'width:64px;height:64px;border-radius:50%;'
    card += 'background:linear-gradient(135deg,' + BORDER + ',' + DARK + ');'
    card += 'border:2px solid rgba(27,231,255,0.25);font-size:2.1rem;line-height:1;">&#x1F464;</div>'
    card += '</div>'

    card += '<div style="text-align:center;margin-bottom:0.7rem;">'
    card += '<div style="font-size:1.22rem;font-weight:800;color:#fff;letter-spacing:-0.01em;line-height:1.15;">' + p["name"] + '</div>'
    card += '<div style="font-size:0.72rem;color:' + MUTED + ';margin-top:0.14rem;">' + p["position"] + '</div>'
    card += '<div style="font-size:0.78rem;font-weight:600;color:' + CYAN + ';margin-top:0.08rem;">' + p["club"] + '</div>'
    card += '</div>'

    card += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.3rem;margin-bottom:0.65rem;">'
    bio_items = [
        ("Ano",           MUTED, str(p["year"])),
        ("Nacionalidade", CYAN,  p["nat"]),
        ("Altura",        MUTED, str(p["height"]) + " cm"),
        ("Pe dominante",  CYAN,  p["foot"]),
    ]
    for bio_lbl, bio_col, bio_val in bio_items:
        card += '<div style="background:' + DARK + ';border:1px solid rgba(26,58,92,0.5);border-radius:6px;padding:0.28rem 0.4rem;">'
        card += '<div style="font-size:0.52rem;color:' + bio_col + ';text-transform:uppercase;letter-spacing:0.1em;">' + bio_lbl + '</div>'
        card += '<div style="font-size:0.84rem;font-weight:700;color:#fff;">' + bio_val + '</div>'
        card += '</div>'
    card += '</div>'

    card += '<div style="background:' + DARK + ';border:1px solid ' + BORDER + ';border-radius:8px;padding:0.5rem 0.55rem;">'
    card += '<div style="display:flex;justify-content:space-between;margin-bottom:0.22rem;">'
    for stat_lbl in ["Minutagem", "Gols", "Assist."]:
        card += '<span style="font-size:0.52rem;color:' + MUTED + ';text-transform:uppercase;letter-spacing:0.1em;">' + stat_lbl + '</span>'
    card += '</div>'
    card += '<div style="display:flex;justify-content:space-between;align-items:baseline;">'
    for stat_val in [str(p["min"]), str(p["goals"]), str(p["ast"])]:
        card += '<span style="font-size:1.45rem;font-weight:900;color:#fff;">' + stat_val + '</span>'
    card += '</div></div>'
    card += '</div>'
    st.markdown(card, unsafe_allow_html=True)

# ── R1C2: RATINGS ──────────────────────────────────────────────────────────
with r1c2:
    rtg  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.9rem;height:100%;">'
    rtg += section_title("Ratings")

    # Rating Geral — uses gradient color
    rtg += '<div style="background:' + DARK + ';border:1px solid ' + BORDER + ';border-radius:8px;padding:0.44rem 0.6rem;margin-bottom:0.35rem;">'
    rtg += '<div style="font-size:0.53rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:' + MUTED + ';">'
    rtg += 'Rating Geral <span style="color:' + CYAN + ';font-size:0.46rem;">(Rank)</span></div>'
    rtg += '<div style="display:flex;align-items:center;gap:0.4rem;margin-top:0.1rem;">'
    rtg += '<div style="background:' + rating_color(p["rtg"]) + ';color:#fff;border-radius:5px;'
    rtg += 'padding:0.04rem 0.5rem;font-size:1.35rem;font-weight:800;min-width:52px;text-align:center;">' + str(p["rtg"]) + '</div>'
    rtg += '<div style="font-size:0.82rem;font-weight:700;color:' + MUTED + ';">#' + str(p["rnk"]) + '</div>'
    rtg += '</div></div>'

    rtg += rating_pill("Combativo",  p["comb"], p["r_comb"])
    rtg += rating_pill("Construtor", p["cons"], p["r_cons"])
    rtg += rating_pill("Posicional", p["posi"], p["r_posi"])
    rtg += "</div>"
    st.markdown(rtg, unsafe_allow_html=True)

# ── R1C3: ASPECTOS DEFENSIVOS + CONSTRUCAO ─────────────────────────────────
with r1c3:
    asp  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.85rem;height:100%;">'
    asp += asp_section_html("Aspectos Defensivos", p["def_asp"])
    asp += '<div style="margin:0.5rem 0;border-top:1px solid rgba(26,58,92,0.6);"></div>'
    asp += asp_section_html("Aspectos de Construcao", p["con_asp"])
    asp += '<div style="margin-top:0.28rem;font-size:0.52rem;color:' + MUTED + ';">*Passes Construtores Finais</div>'
    asp += '</div>'
    st.markdown(asp, unsafe_allow_html=True)

# ── R1C4: ASPECTOS OFENSIVOS ───────────────────────────────────────────────
with r1c4:
    off  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.85rem;height:100%;">'
    off += asp_section_html("Aspectos Ofensivos", p["off_asp"])
    off += '</div>'
    st.markdown(off, unsafe_allow_html=True)


st.markdown('<div style="height:0.45rem;"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ROW 2 — Radar / Perfil | Metricas (bar charts)
# ═══════════════════════════════════════════════════════════════════════════
r2c1, r2c2 = st.columns([2.2, 5.2], gap="small")

# ── R2C1: PERFIL RADAR ─────────────────────────────────────────────────────
with r2c1:
    rc  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.75rem 0.9rem 0;">'
    rc += '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
    rc += '<div>'
    rc += '<div style="font-size:0.55rem;color:' + MUTED + ';text-transform:uppercase;letter-spacing:0.13em;font-weight:600;">Perfil</div>'
    rc += '<div style="font-size:1.3rem;font-weight:800;color:#fff;letter-spacing:-0.01em;">' + p["profile"] + '</div>'
    rc += '</div>'
    rc += '<div style="text-align:right;">'
    rc += '<div style="font-size:0.68rem;font-weight:700;color:#6a7a8a;">Combativo '  + str(p["p_comb"]) + '%</div>'
    rc += '<div style="font-size:0.68rem;font-weight:700;color:#6a7a8a;">Construtor ' + str(p["p_cons"]) + '%</div>'
    rc += '<div style="font-size:0.68rem;font-weight:700;color:#6a7a8a;">Posicional ' + str(p["p_posi"]) + '%</div>'
    rc += '</div></div>'
    rc += '</div>'
    st.markdown(rc, unsafe_allow_html=True)
    st.plotly_chart(build_radar(p), use_container_width=True, config={"displayModeBar": False})

# ── R2C2: METRICAS ──────────────────────────────────────────────────────────
with r2c2:
    met  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.85rem;height:100%;">'
    met += section_title("Metricas")
    # 2-column grid for bars
    met += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.1rem 1.4rem;">'
    for lbl, val, col in p["bars"]:
        met += bar_html(lbl, val, col)
    met += '</div>'
    met += '</div>'
    st.markdown(met, unsafe_allow_html=True)
