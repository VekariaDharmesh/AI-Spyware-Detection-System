# SilentGuard AI 2.0 🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js: 16+](https://img.shields.io/badge/Next.js-16+-black.svg)](https://nextjs.org/)
[![FastAPI: 0.100+](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

**SilentGuard AI 2.0** is an enterprise-grade, high-density **SaaS Cybersecurity Command Center** and heuristic threat engine. It protects cross-platform environments (macOS, Windows, Linux, and Android) against zero-day stalkerware and behavioral spyware anomalies without relying on traditional, easily bypassed signature hashes.

Inspired by premium interfaces like **Vercel, Linear, and CrowdStrike Falcon**, it incorporates glassmorphic layouts, dynamic telemetry area charting, interactive process detail drawers, and a persistent AI Copilot.

<br>

---

## 🏗️ Premium Architecture Overview

SilentGuard AI 2.0 implements a decoupled, high-performance dual-process architecture:

```
                          ┌───────────────────────────┐
                          │    Next.js 16 Frontend    │
                          │   (Vercel / static edge)  │
                          └─────────────┬─────────────┘
                                        │ (JSON CORS)
                                        ▼
                          ┌───────────────────────────┐
                          │    FastAPI REST Engine    │
                          │  (Render / Local Agent)   │
                          └─────────────┬─────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
     ┌───────────────────────┐                     ┌───────────────────────┐
     │  Local Process Audits │                     │  ADB Mobile Auditing  │
     │   (psutil anomalies)  │                     │ (Sensor/Permissions)  │
     └───────────────────────┘                     └───────────────────────┘
```

* **Frontend Dashboard (`/frontend`)**: Built with **Next.js 16 (Turbopack)**, **TypeScript**, and **Lucide Icons**. Styled with HSL glassmorphism variables, subtle aurora gradients, bento grids, and responsive slide-out process side-panels.
* **REST API Engine (`/spyware_detection_project`)**: Powered by **FastAPI** and **Uvicorn**, bridging the underlying machine learning autoencoders and system scans to pure JSON endpoints.
* **Unified Launcher (`run_dev.sh`)**: Starts both services concurrently, providing hot-reload and graceful dual-port cleanup.

<br>

---

## ✨ Features & Workflows

- **AI Threat Analysis**: Adaptive anomaly indexes trained on your own computing patterns, flagging resource peaks, unlinked process sockets, and irregular threads.
- **Next-Gen Bento Dashboard**: High-density grid presenting live health scores, CPU/Memory telemetry area graphs, threat feeds, and socket logs.
- **Process Explorer Drawer**: Side-panel detailing deep memory footprint gauges, revocable permission lists, raw JSON states, and instant actions (*Quarantine*, *Force Terminate*).
- **ADB Android Deck**: USB/Wireless Android monitoring showcasing system connection indicators, live GPS/Camera/Mic sensor triggers, and active socket logs.
- **Static File Decompiler**: Allows dragging and dropping static APK binaries or local files for real-time heuristical code analysis.
- **Enterprise-Grade UX**: Premium sans-serif typography (`Inter`), fast responsive layouts, and customizable dark security themes.

<br>

---

## ⚡ Local Setup & Execution

### 1. Clone & Set Up Directory
```bash
git clone https://github.com/VekariaDharmesh/AI-Spyware-Detection-System.git
cd AI-Spyware-Detection-System
```

### 2. Dual-Process Development Boot
Ensure you have `python3` (3.11+) and `node` (18+) installed. Then run the unified dev server launcher from the root folder:
```bash
chmod +x run_dev.sh
./run_dev.sh
```

This single command will automatically:
1. Boot the **FastAPI REST API Server** on `http://localhost:8000`.
2. Boot the **Next.js 16 Frontend App** on `http://localhost:3000`.
3. Provide live hot-reloading for code edits.
4. Cleanly terminate all active background ports upon hitting `Ctrl+C`.

---

## 🚀 Production Cloud Deployment

Deploy SilentGuard AI 2.0 directly to the cloud:

### 1. Deploy the Next.js Frontend to **Vercel**
Since Vercel is the ultimate hosting home for Next.js, you can deploy the dashboard globally in seconds:

1. Log in to [Vercel](https://vercel.com/) and click **Add New** > **Project**.
2. Connect your GitHub repository: `VekariaDharmesh/AI-Spyware-Detection-System`.
3. Under **Project Settings**:
   * Set the **Root Directory** to `frontend`.
   * Keep the Framework Preset as **Next.js**.
4. In **Environment Variables**, add:
   * **Key**: `NEXT_PUBLIC_API_BASE`
   * **Value**: *(The live HTTPS URL of your deployed Render backend, or fallback to `http://localhost:8000` to interact with your local agent!)*
5. Click **Deploy**. Vercel will host your premium dashboard globally on a free SSL-backed edge network.

### 2. Deploy the FastAPI Backend to **Render**
Deploy the dynamic Python backend engine directly using the repository's root **Render Blueprint**:

1. Log in to [Render](https://dashboard.render.com/) and click **New +** > **Blueprint**.
2. Select your GitHub repository: `VekariaDharmesh/AI-Spyware-Detection-System`.
3. Render will parse the `render.yaml` file automatically, establishing the `silentguard-backend` service.
4. Click **Apply** or **Deploy**.
5. Render will build and host your backend service, providing you with a live secure URL (e.g. `https://silentguard-backend.onrender.com`). You can plug this URL into your Vercel frontend environment variable!

> [!NOTE]
> For cloud environments like Vercel and Render, the dashboard acts as a remote command console. To scan your local PC's active memory or check a phone connected over USB, keep the frontend running on Vercel and let it connect to your local FastAPI backend agent running on `http://localhost:8000`!

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

## 👨‍💻 Redesigned & Redefined by
* **Dharmesh Vekaria** — Anand, Gujarat, India
* Premium 2026 SaaS Cybersecurity Command Center Redesign.
