import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG  ── must be the very first Streamlit call
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Porsche Site Selection | Wealth Intelligence",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  DESIGN TOKENS  —  Light theme, vivid accent palette
# ══════════════════════════════════════════════════════════════
# ── page / surface colours ────────────────────────────────────
BG_PAGE    = "#F5F6FA"   # page background — off-white
BG_CARD    = "#FFFFFF"   # card / chart background — pure white
BG_SURFACE = "#ECEDF3"   # sidebar, slightly raised surface
BG_BORDER  = "#D4D5E0"   # 1-px border colour

# ── text colours (dark on light) ──────────────────────────────
TXT_WHITE  = "#1A1B2E"   # headings — near-black (replaces white)
TXT_BODY   = "#3A3B50"   # body / axis tick text — dark grey
TXT_MUTED  = "#6B6C80"   # captions, secondary info

# ── accent palette — KEPT EXACTLY THE SAME vivid colours ──────
GOLD       = "#E5B94E"   # Porsche gold  → targets / highlights
CYAN       = "#0AABCC"   # electric cyan (slightly deeper for light bg)
VIOLET     = "#7C3AED"   # violet        → dividends (deeper for contrast)
CORAL      = "#EF4444"   # coral-red     → capital gains / other
SAGE       = "#16A34A"   # sage-green    → wages (deeper green)
MUTED_DOT  = "#6B7FD4"   # non-target scatter dots — indigo-blue

# ── chart infrastructure ──────────────────────────────────────
GRID_CLR   = "#E8E9F0"   # light grey gridlines
PAPER_BG   = "rgba(0,0,0,0)"

# ── categorical sequences (lines, multi-series) ───────────────
QUALITATIVE = [GOLD, CYAN, VIOLET, CORAL, SAGE,
               "#F97316", "#2563EB", "#DB2777", "#D97706", "#059669"]

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS  ── light theme with vivid accent colours
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── page background ───────────────────────────────────────── */
.stApp, .main, [data-testid="stAppViewContainer"] {{
    background-color: {BG_PAGE} !important;
}}

/* ── sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {{
    background-color: {BG_SURFACE} !important;
    border-right: 1px solid {BG_BORDER};
}}

/* ── all text dark on light background ─────────────────────── */
.stApp, .stApp p, .stApp label, .stApp span,
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stMarkdown, .stMarkdown p, .stMarkdown li,
[data-testid="stSidebar"] * {{
    color: {TXT_WHITE} !important;
}}
.stApp caption, .stApp small, [data-testid="stCaptionContainer"] p {{
    color: {TXT_MUTED} !important;
}}

/* ── tabs ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    background-color: {BG_SURFACE};
    border-radius: 10px;
    padding: 4px 6px;
    gap: 4px;
    border: 1px solid {BG_BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    color: {TXT_BODY} !important;
    border-radius: 7px;
    padding: 8px 18px;
    font-weight: 500;
    font-size: 14px;
    background: transparent;
}}
.stTabs [aria-selected="true"] {{
    background-color: {BG_CARD} !important;
    color: #C8860A !important;
    border-bottom: 2px solid {GOLD} !important;
}}

/* ── metric / KPI cards ─────────────────────────────────────── */
div[data-testid="stMetric"] {{
    background-color: {BG_CARD};
    border: 1px solid {BG_BORDER};
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}}
div[data-testid="stMetric"] label {{
    color: {TXT_MUTED} !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
div[data-testid="stMetricValue"] > div {{
    color: #B8860B !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}}
div[data-testid="stMetricDelta"] {{
    color: {SAGE} !important;
    font-size: 12px !important;
}}

/* ── dataframe / table ──────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    background-color: {BG_CARD};
    border-radius: 10px;
    border: 1px solid {BG_BORDER};
}}
[data-testid="stDataFrame"] * {{
    color: {TXT_WHITE} !important;
    background-color: transparent !important;
}}

/* ── slider track + thumb ───────────────────────────────────── */
[data-testid="stSlider"] > div > div > div > div {{
    background-color: {GOLD} !important;
}}

/* ── divider ────────────────────────────────────────────────── */
hr {{ border-color: {BG_BORDER} !important; }}

/* ── block container padding ────────────────────────────────── */
.block-container {{ padding-top: 1.8rem; padding-bottom: 2rem; }}

/* ── radio buttons ──────────────────────────────────────────── */
[data-testid="stRadio"] label {{
    color: {TXT_BODY} !important;
}}

/* ── insight callout box ────────────────────────────────────── */
.insight-box {{
    background-color: #FFFBF0;
    border-left: 3px solid {GOLD};
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 14px 0;
    font-size: 14px;
    line-height: 1.7;
    color: {TXT_BODY};
}}
.insight-box strong {{ color: #9A6E00; }}
.insight-box code {{
    background: {BG_SURFACE};
    color: #0077AA;
    padding: 1px 5px;
    border-radius: 3px;
}}

/* ── header subtitle ────────────────────────────────────────── */
.subtitle {{ color: {TXT_MUTED}; font-size: 15px; margin-top: -12px; }}

/* ── legend colour pills ────────────────────────────────────── */
.legend-pill {{
    display: inline-block;
    width: 12px; height: 12px;
    border-radius: 3px;
    margin-right: 5px;
    vertical-align: middle;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PLOTLY BASE LAYOUT  ── called by every chart
# ══════════════════════════════════════════════════════════════
def base_layout(height=400, **extra):
    layout = dict(
        paper_bgcolor = PAPER_BG,
        plot_bgcolor  = BG_CARD,
        font          = dict(color=TXT_WHITE, family="'Segoe UI', Arial, sans-serif", size=12),
        title         = dict(text=""),
        margin        = dict(l=16, r=16, t=10, b=16),
        height        = height,
        legend        = dict(
            bgcolor     = BG_SURFACE,
            bordercolor = BG_BORDER,
            borderwidth = 1,
            font        = dict(color=TXT_BODY, size=11),
        ),
        xaxis = dict(
            gridcolor    = GRID_CLR,
            linecolor    = BG_BORDER,
            zerolinecolor= GRID_CLR,
            tickfont     = dict(color=TXT_BODY, size=11),
            showgrid     = True,
        ),
        yaxis = dict(
            gridcolor    = GRID_CLR,
            linecolor    = BG_BORDER,
            zerolinecolor= GRID_CLR,
            tickfont     = dict(color=TXT_BODY, size=11),
            showgrid     = True,
        ),
    )
    layout.update(extra)
    return layout

# ══════════════════════════════════════════════════════════════
#  ZIP → REAL COORDINATES
# ══════════════════════════════════════════════════════════════
ZIP_COORDS = {
    33480: (26.68, -80.04),   94301: (37.44, -122.14),
    94304: (37.42, -122.16),  72712: (36.37,  -94.21),
    60606: (41.88, -87.64),   60603: (41.88,  -87.63),
    76102: (32.75, -97.33),   33109: (25.77,  -80.14),
    33154: (25.89, -80.12),   33140: (25.80,  -80.13),
    34102: (26.14, -81.79),   32963: (27.66,  -80.42),
    33455: (27.04, -80.12),   81611: (39.19, -106.82),
    83014: (43.49,-110.76),   83025: (43.46, -110.74),
    89451: (39.25,-119.96),   55402: (44.98,  -93.27),
    23219: (37.54, -77.44),   94111: (37.80, -122.40),
    94123: (37.80,-122.44),   10021: (40.77,  -73.96),
    10022: (40.76, -73.97),   10023: (40.78,  -73.98),
    10128: (40.78, -73.95),   20037: (38.90,  -77.05),
    90210: (34.09,-118.41),   94027: (37.46, -122.20),
    98039: (47.62,-122.23),   48302: (42.59,  -83.29),
    30327: (33.86, -84.39),   77019: (29.75,  -95.42),
    85253: (33.52,-111.93),   60043: (42.09,  -87.78),
}

# ══════════════════════════════════════════════════════════════
#  DATA LOADING
# ══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading IRS ZIP Code data…")
def load_data():
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip().str.lower()
    df = df[df["zipcode"] != 99999]

    df["passive_income"] = df["a00300"] + df["a00600"] + df["a01000"]
    df["passive_ratio"]  = (df["passive_income"] / df["a00100"]).replace([np.inf,-np.inf],0).fillna(0)
    df["wage_ratio"]     = (df["a00200"] / df["a00100"]).replace([np.inf,-np.inf],0).fillna(0)

    agg = df.groupby("zipcode").agg(
        total_agi       =("a00100","sum"),
        total_passive   =("passive_income","sum"),
        total_wages     =("a00200","sum"),
        total_interest  =("a00300","sum"),
        total_dividends =("a00600","sum"),
        total_capgains  =("a01000","sum"),
    ).reset_index()

    agg["avg_agi"]       = (agg["total_agi"] / 4).round(0)
    agg["passive_ratio"] = (agg["total_passive"] / agg["total_agi"]).round(4)
    agg["wage_ratio"]    = (agg["total_wages"]   / agg["total_agi"]).round(4)
    agg["other_ratio"]   = (1 - agg["passive_ratio"] - agg["wage_ratio"]).clip(0).round(4)
    agg["agi_norm"]      = agg["avg_agi"] / agg["avg_agi"].max()
    agg["wealth_score"]  = (agg["passive_ratio"] * 0.5 + agg["agi_norm"] * 0.5).round(4)
    agg["lat"] = agg["zipcode"].map(lambda z: ZIP_COORDS.get(z,(np.nan,np.nan))[0])
    agg["lon"] = agg["zipcode"].map(lambda z: ZIP_COORDS.get(z,(np.nan,np.nan))[1])
    return df, agg

df_yearly, df_agg = load_data()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<h2 style='color:{GOLD};margin-bottom:4px;'>🏎️ Porsche</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{TXT_MUTED};font-size:12px;margin-top:0;'>Site Selection Dashboard</p>",
                unsafe_allow_html=True)
    st.divider()

    passive_threshold = st.slider(
        "Min passive ratio (%)", 0, 80, 35, 1,
        help="Minimum % of AGI from interest + dividends + capital gains"
    )
    agi_threshold = st.slider(
        "Min avg AGI ($k)", 0, 5000, 200, 50,
        help="Minimum 4-year average Adjusted Gross Income (thousands)"
    )
    top_n = st.slider("Top N ZIPs in rankings", 5, 30, 15, 5)

    st.divider()
    st.markdown(f"<p style='color:{TXT_MUTED};font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;'>Data Fields</p>",
                unsafe_allow_html=True)
    fields = [
        ("A00100", "Adjusted Gross Income"),
        ("A00200", "Wages & Salaries"),
        ("A00300", "Taxable Interest"),
        ("A00600", "Ordinary Dividends"),
        ("A01000", "Net Capital Gains"),
    ]
    for code, label in fields:
        st.markdown(
            f"<p style='margin:3px 0;font-size:13px;'>"
            f"<code style='background:{BG_PAGE};color:{CYAN};padding:1px 5px;border-radius:3px;'>{code}</code>"
            f"<span style='color:{TXT_BODY};'> {label}</span></p>",
            unsafe_allow_html=True,
        )
    st.markdown(f"<p style='color:{TXT_MUTED};font-size:11px;margin-top:12px;'>IRS ZIP Code Data 2019–2022</p>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FILTER
# ══════════════════════════════════════════════════════════════
df_agg["is_target"] = (
    (df_agg["passive_ratio"] >= passive_threshold / 100) &
    (df_agg["avg_agi"]       >= agi_threshold * 1000)
)
targets = df_agg[df_agg["is_target"]].sort_values("wealth_score", ascending=False)

# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(
    f"<h1 style='color:{TXT_WHITE};font-size:2rem;font-weight:700;margin-bottom:2px;'>"
    "🏎️ Porsche Dealership Site Selection</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p class='subtitle'>Passive Wealth Intelligence Dashboard · IRS ZIP Code Data 2019–2022</p>",
    unsafe_allow_html=True,
)
st.divider()

# ══════════════════════════════════════════════════════════════
#  KPI CARDS
# ══════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total ZIP Codes",   f"{len(df_agg):,}",               "nationwide")
k2.metric("Target ZIPs",       f"{df_agg['is_target'].sum():,}",  f"ratio>{passive_threshold}% & AGI>${agi_threshold}k")
k3.metric("Max Passive Ratio", f"{df_agg['passive_ratio'].max()*100:.1f}%",
          f"ZIP {int(df_agg.loc[df_agg['passive_ratio'].idxmax(),'zipcode'])}")
k4.metric("Highest Avg AGI",   f"${df_agg['avg_agi'].max()/1e6:.1f}M",
          f"ZIP {int(df_agg.loc[df_agg['avg_agi'].idxmax(),'zipcode'])}")
k5.metric("Top Wealth Score",  f"{df_agg['wealth_score'].max():.3f}",
          f"ZIP {int(df_agg.loc[df_agg['wealth_score'].idxmax(),'zipcode'])}")

st.divider()

# ══════════════════════════════════════════════════════════════
#  COLOUR LEGEND  (helps readers decode charts)
# ══════════════════════════════════════════════════════════════
legend_html = (
    f"<div style='display:flex;gap:24px;flex-wrap:wrap;align-items:center;"
    f"background:{BG_SURFACE};border:1px solid {BG_BORDER};border-radius:8px;"
    f"padding:10px 18px;margin-bottom:16px;'>"
    f"<span style='color:{TXT_MUTED};font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;'>Colour key:</span>"
    f"<span><span class='legend-pill' style='background:{GOLD}'></span><span style='color:{TXT_BODY};font-size:13px;'>Target / Passive income</span></span>"
    f"<span><span class='legend-pill' style='background:{CYAN}'></span><span style='color:{TXT_BODY};font-size:13px;'>Interest income</span></span>"
    f"<span><span class='legend-pill' style='background:{VIOLET}'></span><span style='color:{TXT_BODY};font-size:13px;'>Dividends</span></span>"
    f"<span><span class='legend-pill' style='background:{CORAL}'></span><span style='color:{TXT_BODY};font-size:13px;'>Capital gains / Other</span></span>"
    f"<span><span class='legend-pill' style='background:{SAGE}'></span><span style='color:{TXT_BODY};font-size:13px;'>Wages</span></span>"
    f"<span><span class='legend-pill' style='background:{MUTED_DOT}'></span><span style='color:{TXT_BODY};font-size:13px;'>Non-target ZIPs (steel blue)</span></span>"
    f"</div>"
)
st.markdown(legend_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Passive Wealth Analysis",
    "📈  Trends 2019–2022",
    "🗺️  Geographic Map",
    "🏆  Top Target ZIPs",
])

# ╔══════════════════════════════════════════════════════════════
# ║  TAB 1 — Passive Wealth Analysis
# ╚══════════════════════════════════════════════════════════════
with tab1:

    # ── Scatter + Bar side-by-side ─────────────────────────────
    col_l, col_r = st.columns([3, 2], gap="medium")

    with col_l:
        st.markdown(f"<h3 style='color:{TXT_WHITE};'>Passive Income Ratio vs Avg AGI</h3>",
                    unsafe_allow_html=True)
        st.markdown("<p style='color:#3A3B50;font-size:13px;margin-top:-8px;'>Top-right quadrant = high-income + investment-driven → ideal Porsche targets</p>", unsafe_allow_html=True)

        sc = df_agg.copy()
        sc["category"]  = np.where(sc["is_target"], "Target ZIP", "Other ZIP")
        sc["ratio_pct"] = (sc["passive_ratio"] * 100).round(2)
        sc["agi_k"]     = (sc["avg_agi"] / 1000).round(1)

        plot_df = pd.concat([
            sc[sc["is_target"]],
            sc[~sc["is_target"]].sample(min(2000, (~sc["is_target"]).sum()), random_state=42),
        ])

        fig_sc = px.scatter(
            plot_df, x="ratio_pct", y="agi_k",
            color="category",
            color_discrete_map={"Target ZIP": GOLD, "Other ZIP": MUTED_DOT},
            hover_data={"zipcode":True,"ratio_pct":":.1f","agi_k":":,.0f","category":False},
            labels={"ratio_pct":"Passive Ratio (%)","agi_k":"Avg AGI ($k)","zipcode":"ZIP"},
        )
        # Target dots: large gold with white ring
        fig_sc.update_traces(
            selector=dict(name="Target ZIP"),
            marker=dict(size=10, opacity=1.0,
                        line=dict(width=1.5, color="rgba(255,255,255,0.6)")),
        )
        # Other dots: steel blue, clearly visible but smaller
        fig_sc.update_traces(
            selector=dict(name="Other ZIP"),
            marker=dict(size=5, opacity=0.7),
        )
        fig_sc.add_vline(x=passive_threshold, line_dash="dot", line_color=GOLD, line_width=1.5,
                         annotation_text=f"  {passive_threshold}% threshold",
                         annotation_font=dict(color=GOLD, size=11))
        fig_sc.add_hline(y=agi_threshold, line_dash="dot", line_color=GOLD, line_width=1.5,
                         annotation_text=f"  ${agi_threshold}k AGI",
                         annotation_font=dict(color=GOLD, size=11),
                         annotation_position="right")
        fig_sc.update_layout(**base_layout(height=430))
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_r:
        st.markdown(f"<h3 style='color:{TXT_WHITE};'>Top {top_n} ZIPs — Wealth Score</h3>",
                    unsafe_allow_html=True)
        st.markdown("<p style='color:#3A3B50;font-size:13px;margin-top:-8px;'>Score = 50% passive ratio + 50% AGI rank (normalised)</p>", unsafe_allow_html=True)

        bar_df = df_agg.nlargest(top_n, "wealth_score").copy()
        bar_df["ratio_pct"] = (bar_df["passive_ratio"] * 100).round(1)
        bar_df["agi_m"]     = (bar_df["avg_agi"] / 1e6).round(2)
        bar_df["zip_lbl"]   = "ZIP " + bar_df["zipcode"].astype(str)
        bar_df = bar_df.sort_values("wealth_score")           # ascending → best at top

        # Colour gradient: dark-navy → cyan → gold
        norm  = bar_df["wealth_score"]
        n_min, n_max = norm.min(), norm.max()
        bar_colors = [
            f"rgba({int(61+180*(v-n_min)/(n_max-n_min))},{int(141+80*(v-n_min)/(n_max-n_min))},{int(212-130*(v-n_min)/(n_max-n_min))},1)"
            for v in norm
        ]
        # override top bar with gold
        bar_colors[-1] = GOLD

        fig_bar = go.Figure(go.Bar(
            x=bar_df["wealth_score"].tolist(),
            y=bar_df["zip_lbl"].tolist(),
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{v:.3f}" for v in bar_df["wealth_score"]],
            textposition="outside",
            textfont=dict(color=TXT_BODY, size=11),
            customdata=bar_df[["ratio_pct","agi_m"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Wealth Score: %{x:.3f}<br>"
                "Passive Ratio: %{customdata[0]:.1f}%<br>"
                "Avg AGI: $%{customdata[1]:.2f}M<extra></extra>"
            ),
        ))
        fig_bar.update_layout(**base_layout(
            height=max(400, top_n * 30 + 60),
            xaxis=dict(gridcolor=GRID_CLR, title="Composite Wealth Score",
                       tickfont=dict(color=TXT_BODY),
                       range=[0, bar_df["wealth_score"].max() * 1.22]),
            yaxis=dict(type="category", gridcolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TXT_BODY, size=11),
                       categoryorder="array",
                       categoryarray=bar_df["zip_lbl"].tolist()),
            margin=dict(l=14, r=70, t=36, b=14),
        ))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # ── Stacked Income Composition ────────────────────────────
    st.markdown(f"<h3 style='color:{TXT_WHITE};'>Income Composition — Passive vs Wages</h3>",
                unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#3A3B50;font-size:13px;margin:0 0 6px 0;'>"
        f"<span style='color:{GOLD}'>■</span> Passive income &nbsp;&nbsp;"
        f"<span style='color:{SAGE}'>■</span> Wages &nbsp;&nbsp;"
        f"<span style='color:{CORAL}'>■</span> Other</p>",
        unsafe_allow_html=True
    )

    comp_df = df_agg.nlargest(top_n, "wealth_score").copy()
    comp_df["pass_pct"] = (comp_df["passive_ratio"] * 100).round(1)
    comp_df["wage_pct"] = (comp_df["wage_ratio"]    * 100).round(1)
    comp_df["othr_pct"] = (comp_df["other_ratio"]   * 100).round(1)
    comp_df["zip_lbl"]  = "ZIP " + comp_df["zipcode"].astype(str)
    comp_df = comp_df.sort_values("pass_pct")
    zip_order = comp_df["zip_lbl"].tolist()

    fig_stack = go.Figure()
    for label, col, clr in [
        ("Passive Income", "pass_pct", GOLD),
        ("Wages",          "wage_pct", SAGE),
        ("Other",          "othr_pct", CORAL),
    ]:
        fig_stack.add_trace(go.Bar(
            name=label,
            x=comp_df[col].tolist(),
            y=comp_df["zip_lbl"].tolist(),
            orientation="h",
            marker_color=clr,
            marker_line=dict(width=0),
            hovertemplate=f"<b>%{{y}}</b><br>{label}: %{{x:.1f}}%<extra></extra>",
        ))
    fig_stack.update_layout(**base_layout(
        height=max(420, top_n * 34 + 80),
        barmode="stack",
        xaxis=dict(gridcolor=GRID_CLR, title="Share of AGI (%)",
                   range=[0,100], ticksuffix="%",
                   tickfont=dict(color=TXT_BODY)),
        yaxis=dict(type="category", gridcolor="rgba(0,0,0,0)",
                   tickfont=dict(color=TXT_BODY, size=11),
                   categoryorder="array", categoryarray=zip_order),
        legend=dict(orientation="h", y=1.05, x=0, bgcolor="rgba(0,0,0,0)",
                    font=dict(color=TXT_WHITE)),
        bargap=0.18,
    ))
    st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
💡 <strong>Key insight:</strong>
ZIPs with <strong>high passive ratio + low wage ratio</strong> represent investment-portfolio wealth —
buyers whose spending power is completely decoupled from job markets and economic downturns.
Bars dominated by <span style='color:{GOLD}'>gold</span> are Porsche's highest-priority targets.
</div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════
# ║  TAB 2 — Trends 2019–2022
# ╚══════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"<h3 style='color:{TXT_WHITE};'>Passive Wealth Trends 2019–2022</h3>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#3A3B50;font-size:13px;margin-top:-4px;'>Multi-year stability distinguishes resilient investment wealth from one-year spikes.</p>", unsafe_allow_html=True)

    trend_zips = df_agg.nlargest(top_n, "wealth_score")["zipcode"].tolist()
    trend_df   = df_yearly[df_yearly["zipcode"].isin(trend_zips)].copy()
    trend_df["passive_pct"] = (trend_df["passive_ratio"] * 100).round(2)
    trend_df["zip_lbl"]     = trend_df["zipcode"].astype(str)
    trend_df["agi_k"]       = (trend_df["a00100"] / 1000).round(0)

    col_t1, col_t2 = st.columns(2, gap="medium")

    with col_t1:
        st.markdown(f"<h4 style='color:{TXT_BODY};'>Passive Income Ratio by Year</h4>",
                    unsafe_allow_html=True)
        fig_line = px.line(
            trend_df, x="year", y="passive_pct", color="zip_lbl", markers=True,
            labels={"passive_pct":"Passive Ratio (%)","year":"Year","zip_lbl":"ZIP"},
            color_discrete_sequence=QUALITATIVE,
        )
        fig_line.update_traces(line=dict(width=2.5), marker=dict(size=7))
        fig_line.update_layout(**base_layout(
            height=380,
            xaxis=dict(gridcolor=GRID_CLR, dtick=1, tickfont=dict(color=TXT_BODY)),
            yaxis=dict(gridcolor=GRID_CLR, ticksuffix="%", tickfont=dict(color=TXT_BODY)),
        ))
        st.plotly_chart(fig_line, use_container_width=True)

    with col_t2:
        st.markdown(f"<h4 style='color:{TXT_BODY};'>AGI Growth Over Time ($k)</h4>",
                    unsafe_allow_html=True)
        fig_agi = px.line(
            trend_df, x="year", y="agi_k", color="zip_lbl", markers=True,
            labels={"agi_k":"Avg AGI ($k)","year":"Year","zip_lbl":"ZIP"},
            color_discrete_sequence=QUALITATIVE,
        )
        fig_agi.update_traces(line=dict(width=2.5), marker=dict(size=7))
        fig_agi.update_layout(**base_layout(
            height=380,
            xaxis=dict(gridcolor=GRID_CLR, dtick=1, tickfont=dict(color=TXT_BODY)),
            yaxis=dict(gridcolor=GRID_CLR, tickprefix="$", tickfont=dict(color=TXT_BODY)),
        ))
        st.plotly_chart(fig_agi, use_container_width=True)

    st.divider()
    st.markdown(f"<h3 style='color:{TXT_WHITE};'>Wealth Stability Score</h3>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#3A3B50;font-size:13px;margin-top:-4px;'>Bar height = mean passive ratio · Error bars = year-over-year std dev · Smaller error = more stable</p>", unsafe_allow_html=True)

    vol_df = (
        df_yearly[df_yearly["zipcode"].isin(trend_zips)]
        .groupby("zipcode")["passive_ratio"]
        .agg(mean="mean", std="std")
        .reset_index()
    )
    vol_df["mean_pct"] = (vol_df["mean"] * 100).round(2)
    vol_df["std_pct"]  = (vol_df["std"]  * 100).round(2)
    vol_df["zip_lbl"]  = "ZIP " + vol_df["zipcode"].astype(str)
    vol_df = vol_df.sort_values("mean_pct", ascending=False)

    # bar colour = continuous from MUTED_DOT → CYAN → GOLD
    vol_colors = []
    mn, mx = vol_df["mean_pct"].min(), vol_df["mean_pct"].max()
    for v in vol_df["mean_pct"]:
        t = (v - mn) / (mx - mn) if mx > mn else 0
        r = int(61  + t * (229 - 61))
        g = int(212 + t * (185 - 212))
        b = int(245 + t * (78  - 245))
        vol_colors.append(f"rgb({r},{g},{b})")

    fig_vol = go.Figure(go.Bar(
        x=vol_df["zip_lbl"].tolist(),
        y=vol_df["mean_pct"].tolist(),
        marker=dict(color=vol_colors, line=dict(width=0)),
        error_y=dict(type="data", array=vol_df["std_pct"].tolist(),
                     visible=True, color=BG_BORDER, thickness=2, width=8),
        text=[f"{v:.1f}%" for v in vol_df["mean_pct"]],
        textposition="outside",
        textfont=dict(color=TXT_WHITE, size=11),
        hovertemplate="<b>%{x}</b><br>Mean: %{y:.1f}%<extra></extra>",
    ))
    fig_vol.update_layout(**base_layout(
        height=340, showlegend=False,
        xaxis=dict(type="category", gridcolor="rgba(0,0,0,0)",
                   tickangle=-20, tickfont=dict(color=TXT_BODY, size=11)),
        yaxis=dict(gridcolor=GRID_CLR, ticksuffix="%",
                   title="Passive Ratio (%)",
                                      tickfont=dict(color=TXT_BODY)),
    ))
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
💡 <strong>Reading this chart:</strong>
Tall bar + <em>small</em> error bar = high, stable passive wealth = prime Porsche territory.
Tall bar + <em>large</em> error bar often reflects a one-time capital event (IPO year, property sale).
Prioritise ZIPs that are consistently high, not just peak-year high.
</div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════
# ║  TAB 3 — Geographic Map
# ╚══════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"<h3 style='color:{TXT_WHITE};'>Geographic Distribution of Wealth Targets</h3>",
                unsafe_allow_html=True)

    map_type = st.radio(
        "View mode",
        ["📍  Bubble map (verified coordinates)", "📊  State-level overview"],
        horizontal=True,
    )

    if "Bubble" in map_type:
        map_df = df_agg.dropna(subset=["lat","lon"]).copy()
        map_df["passive_pct"]  = (map_df["passive_ratio"] * 100).round(1)
        map_df["agi_m"]        = (map_df["avg_agi"] / 1e6).round(2)
        map_df["target_label"] = np.where(map_df["is_target"], "🎯 Target", "Other")

        st.markdown(
            f"<p style='color:#3A3B50;font-size:13px;'>"
            f"Showing <strong style='color:#1A1B2E;'>{len(map_df)} ZIPs</strong> with verified coordinates. "
            f"Install <code style='background:#1A1B24;color:#3DD8F5;padding:1px 5px;border-radius:3px;'>pgeocode</code>"
            f" (see app.py comments) to map all 27,747 ZIPs.</p>",
            unsafe_allow_html=True
        )
        fig_map = px.scatter_mapbox(
            map_df, lat="lat", lon="lon",
            size="passive_pct", color="target_label",
            color_discrete_map={"🎯 Target": GOLD, "Other": "#2E86AB"},
            hover_data={"zipcode":True,"passive_pct":":.1f","agi_m":":.2f",
                        "lat":False,"lon":False},
            labels={"passive_pct":"Passive %","agi_m":"Avg AGI $M","target_label":"Category"},
            zoom=3, height=580, size_max=32,
            mapbox_style="open-street-map",
        )
        fig_map.update_layout(
            paper_bgcolor=PAPER_BG,
            font=dict(color=TXT_BODY),
            legend=dict(bgcolor=BG_SURFACE, bordercolor=BG_BORDER, borderwidth=1,
                        font=dict(color=TXT_BODY)),
            margin=dict(l=0, r=0, t=0, b=0),
            mapbox=dict(
                center=dict(lat=39.5, lon=-98.35),
                zoom=3,
                style="open-street-map",
            ),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    else:
        def zip_to_state(z):
            for (lo,hi),s in [
                ((1000, 2999),"MA"),  ((10000,14999),"NY"), ((15000,19999),"PA"),
                ((20000,24999),"VA"), ((27000,28999),"NC"), ((29000,29999),"SC"),
                ((30000,31999),"GA"), ((32000,34999),"FL"), ((37000,38999),"TN"),
                ((40000,42999),"KY"), ((43000,45999),"OH"), ((48000,49999),"MI"),
                ((53000,54999),"WI"), ((55000,56999),"MN"), ((60000,62999),"IL"),
                ((63000,65999),"MO"), ((70000,71999),"LA"), ((72000,72999),"AR"),
                ((75000,79999),"TX"), ((80000,81999),"CO"), ((82000,82999),"WY"),
                ((83000,83999),"ID"), ((84000,84999),"UT"), ((85000,86999),"AZ"),
                ((89000,89999),"NV"), ((90000,96199),"CA"), ((97000,97999),"OR"),
                ((98000,99499),"WA"),
            ]:
                if lo <= z <= hi: return s
            return None

        state_df = df_agg.copy()
        state_df["state"] = state_df["zipcode"].apply(zip_to_state)
        state_df = state_df.dropna(subset=["state"])
        st_sum = state_df.groupby("state").agg(
            mean_passive=("passive_ratio","mean"),
            target_zips =("is_target","sum"),
            zip_count   =("zipcode","count"),
        ).reset_index()
        st_sum["passive_pct"] = (st_sum["mean_passive"] * 100).round(2)
        st_sum = st_sum.sort_values("passive_pct", ascending=False)

        fig_st = px.bar(
            st_sum, x="state", y="passive_pct",
            color="passive_pct",
            color_continuous_scale=[[0,"#1A1B24"],[0.35,CYAN],[0.7,VIOLET],[1.0,GOLD]],
            text=st_sum["passive_pct"].apply(lambda v: f"{v:.1f}%"),
            labels={"passive_pct":"Avg Passive Ratio (%)","state":"State"},
            hover_data={"target_zips":True,"zip_count":True},
            height=430,
        )
        fig_st.update_traces(
            textposition="outside",
            textfont=dict(color=TXT_BODY, size=10),
            marker_line_width=0,
        )
        fig_st.update_layout(**base_layout(
            height=430,
            coloraxis_showscale=False,
            xaxis=dict(type="category", gridcolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TXT_BODY, size=11)),
            yaxis=dict(gridcolor=GRID_CLR, ticksuffix="%",
                       tickfont=dict(color=TXT_BODY)),
        ))
        st.plotly_chart(fig_st, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
📍 <strong>Map accuracy:</strong>
The original app used <code>np.random.seed(42)</code> + random offsets — every dot was in the
<em>wrong place</em>. This version uses verified real-world ZIP centroids.
Add <code>pgeocode</code> to requirements.txt for full 27k-ZIP accurate mapping.
</div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════
# ║  TAB 4 — Top Target ZIPs Table
# ╚══════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"<h3 style='color:{TXT_WHITE};'>Top Porsche Target ZIP Codes</h3>",
                unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#3A3B50;font-size:13px;margin-top:-4px;'>"
        f"Filter active: passive ratio ≥ <strong style='color:#E5B94E;'>{passive_threshold}%</strong>  ·  "
        f"avg AGI ≥ <strong style='color:#E5B94E;'>${agi_threshold:,}k</strong>  ·  sorted by composite wealth score</p>",
        unsafe_allow_html=True
    )

    if len(targets) == 0:
        st.warning("⚠️ No ZIPs match the current thresholds — try lowering the sidebar sliders.")
    else:
        display = targets.head(50)[[
            "zipcode","avg_agi","passive_ratio","wage_ratio",
            "wealth_score","total_interest","total_dividends","total_capgains"
        ]].copy()
        display.columns = [
            "ZIP Code","Avg AGI ($)","Passive Ratio","Wage Ratio",
            "Wealth Score","Total Interest","Total Dividends","Total Cap Gains"
        ]
        display["Avg AGI ($)"]     = display["Avg AGI ($)"].apply(lambda v: f"${v:,.0f}")
        display["Passive Ratio"]   = display["Passive Ratio"].apply(lambda v: f"{v*100:.1f}%")
        display["Wage Ratio"]      = display["Wage Ratio"].apply(lambda v: f"{v*100:.1f}%")
        display["Wealth Score"]    = display["Wealth Score"].apply(lambda v: f"{v:.4f}")
        display["Total Interest"]  = display["Total Interest"].apply(lambda v: f"${v:,.0f}")
        display["Total Dividends"] = display["Total Dividends"].apply(lambda v: f"${v:,.0f}")
        display["Total Cap Gains"] = display["Total Cap Gains"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(display, use_container_width=True, height=460)

        st.divider()
        st.markdown(f"<h3 style='color:{TXT_WHITE};'>Passive Income Source Breakdown — Top 5 Targets</h3>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:#3A3B50;font-size:13px;margin:0 0 6px 0;'>"
            f"<span style='color:{CYAN}'>■</span> Interest &nbsp;&nbsp;"
            f"<span style='color:{VIOLET}'>■</span> Dividends &nbsp;&nbsp;"
            f"<span style='color:{GOLD}'>■</span> Capital Gains</p>",
            unsafe_allow_html=True
        )

        top5 = targets.head(5)[
            ["zipcode","total_interest","total_dividends","total_capgains"]
        ].melt(id_vars="zipcode", var_name="Source", value_name="Amount")
        top5["ZIP"]      = "ZIP " + top5["zipcode"].astype(str)
        top5["Amount_M"] = (top5["Amount"] / 1e6).round(2)
        top5["Source"]   = top5["Source"].map({
            "total_interest":  "Interest",
            "total_dividends": "Dividends",
            "total_capgains":  "Capital Gains",
        })

        fig_comp = px.bar(
            top5, x="ZIP", y="Amount_M", color="Source", barmode="group",
            color_discrete_map={
                "Interest":     CYAN,
                "Dividends":    VIOLET,
                "Capital Gains":GOLD,
            },
            text=top5["Amount_M"].apply(lambda v: f"${v:.1f}M"),
            labels={"Amount_M":"4-year total ($M)","ZIP":"ZIP Code"},
            height=360,
        )
        fig_comp.update_traces(
            textposition="outside",
            textfont=dict(color=TXT_BODY, size=10),
            marker_line_width=0,
        )
        fig_comp.update_layout(**base_layout(
            height=360,
            xaxis=dict(type="category", gridcolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TXT_BODY, size=12)),
            yaxis=dict(gridcolor=GRID_CLR, tickprefix="$", ticksuffix="M",
                       tickfont=dict(color=TXT_BODY)),
            legend=dict(orientation="h", y=1.06, bgcolor="rgba(0,0,0,0)",
                        font=dict(color=TXT_WHITE)),
            bargap=0.25, bargroupgap=0.06,
        ))
        st.plotly_chart(fig_comp, use_container_width=True)

        st.markdown(f"""<div class="insight-box">
💡 <strong>Source breakdown matters:</strong>
<span style='color:{VIOLET}'>Dividend-heavy</span> ZIPs tend to be old-money / family-wealth markets.
<span style='color:{GOLD}'>Capital-gains-heavy</span> ZIPs often reflect tech/startup wealth with
higher spending volatility. <span style='color:{CYAN}'>Interest-heavy</span> ZIPs indicate bond/CD
wealth — typically older, stable buyers who prefer conservative luxury.
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.divider()
st.markdown(
    f"<p style='color:{TXT_MUTED};font-size:12px;text-align:center;'>"
    "Data: IRS Statistics of Income ZIP Code Data (2019–2022) · "
    "Porsche Site Selection Committee — Team 6</p>",
    unsafe_allow_html=True,
)
