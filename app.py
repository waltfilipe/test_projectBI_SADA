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
            ("Duelo Aero", 31, "#FE4A49"),
        ],
    },
}

# CSS — build as plain string, no f-string, then format() to inject colors
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
    border-right: 1px solid CYAN_COLOR33;
}
section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}
.block-container {
    padding: 0.5rem 1rem 1rem !important;
    max-width: 100% !important;
}
#MainMenu, footer, header {
    visibility: hidden;
}
.stButton > button {
    background: CARD_COLOR;
    color: TEXT_COLOR;
    border: 1px solid BORDER_COLOR;
    border-radius: 7px;
    width: 100%;
    font-size: 0.79rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    padding: 0.38rem;
    transition: all 0.15s ease;
    margin-bottom: 2px;
}
.stButton > button:hover {
    background: CYAN_COLOR16;
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


def rating_pill(label, value, rank, pill_color):
    h  = '<div style="background:' + DARK + ';border:1px solid ' + BORDER + ';border-radius:8px;'
    h += 'padding:0.42rem 0.65rem;margin-bottom:0.38rem;">'
    h += '<div style="font-size:0.56rem;font-weight:600;letter-spacing:0.13em;'
    h += 'text-transform:uppercase;color:' + MUTED + ';">' + str(label) + '</div>'
    h += '<div style="display:flex;align-items:center;gap:0.45rem;margin-top:0.14rem;">'
    h += '<div style="background:' + pill_color + ';color:#fff;border-radius:5px;'
    h += 'padding:0.05rem 0.5rem;font-size:1.15rem;font-weight:800;">' + str(value) + '</div>'
    h += '<div style="font-size:0.8rem;font-weight:700;color:' + MUTED + ';">#' + str(rank) + '</div>'
    h += '</div></div>'
    return h


def asp_section_html(title, items):
    h  = '<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
    h += 'text-transform:uppercase;color:' + CYAN + ';padding-bottom:0.2rem;'
    h += 'border-bottom:1px solid ' + CYAN + '44;margin-bottom:0.35rem;">' + title + '</div>'
    for name_, ico in items:
        h += '<div style="display:flex;align-items:center;gap:0.4rem;padding:0.22rem 0;'
        h += 'font-size:0.76rem;color:' + TEXT + ';border-bottom:1px solid ' + BORDER + '44;">'
        h += icon_html(ico) + '<span>' + name_ + '</span></div>'
    return h


def bar_html(label, value, color):
    pct = min(max(int(value), 0), 100)
    h  = '<div style="margin-bottom:0.62rem;">'
    h += '<div style="font-size:0.68rem;color:' + MUTED + ';font-weight:500;margin-bottom:0.12rem;">' + label + '</div>'
    h += '<div style="display:flex;align-items:center;gap:0.42rem;">'
    h += '<div style="flex:1;height:7px;background:' + DARK + ';border-radius:3px;'
    h += 'overflow:hidden;border:1px solid ' + BORDER + '55;">'
    h += '<div style="height:100%;width:' + str(pct) + '%;background:' + color + ';border-radius:3px;'
    h += 'box-shadow:0 0 6px ' + color + '55;"></div>'
    h += '</div>'
    h += '<div style="font-size:0.68rem;font-weight:700;color:#fff;min-width:20px;'
    h += 'text-align:right;">' + str(value) + '</div>'
    h += '</div></div>'
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


# SIDEBAR
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
    lbl3 += 'text-transform:uppercase;color:' + CYAN + ';margin-bottom:0.2rem;">Navegacao</div>'
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


# LOAD PLAYER
p = PLAYERS[player_key]


# HEADER BAR
hdr  = '<div style="background:' + DARK + ';border-bottom:1px solid ' + CYAN + '22;'
hdr += 'padding:0.35rem 0.2rem;display:flex;justify-content:space-between;'
hdr += 'align-items:center;margin-bottom:0.7rem;">'
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


# MAIN COLUMNS
c1, c2, c3, c4, c5 = st.columns([2.0, 1.5, 2.1, 1.75, 2.0], gap="small")


# C1 — PLAYER CARD
with c1:
    card  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:1rem;height:100%;">'

    # Avatar
    card += '<div style="text-align:center;margin-bottom:0.7rem;">'
    card += '<div style="display:inline-flex;align-items:center;justify-content:center;'
    card += 'width:72px;height:72px;border-radius:50%;'
    card += 'background:linear-gradient(135deg,' + BORDER + ',' + DARK + ');'
    card += 'border:2px solid ' + CYAN + '44;font-size:2.4rem;line-height:1;">&#x1F464;</div>'
    card += '</div>'

    # Name / position / club
    card += '<div style="text-align:center;margin-bottom:0.8rem;">'
    card += '<div style="font-size:1.32rem;font-weight:800;color:#fff;letter-spacing:-0.01em;line-height:1.15;">' + p["name"] + '</div>'
    card += '<div style="font-size:0.75rem;color:' + MUTED + ';margin-top:0.18rem;">' + p["position"] + '</div>'
    card += '<div style="font-size:0.8rem;font-weight:600;color:' + CYAN + ';margin-top:0.1rem;">' + p["club"] + '</div>'
    card += '</div>'

    # Bio grid
    card += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.35rem;margin-bottom:0.75rem;">'
    bio_items = [
        ("Ano",         MUTED, str(p["year"])),
        ("Nacionalidade", CYAN,  p["nat"]),
        ("Altura",      MUTED, str(p["height"]) + " cm"),
        ("Pe dominante", CYAN,  p["foot"]),
    ]
    for bio_lbl, bio_col, bio_val in bio_items:
        card += '<div style="background:' + DARK + ';border:1px solid ' + BORDER + '55;border-radius:6px;padding:0.3rem 0.45rem;">'
        card += '<div style="font-size:0.55rem;color:' + bio_col + ';text-transform:uppercase;letter-spacing:0.1em;">' + bio_lbl + '</div>'
        card += '<div style="font-size:0.88rem;font-weight:700;color:#fff;">' + bio_val + '</div>'
        card += '</div>'
    card += '</div>'

    # Stats strip
    card += '<div style="background:' + DARK + ';border:1px solid ' + BORDER + ';border-radius:8px;padding:0.55rem 0.6rem;">'
    card += '<div style="display:flex;justify-content:space-between;margin-bottom:0.28rem;">'
    for stat_lbl in ["Minutagem", "Gols", "Assist."]:
        card += '<span style="font-size:0.55rem;color:' + MUTED + ';text-transform:uppercase;letter-spacing:0.1em;">' + stat_lbl + '</span>'
    card += '</div>'
    card += '<div style="display:flex;justify-content:space-between;align-items:baseline;">'
    for stat_val in [str(p["min"]), str(p["goals"]), str(p["ast"])]:
        card += '<span style="font-size:1.55rem;font-weight:900;color:#fff;">' + stat_val + '</span>'
    card += '</div></div>'
    card += '</div>'

    st.markdown(card, unsafe_allow_html=True)


# C2 — RATINGS
with c2:
    rtg  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.9rem;height:100%;">'
    rtg += '<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
    rtg += 'text-transform:uppercase;color:' + CYAN + ';padding-bottom:0.2rem;'
    rtg += 'border-bottom:1px solid ' + CYAN + '44;margin-bottom:0.55rem;">Ratings</div>'

    # Rating Geral
    rtg += '<div style="background:' + DARK + ';border:1px solid ' + BORDER + ';border-radius:8px;padding:0.48rem 0.65rem;margin-bottom:0.42rem;">'
    rtg += '<div style="font-size:0.56rem;font-weight:600;letter-spacing:0.13em;text-transform:uppercase;color:' + MUTED + ';">'
    rtg += 'Rating Geral <span style="color:' + CYAN + ';font-size:0.48rem;">(Rank)</span></div>'
    rtg += '<div style="display:flex;align-items:center;gap:0.45rem;margin-top:0.14rem;">'
    rtg += '<div style="background:' + RED + ';color:#fff;border-radius:5px;padding:0.05rem 0.55rem;font-size:1.45rem;font-weight:800;">' + str(p["rtg"]) + '</div>'
    rtg += '<div style="font-size:0.9rem;font-weight:700;color:' + MUTED + ';">#' + str(p["rnk"]) + '</div>'
    rtg += '</div></div>'

    rtg += rating_pill("Combativo",  p["comb"], p["r_comb"], PURPLE)
    rtg += rating_pill("Construtor", p["cons"], p["r_cons"], "#1a4a6e")
    rtg += rating_pill("Posicional", p["posi"], p["r_posi"], "#1a4a3e")
    rtg += "</div>"

    st.markdown(rtg, unsafe_allow_html=True)


# C3 — RADAR
with c3:
    rc  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.75rem 0.9rem 0.2rem;">'
    rc += '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
    rc += '<div>'
    rc += '<div style="font-size:0.58rem;color:' + MUTED + ';text-transform:uppercase;letter-spacing:0.14em;font-weight:600;">Perfil</div>'
    rc += '<div style="font-size:1.45rem;font-weight:800;color:#fff;letter-spacing:-0.01em;">' + p["profile"] + '</div>'
    rc += '</div>'
    rc += '<div style="text-align:right;">'
    rc += '<div style="font-size:0.73rem;font-weight:700;color:' + RED   + ';">Combativo '  + str(p["p_comb"]) + '%</div>'
    rc += '<div style="font-size:0.73rem;font-weight:700;color:' + GREEN + ';">Construtor ' + str(p["p_cons"]) + '%</div>'
    rc += '<div style="font-size:0.73rem;font-weight:700;color:' + CYAN  + ';">Posicional ' + str(p["p_posi"]) + '%</div>'
    rc += '</div></div></div>'
    st.markdown(rc, unsafe_allow_html=True)
    st.plotly_chart(build_radar(p), use_container_width=True, config={"displayModeBar": False})


# C4 — ASPECTOS
with c4:
    asp  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.85rem;height:100%;">'
    asp += asp_section_html("Aspectos Defensivos", p["def_asp"])
    asp += '<div style="margin:0.55rem 0;border-top:1px solid ' + BORDER + '55;"></div>'
    asp += asp_section_html("Aspectos de Construcao", p["con_asp"])
    asp += '<div style="margin-top:0.3rem;font-size:0.55rem;color:' + MUTED + ';">*Passes Construtores Finais</div>'
    asp += '</div>'
    st.markdown(asp, unsafe_allow_html=True)


# C5 — OFENSIVOS + BARS
with c5:
    off  = '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.85rem;">'
    off += asp_section_html("Aspectos Ofensivos", p["off_asp"])
    off += '</div>'
    off += '<div style="margin:0.45rem 0;"></div>'
    off += '<div style="background:' + CARD + ';border:1px solid ' + BORDER + ';border-radius:12px;padding:0.85rem;">'
    off += '<div style="font-size:0.58rem;font-weight:700;letter-spacing:0.16em;'
    off += 'text-transform:uppercase;color:' + CYAN + ';padding-bottom:0.2rem;'
    off += 'border-bottom:1px solid ' + CYAN + '44;margin-bottom:0.55rem;">Metricas</div>'
    for lbl, val, col in p["bars"]:
        off += bar_html(lbl, val, col)
    off += "</div>"
    st.markdown(off, unsafe_allow_html=True)
