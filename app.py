import streamlit as st
import os
import uuid
import base64
import random
import socket
from datetime import datetime
from collections import Counter
from spin_wheel_component import spin_wheel_component

# ----------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLE INJECTION
# ----------------------------------------------------
st.set_page_config(
    page_title="PizzEat Lucky Spin",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for PizzEat branding and premium arcade aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Main Background & Fonts */
    .stApp {
        background: radial-gradient(circle at top, #1E080A 0%, #0F0405 50%, #000000 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Center the main container */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #120405 !important;
        border-right: 2px solid #E50914 !important;
    }
    
    /* Hide developer headers and menus SELECTIVELY - preserve sidebar toggle container */
    div[data-testid="stDecoration"] { display: none !important; }
    iframe[title="Protected content"] { display: none !important; }
    /* Hide toolbar buttons but NOT the whole toolbar (sidebar toggle lives there) */
    div[data-testid="stToolbar"] > div:not([data-testid="collapsedControl"]) { display: none !important; }
    
    /* Make header background transparent so it blends perfectly */
    header[data-testid="stHeader"] {
        background: transparent !important;
        border: none !important;
        height: auto !important;
    }

    /* Sidebar collapsed toggle button - always visible, beautifully styled */
    [data-testid="collapsedControl"] {
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="collapsedControl"] button {
        background-color: #E50914 !important;
        color: #FFFFFF !important;
        border: 2px solid #F5C518 !important;
        border-radius: 50% !important;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.7) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 42px !important;
        height: 42px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    [data-testid="collapsedControl"] button:hover {
        background-color: #F5C518 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 22px rgba(245, 197, 24, 0.9) !important;
        transform: scale(1.1) !important;
    }
    
    /* Icon color inside the button */
    [data-testid="collapsedControl"] button svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    [data-testid="collapsedControl"] button:hover svg {
        fill: #000000 !important;
        color: #000000 !important;
    }
    
    /* PizzEat Custom Header Badge */
    .brand-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .brand-logo {
        background: linear-gradient(135deg, #E50914 0%, #F5C518 100%);
        color: white;
        font-size: 2.2rem;
        font-weight: 800;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        box-shadow: 0 0 25px rgba(229, 9, 20, 0.6);
        border: 3px solid #FFFFFF;
        font-family: 'Outfit', sans-serif;
        letter-spacing: 1px;
    }
    
    .brand-logo span {
        color: #F5C518;
        font-style: italic;
    }
    
    .brand-subtitle {
        color: #FFFFFF;
        opacity: 0.9;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.8rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Style columns as Glassmorphism Cards */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px !important;
        padding: 1.8rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
    }
    
    .glass-card-header {
        color: #F5C518;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        border-bottom: 2px solid rgba(245, 197, 24, 0.2);
        padding-bottom: 0.4rem;
        letter-spacing: 0.5px;
    }
    
    /* Result Cards */
    .result-card-winner {
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.95) 0%, rgba(150, 6, 12, 0.95) 100%);
        border: 3px solid #F5C518;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 0 35px rgba(245, 197, 24, 0.4);
        margin: 1.5rem 0;
        animation: cardGlow 1.5s infinite alternate;
    }
    
    .result-card-jackpot {
        background: linear-gradient(135deg, rgba(245, 197, 24, 0.95) 0%, rgba(200, 150, 10, 0.95) 100%);
        border: 4px solid #FFFFFF;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.8);
        margin: 1.5rem 0;
        animation: jackpotGlow 1s infinite alternate;
    }
    
    @keyframes cardGlow {
        0% { box-shadow: 0 0 20px rgba(245, 197, 24, 0.3); }
        100% { box-shadow: 0 0 35px rgba(245, 197, 24, 0.6); }
    }
    
    @keyframes jackpotGlow {
        0% { box-shadow: 0 0 25px rgba(255, 215, 0, 0.5), inset 0 0 15px rgba(255,255,255,0.4); }
        100% { box-shadow: 0 0 50px rgba(255, 215, 0, 0.9), inset 0 0 30px rgba(255,255,255,0.6); }
    }
    
    /* Stats grid */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .stat-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F5C518;
    }
    
    .stat-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        opacity: 0.7;
        margin-top: 0.3rem;
    }
    
    /* Main Glowing Action Button */
    div.stButton > button {
        background: linear-gradient(135deg, #E50914 0%, #B0060E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #F5C518 !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        padding: 0.8rem 3rem !important;
        border-radius: 50px !important;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.5) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
        height: auto !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #F5C518 0%, #D8A50B 100%) !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 25px rgba(245, 197, 24, 0.8) !important;
        transform: scale(1.03);
    }
    
    div.stButton > button:active {
        transform: scale(0.97);
    }
    
    /* Custom Styling for Streamlit Tables */
    .stTable {
        background-color: transparent !important;
    }
    
    thead th {
        background-color: rgba(229, 9, 20, 0.15) !important;
        color: #F5C518 !important;
        font-weight: bold !important;
        border-bottom: 2px solid #E50914 !important;
    }
    
    tbody tr {
        background-color: rgba(255, 255, 255, 0.01) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    tbody tr:hover {
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 1b. HELPER: BASE64 ASSET LOADER
# ----------------------------------------------------
def load_asset_b64(filepath, mime="audio/mpeg"):
    """Load a local file as a base64 data URI."""
    try:
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return None

_music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Pizza Napolitana.mp3")
_logo_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "pizzeatlogo.png")

_music_b64 = load_asset_b64(_music_path, "audio/mpeg")
_logo_b64  = load_asset_b64(_logo_path,  "image/png")

# ----------------------------------------------------
# 2. AUDIO DOWNLOAD WORKFLOW
# ----------------------------------------------------
def check_and_download_assets():
    """
    Downloads audio files from public URLs if they are not already present.
    Saves to both root 'assets' and component 'spin_wheel_component/assets' folders.
    """
    dirs = ["assets", os.path.join("spin_wheel_component", "assets")]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
        
    sounds = {
        "spin.mp3": "https://github.com/scottschiller/soundmanager2/raw/master/demo/_mp3/click-low.mp3",
        "win.mp3": "https://github.com/scottschiller/soundmanager2/raw/master/demo/_mp3/click-high.mp3",
        "jackpot.mp3": "https://github.com/scottschiller/soundmanager2/raw/master/demo/_mp3/click-high.mp3"
    }
    
    warning_msgs = []
    
    for d in dirs:
        for filename, url in sounds.items():
            filepath = os.path.join(d, filename)
            if not os.path.exists(filepath):
                try:
                    socket.setdefaulttimeout(3.5)
                    urllib_download(url, filepath)
                except Exception as e:
                    warning_msgs.append(f"Gagal mengunduh {filename} ke {d}: {e}")
                
    if warning_msgs:
        return "⚠️ Beberapa audio lokal gagal diunduh. Sistem menggunakan synthesizer."
    return None

def urllib_download(url, filepath):
    import urllib.request
    urllib.request.urlretrieve(url, filepath)

def copy_bg_music_to_component():
    """Copy the background music to spin_wheel_component/assets/ so it can be served by the component file server."""
    import shutil
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Pizza Napolitana.mp3")
    dst_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spin_wheel_component", "assets")
    dst = os.path.join(dst_dir, "bg_music.mp3")
    if os.path.exists(src) and not os.path.exists(dst):
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src, dst)

copy_bg_music_to_component()
audio_warning = check_and_download_assets()

# ----------------------------------------------------
# 3. PRIZE LIST & WEIGHTED PROBABILITIES DEF (Zonk Removed!)
# ----------------------------------------------------
# 'prob'   = angka display di UI (gimmick, biar keliatan menarik)
# 'weight' = probabilitas aktual yang dipakai random.choices (total = 100%)
#   Jackpot  : 0.05%  | Permen      : 50%
#   PizzRoll : 5%     | Stiker      : 20%
#   Pulpen   : 10%    | Tambahan Kentang : 14.95% (sisa dari 100%)
prizes = [
    {"name": "🍕 JACKPOT – 1 Porsi PizzEat Gratis", "prob": 5.00,  "weight": 0.05,  "color": "#FFD700", "text_color": "#000000", "is_jackpot": True},
    {"name": "🍟 Tambahan Kentang",                  "prob": 40.00, "weight": 14.95, "color": "#E50914", "text_color": "#FFFFFF", "is_jackpot": False},
    {"name": "🍬 Permen",                            "prob": 7.50,  "weight": 50.00, "color": "#E50914", "text_color": "#FFFFFF", "is_jackpot": False},
    {"name": "🌯 1 PizzRoll",                        "prob": 10.00, "weight": 5.00,  "color": "#F5C518", "text_color": "#000000", "is_jackpot": False},
    {"name": "🖊️ Pulpen",                            "prob": 15.00, "weight": 10.00, "color": "#E50914", "text_color": "#FFFFFF", "is_jackpot": False},
    {"name": "🏷️ Stiker PizzEat",                   "prob": 22.50, "weight": 20.00, "color": "#F5C518", "text_color": "#000000", "is_jackpot": False}
]

# ----------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# ----------------------------------------------------
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "trigger_id" not in st.session_state:
    st.session_state.trigger_id = None
if "target_prize_index" not in st.session_state:
    st.session_state.target_prize_index = None
if "last_processed_trigger" not in st.session_state:
    st.session_state.last_processed_trigger = None
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "spinning_state" not in st.session_state:
    st.session_state.spinning_state = False

# ----------------------------------------------------
# 5. LAYOUT: SIDEBAR (STATS, HISTORY, ADMIN)
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-container" style="margin-top: 1rem;">
        <div class="brand-logo" style="font-size: 1.6rem; padding: 0.4rem 1.2rem;">Pizz<span>Eat</span></div>
        <div style="font-size: 0.9rem; font-weight: bold; color: #F5C518; margin-top: 0.4rem; text-transform: uppercase; letter-spacing: 1px;">Lucky Spin Panel</div>
    </div>
    """, unsafe_allow_html=True)
    
    if audio_warning:
        st.info(audio_warning)
        
    st.markdown('<div class="glass-card-header">📊 Statistik Pemenang</div>', unsafe_allow_html=True)
    
    total_spins = len(st.session_state.riwayat)
    jackpots_won = sum(1 for item in st.session_state.riwayat if "JACKPOT" in item["hadiah"])
    
    if st.session_state.riwayat:
        prizes_won_names = [item["hadiah"] for item in st.session_state.riwayat]
        most_frequent_prize = Counter(prizes_won_names).most_common(1)[0][0]
    else:
        most_frequent_prize = "Belum Ada"
        
    st.markdown(f"""
    <div class="stats-container" style="margin-bottom: 1rem;">
        <div class="stat-box">
            <div class="stat-val">{total_spins}</div>
            <div class="stat-label">Total Spin</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{jackpots_won}</div>
            <div class="stat-label">Jackpot</div>
        </div>
    </div>
    <div class="stat-box" style="margin-bottom: 1.5rem;">
        <div class="stat-val" style="font-size: 1.1rem; color: #FFFFFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 5px;">
            {most_frequent_prize}
        </div>
        <div class="stat-label">Hadiah Paling Sering</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card-header">🛠️ Admin Control</div>', unsafe_allow_html=True)
    if st.button("🔄 Reset Riwayat", use_container_width=True):
        st.session_state.riwayat = []
        st.session_state.last_processed_trigger = None
        st.session_state.target_prize_index = None
        st.session_state.trigger_id = None
        st.session_state.current_result = None
        st.session_state.spinning_state = False
        st.success("Riwayat spin berhasil di-reset!")
        st.rerun()

# ----------------------------------------------------
# 6. LAYOUT: MAIN GAME PAGE
# ----------------------------------------------------

# Brand header
_logo_img = f'<img src="{_logo_b64}" style="height:54px;width:54px;object-fit:contain;border-radius:50%;border:2px solid #F5C518;box-shadow:0 0 10px rgba(245,197,24,0.5);vertical-align:middle;margin-right:0.5rem;">'
if not _logo_b64:
    _logo_img = "🍕 "

st.markdown(f"""
<div class="brand-container">
    <div class="brand-logo">{_logo_img}Pizz<span>Eat</span></div>
    <div class="brand-subtitle">🎉 PizzEat Lucky Spin — Beli PizzEat, Putar Roda, Menangkan Hadiah!</div>
</div>
""", unsafe_allow_html=True)

col_wheel, col_results = st.columns([1.1, 0.9])

with col_wheel:

    spin_button_label = "🎯 PUTAR RODA"
    if st.session_state.spinning_state:
        spin_button_label = "⌛ SEDANG BERPUTAR..."
        
    spin_clicked = st.button(
        spin_button_label, 
        disabled=st.session_state.spinning_state,
        key="btn_spin"
    )

    if spin_clicked and not st.session_state.spinning_state:
        weights = [p["weight"] for p in prizes]  # gunakan actual weight, bukan display prob
        chosen_prize_dict = random.choices(prizes, weights=weights, k=1)[0]
        chosen_index = prizes.index(chosen_prize_dict)
        
        st.session_state.target_prize_index = chosen_index
        st.session_state.trigger_id = str(uuid.uuid4())
        st.session_state.spinning_state = True
        st.session_state.current_result = None
        st.rerun()
        
    # Render custom component.
    result = spin_wheel_component(
        target_prize_index=st.session_state.target_prize_index,
        trigger_id=st.session_state.trigger_id,
        prizes=prizes,
        key="lucky_spin_wheel"
    )
    
    # Handle spin complete callback OR cheat jackpot trigger
    if result:
        if result.get("status") == "cheat_jackpot" and not st.session_state.spinning_state:
            # Q-key easter egg: force JACKPOT spin
            st.session_state.target_prize_index = 0  # index 0 = JACKPOT
            st.session_state.trigger_id = str(uuid.uuid4())
            st.session_state.spinning_state = True
            st.session_state.current_result = None
            st.rerun()

        elif result.get("status") == "finished":
            trigger_id = result.get("trigger_id")
            prize_index = result.get("prize_index")
        
            if trigger_id and trigger_id != st.session_state.last_processed_trigger:
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                prize_name = prizes[prize_index]["name"]
                
                st.session_state.riwayat.append({
                    "no": len(st.session_state.riwayat) + 1,
                    "hadiah": prize_name,
                    "waktu": waktu_sekarang
                })
                st.session_state.last_processed_trigger = trigger_id
                st.session_state.spinning_state = False
                st.session_state.current_result = prizes[prize_index]
                st.rerun()
            
with col_results:
    st.markdown('<div class="glass-card-header">🎁 Hasil Undian</div>', unsafe_allow_html=True)
    
    if st.session_state.spinning_state:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 0;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #F5C518; margin-bottom: 0.5rem;">Memutar Roda Keberuntungan...</div>
            <div style="font-size: 1.1rem; opacity: 0.7; animation: pulse 0.8s infinite alternate;">Harap tunggu! Menghitung koordinat pizza Anda...</div>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.current_result:
        res = st.session_state.current_result
        name = res["name"]
        
        if res.get("is_jackpot"):
            st.markdown(f"""
            <div class="result-card-jackpot">
                <div style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; text-shadow: 0 0 10px rgba(0,0,0,0.5);">🌟 JACKPOT LEGENDARY 🌟</div>
                <div style="font-size: 2.4rem; margin: 1rem 0;">🍕🍕🍕</div>
                <div style="font-size: 1.4rem; font-weight: bold; color: #FFFFFF; line-height: 1.5;">
                    Anda mendapatkan PizzEat GRATIS!
                </div>
                <div style="font-size: 0.9rem; opacity: 0.8; margin-top: 1rem; color: #FFFFFF; font-style: italic;">
                    Tunjukkan layar ini ke kasir PizzEat untuk menukarkan pizza gratis Anda!
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card-winner">
                <div style="font-size: 1.4rem; font-weight: 800; color: #FFFFFF; text-shadow: 0 2px 4px rgba(0,0,0,0.4);">🎊 SELAMAT! 🎊</div>
                <div style="font-size: 1.1rem; opacity: 0.9; margin: 0.4rem 0;">Anda mendapatkan:</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #F5C518; margin: 0.6rem 0; text-shadow: 0 0 10px rgba(245, 197, 24, 0.4);">
                    {name}
                </div>
                <div style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.8rem; font-style: italic; color: #FFFFFF;">
                    Laporkan ke booth penukaran hadiah PizzEat Market Day!
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0; opacity: 0.5;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 1.1rem; font-weight: bold;">Klik "PUTAR RODA" untuk memulai petualangan!</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card-header">📋 Riwayat Pemenang</div>', unsafe_allow_html=True)
    
    if st.session_state.riwayat:
        reversed_riwayat = list(reversed(st.session_state.riwayat))
        table_data = []
        for item in reversed_riwayat:
            table_data.append({
                "No": item["no"],
                "Hadiah": item["hadiah"],
                "Waktu": item["waktu"]
            })
            
        st.table(table_data)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0; opacity: 0.5; font-size: 0.95rem;">
            Belum ada data pemenang. Roda belum diputar.
        </div>
        """, unsafe_allow_html=True)
        
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ----------------------------------------------------
    # 7. PROBABILITY LEGEND
    # ----------------------------------------------------
    legend_items = ""
    for prize in prizes:
        legend_items += (
            '<div style="display:flex;align-items:center;gap:0.5rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;box-shadow:0 4px 15px rgba(0,0,0,0.2);">'
            '<div style="width:14px;height:14px;border-radius:50%;background-color:' + prize['color'] + ';box-shadow:0 0 5px ' + prize['color'] + ';flex-shrink:0;"></div>'
            '<div style="font-size:0.95rem;font-weight:bold;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex-grow:1;color:#FFFFFF;">' + prize['name'] + '</div>'
            '<div style="font-size:0.9rem;color:#F5C518;font-weight:bold;flex-shrink:0;">' + str(prize['prob']) + '%</div>'
            '</div>'
        )

    legend_html = (
        '<div style="margin-top:1rem;">'
        '<div class="glass-card-header" style="border-bottom:2px solid rgba(229,9,20,0.2);color:#E50914;margin-bottom:1.2rem;">🍕 Peluang Hadiah (Weighted Odds)</div>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;">'
        + legend_items +
        '</div></div>'
    )
    st.markdown(legend_html, unsafe_allow_html=True)
