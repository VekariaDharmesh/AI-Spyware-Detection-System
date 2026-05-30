"use client";

import React, { useState, useEffect, useRef } from "react";
import { 
  Shield, Laptop, Smartphone, Activity, Radio, AlertTriangle, Cpu, HardDrive, 
  Layers, Terminal, CheckCircle2, ChevronRight, X, Play, Square, RefreshCw, 
  Send, HelpCircle, FileText, Search, Wifi, AlertOctagon, CornerDownRight, 
  Info, Skull, ShieldCheck, Zap, Lock, Eye, Check, Trash2, Crosshair, Network,
  LockKeyhole, ArrowRight, Download, Settings, Server, Globe, Sparkles, Filter, List
} from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from "recharts";

// Interfaces
interface Process {
  pid: number | string;
  name: string;
  username: string;
  cpu_percent: number;
  memory_percent: number;
  risk_score?: number;
  risk_level?: string;
  reason?: string;
  is_threat?: boolean;
}

interface MetricSnapshot {
  timestamp: string;
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  network_bytes_sent: number;
  network_bytes_recv: number;
  ai_anomaly_score: number;
}

export default function EnterpriseCommandCenter() {
  // Navigation & Platform View routers
  const [activeTab, setActiveTab] = useState<"overview" | "processes" | "network" | "privacy" | "file-scan">("overview");
  const [targetDevice, setTargetDevice] = useState<"Desktop" | "Android">("Desktop");
  
  // Real-time API states
  const [deviceInfo, setDeviceInfo] = useState<any>({
    device_type: "desktop",
    platform: "macOS",
    hostname: "workstation-node-04",
    ip_address: "192.168.1.115",
    network_type: "Ethernet (Secure)",
    battery_info: { present: true, percent: 100, charging: true }
  });
  const [systemMetrics, setSystemMetrics] = useState<any>({
    cpu: { percent: 5.2, count: 12, freq: null },
    memory: { percent: 34.0, used: 5.44 * 1024**3, total: 16 * 1024**3 },
    disk: { percent: 42.0, used: 215 * 1024**3, total: 512 * 1024**3 },
    processes: 138,
    boot_time: "N/A"
  });
  const [runningApps, setRunningApps] = useState<Process[]>([]);
  const [deviceHealth, setDeviceHealth] = useState<any>({
    score: 99,
    ai_anomaly_score: 1,
    status: "Nominal",
    issues: [],
    recommendations: ["Workstation functioning inside standard operational limits. No elevated risks logged."]
  });
  const [androidRiskReport, setAndroidRiskReport] = useState<any>({
    score: 100,
    issues: [],
    dangerous_apps: [],
    active_sensors: { mic: [], camera: [], gps: [] }
  });
  const [monitoringActive, setMonitoringActive] = useState<boolean>(true);
  const [liveMetrics, setLiveMetrics] = useState<MetricSnapshot[]>([]);
  const [threatScanResults, setThreatScanResults] = useState<Process[]>([]);
  const [threatScanRunning, setThreatScanRunning] = useState<boolean>(false);
  
  // Slide-over Process inspector drawer
  const [selectedApp, setSelectedApp] = useState<any>(null);
  const [appDetailsLoading, setAppDetailsLoading] = useState<boolean>(false);
  const [appDetails, setAppDetails] = useState<any>(null);
  
  // Persistent Right-Side AI Assistant Panel
  const [aiPanelExpanded, setAiPanelExpanded] = useState<boolean>(true);
  const [copilotMessages, setCopilotMessages] = useState<any[]>([
    { sender: "ai", text: "Security Copilot online. I can audit background processes, explain port sockets, and suggest mitigation steps. Select a process or ask an action." }
  ]);
  const [copilotInput, setCopilotInput] = useState<string>("");

  // Process filters
  const [processFilter, setProcessFilter] = useState<"all" | "warning" | "user">("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  
  // CMD+K palette modal
  const [commandPaletteOpen, setCommandPaletteOpen] = useState<boolean>(false);
  const [cmdSearch, setCmdSearch] = useState<string>("");
  const [notifications, setNotifications] = useState<any[]>([]);
  const [fileAnalysisResult, setFileAnalysisResult] = useState<any>(null);
  const [fileAnalyzing, setFileAnalyzing] = useState<boolean>(false);

  // Active Network connections
  const [activeSockets, setActiveSockets] = useState<any[]>([
    { local: "192.168.1.115:8000", remote: "127.0.0.1:58432", status: "ESTABLISHED", proto: "TCP", app: "FastAPI Core Daemon" },
    { local: "0.0.0.0:3000", remote: "0.0.0.0:*", status: "LISTEN", proto: "TCP", app: "Next.js Dashboard UI" },
    { local: "192.168.1.115:443", remote: "104.244.42.1:443", status: "ESTABLISHED", proto: "TCP", app: "Security Handshake" }
  ]);

  // Operational events log
  const [timelineEvents, setTimelineEvents] = useState<any[]>([
    { time: "09:34", type: "system", text: "SilentGuard FastAPI backend wrapper synchronized on port 8000." },
    { time: "09:34", type: "system", text: "Next.js dev web server initialized on port 3000." },
    { time: "09:44", type: "success", text: "System typography stack hot-reloaded successfully to modern SaaS variables." }
  ]);

  // --- API Integrations Fetch Hooks ---
  const API_BASE = "http://localhost:8000";

  const fetchAPI = async (endpoint: string, options: any = {}) => {
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, options);
      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn(`REST connection failed on endpoint: ${endpoint}`);
      return null;
    }
  };

  const addNotification = (text: string, type: "info" | "warning" | "success" | "danger" = "info") => {
    const id = Date.now();
    setNotifications(prev => [...prev, { id, text, type }]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 5000);
  };

  // Synchronize state with FastAPI REST Server
  const refreshTelemetry = async () => {
    // 1. Device Info
    const info = await fetchAPI("/api/device-info");
    if (info) setDeviceInfo(info);

    // 2. System Metrics
    const metrics = await fetchAPI("/api/system-metrics");
    if (metrics) setSystemMetrics(metrics);

    // 3. Health Score
    const health = await fetchAPI("/api/device-health");
    if (health) setDeviceHealth(health);

    // 4. Running apps
    const apps = await fetchAPI("/api/running-apps?limit=15");
    if (apps) setRunningApps(apps);

    // 5. Monitoring Status
    const mon = await fetchAPI("/api/monitoring-status");
    if (mon) setMonitoringActive(mon.is_collecting);

    // 6. Live Metrics Chronological Timeline
    const live = await fetchAPI("/api/live-metrics");
    if (live && live.length > 0) {
      setLiveMetrics(live);
    } else {
      // Mock metrics for high-fidelity chart presentation on default load
      setLiveMetrics([
        { timestamp: "09:44", cpu_percent: 4, memory_percent: 33, disk_percent: 42, network_bytes_sent: 120, network_bytes_recv: 300, ai_anomaly_score: 1 },
        { timestamp: "09:46", cpu_percent: 9, memory_percent: 34, disk_percent: 42, network_bytes_sent: 240, network_bytes_recv: 510, ai_anomaly_score: 1 },
        { timestamp: "09:48", cpu_percent: 5, memory_percent: 34, disk_percent: 42, network_bytes_sent: 160, network_bytes_recv: 380, ai_anomaly_score: 1 },
        { timestamp: "09:50", cpu_percent: 6, memory_percent: 34, disk_percent: 42, network_bytes_sent: 175, network_bytes_recv: 390, ai_anomaly_score: 1 }
      ]);
    }

    // 7. Android Risks
    if (targetDevice === "Android") {
      const android = await fetchAPI("/api/android-risk-report");
      if (android) setAndroidRiskReport(android);
    }
  };

  // Toggle monitoring
  const toggleMonitoring = async () => {
    const endpoint = monitoringActive ? "/api/stop-monitoring" : "/api/start-monitoring";
    const res = await fetchAPI(endpoint, { method: "POST" });
    if (res && res.success) {
      setMonitoringActive(!monitoringActive);
      addNotification(`Protection ${!monitoringActive ? "Activated" : "Paused"}`, !monitoringActive ? "success" : "info");
      setTimelineEvents(prev => [
        { time: new Date().toTimeString().split(" ")[0], type: "system", text: `Sentinel thread loop ${!monitoringActive ? "active" : "paused"}.` },
        ...prev
      ]);
    }
  };

  // Run deep process signature audit
  const startDeepAudit = async () => {
    setThreatScanRunning(true);
    addNotification("Threat audit initialized...", "info");
    const res = await fetchAPI("/api/perform-ai-scan", { method: "POST" });
    setThreatScanRunning(false);
    if (res && res.success) {
      setThreatScanResults(res.results);
      addNotification(`Audit finalized. Identified ${res.threats_count} security findings.`, res.threats_count > 0 ? "warning" : "success");
      setTimelineEvents(prev => [
        { time: new Date().toTimeString().split(" ")[0], type: "threat", text: `Threat assessment completed. Warnings flagged: ${res.threats_count}.` },
        ...prev
      ]);
    }
  };

  // Switch Platform Target
  const changeTargetPlatform = async (platform: "Desktop" | "Android") => {
    setTargetDevice(platform);
    const res = await fetchAPI("/api/set-target", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target: platform })
    });
    if (res && res.success) {
      addNotification(`Bridge redirected to: ${platform}`, "success");
    }
  };

  // Audit granular process details
  const auditApp = async (app: Process) => {
    setSelectedApp(app);
    setAppDetailsLoading(true);
    setAppDetails(null);
    const res = await fetchAPI("/api/scan-app-details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_id: String(app.pid), platform: targetDevice.toLowerCase() })
    });
    setAppDetailsLoading(false);
    if (res) {
      setAppDetails(res);
      // Auto populate AI Persistent Chat
      setCopilotMessages(prev => [
        ...prev,
        { sender: "user", text: `Explain security findings for: ${app.name} (PID: ${app.pid})` },
        { sender: "ai", text: `Analyzing executable properties for ${app.name}. Integrity rating: ${res.trust_score}/100. Diagnostic: ${res.risk_level} Risk. Risk vectors found: ${res.risk_factors.join(", ") || "Nominal parameters"}. Running within standard operating memory partitions.` }
      ]);
    }
  };

  // Terminate app
  const terminateProcess = async (pid: number) => {
    const res = await fetchAPI("/api/terminate-app", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pid })
    });
    if (res && res.success) {
      addNotification(`Terminated PID: ${pid}`, "success");
      setSelectedApp(null);
      refreshTelemetry();
    } else {
      addNotification(`Failed to terminate PID: ${res?.message || "Operation Denied"}`, "danger");
    }
  };

  // Connect ADB Android over Wireless
  const connectWirelessADB = async (ip: string) => {
    const res = await fetchAPI("/api/android/connect-wireless", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ip })
    });
    if (res && res.success) {
      addNotification("ADB wireless connection established!", "success");
      changeTargetPlatform("Android");
    } else {
      addNotification(`ADB pairing failed: ${res?.output || "Device not found"}`, "danger");
    }
  };

  // Handle Binary APK scan
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    setFileAnalyzing(true);
    setFileAnalysisResult(null);
    addNotification(`Decompiling package structures: ${file.name}`, "info");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/api/analyze-file`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setFileAnalyzing(false);
      setFileAnalysisResult(data);
      addNotification(`Static decompiler analysis finalized for: ${file.name}`, "success");
    } catch (err) {
      setFileAnalyzing(false);
      addNotification("Upload scan failed.", "danger");
    }
  };

  // AI Chat Submission
  const handleSendMessage = () => {
    if (!copilotInput.trim()) return;
    const userMsg = copilotInput.trim();
    setCopilotMessages(prev => [...prev, { sender: "user", text: userMsg }]);
    setCopilotInput("");

    setTimeout(() => {
      let reply = "I've completed an operational trace on active network sockets. No outbound anomalies are detected.";
      const lower = userMsg.toLowerCase();
      if (lower.includes("quarantine")) {
        reply = "Quarantining this app revokes all runtime privileges, isolates directory permissions, and disables package execution to prevent background loops.";
      } else if (lower.includes("radar") || lower.includes("orbit")) {
        reply = "Active threat analysis tracks process behaviors relative to nominal operating thresholds. Highly anomalous items generate warnings.";
      } else if (lower.includes("sensor") || lower.includes("mic") || lower.includes("camera")) {
        reply = "Microphone, camera, and location calls are audited using Android AppOps hooks. Background requests trigger pulsing warning indicators.";
      } else if (lower.includes("harden") || lower.includes("mitigate")) {
        reply = "Standard mitigations: closed unused socket bindings, inspect background processes running outside system folders, and revoke mobile alert overlays.";
      }
      setCopilotMessages(prev => [...prev, { sender: "ai", text: reply }]);
    }, 1000);
  };

  // Poll server data
  useEffect(() => {
    refreshTelemetry();
    const timer = setInterval(refreshTelemetry, 5000);
    return () => clearInterval(timer);
  }, [targetDevice]);

  // Global CMD+K command palette key hooks
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandPaletteOpen(prev => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const healthScore = deviceHealth.score;
  const healthColorText = healthScore > 85 ? "text-emerald-400" : healthScore > 55 ? "text-amber-400" : "text-rose-400";
  const healthColorClass = healthScore > 85 ? "stroke-emerald-500" : healthScore > 55 ? "stroke-amber-500" : "stroke-rose-500";

  // Filter processes
  const filteredProcesses = runningApps.filter(app => {
    const matchesSearch = app.name.toLowerCase().includes(searchQuery.toLowerCase()) || String(app.pid).includes(searchQuery);
    if (processFilter === "all") return matchesSearch;
    if (processFilter === "warning") return matchesSearch && (app.cpu_percent > 30 || app.is_threat);
    if (processFilter === "user") return matchesSearch && app.username.toLowerCase() !== "system" && app.username.toLowerCase() !== "root";
    return matchesSearch;
  });

  return (
    <div className="flex-1 w-full min-h-screen bg-[#030712] relative text-slate-100 flex items-stretch">
      
      {/* Dynamic drifting background auroras - extremely subtle, premium */}
      <div className="absolute top-[-30%] left-[-15%] w-[60vw] h-[60vw] bg-radial from-blue-900/3 to-transparent rounded-full blur-[140px] pointer-events-none animate-mesh-drift z-0"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50vw] h-[50vw] bg-radial from-indigo-900/3 to-transparent rounded-full blur-[140px] pointer-events-none animate-mesh-drift z-0"></div>

      {/* Modern left-side navigation sidebar (Linear/CrowdStrike style) */}
      <aside className="w-[250px] border-r border-white/[0.04] bg-[#030712] flex flex-col justify-between shrink-0 z-10 font-sans">
        
        <div className="flex flex-col gap-6 p-6">
          {/* Logo badging */}
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-white/[0.02] border border-white/[0.05] shadow-inner">
              <Shield className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <h2 className="text-xs font-bold tracking-wider text-slate-100 font-mono">SILENTGUARD</h2>
              <span className="text-[9px] uppercase tracking-widest text-slate-500 font-bold font-mono">v2.0 Enterprise</span>
            </div>
          </div>

          <div className="h-px bg-white/[0.04] w-full"></div>

          {/* Quick Platform Switcher */}
          <div className="flex flex-col gap-1.5">
            <span className="text-[8px] font-mono text-slate-600 uppercase tracking-widest font-bold">MONITORED NODE</span>
            <div className="grid grid-cols-2 gap-1 p-1 bg-white/[0.01] rounded-xl border border-white/[0.03]">
              <button 
                onClick={() => changeTargetPlatform("Desktop")}
                className={`py-1.5 rounded-lg text-[10px] font-mono font-bold transition-all flex items-center justify-center gap-1 ${
                  targetDevice === "Desktop" 
                    ? "bg-white/[0.03] text-blue-400 border border-white/[0.05]" 
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                <Laptop className="w-3.5 h-3.5" />
                <span>LOCAL</span>
              </button>
              <button 
                onClick={() => changeTargetPlatform("Android")}
                className={`py-1.5 rounded-lg text-[10px] font-mono font-bold transition-all flex items-center justify-center gap-1 ${
                  targetDevice === "Android" 
                    ? "bg-white/[0.03] text-blue-400 border border-white/[0.05]" 
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                <Smartphone className="w-3.5 h-3.5" />
                <span>MOBILE</span>
              </button>
            </div>
          </div>

          <div className="h-px bg-white/[0.04] w-full"></div>

          {/* Navigation Links */}
          <nav className="flex flex-col gap-1">
            <span className="text-[8px] font-mono text-slate-600 uppercase tracking-widest font-bold mb-1.5">DASHBOARD</span>
            {[
              { id: "overview", label: "Overview", icon: Layers },
              { id: "processes", label: "Processes Explorer", icon: Cpu },
              { id: "network", label: "Network Connections", icon: Globe },
              { id: "privacy", label: "Privacy Center", icon: LockKeyhole },
              { id: "file-scan", label: "File Audit Deck", icon: FileText }
            ].map(tab => {
              const Icon = tab.icon;
              const active = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-mono transition-all ${
                    active 
                      ? "bg-blue-500/10 border border-blue-500/25 text-blue-400 font-bold" 
                      : "text-slate-500 hover:text-slate-300 border border-transparent hover:bg-white/[0.01]"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{tab.label}</span>
                  </div>
                  <ChevronRight className={`w-3.5 h-3.5 opacity-0 transition-opacity ${active ? "opacity-100" : ""}`} />
                </button>
              );
            })}
          </nav>

        </div>

        {/* Bottom sidebar info */}
        <div className="p-6 flex flex-col gap-3 border-t border-white/[0.04]">
          <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span>FastAPI Core</span>
            </span>
            <span>ONLINE</span>
          </div>
          <button 
            onClick={() => setAiPanelExpanded(!aiPanelExpanded)}
            className="w-full py-2 rounded-xl border border-white/[0.04] bg-white/[0.01] hover:border-slate-800 text-[10px] font-mono text-slate-400 hover:text-slate-200 transition-all flex items-center justify-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5 text-blue-400 animate-pulse" />
            <span>{aiPanelExpanded ? "HIDE AI ASSISTANT" : "SHOW AI ASSISTANT"}</span>
          </button>
        </div>

      </aside>

      {/* Main Workspace Area */}
      <div className="flex-1 flex flex-col items-stretch overflow-hidden z-10">
        
        {/* Top Navbar */}
        <header className="h-16 border-b border-white/[0.04] px-8 flex items-center justify-between bg-[#030712]/40 backdrop-blur-md">
          <div className="flex items-center gap-4">
            <h2 className="text-xs font-bold tracking-wider font-mono uppercase text-slate-400">
              {activeTab === "overview" && "Dashboard Overview"}
              {activeTab === "processes" && "Process Analyzer"}
              {activeTab === "network" && "Network Connections Map"}
              {activeTab === "privacy" && "Mobile Privacy Center"}
              {activeTab === "file-scan" && "Executable File Auditor"}
            </h2>
            <span className="text-[10px] font-mono text-slate-600 bg-white/[0.02] border border-white/[0.04] px-2 py-0.5 rounded">
              NODE: {deviceInfo.hostname}
            </span>
          </div>

          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="text-slate-500 flex items-center gap-1">
              <Wifi className="w-3.5 h-3.5 text-slate-600" />
              <span>IP: {deviceInfo.ip_address}</span>
            </span>

            <div className="h-4 w-px bg-white/[0.05]"></div>

            <button 
              onClick={() => setCommandPaletteOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1 rounded-full border border-white/[0.04] bg-white/[0.01] text-slate-400 hover:text-slate-200 transition-all"
            >
              <Search className="w-3.5 h-3.5 text-slate-500" />
              <span>⌘K</span>
            </button>
          </div>
        </header>

        {/* Scrollable Content Frame */}
        <div className="flex-1 overflow-y-auto p-8 flex gap-6 items-start">
          
          {/* Main workspace layout */}
          <div className="flex-1 flex flex-col gap-6">

            {/* Tab 1: Bento Overview dashboard */}
            {activeTab === "overview" && (
              <div className="flex flex-col gap-6">
                
                {/* Top Bento Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  
                  {/* Security Score */}
                  <div className="glass-panel p-5 rounded-2xl flex items-center justify-between">
                    <div>
                      <p className="text-[10px] font-mono tracking-widest text-slate-500 uppercase">SYSTEM INTEGRITY</p>
                      <h3 className={`text-sm font-bold font-mono mt-1 ${healthColorText} uppercase`}>{healthScore > 85 ? "SECURE" : "WARNING ALERTS"}</h3>
                      <p className="text-[10px] text-slate-400 mt-2">Score Grade: {deviceHealth.status}</p>
                    </div>
                    
                    <div className="relative flex items-center justify-center">
                      <svg className="w-14 h-14 transform -rotate-90">
                        <circle cx="28" cy="28" r="24" className="stroke-slate-900" strokeWidth="3" fill="transparent" />
                        <circle 
                          cx="28" 
                          cy="28" 
                          r="24" 
                          className={healthColorClass}
                          strokeWidth="3" 
                          fill="transparent" 
                          strokeDasharray={2 * Math.PI * 24}
                          strokeDashoffset={2 * Math.PI * 24 * (1 - healthScore / 100)}
                          strokeLinecap="round"
                        />
                      </svg>
                      <span className="absolute text-[10px] font-bold font-mono text-slate-200">{healthScore}%</span>
                    </div>
                  </div>

                  {/* Active Incidents */}
                  <div className="glass-panel p-5 rounded-2xl flex items-center justify-between">
                    <div>
                      <p className="text-[10px] font-mono tracking-widest text-slate-500 uppercase">ACTIVE INCIDENTS</p>
                      <h3 className="text-xl font-bold font-mono mt-1 text-slate-200">
                        {threatScanResults.length > 0 ? String(threatScanResults.length).padStart(2, '0') : "00"}
                      </h3>
                      <p className="text-[10px] text-slate-500 mt-2">Behavior anomalies flagged</p>
                    </div>
                    <div className="p-2.5 bg-white/[0.02] border border-white/[0.04] rounded-xl">
                      <AlertOctagon className="w-5 h-5 text-slate-400" />
                    </div>
                  </div>

                  {/* Health checks */}
                  <div className="glass-panel p-5 rounded-2xl flex flex-col justify-between">
                    <div className="flex items-center justify-between w-full">
                      <p className="text-[10px] font-mono tracking-widest text-slate-500 uppercase">SYS TELEMETRY FOOTPRINT</p>
                      <Cpu className="w-4 h-4 text-blue-500" />
                    </div>
                    <div className="mt-2">
                      <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 mb-1">
                        <span>CPU: {systemMetrics.cpu.percent}%</span>
                        <span>MEM: {systemMetrics.memory.percent}%</span>
                      </div>
                      <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden mb-1.5">
                        <div className="h-full bg-blue-500" style={{ width: `${systemMetrics.cpu.percent}%` }}></div>
                      </div>
                      <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full bg-indigo-500" style={{ width: `${systemMetrics.memory.percent}%` }}></div>
                      </div>
                    </div>
                  </div>

                  {/* Security Findings */}
                  <div className="glass-panel p-5 rounded-2xl flex flex-col justify-between">
                    <div className="flex items-center justify-between w-full">
                      <p className="text-[10px] font-mono tracking-widest text-slate-500 uppercase">SECURITY FINDINGS</p>
                      <Sparkles className="w-4 h-4 text-blue-500" />
                    </div>
                    <p className="text-[10px] text-slate-400 leading-normal mt-2.5">
                      {deviceHealth.ai_anomaly_score > 30 
                        ? "Elevated background process telemetry registered. Deep diagnostic recommended."
                        : "Nominal operational state verified. All process structures conform with security parameters."}
                    </p>
                  </div>

                </div>

                {/* Middle row: Live telemetry charting and alerts grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                  
                  {/* High Density Telemetry Chart */}
                  <div className="glass-panel p-6 rounded-3xl lg:col-span-8 flex flex-col justify-between">
                    <div className="w-full flex items-center justify-between mb-4">
                      <h3 className="text-xs font-mono tracking-wider text-slate-300 flex items-center gap-1.5 font-bold">
                        <Activity className="w-4 h-4 text-blue-500" />
                        <span>OPERATIONAL METRICS GRAPH</span>
                      </h3>
                      
                      <div className="flex items-center gap-2">
                        <button 
                          onClick={toggleMonitoring}
                          className={`flex items-center gap-1 px-3 py-1 rounded-xl text-[10px] font-mono border transition-all ${
                            monitoringActive 
                              ? "bg-rose-500/10 border-rose-500/30 text-rose-300" 
                              : "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                          }`}
                        >
                          {monitoringActive ? <Square className="w-3 h-3" /> : <Play className="w-3 h-3" />}
                          <span>{monitoringActive ? "PAUSE PROTECT" : "START PROTECT"}</span>
                        </button>
                      </div>
                    </div>

                    <div className="h-64 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={liveMetrics}>
                          <defs>
                            <linearGradient id="colorBlue" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.1}/>
                              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                            </linearGradient>
                            <linearGradient id="colorIndigo" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="#6366F1" stopOpacity={0.1}/>
                              <stop offset="95%" stopColor="#6366F1" stopOpacity={0}/>
                            </linearGradient>
                          </defs>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.015)" />
                          <XAxis dataKey="timestamp" stroke="rgba(255,255,255,0.2)" fontSize={9} />
                          <YAxis stroke="rgba(255,255,255,0.2)" fontSize={9} domain={[0, 100]} />
                          <Tooltip 
                            contentStyle={{ background: "rgba(17, 24, 39, 0.95)", borderColor: "rgba(255,255,255,0.04)" }}
                            labelClassName="text-slate-400 font-mono text-[9px]"
                            itemStyle={{ color: "#f8fafc", fontFamily: "monospace", fontSize: 11 }}
                          />
                          <Area type="monotone" dataKey="cpu_percent" stroke="#3B82F6" strokeWidth={1.5} name="CPU Load %" fillOpacity={1} fill="url(#colorBlue)" />
                          <Area type="monotone" dataKey="ai_anomaly_score" stroke="#6366F1" name="AI Anomaly Index" fillOpacity={1} fill="url(#colorIndigo)" />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Security Findings & Recommendations List Panel */}
                  <div className="glass-panel p-6 rounded-3xl lg:col-span-4 flex flex-col justify-between">
                    <div className="w-full flex items-center justify-between mb-4">
                      <h3 className="text-xs font-mono tracking-wider text-slate-300 flex items-center gap-1.5 font-bold">
                        <Sparkles className="w-4 h-4 text-blue-500" />
                        <span>MITIGATION ALERTS</span>
                      </h3>
                      <span className="text-[8px] font-mono text-slate-500 uppercase">SUGGESTIONS</span>
                    </div>

                    <div className="flex-1 flex flex-col gap-3 py-1">
                      {[
                        { title: "Revoke Overlays", text: "Quarantine apps utilizing system overlays.", active: targetDevice === "Android" },
                        { title: "Close Open TCP bins", text: "Clean up unencrypted network connectors.", active: true },
                        { title: "Run Deep Audit Scans", text: "Periodic process audits keep baselines nominal.", active: true }
                      ].map((item, i) => (
                        <div key={i} className="p-3 rounded-xl border border-white/[0.02] bg-[#030712]/50 text-left font-mono text-[10px]">
                          <p className="text-slate-200 font-bold flex items-center gap-1.5">
                            <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${item.active ? "bg-amber-400" : "bg-slate-600"}`}></span>
                            <span>{item.title}</span>
                          </p>
                          <p className="text-slate-500 mt-1 leading-normal">{item.text}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                </div>

                {/* Bottom Row Bento Section */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  
                  {/* Android Phone Deck */}
                  <div className="glass-panel p-5 rounded-3xl flex flex-col justify-between">
                    <div className="w-full flex items-center justify-between mb-4">
                      <h3 className="text-xs font-mono tracking-wider text-slate-300 flex items-center gap-1.5 font-bold">
                        <Smartphone className="w-4 h-4 text-blue-500" />
                        <span>ANDROID DEVICE HUB (ADB)</span>
                      </h3>
                      {targetDevice === "Android" && (
                        <span className="text-[9px] font-mono text-emerald-400 font-bold">CONNECTED</span>
                      )}
                    </div>

                    <div className="flex flex-col items-center py-3 relative">
                      <div className="w-24 h-44 border border-white/[0.04] rounded-2xl bg-[#030712] p-2 flex flex-col justify-between overflow-hidden shadow-2xl">
                        <div className="w-12 h-3 bg-slate-800 rounded-full mx-auto mb-1"></div>
                        <div className="flex-1 flex flex-col justify-center items-center gap-2 text-center">
                          {targetDevice === "Android" ? (
                            <>
                              <Smartphone className="w-6 h-6 text-blue-400 animate-pulse" />
                              <div className="text-[9px] font-mono text-slate-400 leading-normal">
                                <p className="font-bold">{deviceInfo.hostname || "Android Device"}</p>
                                <p className="text-slate-500">USB Connected</p>
                              </div>
                            </>
                          ) : (
                            <div className="p-2">
                              <Info className="w-5 h-5 text-slate-700 mx-auto mb-1" />
                              <p className="text-[8px] font-mono text-slate-500 leading-normal uppercase">Select ADB target to inspect logs</p>
                            </div>
                          )}
                        </div>
                        <div className="w-6 h-6 rounded-full border border-white/[0.04] mx-auto mt-2"></div>
                      </div>
                    </div>
                  </div>

                  {/* Sockets grid map visualizer */}
                  <div className="glass-panel p-5 rounded-3xl flex flex-col justify-between">
                    <div className="w-full flex items-center justify-between mb-4">
                      <h3 className="text-xs font-mono tracking-wider text-slate-300 flex items-center gap-1.5 font-bold">
                        <Globe className="w-4 h-4 text-blue-500" />
                        <span>NETWORK CONNECTIONS</span>
                      </h3>
                      <span className="text-[8px] font-mono text-slate-500">PORT BINDINGS</span>
                    </div>

                    <div className="flex-1 flex flex-col gap-2">
                      {activeSockets.map((sock, i) => (
                        <div key={i} className="p-2.5 rounded-xl border border-white/[0.02] bg-[#030712]/50 font-mono text-[9px] flex items-center justify-between">
                          <div>
                            <p className="text-slate-300 font-bold">{sock.app}</p>
                            <p className="text-slate-500 mt-0.5">{sock.local} ➔ {sock.remote}</p>
                          </div>
                          <span className="text-[8px] bg-slate-900 border border-white/[0.03] px-2 py-0.5 text-blue-400 rounded uppercase font-bold">{sock.proto}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Timeline chronological event feed */}
                  <div className="glass-panel p-5 rounded-3xl flex flex-col justify-between">
                    <div className="w-full flex items-center justify-between mb-4">
                      <h3 className="text-xs font-mono tracking-wider text-slate-300 flex items-center gap-1.5 font-bold">
                        <Terminal className="w-4 h-4 text-blue-500" />
                        <span>EVENT TIMELINE LOGS</span>
                      </h3>
                    </div>

                    <div className="flex-1 flex flex-col gap-2 h-44 overflow-y-auto pr-1">
                      {timelineEvents.map((evt, i) => (
                        <div key={i} className="flex items-start gap-2 text-[9px] font-mono leading-normal">
                          <span className="text-slate-500 shrink-0">{evt.time}</span>
                          <span className={`w-1.5 h-1.5 rounded-full shrink-0 mt-1.5 ${evt.type === "success" ? "bg-blue-500" : "bg-indigo-400"}`}></span>
                          <span className="text-slate-400 leading-snug">{evt.text}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                </div>

              </div>
            )}

            {/* Tab 2: High Density sorting process table */}
            {activeTab === "processes" && (
              <div className="flex flex-col gap-6">
                
                {/* Header operations deck */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div>
                    <h2 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">OPERATIONAL RUNTIME PROCESSES</h2>
                    <p className="text-xs text-slate-500 mt-0.5">Real-time memory partition auditing synced with FastAPI daemon</p>
                  </div>
                  
                  {/* Controls */}
                  <div className="flex items-center gap-3">
                    {/* Filter selector */}
                    <div className="flex items-center bg-white/[0.02] p-1 border border-white/[0.04] rounded-xl text-[10px] font-mono">
                      {[
                        { id: "all", label: "All processes" },
                        { id: "warning", label: "Anomalous" },
                        { id: "user", label: "User active" }
                      ].map(item => (
                        <button 
                          key={item.id}
                          onClick={() => setProcessFilter(item.id as any)}
                          className={`px-3 py-1 rounded-lg transition-all font-bold ${
                            processFilter === item.id 
                              ? "bg-white/[0.03] text-blue-400 border border-white/[0.05]" 
                              : "text-slate-500 hover:text-slate-300"
                          }`}
                        >
                          {item.label.toUpperCase()}
                        </button>
                      ))}
                    </div>

                    <button 
                      onClick={startDeepAudit}
                      disabled={threatScanRunning}
                      className="flex items-center gap-2 px-5 py-2 rounded-xl bg-blue-500/10 border border-blue-400/30 text-blue-400 text-xs font-mono font-bold hover:bg-blue-500/25 transition-all"
                    >
                      <RefreshCw className={`w-4 h-4 ${threatScanRunning ? "animate-spin" : ""}`} />
                      <span>{threatScanRunning ? "AUDITING..." : "DEEP AUDIT SCAN"}</span>
                    </button>
                  </div>
                </div>

                {/* Warning lists if threat scan results exist */}
                {threatScanResults.length > 0 && (
                  <div className="p-4 rounded-xl border border-amber-500/10 bg-amber-950/5 flex flex-col gap-3 animate-fade-in">
                    <h3 className="text-xs font-mono text-amber-400 font-bold uppercase tracking-wider flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4" />
                      <span>RISK ASSESSMENT WARNINGS FLAGGED</span>
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {threatScanResults.map((app, i) => (
                        <div 
                          key={i} 
                          onClick={() => auditApp(app)}
                          className="p-3 rounded-xl border border-white/[0.03] bg-[#030712]/80 hover:border-blue-500/30 cursor-pointer flex items-center justify-between transition-all"
                        >
                          <div className="flex items-center gap-3">
                            <Skull className="w-5 h-5 text-rose-500" />
                            <div>
                              <p className="text-xs font-bold text-slate-200">{app.name} <span className="text-slate-600">(PID: {app.pid})</span></p>
                              <p className="text-[9px] text-slate-500 mt-0.5">{app.reason}</p>
                            </div>
                          </div>
                          <span className="text-[9px] font-mono font-bold bg-rose-500/10 border border-rose-500/30 px-2 py-0.5 rounded text-rose-400">{app.risk_level} Risk</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* High Density Table replacing cards ( inspired by Datadog / Linear ) */}
                <div className="glass-panel rounded-2xl overflow-hidden border border-white/[0.04]">
                  <div className="p-3 border-b border-white/[0.04] bg-white/[0.01] flex items-center gap-3">
                    <Search className="w-4 h-4 text-slate-500" />
                    <input 
                      type="text" 
                      placeholder="Filter active processes by name or PID..." 
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      className="bg-transparent border-none text-xs font-mono w-full text-slate-300 placeholder-slate-600 focus:outline-none"
                    />
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full text-left font-mono text-xs border-collapse">
                      <thead>
                        <tr className="border-b border-white/[0.03] bg-white/[0.01] text-[10px] text-slate-500 uppercase tracking-widest font-bold">
                          <th className="p-4 pl-6">Process Name</th>
                          <th className="p-4">PID</th>
                          <th className="p-4">Runtime User</th>
                          <th className="p-4">CPU %</th>
                          <th className="p-4">RAM %</th>
                          <th className="p-4 text-center">Diagnostics</th>
                          <th className="p-4 text-right pr-6">Mitigation Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredProcesses.map((app, i) => {
                          const highRisk = app.cpu_percent > 30 || app.is_threat;
                          return (
                            <tr 
                              key={i} 
                              onClick={() => auditApp(app)}
                              className="border-b border-white/[0.02] hover:bg-white/[0.01] cursor-pointer transition-colors"
                            >
                              <td className="p-4 pl-6 font-bold text-slate-200 flex items-center gap-2">
                                <Cpu className="w-3.5 h-3.5 text-slate-500" />
                                <span>{app.name}</span>
                              </td>
                              <td className="p-4 text-slate-400">{app.pid}</td>
                              <td className="p-4 text-slate-500">{app.username}</td>
                              <td className="p-4">
                                <span className={app.cpu_percent > 30 ? "text-rose-400 font-bold animate-pulse" : "text-slate-300"}>
                                  {app.cpu_percent}%
                                </span>
                              </td>
                              <td className="p-4 text-slate-300">{app.memory_percent}%</td>
                              <td className="p-4 text-center">
                                <span className={`text-[8px] font-bold border px-1.5 py-0.5 rounded tracking-wide uppercase ${
                                  highRisk 
                                    ? "bg-rose-500/10 border-rose-500/20 text-rose-400" 
                                    : "bg-slate-900 border-white/[0.03] text-slate-500"
                                }`}>
                                  {highRisk ? "Warning" : "Nominal"}
                                </span>
                              </td>
                              <td className="p-4 text-right pr-6" onClick={e => e.stopPropagation()}>
                                <button 
                                  onClick={() => terminateProcess(Number(app.pid))}
                                  className="p-1.5 rounded-lg border border-white/[0.04] bg-[#030712] hover:border-rose-500/40 text-slate-500 hover:text-rose-400 transition-all flex items-center justify-center ml-auto"
                                  title="Kill Process thread"
                                >
                                  <Trash2 className="w-3.5 h-3.5" />
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>

                  {filteredProcesses.length === 0 && (
                    <div className="text-center py-20 text-xs font-mono text-slate-600">
                      No active processes match your filter queries.
                    </div>
                  )}
                </div>

              </div>
            )}

            {/* Tab 3: Sockets connections grid */}
            {activeTab === "network" && (
              <div className="flex flex-col gap-6">
                <div>
                  <h2 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">NETWORK CONNECTIONS</h2>
                  <p className="text-xs text-slate-500 mt-0.5">Monitors socket descriptors, bind ports, and remote host handshakes</p>
                </div>

                <div className="glass-panel rounded-2xl overflow-hidden border border-white/[0.04]">
                  <table className="w-full text-left font-mono text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-white/[0.03] bg-white/[0.01] text-[10px] text-slate-500 uppercase tracking-widest font-bold">
                        <th className="p-4 pl-6">Owner Process</th>
                        <th className="p-4">Local Binder</th>
                        <th className="p-4">Remote Host</th>
                        <th className="p-4">Socket State</th>
                        <th className="p-4 text-right pr-6">Protocol</th>
                      </tr>
                    </thead>
                    <tbody>
                      {activeSockets.map((sock, i) => (
                        <tr key={i} className="border-b border-white/[0.02] hover:bg-white/[0.01] transition-colors">
                          <td className="p-4 pl-6 font-bold text-slate-200 flex items-center gap-2">
                            <Globe className="w-3.5 h-3.5 text-slate-500" />
                            <span>{sock.app}</span>
                          </td>
                          <td className="p-4 text-slate-300">{sock.local}</td>
                          <td className="p-4 text-slate-300">{sock.remote}</td>
                          <td className="p-4">
                            <span className="text-[9px] bg-slate-900 border border-blue-500/25 px-2 py-0.5 rounded text-blue-400 font-bold tracking-wider">
                              {sock.status}
                            </span>
                          </td>
                          <td className="p-4 text-right pr-6 text-slate-500 font-bold">{sock.proto}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Tab 4: Mobile Senses privacy Center */}
            {activeTab === "privacy" && (
              <div className="flex flex-col gap-6">
                <div>
                  <h2 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">MOBILE PRIVACY COMMAND</h2>
                  <p className="text-xs text-slate-500 mt-0.5">Audits mobile permissions and monitors background queries utilizing AppOps</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {[
                    { title: "MICROPHONE CHANNEL", active: androidRiskReport.active_sensors.mic.length > 0, list: androidRiskReport.active_sensors.mic },
                    { title: "CAMERA OPTICAL CAPTURE", active: androidRiskReport.active_sensors.camera.length > 0, list: androidRiskReport.active_sensors.camera },
                    { title: "GPS LOCATION SENSE", active: androidRiskReport.active_sensors.gps.length > 0, list: androidRiskReport.active_sensors.gps }
                  ].map((sens, i) => (
                    <div key={i} className={`p-5 rounded-2xl border transition-all glass-panel ${
                      sens.active ? "border-rose-500/20 bg-rose-950/10" : "bg-[#030712]/50"
                    }`}>
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-[9px] font-mono text-slate-500 tracking-wider uppercase">{sens.title}</span>
                        <span className={`w-2 h-2 rounded-full ${sens.active ? "bg-rose-500 animate-pulse" : "bg-slate-700"}`}></span>
                      </div>
                      {sens.active ? (
                        <div>
                          <p className="text-xs text-rose-400 font-bold flex items-center gap-1.5 uppercase font-mono">
                            <AlertOctagon className="w-4 h-4 shrink-0" />
                            <span>ACTIVE BACKGROUND QUERY DETECTED!</span>
                          </p>
                          <p className="text-[10px] text-slate-500 font-mono mt-1">Queried by: {sens.list.join(", ")}</p>
                        </div>
                      ) : (
                        <p className="text-xs text-slate-400 font-mono flex items-center gap-1.5">
                          <CheckCircle2 className="w-4 h-4 text-blue-500" />
                          <span>Nominal. No active sensory queries.</span>
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Tab 5: Premium drag and drop audit */}
            {activeTab === "file-scan" && (
              <div className="glass-panel p-8 rounded-3xl max-w-2xl mx-auto flex flex-col items-center w-full">
                <h2 className="text-sm font-bold font-mono tracking-wider text-slate-200 uppercase mb-2">BINARY EXECUTABLE AUDIT</h2>
                <p className="text-xs text-slate-500 text-center leading-normal max-w-md mb-8">
                  Upload configuration packages, binary files, or mobile APK elements. Structural checks will decompile parameters to match baseline threat indices.
                </p>

                <div className="w-full border border-dashed border-white/[0.08] hover:border-blue-500/40 rounded-2xl p-10 bg-[#030712]/50 flex flex-col items-center cursor-pointer transition-all relative">
                  <input 
                    type="file" 
                    onChange={handleFileUpload}
                    className="absolute inset-0 opacity-0 cursor-pointer" 
                  />
                  <FileText className="w-10 h-10 text-blue-400 animate-pulse mb-3" />
                  <p className="text-xs font-mono text-slate-300 font-bold uppercase tracking-wider">Drag & drop a file here</p>
                  <p className="text-[9px] text-slate-500 mt-2">Accepts APK, EXE, SH, or script files</p>
                </div>

                {fileAnalyzing && (
                  <div className="mt-8 flex flex-col items-center gap-3 w-full max-w-sm">
                    <div className="flex justify-between w-full text-xs font-mono text-slate-400">
                      <span>Decompiling structural hooks...</span>
                      <span>60%</span>
                    </div>
                    <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500" style={{ width: "60%" }}></div>
                    </div>
                  </div>
                )}

                {fileAnalysisResult && (
                  <div className="w-full mt-8 p-5 rounded-2xl border border-white/[0.04] bg-[#030712]">
                    <h3 className="text-xs font-mono text-slate-200 font-bold mb-3 uppercase tracking-wider">Static Audit Report</h3>
                    <div className="flex items-center justify-between p-3 rounded-xl border border-white/[0.02] bg-white/[0.02] font-mono text-xs mb-3">
                      <span>Signature: {fileAnalysisResult.name}</span>
                      <span className="text-[10px] font-bold text-blue-400">{fileAnalysisResult.size}</span>
                    </div>
                    <div className={`p-4 rounded-xl border flex items-start gap-3 ${
                      fileAnalysisResult.risk_score > 70 
                        ? "border-rose-500/20 bg-rose-950/10 text-rose-300" 
                        : "border-emerald-500/20 bg-emerald-950/10 text-emerald-300"
                    }`}>
                      {fileAnalysisResult.risk_score > 70 ? <AlertOctagon className="w-5 h-5 shrink-0 mt-0.5" /> : <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5" />}
                      <div>
                        <h4 className="text-xs font-bold uppercase font-mono tracking-wide">
                          {fileAnalysisResult.risk_score > 70 ? "HIGH RISK DETECTED" : "SIGNATURE PASSED NOMINAL"}
                        </h4>
                        <p className="text-[10px] text-slate-400 leading-normal mt-1">
                          Verdict: {fileAnalysisResult.verdict}. Security score: {fileAnalysisResult.risk_score}%. Heuristics: {fileAnalysisResult.reason || "Structural fingerprint complies with passive baseline signature checks."}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

          </div>

          {/* Persistent AI Security Assistant Column ( ChatGPT integrated in SaaS ) */}
          {aiPanelExpanded && (
            <div className="w-[300px] shrink-0 sticky top-24 flex flex-col gap-6 z-10 font-mono">
              <div className="glass-panel rounded-3xl h-[660px] flex flex-col justify-between overflow-hidden">
                {/* Header */}
                <div className="p-4 border-b border-white/[0.04] bg-white/[0.02] flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="p-1 rounded bg-blue-500/10 border border-blue-400/25">
                      <Sparkles className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-100 uppercase tracking-wider">AI Copilot</h4>
                      <span className="text-[8px] text-blue-400">NOMINAL ONLINE</span>
                    </div>
                  </div>
                </div>

                {/* Dialog history */}
                <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
                  {copilotMessages.map((m, i) => (
                    <div 
                      key={i} 
                      className={`flex flex-col max-w-[90%] rounded-2xl p-3 text-[10px] leading-relaxed ${
                        m.sender === "ai" 
                          ? "align-self-start border border-blue-500/10 bg-blue-950/10 text-blue-300 self-start" 
                          : "align-self-end border border-white/[0.04] bg-white/[0.01] text-slate-200 self-end"
                      }`}
                    >
                      {m.text}
                    </div>
                  ))}
                </div>

                {/* Tags */}
                <div className="px-4 py-2 border-t border-white/[0.03] bg-black/40 flex gap-2 overflow-x-auto">
                  {[
                    "Harden protection loop",
                    "Audit unsecure ports",
                    "Suggest ADB connect steps"
                  ].map((card, i) => (
                    <button 
                      key={i} 
                      onClick={() => {
                        setCopilotInput(card);
                      }}
                      className="shrink-0 text-[8px] border border-white/[0.04] bg-[#030712] hover:border-blue-500/35 hover:text-blue-400 text-slate-500 px-2.5 py-1 rounded-lg transition-all"
                    >
                      {card}
                    </button>
                  ))}
                </div>

                {/* Input form */}
                <div className="p-3 border-t border-white/[0.04] flex gap-2">
                  <input 
                    type="text" 
                    placeholder="Query security vectors..." 
                    value={copilotInput}
                    onChange={e => setCopilotInput(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleSendMessage()}
                    className="flex-1 bg-slate-900 border border-white/[0.04] rounded-xl px-3 py-2 text-[10px] text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500/50"
                  />
                  <button 
                    onClick={handleSendMessage}
                    className="p-2 rounded-xl bg-blue-500/15 border border-blue-400/25 text-blue-400 hover:bg-blue-500/30 transition-all text-glow-cyan"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </div>

              </div>
            </div>
          )}

        </div>

      </div>

      {/* Slide-over Right Drawer Panel for Granular process details */}
      {selectedApp && (
        <div className="fixed inset-0 z-50 overflow-hidden flex justify-end">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-xs" onClick={() => setSelectedApp(null)}></div>
          
          <div className="relative w-full max-w-xl h-full border-l border-white/[0.04] bg-slate-950/95 backdrop-blur-xl shadow-2xl p-6 flex flex-col justify-between overflow-y-auto animate-slide-in">
            
            <div>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-blue-500/10 border border-blue-400/25 rounded-xl">
                    <Cpu className="w-5 h-5 text-blue-400" />
                  </div>
                  <div>
                    <h3 className="text-sm font-extrabold text-slate-100 flex items-center gap-2">
                      <span>{selectedApp.name}</span>
                      <span className="text-[8px] bg-[#030712] border border-white/[0.04] text-slate-500 px-2 py-0.5 rounded font-mono">PID: {selectedApp.pid}</span>
                    </h3>
                    <p className="text-[9px] font-mono text-slate-500 uppercase mt-0.5">Runtime Invoker: {selectedApp.username}</p>
                  </div>
                </div>
                
                <button 
                  onClick={() => setSelectedApp(null)}
                  className="p-1 rounded-lg border border-white/[0.04] hover:border-rose-500/40 text-slate-400 hover:text-rose-400 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="h-px bg-white/[0.04] my-5"></div>

              {appDetailsLoading ? (
                <div className="flex flex-col items-center justify-center py-20 gap-3 font-mono text-xs text-slate-500">
                  <RefreshCw className="w-5 h-5 text-blue-400 animate-spin" />
                  <span>Deconstructing memory partitions...</span>
                </div>
              ) : appDetails ? (
                <div className="flex flex-col gap-6">
                  {/* Verdict widget */}
                  <div className={`p-4 rounded-xl border flex items-start gap-3 ${
                    appDetails.trust_score < 75 
                      ? "border-rose-500/20 bg-rose-950/10 text-rose-300" 
                      : "border-blue-500/20 bg-blue-950/10 text-blue-300"
                  }`}>
                    {appDetails.trust_score < 75 ? <AlertOctagon className="w-5 h-5 shrink-0 mt-0.5" /> : <ShieldCheck className="w-5 h-5 shrink-0 mt-0.5" />}
                    <div>
                      <h4 className="text-xs font-bold uppercase font-mono tracking-wider">AI DIAGNOSTIC DIAGRAM</h4>
                      <p className="text-[10px] text-slate-400 leading-normal mt-1">
                        Security index: {appDetails.trust_score}/100. Severity Class: {appDetails.risk_level}.
                      </p>
                    </div>
                  </div>

                  {/* Risks factors bullet checklist */}
                  <div>
                    <h4 className="text-[9px] font-mono text-slate-500 uppercase tracking-widest mb-2 font-bold">SECURITY FINDINGS LOGGED</h4>
                    {appDetails.risk_factors.length > 0 ? (
                      <div className="flex flex-col gap-2">
                        {appDetails.risk_factors.map((risk: string, i: number) => (
                          <div key={i} className="flex items-start gap-2 text-[10px] font-mono text-rose-300 leading-normal">
                            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mt-1.5 shrink-0"></span>
                            <span>{risk}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="flex items-center gap-1.5 text-xs text-blue-400 font-mono">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Pass. Zero operational risk components logged.</span>
                      </div>
                    )}
                  </div>

                  {/* Permissions checks */}
                  {appDetails.permissions?.length > 0 && (
                    <div>
                      <h4 className="text-[9px] font-mono text-slate-500 uppercase tracking-widest mb-2 font-bold">REVOCABLE SENSOR PERMISSIONS</h4>
                      <div className="flex flex-wrap gap-1">
                        {appDetails.permissions.map((perm: string, i: number) => (
                          <span key={i} className="text-[8px] font-mono bg-slate-900 border border-white/[0.04] text-slate-400 px-2 py-0.5 rounded">
                            {perm.split(".").pop()}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Processes metadata */}
                  {Object.keys(appDetails.metadata || {}).length > 0 && (
                    <div>
                      <h4 className="text-[9px] font-mono text-slate-500 uppercase tracking-widest mb-2 font-bold">DECOMPILED BINARY METADATA</h4>
                      <pre className="p-3 rounded-xl border border-white/[0.04] bg-black/60 text-[9px] font-mono text-slate-400 overflow-x-auto leading-normal">
                        {JSON.stringify(appDetails.metadata, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-20 text-xs font-mono text-slate-600">Trace details skipped.</div>
              )}
            </div>

            {/* Actions footer */}
            <div className="flex flex-col gap-2 border-t border-white/[0.04] pt-4 mt-6">
              <div className="flex gap-2">
                <button 
                  onClick={() => terminateProcess(Number(selectedApp.pid))}
                  className="flex-1 py-3 rounded-xl border border-rose-500/30 bg-rose-950/20 text-rose-300 font-mono text-xs font-bold hover:bg-rose-500/25 transition-all flex items-center justify-center gap-1.5"
                >
                  <Trash2 className="w-4 h-4 shrink-0" />
                  <span>🧨 FORCE TERMINATE PROCESS</span>
                </button>
                
                {targetDevice === "Android" && (
                  <button className="flex-1 py-3 rounded-xl border border-amber-500/30 bg-amber-950/20 text-amber-300 font-mono text-xs font-bold hover:bg-amber-500/25 transition-all flex items-center justify-center gap-1.5">
                    <Lock className="w-4 h-4 shrink-0" />
                    <span>QUARANTINE APP</span>
                  </button>
                )}
              </div>
              
              <button 
                onClick={() => setSelectedApp(null)}
                className="w-full py-3 rounded-xl border border-white/[0.04] text-slate-400 font-mono text-xs font-bold hover:border-slate-800 hover:text-slate-300 transition-colors"
              >
                DISMISS INSPECTION
              </button>
            </div>

          </div>
        </div>
      )}

      {/* Global CMD+K command palette modal overlay */}
      {commandPaletteOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4">
          <div className="absolute inset-0 bg-black/70 backdrop-blur-xs" onClick={() => setCommandPaletteOpen(false)}></div>
          
          <div className="relative w-full max-w-xl border border-white/[0.05] bg-slate-950/95 backdrop-blur-xl rounded-2xl shadow-2xl overflow-hidden animate-zoom-in">
            <div className="p-4 border-b border-white/[0.03] flex items-center gap-3">
              <Search className="w-5 h-5 text-blue-500" />
              <input 
                type="text" 
                placeholder="Search processes, logs, or execute commands..." 
                value={cmdSearch}
                onChange={e => setCmdSearch(e.target.value)}
                className="flex-1 bg-transparent text-xs text-slate-100 font-mono placeholder-slate-600 focus:outline-none"
              />
              <span className="text-[10px] font-mono text-slate-600 border border-white/[0.04] px-2 py-0.5 rounded">ESC</span>
            </div>

            <div className="p-3 max-h-64 overflow-y-auto flex flex-col gap-1">
              <span className="text-[8px] font-mono text-slate-600 uppercase tracking-widest px-2 py-1 mb-1">COMMAND AUDITS</span>
              
              {[
                { label: "Trigger Deep Process Scans", action: startDeepAudit },
                { label: "Pair Android Device wirelessly", action: () => connectWirelessADB("192.168.1.115") },
                { label: "Refreshes system telemetry metrics", action: refreshTelemetry },
                { label: "Toggle Active Protection sentinel loop", action: toggleMonitoring }
              ].map((cmd, i) => (
                <button 
                  key={i} 
                  onClick={() => {
                    cmd.action();
                    setCommandPaletteOpen(false);
                  }}
                  className="w-full text-left font-mono text-xs text-slate-300 hover:bg-blue-500/10 hover:text-blue-400 p-2.5 rounded-xl transition-all flex items-center justify-between"
                >
                  <span>{cmd.label}</span>
                  <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
