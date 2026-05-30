"""
SilentGuard AI 2.0 - High Performance FastAPI Backend Server
Bridges existing universal_interface.py logic to a modern REST API for the Next.js React frontend.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import sys

# Ensure local imports are correct
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_interface import UniversalDeviceInterface
from database_manager import DatabaseManager

app = FastAPI(
    title="SilentGuard AI 2.0 Backend",
    description="Futuristic Cybersecurity Command Center API Wrapper",
    version="2.0.0"
)

# Enable CORS for the Next.js Frontend (port 3000) and general localhost routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local testing convenience
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate the Core Bridge Layer
udi = UniversalDeviceInterface()

# --- Request Data Models ---
class TargetDeviceModel(BaseModel):
    target: str  # "Desktop" or "Android"

class ScanAppDetailsModel(BaseModel):
    target_id: str
    platform: str  # "desktop" or "android"

class TerminateAppModel(BaseModel):
    pid: int

class AndroidPackageModel(BaseModel):
    package_name: str

class ConnectWirelessModel(BaseModel):
    ip: str
    port: Optional[str] = "5555"

class PairWirelessModel(BaseModel):
    host: str
    port: str
    code: str


# --- CORS Root & Info ---
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "SilentGuard AI 2.0 REST Engine",
        "target_device": udi.target_device,
        "device_type": udi.device_type,
        "android_connected": bool(udi.android.connected) if udi.android else False
    }


# --- Device Configuration ---
@app.post("/api/set-target")
async def set_target(data: TargetDeviceModel):
    target = data.target
    if target not in ["Desktop", "Android"]:
        raise HTTPException(status_code=400, detail="Invalid target device. Must be 'Desktop' or 'Android'")
    
    udi.target_device = target
    if target == "Android":
        udi.device_type = "mobile"
    else:
        udi.device_type = "desktop"
        
    udi.refresh_device_info()
    return {
        "success": True,
        "target": udi.target_device,
        "device_type": udi.device_type,
        "device_info": udi.device_info
    }

@app.get("/api/device-info")
async def get_device_info():
    if udi.android:
        udi.android.check_connection()
    udi.refresh_device_info()
    return udi.device_info


# --- Performance & Resource Metrics ---
@app.get("/api/system-metrics")
async def get_system_metrics():
    try:
        return udi.get_system_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch system metrics: {str(e)}")

@app.get("/api/running-apps")
async def get_running_apps(limit: Optional[int] = 100):
    try:
        return udi.get_running_apps(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch running apps: {str(e)}")

@app.get("/api/device-health")
async def get_device_health():
    try:
        return udi.get_device_health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate health score: {str(e)}")


# --- Live Telemetry Background Threading ---
@app.post("/api/start-monitoring")
async def start_monitoring():
    udi.start_live_monitoring()
    return {
        "success": True,
        "status": udi.live_collector.status,
        "is_collecting": udi.live_collector.is_collecting
    }

@app.post("/api/stop-monitoring")
async def stop_monitoring():
    udi.stop_live_monitoring()
    return {
        "success": True,
        "status": udi.live_collector.status,
        "is_collecting": udi.live_collector.is_collecting
    }

@app.get("/api/monitoring-status")
async def get_monitoring_status():
    return {
        "is_collecting": udi.live_collector.is_collecting,
        "status": udi.live_collector.status,
        "last_error": udi.live_collector.last_error
    }

@app.get("/api/live-metrics")
async def get_live_metrics():
    metrics = udi.live_collector.get_live_metrics()
    return metrics or []


# --- Heuristic AI Deep Scans ---
@app.post("/api/perform-ai-scan")
async def perform_ai_scan(limit: Optional[int] = 10):
    try:
        results = udi.perform_ai_scan(limit=limit)
        return {
            "success": True,
            "threats_count": sum(1 for res in results if res.get("is_threat", False)),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Deep Scan failed: {str(e)}")

@app.post("/api/scan-app-details")
async def scan_app_details(data: ScanAppDetailsModel):
    try:
        # Scan detailed properties and permissions
        results = udi.scan_app_details(data.target_id, data.platform)
        
        # Calculate BDI insights for extra UX polish
        bdi_insights = {
            "data_collection": False,
            "send_window": "Unknown",
            "conditions": []
        }
        
        if data.platform == "android" and udi.android and udi.android.connected:
            try:
                exfil = udi.android.get_exfiltration_insights(data.target_id)
                bdi_insights["data_collection"] = exfil.get("is_collecting", False) or exfil.get("is_sending", False)
                bdi_insights["send_window"] = exfil.get("when_next", "Unknown")
                bdi_insights["conditions"] = exfil.get("conditions", [])
            except Exception:
                pass
                
        results["bdi_insights"] = bdi_insights
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scan app details: {str(e)}")


# --- Active Action Terminations ---
@app.post("/api/terminate-app")
async def terminate_app(data: TerminateAppModel):
    try:
        return udi.terminate_app(data.pid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Termination failed: {str(e)}")


# --- Android Specific Integration Controllers ---
@app.get("/api/android-risk-report")
async def get_android_risk_report():
    if not udi.android or not udi.android.connected:
        return {
            "score": 100,
            "issues": ["Android device not connected"],
            "dangerous_apps": [],
            "active_sensors": {"mic": [], "camera": [], "gps": []}
        }
    try:
        return udi.get_android_risk_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Android report: {str(e)}")

@app.post("/api/android/quarantine")
async def android_quarantine(data: AndroidPackageModel):
    if not udi.android or not udi.android.connected:
        raise HTTPException(status_code=400, detail="Android device not connected")
    try:
        success = udi.android.quarantine_app(data.package_name)
        return {"success": success, "message": f"App {data.package_name} quarantine trigger ran."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quarantine command failed: {str(e)}")

@app.post("/api/android/stop")
async def android_stop(data: AndroidPackageModel):
    if not udi.android or not udi.android.connected:
        raise HTTPException(status_code=400, detail="Android device not connected")
    try:
        success = udi.android.stop_app(data.package_name)
        return {"success": success, "message": f"App {data.package_name} force-stopped successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Force stop command failed: {str(e)}")

@app.get("/api/android/active-sensors")
async def android_sensors():
    if not udi.android or not udi.android.connected:
        return {"mic": [], "camera": [], "gps": []}
    try:
        return udi.android.get_active_sensors()
    except Exception as e:
        return {"mic": [], "camera": [], "gps": [], "error": str(e)}

@app.get("/api/android/open-ports")
async def android_open_ports(package_name: str):
    if not udi.android or not udi.android.connected:
        return []
    try:
        return udi.android.get_app_open_ports(package_name)
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/android/connect-wireless")
async def android_connect_wireless(data: ConnectWirelessModel):
    if not udi.android:
        raise HTTPException(status_code=500, detail="Android Monitor module not initialized")
    try:
        success, output = udi.android.connect_wireless(data.ip, data.port)
        return {"success": success, "output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/android/pair-wireless")
async def android_pair_wireless(data: PairWirelessModel):
    if not udi.android:
        raise HTTPException(status_code=500, detail="Android Monitor module not initialized")
    try:
        success, output = udi.android.pair_wireless(data.host, data.port, data.code)
        return {"success": success, "output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Static File Audits ---
@app.post("/api/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        analysis = udi.analyze_uploaded_file(file.filename, content)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Static analysis failed: {str(e)}")


# --- Forensic Scans History retrieval ---
@app.get("/api/scan-logs")
async def get_scan_logs(limit: Optional[int] = 50):
    try:
        return udi.db.get_scan_logs(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forensics retrieval failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
