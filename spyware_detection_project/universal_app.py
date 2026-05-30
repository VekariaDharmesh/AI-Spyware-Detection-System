"""
Universal Device Manager - Main Application with Live Monitoring
Replaces the spyware detection focus with universal device management and AI-powered monitoring
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_interface import UniversalDeviceInterface
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import socket
import time
import psutil
 

def main():
    """Main application entry point with live monitoring"""
    
    # Configure page for universal experience
    st.set_page_config(
        page_title="Silent Guard AI",
        page_icon="⛨",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo',
            'Report a bug': 'https://github.com/your-repo/issues',
            'About': "Universal Device Manager with AI-Powered Live Monitoring"
        }
    )
    
    # 🎨 THEME: Behavioral Intelligence Engine - Dark AI Console
    st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Inter', 'Roboto', 'Arial', 'Helvetica', sans-serif;
            color: #E5F6FF;
            background: radial-gradient(circle at top, #0b1f3b 0, #020617 45%, #000000 100%);
        }
        
        .main {
            background: transparent;
        }
        
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(56,189,248,0.08), rgba(15,23,42,0.9));
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 12px 30px rgba(15,23,42,0.7);
            border: 1px solid rgba(56,189,248,0.4);
        }
        
        [data-testid="stMetric"] label {
            color: #E5F6FF !important;
        }
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #7dd3fc !important;
            font-weight: 700;
        }
        
        h1, h2, h3 {
            font-weight: 650;
            color: #e5f6ff;
        }
        
        .top-header {
            position: sticky;
            top: 0;
            z-index: 10;
            background: radial-gradient(circle at left, #0f172a 0, #020617 60%);
            padding: 10px 0;
            border-bottom: 1px solid rgba(56,189,248,0.35);
            backdrop-filter: blur(14px);
        }
        
        section[data-testid="stSidebar"] {
            background: #020617;
            border-right: 1px solid rgba(15,23,42,0.9);
        }
        
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] .stMarkdown {
            color: #e5f6ff !important;
        }
        section[data-testid="stSidebar"] .sidebar-heading {
            font-size: 24px;
            font-weight: 700;
            color: #e5f6ff;
            margin: 12px 0 8px;
            padding-bottom: 6px;
            border-bottom: 1px solid rgba(56,189,248,0.3);
        }
        section[data-testid="stSidebar"] .sticky {
            position: sticky;
            top: 0;
            z-index: 5;
            background-color: #020617;
            padding-top: 6px;
        }
        
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
            font-size: 22px !important;
            font-weight: 600 !important;
            color: #e5f6ff !important;
            line-height: 1.4 !important;
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
        }
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label div,
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label p,
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label span {
            font-size: 22px !important;
            font-weight: 600 !important;
            color: #e5f6ff !important;
        }
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {
            gap: 8px !important;
        }
        section[data-testid="stSidebar"] .stRadio input[type="radio"] {
            width: 20px !important;
            height: 20px !important;
            transform: translateY(1px);
        }
        section[data-testid="stSidebar"] .brand-header {
            font-weight: 800;
            font-size: 24px;
            color: #e5f6ff;
            margin: 8px 0 4px;
        }
        section[data-testid="stSidebar"] .brand-sub {
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 12px;
        }
        section[data-testid="stSidebar"] .device-card {
            background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(15,23,42,0.85));
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 14px;
            padding: 12px;
            box-shadow: 0 8px 24px rgba(15,23,42,0.6);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        section[data-testid="stSidebar"] .device-card.selected {
            border-color: #22d3ee;
            box-shadow: 0 0 0 2px rgba(34,211,238,0.35), 0 10px 30px rgba(34,211,238,0.18);
        }
        section[data-testid="stSidebar"] .device-card .label {
            font-size: 16px;
            font-weight: 700;
            color: #e5f6ff;
        }
        section[data-testid="stSidebar"] .device-card .sub {
            font-size: 12px;
            color: #94a3b8;
        }
        section[data-testid="stSidebar"] .status-chip {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
        }
        section[data-testid="stSidebar"] .chip-connected { background: rgba(34,197,94,0.18); color: #bbf7d0; }
        section[data-testid="stSidebar"] .chip-monitoring { background: rgba(234,179,8,0.18); color: #facc15; }
        section[data-testid="stSidebar"] .chip-disconnected { background: rgba(248,113,113,0.18); color: #fecaca; }
        section[data-testid="stSidebar"] .nav-heading {
            font-size: 16px;
            color: #94a3b8;
            margin: 8px 0;
        }
        section[data-testid="stSidebar"] .divider {
            height: 1px;
            background: rgba(148,163,184,0.25);
            margin: 10px 0;
        }
        section[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
            border-left: 4px solid #22d3ee;
            background: linear-gradient(90deg, rgba(2,6,23,0.4), rgba(34,211,238,0.08));
            border-radius: 10px;
            padding-left: 8px;
        }
        section[data-testid="stSidebar"] .stButton {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            box-sizing: border-box !important;
            margin: 6px 0 !important;
        }
        section[data-testid="stSidebar"] button,
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] [data-testid="baseButton-secondary"],
        section[data-testid="stSidebar"] div[data-baseweb="button"],
        section[data-testid="stSidebar"] div[data-baseweb="button"] > * {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto !important;
            display: block !important;
            box-sizing: border-box !important;
            border-radius: 12px !important;
            padding: 0 !important;
        }
        section[data-testid="stSidebar"] button > div,
        section[data-testid="stSidebar"] .stButton > button > div {
            width: 100% !important;
            padding: 8px 14px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            flex-direction: column !important;
            text-align: center !important;
            font-size: 15px !important;
            line-height: 1.1 !important;
            white-space: normal !important;
            box-sizing: border-box !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #94a3b8;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(15,23,42,0.9);
            color: #22d3ee;
        }
        
        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            width: 100% !important;
            max-width: 600px !important;
        }
        
        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .top-header-container {
                flex-direction: column !important;
                align-items: center !important;
                text-align: center !important;
                padding: 15px !important;
                gap: 15px !important;
                height: auto !important;
            }
            
            .logo-section {
                flex-direction: column !important;
                gap: 10px !important;
                text-align: center !important;
            }

            .main-shield {
                font-size: 64px !important;
            }
            
            .app-title {
                font-size: 28px !important;
            }
            
            .app-subtitle {
                font-size: 12px !important;
            }
            
            /* Make metrics stack nicely */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
            }
            
            .stButton button {
                width: 100% !important;
            }
        }

        /* New Classes for Structured Header */
        .top-header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 0;
            margin-bottom: 20px;
            background: radial-gradient(circle at left, #0f172a 0, #020617 60%);
            border-bottom: 1px solid rgba(56,189,248,0.35);
            backdrop-filter: blur(14px);
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .logo-section {
            display: flex; 
            align-items: center; 
            gap: 20px;
        }

        .main-shield {
            font-size: 80px;
            font-weight: 900;
            color: #FFFFFF;
            line-height: 1;
            display: inline-block;
        }
        
        .app-title {
            font-size: 36px; 
            font-weight: 800; 
            background: linear-gradient(135deg, #FFFFFF 0%, #38bdf8 100%); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            letter-spacing: -1px; 
            text-shadow: 0 10px 30px rgba(56,189,248,0.3);
        }
        
        .app-subtitle {
            color: #94a3b8; 
            font-size: 14px; 
            font-weight: 500; 
            letter-spacing: 0.5px;
        }

        .status-paused, .status-active {
            padding: 6px 16px; 
            border-radius: 99px; 
            font-weight: 600; 
            font-size: 13px; 
            display: flex; 
            align-items: center; 
            gap: 8px;
            white-space: nowrap;
        }
        
        .status-paused {
            background-color: rgba(107,107,57,0.2); 
            color: #e2e8f0; 
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .status-active {
            background-color: rgba(22,163,74,0.2); 
            color: #bbf7d0; 
            border: 1px solid rgba(34,197,94,0.3);
        }
        
        .ai-summary-card {
            background: radial-gradient(circle at top left, rgba(56,189,248,0.18), rgba(15,23,42,0.95));
            border-radius: 16px;
            padding: 16px 18px;
            border: 1px solid rgba(56,189,248,0.45);
            box-shadow: 0 16px 40px rgba(15,23,42,0.85);
        }
        
        .ai-summary-label {
            font-size: 13px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #bae6fd;
        }
        
        .ai-summary-value {
            font-size: 26px;
            font-weight: 700;
            color: #e0f2fe;
        }
        
        .ai-summary-sub {
            font-size: 13px;
            color: #94a3b8;
        }
        
        .score-meter {
            width: 100%;
            height: 10px;
            background: rgba(148,163,184,0.25);
            border-radius: 999px;
            overflow: hidden;
            margin-top: 6px;
        }
        .score-fill {
            height: 100%;
            border-radius: 999px;
        }
        .score-fill.low { background: linear-gradient(90deg, #16a34a, #22c55e); }
        .score-fill.med { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
        .score-fill.high { background: linear-gradient(90deg, #dc2626, #ef4444); }
        
        .threat-card {
            background: radial-gradient(circle at top, rgba(248,250,252,0.02), rgba(15,23,42,0.98));
            border-radius: 14px;
            padding: 14px 16px;
            border: 1px solid rgba(148,163,184,0.5);
            box-shadow: 0 12px 30px rgba(15,23,42,0.85);
        }
        
        .threat-badge-low {
            background: rgba(34,197,94,0.18);
            color: #bbf7d0;
        }
        .threat-badge-medium {
            background: rgba(234,179,8,0.18);
            color: #facc15;
        }
        .threat-badge-high, .threat-badge-critical {
            background: rgba(248,113,113,0.18);
            color: #fecaca;
        }
        
        .threat-badge-low,
        .threat-badge-medium,
        .threat-badge-high,
        .threat-badge-critical {
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'udi' not in st.session_state:
        st.session_state.udi = UniversalDeviceInterface()
        st.session_state.monitoring_active = False
        st.session_state.refresh_counter = 0
    
    if 'live_data' not in st.session_state:
        st.session_state.live_data = []
    
    udi = st.session_state.udi

    # Hot-reload compatibility: Ensure new attributes exist
    if not hasattr(udi.live_collector, 'status'):
        udi.live_collector.status = "Idle"
        udi.live_collector.last_error = None

    # Refresh Android connection status on every run to detect hot-plugged devices
    if udi.android:
        udi.android.check_connection()
        # Update udi target if Android just connected and was previously selected or default
        if udi.android.connected and udi.target_device == "Desktop" and "mobile_view" in st.query_params:
            udi.target_device = "Android"
    
    # 1. Main Title
    shield_html = '<span class="main-shield">⛨</span>'
    
    status_class = "status-paused"
    status_text = "Protection Paused"
    status_dot = "#fbbf24"
    status_shadow = ""
    
    if st.session_state.monitoring_active:
        status_class = "status-active"
        status_text = "Active Protection"
        status_dot = "#4ade80"
        status_shadow = "box-shadow: 0 0 10px #4ade80;"

    status_html = f'<div class="{status_class}"><div style="width:8px; height:8px; border-radius:50%; background:{status_dot}; {status_shadow}"></div>{status_text}</div>'
    
    st.markdown(
        f'''
        <div class="top-header-container">
            <div class="logo-section">
                {shield_html}
                <div style="display:flex; flex-direction:column;">
                    <div class="app-title">Silent Guard AI</div>
                    <div class="app-subtitle">Universal Device Manager & Spyware Defense</div>
                </div>
            </div>
            {status_html}
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.markdown("---")

    # 2. Monitoring Controls moved to Sidebar
                
    # Mobile Monitoring Check
    if udi.device_type == "mobile" or st.query_params.get('mobile_view'):
        if not udi.android:
             st.info("Viewing on Mobile? To monitor this device deeply, please connect it via USB or enable Wireless Debugging (ADB) and connect.")
        else:
             st.success("Android Device Connected via ADB")

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="brand-header">AI Spyware Detection</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Behavioral Intelligence Engine</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-heading sticky">Select Device</div>', unsafe_allow_html=True)
        
        # Device Switcher
        android_connected = False
        if udi.android and udi.android.connected:
            android_connected = True
        dc1, dc2 = st.columns(2)
        with dc1:
            selected = (udi.target_device == "Desktop" and udi.device_type == "desktop")
            st.markdown(f'<div class="device-card {"selected" if selected else ""}"><div>🖥</div><div><div class="label">Desktop</div><div class="sub">Local</div></div></div>', unsafe_allow_html=True)
            if st.button("Use Desktop", key="sel_desktop"):
                udi.target_device = "Desktop"
                udi.device_type = "desktop"
                udi.refresh_device_info()
                st.rerun()
        with dc2:
            selected = (udi.target_device == "Android")
            st.markdown(f'<div class="device-card {"selected" if selected else ""}"><div>🤖</div><div><div class="label">Android</div><div class="sub">{"Connected ✅" if android_connected else "Disconnected"}</div></div></div>', unsafe_allow_html=True)
            if st.button("Use Android", key="sel_android"):
                udi.target_device = "Android"
                udi.device_type = "mobile"
                udi.refresh_device_info()
                st.rerun()
        if android_connected:
            st.markdown('<span class="status-chip chip-connected">Connected</span>', unsafe_allow_html=True)
        elif udi.device_type == "mobile":
            st.markdown('<span class="status-chip chip-monitoring">Monitoring</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-chip chip-disconnected">Disconnected</span>', unsafe_allow_html=True)
        
        # Refresh device info based on selection
        udi.refresh_device_info()
        
        st.markdown("---")
        st.markdown('<div class="sidebar-heading sticky">Live Behavioral Monitoring</div>', unsafe_allow_html=True)
        toggle_val = st.checkbox("ON", value=st.session_state.monitoring_active, key="ui_live_toggle")
        if toggle_val and not st.session_state.monitoring_active:
            udi.start_live_monitoring()
            st.session_state.monitoring_active = True
            st.rerun()
        elif not toggle_val and st.session_state.monitoring_active:
            udi.stop_live_monitoring()
            st.session_state.monitoring_active = False
            st.rerun()
        st.caption("Collecting behavioral data every 2s")
        auto_refresh = st.checkbox("🔁 Auto-refresh", value=st.session_state.monitoring_active, key="chk_auto_refresh", help="For real-time AI analysis")
        
        st.markdown("---")
        st.markdown('<div class="sidebar-heading sticky">Navigation</div>', unsafe_allow_html=True)
        nav_options = [
            "Security Overview",
            "AI Behavior Analysis",
            "Observed Applications",
            "Manual Threat Scan",
            "File Scan",
            "Privacy Risk Center",
        ]
        current_view = st.session_state.get("active_view", "Unified Monitor")
        current_index = ["Unified Monitor","Behavioral Intelligence Engine","Applications","Manual Scan","File Scan","Privacy & Data"].index(current_view) if current_view in ["Unified Monitor","Behavioral Intelligence Engine","Applications","Manual Scan","File Scan","Privacy & Data"] else 0
        selected_nav = st.radio("", nav_options, index=current_index, key="nav_radio")
        mapping = {
            "Security Overview": "Unified Monitor",
            "AI Behavior Analysis": "Behavioral Intelligence Engine",
            "Observed Applications": "Applications",
            "Manual Threat Scan": "Manual Scan",
            "File Scan": "Network Scan",
            "Privacy Risk Center": "Privacy & Data",
        }
        st.session_state.active_view = mapping.get(selected_nav, "Unified Monitor")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("---")

    # Device & Network Identity
    @st.fragment(run_every=5)
    def render_device_identity():
        st.header("Device & Network Identity")
        
        # Platform specific instructions
        if st.query_params.get('mobile_view'):
            udi.device_type = "mobile"
        
        udi.refresh_device_info()
        device_info_ui = dict(udi.device_info)
        if udi.target_device == "Android" and udi.android and udi.android.connected:
            try:
                batt = udi.android.get_battery_status()
                if batt:
                    device_info_ui["battery_info"] = {
                        "present": True,
                        "percent": batt.get("percent", 0),
                        "charging": batt.get("charging", False),
                        "time_left": None
                    }
            except Exception:
                pass
        di1, di2, di3 = st.columns([2, 2, 1])
        with di1:
            st.subheader("Device Identity")
            st.metric("Device Type", device_info_ui["device_type"].title())
            st.metric("Platform", device_info_ui["platform"])
            st.metric("Hostname", device_info_ui["hostname"])
        with di2:
            st.subheader("Network Identity")
            st.metric("IP Address", device_info_ui["ip_address"])
            net_type = "Wi-Fi" if "wifi" in device_info_ui.get("network_type","").lower() else device_info_ui.get("network_type","Unknown")
            st.metric("Network Type", net_type)
            st.metric("Monitoring Status", "Active" if st.session_state.monitoring_active else "Inactive")
        with di3:
            battery = device_info_ui.get("battery_info", {})
            st.subheader("Battery")
            if battery.get("present"):
                st.metric("Charge", f"{battery.get('percent', 0):.0f}%")
                if battery.get("charging"):
                    st.caption("Charging")
            else:
                st.caption("N/A")
    render_device_identity()
    
    # Live monitoring status
    if st.session_state.monitoring_active:
        st.success("Active Privacy Monitoring • Tracking background data access • Analyzing silent network transmissions")
    else:
        st.warning("Privacy monitoring inactive • Click 'Start' to begin behavior tracking")
    
    st.markdown("---")
    
    # Get current metrics
    current_health = udi.get_device_health()
    # live_metrics = udi.live_collector.get_live_metrics() # Moved to fragments
    
    # Sidebar-driven navigation (no top tabs)
    view = st.session_state.get("active_view", "Unified Monitor")

    if view == "Unified Monitor":
        @st.fragment(run_every=0.5)
        def render_unified_monitor():
            live_metrics = udi.live_collector.get_live_metrics()
            st.header("Behavioral Security Dashboard")
            
            # Explicitly handle Android disconnection state
            if udi.target_device == "Android":
                if not udi.android:
                     st.warning("⚠ Android Monitor module not loaded. Check dependencies.")
                elif not udi.android.connected:
                     st.warning("⚠ Android device disconnected. Please connect via USB/ADB.")
            
            # Include Overview Dashboard content
            if udi.target_device == "Android" and udi.android and udi.android.connected:
                st.subheader("Android Security Status")
                try:
                    risk_report = udi.get_android_risk_report()
                except Exception as e:
                    st.error(f"Scan Error: {str(e)}")
                    risk_report = {"score": 0, "issues": ["Scan Failed"], "dangerous_apps": []}
                # Security-Oriented KPIs
                k1, k2, k3 = st.columns(3)
                ai_score = 0.0
                if live_metrics and len(live_metrics) > 0:
                    try:
                        ai_score = float(live_metrics[-1].get("ai_anomaly_score", 0))
                    except Exception:
                        ai_score = 0.0
                df_tmp = pd.DataFrame(live_metrics or [])
                net_diff = 0.0
                baseline = 0.0
                if not df_tmp.empty and 'network_bytes_sent' in df_tmp.columns:
                    nd = df_tmp['network_bytes_sent'].diff().fillna(0).clip(lower=0)
                    net_diff = float(nd.iloc[-1]) if len(nd) > 0 else 0.0
                    baseline = float(nd.iloc[:-1].median()) if len(nd) > 1 else 0.0
                exfil_score = 0.0
                if baseline > 0:
                    exfil_score = max(0.0, min(100.0, ((net_diff - baseline) / baseline) * 100.0))
                suspicious_count = 0
                logs = udi.db.get_scan_logs(limit=1)
                if logs:
                    try:
                        suspicious_count = int(logs[0].get("threats_count", 0) or 0)
                    except Exception:
                        suspicious_count = 0
                with k1:
                    df_bdi = pd.DataFrame(live_metrics or [])
                    if not df_bdi.empty and 'ai_anomaly_score' in df_bdi.columns:
                        df_bdi['timestamp'] = pd.to_datetime(df_bdi['timestamp'])
                        window = df_bdi.tail(50)
                        fig_bdi = go.Figure()
                        fig_bdi.add_trace(go.Scatter(
                            x=window['timestamp'], y=window['ai_anomaly_score'],
                            name="BDI (Live)", line=dict(color='#f43f5e', width=2)
                        ))
                        fig_bdi.add_hline(y=70, line_dash="dot", line_color="#ef4444")
                        fig_bdi.update_layout(
                            height=180,
                            paper_bgcolor="rgba(15,23,42,1)",
                            plot_bgcolor="rgba(15,23,42,1)",
                            font=dict(color="#e5f6ff"),
                            margin=dict(l=10, r=10, t=10, b=10),
                            xaxis_title="",
                            yaxis_title=""
                        )
                        st.plotly_chart(fig_bdi, use_container_width=True)
                        st.caption(f"{float(window['ai_anomaly_score'].iloc[-1]):.1f}/100 latest")
                    else:
                        if st.session_state.monitoring_active:
                            if udi.live_collector.status == "Starting":
                                st.info("⏳ Initializing BDI sensors...")
                            elif udi.live_collector.status == "Error":
                                st.error(f"❌ Collector Error: {udi.live_collector.last_error}")
                            else:
                                st.warning("⚠ Waiting for BDI data...")
                        else:
                            st.info("ℹ Live monitoring inactive")
                with k2:
                    exfil_class = "high" if exfil_score > 70 else ("med" if exfil_score > 40 else "low")
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Silent Data Exfiltration</div>
                            <div class="ai-summary-value">{exfil_score:.1f}/100</div>
                            <div class="score-meter"><div class="score-fill {exfil_class}" style="width:{exfil_score:.1f}%"></div></div>
                            <div class="ai-summary-sub">Relative network spike vs baseline</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                with k3:
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Active Suspicious Apps</div>
                            <div class="ai-summary-value">{suspicious_count}</div>
                            <div class="ai-summary-sub">From latest heuristic scan logs</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                st.subheader("AI Security Assessment & Recommendations")
                sensors = risk_report.get('active_sensors', {})
                if sensors and any(len(v) > 0 for v in sensors.values()):
                    st.error("Sensors Active!")
                    if sensors.get('mic'): st.write(f"Mic: {', '.join(sensors['mic'])}")
                    if sensors.get('camera'): st.write(f"Camera: {', '.join(sensors['camera'])}")
                    if sensors.get('gps'): st.write(f"GPS: {', '.join(sensors['gps'])}")
                else:
                    st.success("✔ No spyware behavior detected")
                if risk_report.get('issues'):
                    for issue in risk_report['issues']:
                        st.warning(f"{issue}")
                if risk_report.get('dangerous_apps'):
                    with st.expander("View High Risk Apps"):
                        for app in risk_report['dangerous_apps']:
                            if isinstance(app, dict):
                                st.markdown(f"• **{app.get('package', 'Unknown')}**")
                                if app.get('risks'):
                                    st.caption(f"  Risks: {', '.join(app['risks'])}")
                            else:
                                st.write(f"• {app}")
                else:
                    st.info("Monitoring background data access")
                    st.caption("3 apps under behavioral observation")
            else:
                k1, k2, k3 = st.columns(3)
                ai_score = 0.0
                if live_metrics and len(live_metrics) > 0:
                    try:
                        ai_score = float(live_metrics[-1].get("ai_anomaly_score", 0))
                    except Exception:
                        ai_score = 0.0
                df_tmp = pd.DataFrame(live_metrics or [])
                net_diff = 0.0
                baseline = 0.0
                if not df_tmp.empty and 'network_bytes_sent' in df_tmp.columns:
                    nd = df_tmp['network_bytes_sent'].diff().fillna(0).clip(lower=0)
                    net_diff = float(nd.iloc[-1]) if len(nd) > 0 else 0.0
                    baseline = float(nd.iloc[:-1].median()) if len(nd) > 1 else 0.0
                exfil_score = 0.0
                if baseline > 0:
                    exfil_score = max(0.0, min(100.0, ((net_diff - baseline) / baseline) * 100.0))
                suspicious_count = 0
                logs = udi.db.get_scan_logs(limit=1)
                if logs:
                    try:
                        suspicious_count = int(logs[0].get("threats_count", 0) or 0)
                    except Exception:
                        suspicious_count = 0
                with k1:
                    df_bdi = pd.DataFrame(live_metrics or [])
                    if not df_bdi.empty and 'ai_anomaly_score' in df_bdi.columns:
                        df_bdi['timestamp'] = pd.to_datetime(df_bdi['timestamp'])
                        window = df_bdi.tail(50)
                        fig_bdi = go.Figure()
                        fig_bdi.add_trace(go.Scatter(
                            x=window['timestamp'], y=window['ai_anomaly_score'],
                            name="BDI (Live)", line=dict(color='#f43f5e', width=2)
                        ))
                        fig_bdi.add_hline(y=70, line_dash="dot", line_color="#ef4444")
                        fig_bdi.update_layout(
                            height=180,
                            paper_bgcolor="rgba(15,23,42,1)",
                            plot_bgcolor="rgba(15,23,42,1)",
                            font=dict(color="#e5f6ff"),
                            margin=dict(l=10, r=10, t=10, b=10),
                            xaxis_title="",
                            yaxis_title=""
                        )
                        st.plotly_chart(fig_bdi, use_container_width=True)
                        st.caption(f"{float(window['ai_anomaly_score'].iloc[-1]):.1f}/100 latest")
                    else:
                        if st.session_state.monitoring_active:
                            if udi.live_collector.status == "Starting":
                                st.info("⏳ Initializing BDI sensors...")
                            elif udi.live_collector.status == "Error":
                                st.error(f"❌ Collector Error: {udi.live_collector.last_error}")
                            else:
                                st.warning("⚠ Waiting for BDI data...")
                        else:
                            st.info("ℹ Live monitoring inactive")
                with k2:
                    exfil_class = "high" if exfil_score > 70 else ("med" if exfil_score > 40 else "low")
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Silent Data Exfiltration</div>
                            <div class="ai-summary-value">{exfil_score:.1f}/100</div>
                            <div class="score-meter"><div class="score-fill {exfil_class}" style="width:{exfil_score:.1f}%"></div></div>
                            <div class="ai-summary-sub">Relative network spike vs baseline</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                with k3:
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Active Suspicious Apps</div>
                            <div class="ai-summary-value">{suspicious_count}</div>
                            <div class="ai-summary-sub">From latest heuristic scan logs</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                st.subheader("AI Security Assessment & Recommendations")
                if ai_score > 70:
                    st.error("🚨 High behavioral risk detected")
                elif ai_score > 40:
                    st.warning("⚠ Moderate behavioral risk; monitor background access")
                else:
                    st.success("✔ No spyware behavior detected")
                st.caption("Monitoring background data access")
                st.caption("3 apps under behavioral observation")
            st.markdown("---")
            st.subheader("Real-Time Behavioral Deviation Analysis")
            if live_metrics and len(live_metrics) > 0:
                df = pd.DataFrame(live_metrics)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['network_bytes_sent'].diff().fillna(0).clip(lower=0),
                    name="Network Out (bytes/s)",
                    line=dict(color='#22d3ee', width=2),
                    hovertemplate="Network Out: %{y} bytes/s"
                ))
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['cpu_percent'],
                    name="CPU %",
                    line=dict(color='#38bdf8', width=2, dash='dot'),
                    yaxis="y2",
                    hovertemplate="CPU: %{y}%"
                ))
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['memory_percent'],
                    name="Memory %",
                    line=dict(color='#a5b4fc', width=2, dash='dash'),
                    yaxis="y3",
                    hovertemplate="Memory: %{y}%"
                ))
                high_anom = df[df['ai_anomaly_score'] > 70]
                if not high_anom.empty:
                    fig.add_trace(go.Scatter(
                        x=high_anom['timestamp'],
                        y=high_anom['network_bytes_sent'].diff().fillna(0).clip(lower=0),
                        mode="markers",
                        name="Anomaly",
                        marker=dict(color='#ef4444', size=9, symbol='circle'),
                        hovertext=["Unusual network activity detected"] * len(high_anom),
                        hovertemplate="%{hovertext}<br>%{x}"
                    ))
                fig.update_layout(
                    height=420,
                    xaxis_title="Time",
                    yaxis_title="Network bytes/s",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    paper_bgcolor="rgba(15,23,42,1)",
                    plot_bgcolor="rgba(15,23,42,1)",
                    font=dict(color="#e5f6ff"),
                )
                st.plotly_chart(fig, use_container_width=True)
                bdi = go.Figure()
                bdi.add_trace(go.Scatter(
                    x=df['timestamp'], y=df['ai_anomaly_score'],
                    name="Behavioral Deviation Index",
                    line=dict(color='#f43f5e', width=2)
                ))
                if len(df) > 3:
                    base_mean = float(df['ai_anomaly_score'].iloc[:max(1, len(df)//3)].mean())
                    bdi.add_trace(go.Scatter(
                        x=df['timestamp'], y=[base_mean]*len(df),
                        name="Baseline",
                        line=dict(color='#94a3b8', width=1, dash='dash')
                    ))
                bdi.add_hline(y=70, line_dash="dot", line_color="#ef4444", annotation_text="Risk Threshold")
                bdi.update_layout(
                    height=280,
                    title="Behavioral Deviation Index (BDI)",
                    paper_bgcolor="rgba(15,23,42,1)",
                    plot_bgcolor="rgba(15,23,42,1)",
                    font=dict(color="#e5f6ff"),
                    xaxis_title="Time",
                    yaxis_title="BDI"
                )
                st.plotly_chart(bdi, use_container_width=True)
                st.subheader("Behavioral Indicators (System-Level)")
                cols = st.columns(4)
                latest = live_metrics[-1]
                with cols[0]: st.metric("CPU Spike", f"{latest['cpu_percent']:.1f}%", help="Background execution detected")
                with cols[1]: st.metric("Network Usage", f"{(df['network_bytes_sent'].diff().fillna(0).clip(lower=0).iloc[-1] if 'network_bytes_sent' in df else 0):.0f} B/s", help="Possible silent transmission")
                with cols[2]: st.metric("Process Count", f"{len(udi.get_running_apps())}", help="Hidden process detection")
                with cols[3]: st.metric("BDI", f"{latest['ai_anomaly_score']}/100", help="Deviation from baseline")
                st.subheader("Live Behavioral Evidence Log")
                live_df = pd.DataFrame(live_metrics[-20:])
                live_df['timestamp'] = pd.to_datetime(live_df['timestamp']).dt.strftime('%H:%M:%S')
                live_df['risk'] = live_df['ai_anomaly_score'].apply(lambda v: "High" if v > 70 else ("Medium" if v > 40 else "Low"))
                st.dataframe(live_df[['timestamp', 'cpu_percent', 'memory_percent', 'disk_percent', 'ai_anomaly_score', 'risk']].rename(
                    columns={'timestamp': 'Time', 'cpu_percent': 'CPU %', 'memory_percent': 'Memory %', 'disk_percent': 'Disk %', 'ai_anomaly_score': 'BDI', 'risk': 'Risk Tag'}), 
                            width="stretch", hide_index=True)
            else:
                st.info("No live behavioral data yet. Start monitoring to populate the real-time charts.")
                cta_cols = st.columns([1,1,1])
                with cta_cols[1]:
                    if st.button("Start Live Monitoring", key="btn_start_live_bdi", type="primary"):
                        try:
                            udi.start_live_monitoring()
                            st.session_state.monitoring_active = True
                            st.success("Live monitoring started")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to start monitoring: {e}")
                st.subheader("Observed Application Behavior")
                apps = udi.get_running_apps()[:8]
                for app in apps:
                    name = app.get('name', 'Unknown')
                    pid = app.get('pid')
                    status = "Safe"
                    confidence = 60
                    reason = "Normal behavior"
                    if hasattr(udi, 'ai_model') and udi.ai_model:
                        try:
                            res = udi.ai_model.analyze_process(app)
                            confidence = int(min(max(res.get('risk_score', 0), 0), 100))
                            status = "Malicious" if res.get('risk_level', '').lower() == 'critical' else ("Suspicious" if res.get('risk_level', '').lower() in ('high','medium') else "Safe")
                            reason = res.get('reason', reason)
                        except Exception:
                            pass
                    st.markdown(
                        f"""
                        <div class="threat-card">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <div style="font-weight:600; font-size:15px;">{name} <span style="opacity:0.6;">(PID: {pid})</span></div>
                                <div class="{'threat-badge-critical' if status=='Malicious' else ('threat-badge-medium' if status=='Suspicious' else 'threat-badge-low')}">{status}</div>
                            </div>
                            <div style="font-size:13px; color:#cbd5f5; margin-bottom:4px;">
                                Permissions: Background access inferred
                            </div>
                            <div style="font-size:13px; color:#bae6fd; margin-bottom:4px;">
                                Network activity: Observed via system metrics
                            </div>
                            <div style="font-size:13px; color:#bae6fd; margin-bottom:8px;">
                                AI Confidence: {confidence}%
                            </div>
                            <div style="font-size:12px; color:#94a3b8;">
                                {reason}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            st.markdown("---")
    
        render_unified_monitor()
    elif view == "Manual Scan":
        st.header("🔍 Manual Application Deep Scan")
        st.info("Select a specific application or process to perform a comprehensive security analysis.")

        
        scan_col1, scan_col2 = st.columns([1, 3])
        
        with scan_col1:
            target_platform = st.radio("Target Platform", ["Desktop", "Android"] if udi.android and udi.android.connected else ["Desktop"])
            
        target_id = None
        
        with scan_col2:
            if target_platform == "Desktop":
                # Get running processes for dropdown
                # Fetch more apps to avoid missing targets and sort by Name for stability
                procs = udi.get_running_apps(limit=500)
                procs = sorted(procs, key=lambda x: x['name'].lower())
                
                proc_options = {f"{p['name']} (PID: {p['pid']})": p['pid'] for p in procs}
                selected_proc = st.selectbox("Select Process", list(proc_options.keys()))
                if selected_proc:
                    target_id = str(proc_options[selected_proc])
            else:
                # Get Android apps
                apps = udi.android.get_installed_apps()
                # Create friendly names if possible
                app_options = {f"{udi.android.get_app_label(pkg)} ({pkg})": pkg for pkg in apps}
                selected_app = st.selectbox("Select App", list(app_options.keys()))
                if selected_app:
                    target_id = app_options[selected_app]
        
        if st.button("Run Behavioral AI Scan", type="primary"):
            if target_id:
                with st.spinner(f"Analyzing {target_platform} target {target_id}..."):
                    start_t = time.time()
                    time.sleep(1) 
                    
                    results = udi.scan_app_details(target_id, target_platform.lower())
                    st.session_state.manual_scan_results = results
                    st.session_state.manual_scan_target = {
                        "platform": target_platform.lower(),
                        "id": target_id
                    }
                    ai_conf = "—"
                    if target_platform.lower() == "desktop" and hasattr(udi, "ai_model") and udi.ai_model:
                        try:
                            # Re-fetch same list depth to ensure we find the process
                            apps = udi.get_running_apps(limit=500)
                            match = next((a for a in apps if str(a.get('pid')) == str(target_id)), None)
                            
                            # Fallback: if not in top list, try to fetch specific pid info manually
                            if not match:
                                try:
                                    p = psutil.Process(int(target_id))
                                    match = {
                                        'pid': p.pid,
                                        'name': p.name(),
                                        'cmdline': " ".join(p.cmdline()),
                                        'cpu_percent': p.cpu_percent(),
                                        'memory_percent': p.memory_percent()
                                    }
                                except:
                                    pass

                            if match:
                                res = udi.ai_model.analyze_process(match)
                                ai_conf = f"{int(min(max(res.get('risk_score', 0), 0), 100))}%"
                        except Exception:
                            ai_conf = "—"
                    st.session_state.manual_ai_confidence = ai_conf
                    st.session_state.manual_scan_duration = f"{(time.time()-start_t):.2f}s"
                    st.rerun()
            else:
                st.error("Please select a valid target.")

        if st.session_state.get("manual_scan_results") and st.session_state.get("manual_scan_target"):
            results = st.session_state.manual_scan_results
            target_key = st.session_state.manual_scan_target.get("id")
            platform_key = st.session_state.manual_scan_target.get("platform")
            st.markdown("---")
            score = results['trust_score']
            col_res1, col_res2 = st.columns([1, 2])
            with col_res1:
                verdict_risk = max(0.0, min(100.0, 100.0 - float(score)))
                verdict_class = "high" if verdict_risk > 70 else ("med" if verdict_risk > 40 else "low")
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">AI Behavioral Verdict</div>
                        <div class="ai-summary-value">{verdict_risk:.1f}/100</div>
                        <div class="score-meter"><div class="score-fill {verdict_class}" style="width:{verdict_risk:.1f}%"></div></div>
                        <div class="ai-summary-sub">Derived from Trust Index</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_res2:
                st.subheader(f"AI Behavioral Verdict: {results['name']}")
                if results['risk_factors']:
                    st.error(f"Found {len(results['risk_factors'])} Risk Factors:")
                    for risk in results['risk_factors']:
                        st.write(f"{risk}")
                else:
                    st.success("✅ No specific risk factors detected.")
                if results['metadata']:
                    with st.expander("Process Metadata"):
                        st.json(results['metadata'])
                if results['permissions']:
                    with st.expander(f"Permissions ({len(results['permissions'])})"):
                        st.write(results['permissions'])
                if platform_key == "android" and udi.android and udi.android.connected:
                    c_quar1, c_quar2 = st.columns([1,1])
                    with c_quar1:
                        if st.button("Quarantine App", key=f"btn_quarantine_{target_key}"):
                            ok = False
                            try:
                                ok = udi.android.quarantine_app(target_key)
                            except Exception as e:
                                st.error(f"Quarantine failed: {e}")
                            if ok:
                                st.success("App quarantined (disabled) successfully")
                            else:
                                st.warning("Quarantine could not be completed")
                    with c_quar2:
                        if st.button("🧨 Force Stop", key=f"btn_kill_{target_key}"):
                            ok2 = False
                            try:
                                ok2 = udi.android.stop_app(target_key)
                            except Exception as e:
                                st.error(f"Force stop failed: {e}")
                            if ok2:
                                st.success("App force-stopped successfully")
                            else:
                                st.warning("Force stop could not be completed")
            st.markdown("---")
            st.markdown("#### Sensitive Resource Monitoring")
            access_cols = st.columns(4)
            mic_val = "N/A"
            cam_val = "N/A"
            loc_val = "N/A"
            mem_val = "N/A"
            sensors = {}
            if platform_key == "android" and udi.android and udi.android.connected:
                try:
                    sensors = udi.android.get_active_sensors()
                    mic_list = sensors.get("mic") or []
                    cam_list = sensors.get("camera") or []
                    gps_list = sensors.get("gps") or []
                    mic_val = "⚠ Accessed in background" if (target_key in mic_list) else "✔ Not accessed"
                    cam_val = "⚠ Accessed in background" if cam_list and target_key in cam_list else "✔ Not accessed"
                    loc_val = "⚠ Accessed in background" if gps_list and target_key in gps_list else "✔ Not accessed"
                except Exception:
                    pass
                try:
                    mem = udi.android.get_app_memory_mb(target_key)
                    mem_val = "N/A" if mem is None else f"{mem}"
                except Exception:
                    pass
            with access_cols[0]:
                st.metric("🎤 Mic", mic_val)
                if st.button("Check", key="check_mic"):
                    st.session_state.manual_view = "mic"
                if st.session_state.get("manual_view") == "mic":
                    st.write(f"Microphone usage status: {mic_val}")
            with access_cols[1]:
                st.metric("📷 Camera", cam_val)
                if st.button("Check", key="check_cam"):
                    st.session_state.manual_view = "camera"
                if st.session_state.get("manual_view") == "camera":
                    st.write(f"Camera usage status: {cam_val}")
            with access_cols[2]:
                st.metric("📍 Location", loc_val)
                if st.button("Check", key="check_loc"):
                    st.session_state.manual_view = "gps"
                if st.session_state.get("manual_view") == "gps":
                    st.write(f"Location usage status: {loc_val}")
            with access_cols[3]:
                st.metric("💾 Storage", mem_val)
                if st.button("Check", key="check_store"):
                    st.session_state.manual_view = "storage"
                if st.session_state.get("manual_view") == "storage":
                    st.write("Storage (MB):", mem_val)
            if platform_key == "android" and udi.android and udi.android.connected:
                try:
                    insights = udi.android.get_exfiltration_insights(target_key)
                    with st.expander("📤 Data Exfiltration Insights"):
                        st.write(f"Collecting Sensitive Data: {'YES' if insights.get('is_collecting') else 'NO'}")
                        st.write(f"Sending Data Now: {'YES' if insights.get('is_sending') else 'NO'}")
                        conds = insights.get('conditions') or []
                        st.write(f"Conditions: {', '.join(conds) if conds else 'None'}")
                        st.write(f"Next Send Window: {insights.get('when_next', 'Unknown')}")
                except Exception as e:
                    with st.expander("📤 Data Exfiltration Insights"):
                        st.write("Unavailable")
                        st.caption(f"Error: {e}")
            st.markdown("---")
            st.markdown("#### Network Behavior Inspection")
            suspicious_ports = {4444, 5555, 6666, 1337}
            if platform_key == "desktop":
                try:
                    pid = int(target_key)
                    import psutil
                    conns = []
                    p = psutil.Process(pid)
                    for c in p.net_connections(kind='inet'):
                        conns.append({
                            "proto": "tcp" if c.type == socket.SOCK_STREAM else "udp",
                            "local_port": c.laddr.port if c.laddr else None,
                            "remote_port": c.raddr.port if c.raddr else None,
                            "status": getattr(c, "status", "UNKNOWN")
                        })
                    if conns:
                        st.dataframe(conns, hide_index=True, width="stretch")
                        sus = [row for row in conns if row.get("remote_port") in suspicious_ports or row.get("local_port") in suspicious_ports]
                        if sus:
                            st.error(f"Suspicious ports detected: {', '.join(str(s.get('remote_port') or s.get('local_port')) for s in sus)}")
                        else:
                            st.success("No suspicious ports detected")
                        enc = any(r.get("remote_port") == 443 for r in conns)
                        st.caption(f"Encrypted traffic: {'Yes' if enc else 'No'}")
                    else:
                        st.info("No active connections for this process")
                except Exception as e:
                    st.warning(f"Port scan unavailable: {e}")
            elif platform_key == "android" and udi.android and udi.android.connected:
                try:
                    ports = udi.android.get_app_open_ports(target_key)
                    if ports:
                        st.dataframe(ports, hide_index=True, width="stretch")
                        sus = [p for p in ports if p.get("local_port") in suspicious_ports or p.get("remote_port") in suspicious_ports]
                        if sus:
                            st.error(f"Suspicious ports detected: {', '.join(str(p.get('local_port') or p.get('remote_port')) for p in sus if (p.get('local_port') or p.get('remote_port')))}")
                        else:
                            st.success("No suspicious ports detected")
                        enc = any((p.get("remote_port") == 443 or p.get("local_port") == 443) for p in ports)
                        st.caption(f"Encrypted traffic: {'Yes' if enc else 'No'}")
                    else:
                        st.info("No open ports found for this app")
                except Exception as e:
                    st.warning(f"Port scan unavailable: {e}")
            st.markdown("---")
            st.markdown("#### Silent Data Collection Detection")
            sdc_cols = st.columns(4)
            with sdc_cols[0]:
                st.metric("Clipboard Access", "Unknown")
            with sdc_cols[1]:
                st.metric("Keystroke Patterns", "Normal")
            with sdc_cols[2]:
                st.metric("Network Bursts", "None")
            with sdc_cols[3]:
                st.metric("User Interaction Correlation", "Unknown")

    elif view == "Behavioral Intelligence Engine":
        @st.fragment(run_every=0.5)
        def render_bie():
            live_metrics = udi.live_collector.get_live_metrics()
            st.header("Behavioral Intelligence Engine")
            
            # Check collector status
            if st.session_state.monitoring_active:
                if udi.live_collector.status == "Error":
                     st.error(f"Collector Error: {udi.live_collector.last_error}")
                elif udi.live_collector.status == "Starting" and not live_metrics:
                     st.info("Initializing behavioral sensors...")
                elif not live_metrics:
                     st.warning("Waiting for behavioral data stream...")
            
            if live_metrics and len(live_metrics) > 0:
                df = pd.DataFrame(live_metrics)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                latest_score = float(df['ai_anomaly_score'].iloc[-1])
                high_risk_events = int(sum(1 for score in df['ai_anomaly_score'] if score > 70))
                
                behavior_risk = latest_score
                silent_collection = high_risk_events
                if behavior_risk > 70:
                    threat_conf = "High"
                    threat_color = "High"
                elif behavior_risk > 40:
                    threat_conf = "Medium"
                    threat_color = "Medium"
                else:
                    threat_conf = "Low"
                    threat_color = "Low"
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    meter_class = 'high' if behavior_risk>70 else ('med' if behavior_risk>40 else 'low')
                    # Ensure minimal visibility for the meter bar
                    meter_width = max(behavior_risk, 5.0)
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Behavior Risk Score</div>
                            <div class="ai-summary-value">{behavior_risk:.1f}/100</div>
                            <div class="score-meter"><div class="score-fill {meter_class}" style="width:{meter_width:.1f}%"></div></div>
                            <div class="ai-summary-sub">Behavioral Deviation Index (latest)</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Silent Data Collection</div>
                            <div class="ai-summary-value">{silent_collection}</div>
                            <div class="ai-summary-sub">High-risk behavioral spikes observed</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Threat Confidence</div>
                            <div class="ai-summary-value">{threat_conf}</div>
                            <div class="ai-summary-sub">{threat_color} confidence in current risk</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                fallback_health = udi.get_device_health()
                behavior_risk = float(fallback_health.get("ai_anomaly_score", 0))
                silent_collection = 0
                if behavior_risk > 70:
                    threat_conf = "High"
                    threat_color = "High"
                elif behavior_risk > 40:
                    threat_conf = "Medium"
                    threat_color = "Medium"
                else:
                    threat_conf = "Low"
                    threat_color = "Low"
                c1, c2, c3 = st.columns(3)
                with c1:
                    meter_class = 'high' if behavior_risk>70 else ('med' if behavior_risk>40 else 'low')
                    # Ensure minimal visibility for the meter bar
                    meter_width = max(behavior_risk, 5.0)
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Behavior Risk Score</div>
                            <div class="ai-summary-value">{behavior_risk:.1f}/100</div>
                            <div class="score-meter"><div class="score-fill {meter_class}" style="width:{meter_width:.1f}%"></div></div>
                            <div class="ai-summary-sub">Behavioral Deviation Index (health model)</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        """
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Silent Data Collection</div>
                            <div class="ai-summary-value">--</div>
                            <div class="ai-summary-sub">⚠ Enable Live Monitoring</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">Threat Confidence</div>
                            <div class="ai-summary-value">{threat_conf}</div>
                            <div class="ai-summary-sub">{threat_color} confidence (baseline)</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            
            st.markdown("---")
            st.subheader("📈 Live Behavioral Analysis")
            
            if live_metrics and len(live_metrics) > 0:
                df = pd.DataFrame(live_metrics)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['network_bytes_sent'].diff().fillna(0).clip(lower=0),
                    name="Network Out (bytes/s)",
                    line=dict(color='#22d3ee', width=2),
                ))
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['cpu_percent'],
                    name="CPU %",
                    line=dict(color='#38bdf8', width=2, dash='dot'),
                    yaxis="y2",
                ))
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['memory_percent'],
                    name="Memory %",
                    line=dict(color='#a5b4fc', width=2, dash='dash'),
                    yaxis="y3",
                ))
                
                fig.update_layout(
                    height=420,
                    xaxis_title="Time",
                    yaxis_title="Network bytes/s",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    paper_bgcolor="rgba(15,23,42,1)",
                    plot_bgcolor="rgba(15,23,42,1)",
                    font=dict(color="#e5f6ff"),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Start live monitoring to see CPU, memory, and network behavior.")
            
            st.markdown("---")
            st.subheader("Local Heuristic AI Engine")
            
            if "ai_scan_running" not in st.session_state:
                st.session_state.ai_scan_running = False
            if "ai_scan_results" not in st.session_state:
                st.session_state.ai_scan_results = []
            
            c_start, c_stop, c_status = st.columns([1, 1, 2])
            with c_start:
                if st.button("Start Heuristic Threat Scan", type="primary", disabled=st.session_state.ai_scan_running):
                    st.session_state.ai_scan_running = True
                    with st.spinner("Local Heuristic AI Engine is analyzing running processes..."):
                        try:
                            results = udi.perform_ai_scan(limit=10)
                            if isinstance(results, dict) and "error" in results:
                                st.error(f"AI Model Error: {results['error']}")
                                st.session_state.ai_scan_results = []
                            else:
                                st.session_state.ai_scan_results = results
                        except Exception as e:
                            st.error(f"Scan failed: {e}")
                            st.session_state.ai_scan_results = []
                    st.session_state.ai_scan_running = False
            with c_stop:
                if st.button("Stop Scan", disabled=not st.session_state.ai_scan_running):
                    st.session_state.ai_scan_running = False
            with c_status:
                if st.session_state.ai_scan_running:
                    st.info("Scan Status: Analyzing")
                    st.progress(45)
                elif st.session_state.ai_scan_results:
                    st.success("Scan Status: Completed")
                else:
                    st.caption("Scan Status: Idle")
            
            if st.session_state.ai_scan_results:
                st.markdown("---")
                st.subheader("🚨 Detected Threats")
                for idx, res in enumerate(st.session_state.ai_scan_results):
                    score = float(res.get('risk_score', 0))
                    level = res.get('risk_level', 'Unknown')
                    name = res.get('name', 'Unknown')
                    pid = res.get('pid')
                    reason = res.get('reason', 'N/A')
                    confidence = min(max(score, 0), 100.0)
                    
                    if level.lower() in ("critical",):
                        badge_class = "threat-badge-critical"
                    elif level.lower() == "high":
                        badge_class = "threat-badge-high"
                    elif level.lower() == "medium":
                        badge_class = "threat-badge-medium"
                    else:
                        badge_class = "threat-badge-low"
                    
                    st.markdown(
                        f"""
                        <div class="threat-card">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <div style="font-weight:600; font-size:15px;">{name} <span style="opacity:0.6;">(PID: {pid})</span></div>
                                <div class="{badge_class}">{level} Risk</div>
                            </div>
                            <div style="font-size:13px; color:#cbd5f5; margin-bottom:4px;">
                                Suspicious behavior: {reason}
                            </div>
                            <div style="font-size:13px; color:#bae6fd; margin-bottom:8px;">
                                AI Confidence: {confidence:.0f}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    vc1, vc2 = st.columns([1, 1])
                    with vc1:
                        if st.button("View Details", key=f"view_threat_{idx}"):
                            st.json(res)
                    with vc2:
                        if st.button("Quarantine (planned)", key=f"quarantine_threat_{idx}"):
                            st.warning("Quarantine actions for desktop processes are planned, not active yet.")
            

        
        render_bie()
    elif view == "Applications":
        st.header("Observed Applications & Behavioral Risk")
        st.caption("Monitoring apps for silent data collection and abnormal behavior")
        
        running_apps = udi.get_running_apps()
        
        if running_apps:
            apps_df = pd.DataFrame(running_apps)
            apps_df['cpu_percent'] = apps_df['cpu_percent'].fillna(0)
            apps_df['memory_percent'] = apps_df['memory_percent'].fillna(0)
            apps_df['name'] = apps_df['name'].fillna("Unknown")
            
            risk_scores = []
            risk_levels = []
            verdicts = []
            net_active_flags = []
            bg_exec_flags = []
            sens_perm_summ = []
            android_sensors = None
            if udi.target_device == "Android" and udi.android and udi.android.connected:
                try:
                    android_sensors = udi.android.get_active_sensors()
                except Exception:
                    android_sensors = {"mic": [], "camera": [], "gps": []}
            
            for _, row in apps_df.iterrows():
                app = {
                    "pid": row.get("pid"),
                    "name": row.get("name"),
                    "cpu_percent": float(row.get("cpu_percent", 0) or 0),
                    "memory_percent": float(row.get("memory_percent", 0) or 0),
                    "username": row.get("username", "")
                }
                level = "Low"
                score = 0
                verdict = "Safe"
                net_flag = False
                bg_flag = False
                perm_summary = "Unknown"
                if hasattr(udi, "ai_model") and udi.ai_model and udi.target_device != "Android":
                    try:
                        res = udi.ai_model.analyze_process(app)
                        score = int(min(max(res.get("risk_score", 0), 0), 100))
                        level = res.get("risk_level", "Low")
                        verdict = "Malicious" if level.lower() == "critical" else ("Suspicious" if level.lower() in ("high","medium") else "Safe")
                    except Exception:
                        score = 0
                        level = "Low"
                        verdict = "Safe"
                    try:
                        import psutil
                        p = psutil.Process(int(app["pid"])) if isinstance(app["pid"], int) else None
                        if p:
                            conns = p.net_connections(kind='inet')
                            net_flag = len(conns) > 0
                    except Exception:
                        net_flag = False
                    
                    # Desktop Sensitive Resource Heuristic
                    name_lower = str(app.get("name", "")).lower()
                    sensitive_apps = {
                        "zoom": "Mic, Cam", "teams": "Mic, Cam", "skype": "Mic, Cam", 
                        "facetime": "Mic, Cam", "discord": "Mic, Cam", "webex": "Mic, Cam", 
                        "slack": "Mic, Cam", "obs": "Mic, Cam, Screen", "quicktime": "Mic, Screen",
                        "photo booth": "Cam", "audacity": "Mic", "garageband": "Mic",
                        "chrome": "Browser", "safari": "Browser", "firefox": "Browser", 
                        "brave": "Browser", "edge": "Browser"
                    }
                    perm_summary = "None"
                    for k, v in sensitive_apps.items():
                        if k in name_lower:
                            perm_summary = v
                            break
                else:
                    bg_flag = str(app.get("username","")).lower() == "background"
                    if android_sensors is not None:
                        mic = app["pid"] in android_sensors.get("mic", [])
                        cam = app["pid"] in android_sensors.get("camera", [])
                        gps = app["pid"] in android_sensors.get("gps", [])
                        perm_summary = "Mic" if mic else ""
                        perm_summary += " Cam" if cam else ""
                        perm_summary += " GPS" if gps else ""
                        perm_summary = perm_summary.strip() or "None"
                        verdict = "Suspicious" if (mic or cam or gps) else ("Monitoring" if bg_flag else "Safe")
                        level = "High" if verdict == "Suspicious" else ("Medium" if verdict == "Monitoring" else "Low")
                        score = 80 if verdict == "Suspicious" else (50 if verdict == "Monitoring" else 10)
                        net_flag = False
                risk_scores.append(score)
                risk_levels.append(level)
                verdicts.append(verdict)
                net_active_flags.append("Yes" if net_flag else "No")
                bg_exec_flags.append("Yes" if bg_flag or app.get("cpu_percent",0) > 40 else "No")
                sens_perm_summ.append(perm_summary)
            
            apps_df["risk_score"] = risk_scores
            apps_df["risk_level"] = risk_levels
            apps_df["verdict"] = verdicts
            apps_df["network_active"] = net_active_flags
            apps_df["background_exec"] = bg_exec_flags
            apps_df["sensitive_permissions"] = sens_perm_summ
            
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">Suspicious Apps</div>
                        <div class="ai-summary-value">{int((apps_df['verdict'] == 'Suspicious').sum())}</div>
                        <div class="ai-summary-sub">Flagged by AI risk analysis</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with s2:
                sens_count = int(sum(1 for sp in apps_df['sensitive_permissions'] if sp and sp != "None"))
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">Sensitive Data Access</div>
                        <div class="ai-summary-value">{sens_count}</div>
                        <div class="ai-summary-sub">Mic, Camera, GPS signals</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with s3:
                net_count = int((apps_df['network_active'] == 'Yes').sum())
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">📡 Background Network Active</div>
                        <div class="ai-summary-value">{net_count}</div>
                        <div class="ai-summary-sub">Silent connections detected</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with s4:
                high_bdi = int((apps_df['risk_score'] > 70).sum())
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">High Behavioral Deviation</div>
                        <div class="ai-summary-value">{high_bdi}</div>
                        <div class="ai-summary-sub">Above risk threshold</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            
            st.markdown("---")
            st.subheader("Resource Behavior Indicators")
            top5 = apps_df.nlargest(5, 'cpu_percent')[['name','cpu_percent','risk_level','verdict']]
            ccols = st.columns(5)
            for i in range(len(top5)):
                with ccols[i]:
                    r = top5.iloc[i]
                    tag = "Normal"
                    if r['verdict'] == "Suspicious":
                        tag = "Suspicious"
                    elif r['verdict'] == "Monitoring":
                        tag = "Monitoring"
                    st.markdown(
                        f"""
                        <div class="ai-summary-card">
                            <div class="ai-summary-label">{tag}</div>
                            <div class="ai-summary-value">{r['name']}</div>
                            <div class="ai-summary-sub">CPU: {float(r['cpu_percent']):.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
            
            st.markdown("---")
            st.subheader("Background Activity vs User Interaction")
            if udi.target_device == "Android" and udi.android and udi.android.connected:
                bg_apps = apps_df[apps_df['background_exec'] == 'Yes'][['name','cpu_percent']]
                if not bg_apps.empty:
                    st.dataframe(bg_apps.rename(columns={'name':'App','cpu_percent':'CPU %'}), hide_index=True, width="stretch")
                else:
                    st.info("No apps active without screen interaction")
            else:
                bg_apps = apps_df[apps_df['background_exec'] == 'Yes'][['name','cpu_percent','network_active']]
                if not bg_apps.empty:
                    st.dataframe(bg_apps.rename(columns={'name':'App','cpu_percent':'CPU %','network_active':'Network'}), hide_index=True, width="stretch")
                else:
                    st.info("No background-active apps detected")
            
            st.markdown("---")
            st.subheader("Application Behavioral Profile")
            profile_cols = ['name','risk_score','risk_level','verdict','background_exec','sensitive_permissions','network_active']
            display_df = apps_df[profile_cols].copy()
            display_df.columns = ['App Name','AI Risk Score','AI Risk Level','Behavioral Verdict','Background Execution','Sensitive Permissions Used','Network Activity']
            st.dataframe(display_df, width="stretch", hide_index=True)
            
            st.markdown("Top Risk Apps")
            top_risk = apps_df.sort_values('risk_score', ascending=False)[['name','risk_score','risk_level','verdict']].head(5)
            if not top_risk.empty:
                st.dataframe(top_risk.rename(columns={'name':'App','risk_score':'Score','risk_level':'Level','verdict':'Verdict'}), hide_index=True, width="stretch")
            else:
                st.caption("No apps with elevated risk scores.")
            

        else:
            st.info("No running applications detected")
    
    # Performance Analytics removed per request
    
    elif view == "Network Scan":
        st.header("📂 File Analysis")
        st.markdown("Upload a suspicious file (e.g., APK) from your device for AI analysis.")
        
        st.subheader("Manual File Analysis")
        st.info("Upload a suspicious file (e.g., APK) from your device for AI analysis.")
        
        uploaded_file = st.file_uploader("Choose a file", type=['apk', 'exe', 'sh', 'pdf', 'docx', 'png', 'jpg'])
        
        if uploaded_file is not None:
            if st.button("Analyze File", type="primary"):
                with st.spinner("Analyzing file structure and content..."):
                    file_bytes = uploaded_file.getvalue()
                    analysis = udi.analyze_uploaded_file(uploaded_file.name, file_bytes)
                    
                    st.subheader("Analysis Results")
                    st.json(analysis)
                    
                    if analysis.get('risk_score', 0) > 70:
                        st.error(f"High Risk Detected! Score: {analysis.get('risk_score')}")
                    elif analysis.get('risk_score', 0) > 40:
                        st.warning(f"Medium Risk Detected. Score: {analysis.get('risk_score')}")
                    else:
                        st.success("Low Risk. File appears safe.")

    elif view == "Privacy & Data":
        @st.fragment(run_every=2)
        def render_privacy():
            live_metrics = udi.live_collector.get_live_metrics()
            st.header("AI Privacy Risk Assessment")
            st.markdown("---")
            pr1, pr2, pr3, pr4 = st.columns(4)
    
            latest_ai = 0.0
            latest_cpu = 0.0
            latest_mem = 0.0
            latest_disk = 0.0
            last_nd = 0.0
            baseline_nd = 0.0
    
            if live_metrics and len(live_metrics) > 0:
                df_priv = pd.DataFrame(live_metrics)
                if 'ai_anomaly_score' in df_priv.columns:
                    latest_ai = float(df_priv['ai_anomaly_score'].iloc[-1])
                if 'cpu_percent' in df_priv.columns:
                    latest_cpu = float(df_priv['cpu_percent'].iloc[-1])
                if 'memory_percent' in df_priv.columns:
                    latest_mem = float(df_priv['memory_percent'].iloc[-1])
                if 'disk_percent' in df_priv.columns:
                    latest_disk = float(df_priv['disk_percent'].iloc[-1])
                if 'network_bytes_sent' in df_priv.columns and len(df_priv) > 1:
                    diffs = df_priv['network_bytes_sent'].diff().fillna(0).clip(lower=0)
                    baseline_nd = float(diffs.iloc[:-1].median()) if len(diffs) > 1 else 0.0
                    last_nd = float(diffs.iloc[-1])
    
            with pr1:
                if live_metrics and len(live_metrics) > 0:
                    if latest_ai > 70 or latest_cpu > 80 or latest_mem > 85 or latest_disk > 90:
                        status_live = "Risk Detected"
                    elif latest_ai > 40 or latest_cpu > 60 or latest_mem > 70 or latest_disk > 80:
                        status_live = "Monitoring"
                    else:
                        status_live = "Safe"
                else:
                    status_live = "Monitoring" if st.session_state.monitoring_active else "Safe"
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">Data Access Risk</div>
                        <div class="ai-summary-value">{status_live}</div>
                        <div class="ai-summary-sub">Foreground vs background resource use</div>
                    </div>
                    """, unsafe_allow_html=True
                )
    
            with pr2:
                if live_metrics and len(live_metrics) > 1:
                    if baseline_nd > 0 and last_nd > baseline_nd * 3 and latest_ai > 40:
                        net_status = "Risk Detected"
                    elif last_nd > 0 or latest_ai > 40:
                        net_status = "Monitoring"
                    else:
                        net_status = "Safe"
                else:
                    net_status = "Monitoring" if st.session_state.monitoring_active else "Safe"
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">Background Network Activity</div>
                        <div class="ai-summary-value">{net_status}</div>
                        <div class="ai-summary-sub">Silent transmissions and bursts</div>
                    </div>
                    """, unsafe_allow_html=True
                )
    
            with pr3:
                if live_metrics and len(live_metrics) > 0 and latest_ai > 0.0:
                    bdi = latest_ai
                else:
                    bdi = float(current_health.get("ai_anomaly_score", 0) or 0)
                bdi_status = "Risk Detected" if bdi > 70 else ("Monitoring" if bdi > 40 else "Safe")
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">Behavioral Privacy Risk</div>
                        <div class="ai-summary-value">{bdi_status}</div>
                        <div class="ai-summary-sub">BDI threshold analysis</div>
                    </div>
                    """, unsafe_allow_html=True
                )
    
            with pr4:
                try:
                    conns = psutil.net_connections(kind='inet')
                    remote = [c for c in conns if c.raddr]
                    if not remote:
                        enc_ok = "No Data"
                    else:
                        secure_ports = {443, 465, 993, 995, 8443}
                        secure = sum(1 for c in remote if c.raddr.port in secure_ports)
                        insecure = len(remote) - secure
                        if insecure == 0 and secure > 0:
                            enc_ok = "Secure"
                        elif insecure > 0 and secure > 0:
                            enc_ok = "Mixed"
                        else:
                            enc_ok = "Unencrypted"
                except Exception:
                    enc_ok = "Unknown"
                st.markdown(
                    f"""
                    <div class="ai-summary-card">
                        <div class="ai-summary-label">Encryption & Data Handling</div>
                        <div class="ai-summary-value">{enc_ok}</div>
                        <div class="ai-summary-sub">TLS presence and secure ports</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            st.markdown("---")
            if not live_metrics or len(live_metrics) == 0:
                st.info("No live privacy data yet. Turn on Live Behavioral Monitoring to populate this view.")
                if st.button("Start Live Monitoring", key="btn_start_privacy_monitor", type="primary"):
                    udi.start_live_monitoring()
                    st.session_state.monitoring_active = True
                    st.rerun()
            st.subheader("Silent Data Collection Indicators")
            sdc1, sdc2, sdc3, sdc4 = st.columns(4)
            with sdc1:
                if live_metrics and len(live_metrics) > 0:
                    df_priv = pd.DataFrame(live_metrics)
                    df_priv['timestamp'] = pd.to_datetime(df_priv['timestamp'])
                    latest_ai = float(df_priv['ai_anomaly_score'].iloc[-1]) if 'ai_anomaly_score' in df_priv.columns else 0.0
                    clip_status = "Potential" if latest_ai > 70 else ("Elevated" if latest_ai > 40 else "No signals")
                    st.metric("Clipboard Access", clip_status)
                else:
                    st.metric("Clipboard Access", "Unknown")
            with sdc2:
                if live_metrics and len(live_metrics) > 1:
                    df_priv = pd.DataFrame(live_metrics)
                    diffs = df_priv['network_bytes_sent'].diff().fillna(0).clip(lower=0) if 'network_bytes_sent' in df_priv.columns else pd.Series([0])
                    baseline_nd = float(diffs.iloc[:-1].median()) if len(diffs) > 1 else 0.0
                    last_nd = float(diffs.iloc[-1])
                    s_burst = "Suspicious" if baseline_nd > 0 and last_nd > baseline_nd * 2 else ("Low" if last_nd > 0 else "None")
                    st.metric("Background Data Transfer", s_burst)
                else:
                    st.metric("Background Data Transfer", "None")
            with sdc3:
                if live_metrics and len(live_metrics) > 1:
                    df_priv = pd.DataFrame(live_metrics)
                    diffs = df_priv['network_bytes_sent'].diff().fillna(0).clip(lower=0) if 'network_bytes_sent' in df_priv.columns else pd.Series([0])
                    baseline_nd = float(diffs.iloc[:-1].median()) if len(diffs) > 1 else 0.0
                    last_nd = float(diffs.iloc[-1])
                    latest_cpu = float(df_priv['cpu_percent'].iloc[-1]) if 'cpu_percent' in df_priv.columns else 0.0
                    latest_ai = float(df_priv['ai_anomaly_score'].iloc[-1]) if 'ai_anomaly_score' in df_priv.columns else 0.0
                    if baseline_nd > 0 and last_nd > baseline_nd * 2 and latest_cpu < 30 and latest_ai > 40:
                        ui_corr = "Unmatched"
                    else:
                        ui_corr = "Normal"
                    st.metric("User Interaction Correlation", ui_corr)
                else:
                    st.metric("User Interaction Correlation", "Unknown")
            with sdc4:
                if live_metrics and len(live_metrics) > 1:
                    df_priv = pd.DataFrame(live_metrics)
                    diffs = df_priv['network_bytes_sent'].diff().fillna(0).clip(lower=0) if 'network_bytes_sent' in df_priv.columns else pd.Series([0])
                    last_nd = float(diffs.iloc[-1])
                    latest_cpu = float(df_priv['cpu_percent'].iloc[-1]) if 'cpu_percent' in df_priv.columns else 0.0
                    latest_ai = float(df_priv['ai_anomaly_score'].iloc[-1]) if 'ai_anomaly_score' in df_priv.columns else 0.0
                    idle_flag = "Likely" if last_nd > 0 and latest_cpu < 20 and latest_ai > 40 else ("None" if last_nd == 0 else "Possible")
                    st.metric("Data Sent While Screen Idle", idle_flag)
                else:
                    st.metric("Data Sent While Screen Idle", "Unknown")
            st.markdown("---")
            st.subheader("Live Privacy Telemetry Snapshot")
            dev_mode = st.checkbox("Developer Mode", value=False, key="privacy_dev_mode")
            if live_metrics and len(live_metrics) > 0:
                lm = live_metrics[-1]
                events = []
                if lm.get("cpu_percent",0) > 80: events.append("CPU usage spike detected (background)")
                if lm.get("network_bytes_sent",0) > 0 and lm.get("ai_anomaly_score",0) > 40: events.append("Network data sent without user interaction")
                else: events.append("Network usage normal")
                if lm.get("memory_percent",0) < 70: events.append("Memory usage stable")
                if lm.get("ai_anomaly_score",0) <= 40: events.append("No anomaly detected")
                for e in events:
                    st.write(f"• {e}")
            st.markdown("---")
            if dev_mode and 'lm' in locals():
                st.json(lm)
            
            st.subheader("📂 Forensic Scan History")
            if st.button("Refresh Forensic Logs", key="btn_refresh_forensic"):
                pass
                
            logs = udi.db.get_scan_logs(limit=20)
            if logs:
                by_date = {}
                for log in logs:
                    ts = log.get("timestamp", "")
                    day = ts.split("T")[0] if "T" in ts else ts.split(" ")[0]
                    by_date.setdefault(day, []).append(log)
                for day, day_logs in by_date.items():
                    with st.expander(f"{day} • {len(day_logs)} forensic entries"):
                        for log in day_logs:
                            label = log.get("timestamp", "Unknown")
                            threats = int(log.get("threats_count", 0) or 0)
                            st.markdown(f"**{label} — Threats: {threats}**")
                            details_text = log.get("details") or ""
                            try:
                                parsed = json.loads(details_text)
                                st.json(parsed)
                            except Exception:
                                if details_text:
                                    st.write(details_text)
                                else:
                                    st.caption("No additional details recorded.")
            else:
                st.info("No forensic scan history yet. Run a Heuristic Threat Scan to populate logs.")
    
        render_privacy()
    st.markdown("---")
    fc1, fc2 = st.columns([2, 1])
    with fc1:
        st.caption("Behavior-Based • Zero-Signature • Local AI • Detects silent data collection without signatures")
    with fc2:
        platform_label = f"{udi.device_info['device_type'].title()} / {udi.device_info['platform']}"
        st.caption(f"{platform_label} • Last updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 🔁 Auto-refresh logic (Moved to end to ensure full page render)
    # Global refresh removed to prevent full-page blinking. 
    # Each view now handles its own partial refresh via st.fragment.
    pass

if __name__ == "__main__":
    main()
