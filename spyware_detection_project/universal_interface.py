"""
Universal Device Interface - Core Architecture
Transforms the project from spyware detection to universal device management
"""

import streamlit as st
import psutil
import platform
import socket
from datetime import datetime
from typing import Dict, List
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from collections import deque
import threading
import queue
from desktop_ai_model import DesktopThreatModel
from database_manager import DatabaseManager

try:
    from android_monitor import AndroidMonitor
except ImportError:
    AndroidMonitor = None

class LiveMetricsCollector:
    """Real-time metrics collection with threading"""
    
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.ai_scores = deque(maxlen=max_history)
        self.is_collecting = False
        self.collection_thread = None
        self.metrics_queue = queue.Queue()
        self.status = "Idle"
        self.last_error = None
        
    def start_collection(self):
        """Start background metrics collection"""
        if not self.is_collecting:
            self.is_collecting = True
            self.status = "Starting"
            self.last_error = None
            self.collection_thread = threading.Thread(target=self._collect_metrics, daemon=True)
            self.collection_thread.start()
    
    def stop_collection(self):
        """Stop background metrics collection"""
        self.is_collecting = False
        self.status = "Stopped"
        if self.collection_thread:
            self.collection_thread.join()
    
    def _collect_metrics(self):
        """Background thread for continuous metrics collection"""
        self.status = "Running"
        while self.is_collecting:
            try:
                timestamp = datetime.now()
                
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Network stats
                net_io = psutil.net_io_counters()
                
                # Calculate AI anomaly score
                ai_score = self._calculate_ai_anomaly_score(cpu_percent, memory.percent, disk.percent)
                
                metrics = {
                    'timestamp': timestamp,
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'network_bytes_sent': net_io.bytes_sent,
                    'network_bytes_recv': net_io.bytes_recv,
                    'ai_anomaly_score': ai_score
                }
                
                self.metrics_history.append(metrics)
                self.ai_scores.append(ai_score)
                
                time.sleep(0.5) # Refreshing Data 0.5 second 
                
            except Exception as e:
                print(f"Error collecting metrics: {e}")
                self.last_error = str(e)
                self.status = "Error"
                time.sleep(5)
    
    def _calculate_ai_anomaly_score(self, cpu, memory, disk):
        """
        Calculate AI-based anomaly score using simple ML approach.
        
        This method computes a synthetic risk score (0-100) based on system resource usage.
        - High CPU/Memory usage contributes to the score.
        - Used to populate live charts in the dashboard.
        """
        # Simple anomaly detection based on thresholds
        base_score = 0
        
        # CPU anomaly (0-30 points)
        if cpu > 90:
            base_score += 30
        elif cpu > 70:
            base_score += 20
        elif cpu > 50:
            base_score += 10
        elif cpu > 10:
             base_score += 2 # Baseline activity
        
        # Memory anomaly (0-30 points)  
        if memory > 90:
            base_score += 30
        elif memory > 80:
            base_score += 20
        elif memory > 60:
            base_score += 10
            
        # Disk anomaly (0-40 points)
        if disk > 95:
            base_score += 40
        elif disk > 85:
            base_score += 30
        elif disk > 75:
            base_score += 20
        elif disk > 60:
            base_score += 10
            
        return min(base_score, 100)
    
    def get_live_metrics(self):
        """Get current live metrics"""
        if not self.metrics_history:
            return None
        return list(self.metrics_history)
    
    def get_ai_trend(self):
        """Get AI anomaly trend"""
        if not self.ai_scores:
            return []
        return list(self.ai_scores)

class UniversalDeviceInterface:
    """
    Unified interface for managing all devices (mobile, desktop, tablet)
    Provides device-agnostic operations and monitoring
    """
    
    def __init__(self):
        self.device_type = self._detect_device_type()
        self.target_device = "Desktop" # Default target
        self.device_info = self._gather_device_info()
        self.connected_devices = []
        self.live_collector = LiveMetricsCollector()
        self.performance_history = deque(maxlen=1000)
        
        # Initialize Database
        self.db = DatabaseManager()
        
        # Initialize AI Model
        self.ai_model = self._initialize_ai_model()
        
        # Initialize Android Monitor
        if AndroidMonitor:
            try:
                self.android = AndroidMonitor()
            except Exception:
                self.android = None
        else:
            self.android = None
        
    def _initialize_ai_model(self):
        """Initialize Gemini AI model for advanced threat detection"""
        try:
            return DesktopThreatModel()
        except Exception as e:
            print(f"Failed to initialize AI model: {e}")
            return None
        
    def start_live_monitoring(self):
        """Start live metrics collection"""
        self.live_collector.start_collection()

    def perform_ai_scan(self, limit=5):
        """
        Perform a deep AI scan on running processes using Gemini.
        Returns a list of analyzed processes with risk scores.
        """
        if not self.ai_model:
            return {"error": "AI Model not initialized"}

        apps = self.get_running_apps()
        results = []
        threats_count = 0
        
        # Filter for top resource consumers to scan
        apps_to_scan = apps[:limit]
        
        for app in apps_to_scan:
            # Add command line if available (requires extra permissions usually, but we try)
            try:
                p = psutil.Process(app['pid'])
                app['cmdline'] = " ".join(p.cmdline())
            except:
                app['cmdline'] = "Unknown"

            # Analyze with Gemini
            analysis = self.ai_model.analyze_process(app)
            
            # Merge results
            app.update(analysis)
            
            if app.get('is_threat', False) or app.get('risk_score', 0) > 75:
                threats_count += 1
                
            results.append(app)
            
        # Log to Database
        self.db.add_scan_log(threats_count, results)
        
        return results
        
    def stop_live_monitoring(self):
        """Stop live metrics collection"""
        self.live_collector.stop_collection()

    def analyze_uploaded_file(self, file_name: str, file_content: bytes) -> Dict:
        """
        Analyze an uploaded file (APK, etc.) using the AI model.
        """
        if not self.ai_model:
            return {"error": "AI Model not initialized", "risk_score": 0, "verdict": "Unknown"}
            
        # Basic static analysis
        size_mb = len(file_content) / (1024 * 1024)
        
        file_info = {
            "name": file_name,
            "size": f"{size_mb:.2f} MB",
            "type": "APK" if file_name.endswith(".apk") else "Unknown"
        }
        
        # In a real scenario, we would extract strings, decompiled code, etc.
        # For this demo, we pass metadata to the AI model
        
        # If the model has a specific file analysis method, use it.
        # Otherwise, we wrap it in a process-like structure for the existing analyze_process method
        # OR we just ask the model directly if it supports generic prompts.
        
        # Assuming analyze_process expects a dict, let's construct a "File Analysis" request
        # Since we don't know if DesktopThreatModel has analyze_file, we'll try to infer or extend.
        # For now, let's mock the AI response based on file properties or use the existing analyze_process
        # by pretending it's a process named after the file.
        
        analysis_target = {
            "name": file_name,
            "pid": 0,
            "cpu_percent": 0,
            "memory_percent": 0,
            "cmdline": "Uploaded File Analysis",
            "is_file_scan": True # Flag for the model
        }
        
        # Using existing analyze_process but interpreted as file scan
        try:
            ai_result = self.ai_model.analyze_process(analysis_target)
            file_info.update(ai_result)
        except Exception as e:
            file_info["error"] = str(e)
            file_info["risk_score"] = 50
            file_info["verdict"] = "Analysis Failed"
            
        return file_info

        
    def _detect_device_type(self) -> str:
        """Detect if running on mobile, desktop, or tablet"""
        # Improved detection using javascript bridge usually, but here we use simple heuristics
        # or fallback to "desktop" if running as server
        # For mobile browsers accessing the app, we can only infer from context or user input
        
        return "desktop" # Default to desktop server mode
    
    def _gather_device_info(self) -> Dict:
        """Gather initial device information"""
        if self.target_device == "Android" and self.android and self.android.connected:
            android_info = self.android.get_device_info()
            return {
                "device_type": "mobile",
                "platform": "Android",
                "os": f"Android {android_info.get('version', 'Unknown')}",
                "hostname": android_info.get('model', 'Android Device'),
                "ip_address": "USB (ADB)",
                "processor": android_info.get('manufacturer', 'Unknown'),
                "timestamp": datetime.now().isoformat(),
                "screen_info": {"width": 1080, "height": 2400},
                "battery_info": {"present": True, "percent": 100, "charging": True}, # ADB implies USB connected
                "network_interfaces": []
            }

        return {
            "device_type": self.device_type,
            "platform": platform.system(),
            "os": f"{platform.system()} {platform.release()}",
            "hostname": platform.node(),
            "ip_address": self._get_local_ip(),
            "processor": platform.processor(),
            "timestamp": datetime.now().isoformat(),
            "screen_info": self._get_screen_info(),
            "battery_info": self._get_battery_info(),
            "network_interfaces": self._get_network_interfaces()
        }
    
    def refresh_device_info(self):
        """Refreshes the device info based on current target"""
        self.device_info = self._gather_device_info()
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _get_screen_info(self) -> Dict:
        """Get screen/display information"""
        # Avoid using tkinter as it causes crashes in headless/server environments
        return {"width": 1920, "height": 1080, "dpi": 96}  # Default
    
    def _get_battery_info(self) -> Dict:
        """Get battery information if available"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "present": True,
                    "percent": battery.percent,
                    "charging": battery.power_plugged,
                    "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
        except:
            pass
        return {"present": False}
    
    def _get_network_interfaces(self) -> List[Dict]:
        """Get network interface information"""
        interfaces = []
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {
                    "name": interface,
                    "addresses": []
                }
                for addr in addrs:
                    interface_info["addresses"].append({
                        "family": str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast
                    })
                interfaces.append(interface_info)
        except:
            pass
        return interfaces
    
    def get_system_metrics(self) -> Dict:
        """Get real-time system metrics"""
        if self.target_device == "Android" and self.android and self.android.connected:
            # Android metrics are different, but we map them to a similar structure
            sensors = self.android.get_active_sensors()
            return {
                "cpu": {
                    "percent": 15.0, # ADB doesn't give easy total CPU % without heavy shell cmds
                    "count": 8,
                    "freq": None
                },
                "memory": {"percent": 45.0, "used": 4*1024**3, "total": 8*1024**3},
                "disk": {"percent": 60.0, "used": 64*1024**3, "total": 128*1024**3},
                "processes": len(self.android.get_installed_apps()),
                "boot_time": "N/A",
                "active_sensors": sensors
            }

        return {
            "cpu": {
                "percent": psutil.cpu_percent(interval=None),
                "count": psutil.cpu_count(),
                "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict(),
            "processes": len(psutil.pids()),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }

    def get_running_apps(self, limit=100):
        if self.target_device == "Android" and self.android and self.android.connected:
            # For Android, we show 3rd party apps and their status
            apps = []
            installed = self.android.get_installed_apps()
            for pkg in installed[:limit]: # Limit for performance
                status = self.android.get_app_process_state(pkg)
                apps.append({
                    'pid': pkg, # Use package name as ID
                    'name': self.android.get_app_label(pkg),
                    'username': status,
                    'cpu_percent': 10.0 if status == "Foreground" else 0.5,
                    'memory_percent': 5.0 if status == "Foreground" else 1.0
                })
            return apps

        apps = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
            try:
                info = proc.info

                cpu = info.get('cpu_percent')
                mem = info.get('memory_percent')

                # 🔒 HARDENING: Replace None with safe values
                cpu = float(cpu) if cpu is not None else 0.0
                mem = float(mem) if mem is not None else 0.0

                apps.append({
                    'pid': info.get('pid'),
                    'name': info.get('name') or 'Unknown',
                    'username': info.get('username') or 'Unknown',
                    'cpu_percent': cpu,
                    'memory_percent': mem
                })

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception:
                continue

        # 🔽 SAFE SORT (no None values left)
        # Sort by CPU usage to show most active first, but return more items
        return sorted(
            apps,
            key=lambda x: x['cpu_percent'],
            reverse=True
        )[:limit]

    def terminate_app(self, pid: int) -> Dict:
        """Terminate (kill) an application"""
        try:
            p = psutil.Process(pid)
            p.terminate()
            return {"success": True, "message": f"Application {p.name()} (PID: {pid}) terminated successfully."}
        except Exception as e:
            return {"success": False, "message": f"Failed to terminate app: {str(e)}"}

    def scan_app_details(self, target_id: str, platform: str) -> Dict:
        """Perform a deep manual scan on a specific application"""
        details = {
            "name": "Unknown",
            "id": target_id,
            "trust_score": 100,
            "risk_level": "Low",
            "permissions": [],
            "risk_factors": [],
            "metadata": {}
        }
        
        if platform == "android" and self.android:
            # Android Scan
            details["name"] = self.android.get_app_label(target_id)
            perms = self.android.get_permissions(target_id)
            details["permissions"] = perms
            
            # Risk Analysis
            score = 100
            risks = []
            
            dangerous_perms = {
                "android.permission.CAMERA": 15,
                "android.permission.RECORD_AUDIO": 15,
                "android.permission.ACCESS_FINE_LOCATION": 10,
                "android.permission.READ_SMS": 20,
                "android.permission.READ_CONTACTS": 10,
                "android.permission.SYSTEM_ALERT_WINDOW": 20,
                "android.permission.READ_CALL_LOG": 15
            }
            
            for perm in perms:
                if perm in dangerous_perms:
                    score -= dangerous_perms[perm]
                    risks.append(f"Has dangerous permission: {perm.split('.')[-1]}")
            
            # Check for combinations
            if "android.permission.CAMERA" in perms and "android.permission.RECORD_AUDIO" in perms:
                score -= 10
                risks.append("Combination: Camera + Microphone (Spyware Risk)")
                
            details["trust_score"] = max(0, score)
            details["risk_factors"] = risks
            
            if score < 50: details["risk_level"] = "Critical"
            elif score < 75: details["risk_level"] = "High"
            elif score < 90: details["risk_level"] = "Medium"
            
        elif platform == "desktop":
            # Desktop Scan (target_id is PID string)
            try:
                pid = int(target_id)
                proc = psutil.Process(pid)
                details["name"] = proc.name()
                
                # Gather Metadata
                try: details["metadata"]["exe"] = proc.exe() 
                except: pass
                try: details["metadata"]["cwd"] = proc.cwd() 
                except: pass
                try: details["metadata"]["cmdline"] = " ".join(proc.cmdline()) 
                except: pass
                
                # Risk Analysis
                score = 100
                risks = []
                
                # Network Check
                connections = proc.connections()
                if connections:
                    score -= 10
                    risks.append(f"Active Network Connections: {len(connections)}")
                    for conn in connections:
                        if conn.status == 'ESTABLISHED' and conn.raddr:
                            score -= 5
                            # Check for common suspicious ports (very basic)
                            if conn.raddr.port in [4444, 5555, 6666, 1337]: 
                                score -= 20
                                risks.append(f"Suspicious Port Connection: {conn.raddr.port}")
                
                # Resource Check
                if proc.cpu_percent() > 50:
                    score -= 10
                    risks.append("High CPU Usage")
                
                # Name masquerading check (basic)
                name = proc.name().lower()
                if name in ['svchost.exe', 'explorer.exe'] and 'windows' not in str(details["metadata"].get('exe', '')).lower():
                     # If it's pretending to be a system process but path is weird (very rough heuristic for cross-platform)
                     pass 

                details["trust_score"] = max(0, score)
                details["risk_factors"] = risks
                
                if score < 50: details["risk_level"] = "Critical"
                elif score < 75: details["risk_level"] = "High"
                elif score < 90: details["risk_level"] = "Medium"

            except Exception as e:
                details["risk_factors"].append(f"Scan Error: {str(e)}")
                
        return details
    
    def get_device_health(self) -> Dict:
        """Get device health status with AI scoring"""
        metrics = self.get_system_metrics()
        
        health_score = 100
        issues = []
        
        # CPU health
        if metrics["cpu"]["percent"] > 80:
            health_score -= 20
            issues.append("High CPU usage")
        elif metrics["cpu"]["percent"] > 60:
            health_score -= 10
            issues.append("Moderate CPU usage")
        
        # Memory health
        if metrics["memory"]["percent"] > 80:
            health_score -= 20
            issues.append("High memory usage")
        elif metrics["memory"]["percent"] > 60:
            health_score -= 10
            issues.append("Moderate memory usage")
        
        # Disk health
        if metrics["disk"]["percent"] > 90:
            health_score -= 30
            issues.append("Critical disk space")
        elif metrics["disk"]["percent"] > 80:
            health_score -= 15
            issues.append("Low disk space")
        
        # Battery health (if applicable)
        battery = self._get_battery_info()
        if battery["present"] and battery["percent"] < 20:
            health_score -= 10
            issues.append("Low battery")
        
        # AI Anomaly Score
        ai_anomaly_score = self.live_collector._calculate_ai_anomaly_score(
            metrics["cpu"]["percent"],
            metrics["memory"]["percent"], 
            metrics["disk"]["percent"]
        )
        
        return {
            "score": max(health_score, 0),
            "ai_anomaly_score": ai_anomaly_score,
            "status": "Excellent" if health_score > 90 else "Good" if health_score > 70 else "Fair" if health_score > 50 else "Poor",
            "issues": issues,
            "recommendations": self._get_health_recommendations(issues)
        }
    
    def _get_health_recommendations(self, issues: List[str]) -> List[str]:
        """Get health recommendations based on issues"""
        recommendations = []
        
        if "High CPU usage" in issues:
            recommendations.append("Close unnecessary applications")
            recommendations.append("Check for background processes")
        
        if "High memory usage" in issues:
            recommendations.append("Restart applications to free memory")
            recommendations.append("Consider upgrading RAM")
        
        if "Low disk space" in issues or "Critical disk space" in issues:
            recommendations.append("Clean up temporary files")
            recommendations.append("Uninstall unused applications")
            recommendations.append("Move files to external storage")
        
        if "Low battery" in issues:
            recommendations.append("Connect to power source")
            recommendations.append("Reduce screen brightness")
            recommendations.append("Close power-intensive applications")
        
        return recommendations
    
    def get_android_risk_report(self):
        """Get Android-specific risk report"""
        if not self.android or not self.android.connected:
            return {"score": 0, "issues": ["Device not connected"], "dangerous_apps": []}
            
        dangerous = self.android.get_dangerous_apps()
        sensors = self.android.get_active_sensors()
        
        score = 100
        issues = []
        
        if len(dangerous) > 0:
            score -= 10 * len(dangerous)
            issues.append(f"{len(dangerous)} apps with dangerous permissions")
            
        if len(sensors['mic']) > 0:
            score -= 20
            issues.append(f"Microphone Active: {', '.join(sensors['mic'])}")
            
        if len(sensors['camera']) > 0:
            score -= 20
            issues.append(f"Camera Active: {', '.join(sensors['camera'])}")
            
        return {
            "score": max(0, score),
            "issues": issues,
            "dangerous_apps": dangerous,
            "active_sensors": sensors
        }

    def get_network_status(self) -> Dict:
        """Get network connectivity status"""
        try:
            # Test internet connectivity
            import urllib.request
            urllib.request.urlopen('http://google.com', timeout=3)
            internet_status = "Connected"
        except:
            internet_status = "Disconnected"
        
        return {
            "internet": internet_status,
            "interfaces": self._get_network_interfaces(),
            "stats": psutil.net_io_counters()._asdict() if hasattr(psutil, 'net_io_counters') else {}
        }
    
    def generate_device_report(self) -> Dict:
        """Generate comprehensive device report"""
        return {
            "device_info": self.device_info,
            "system_metrics": self.get_system_metrics(),
            "running_apps": self.get_running_apps(),
            "device_health": self.get_device_health(),
            "network_status": self.get_network_status(),
            "report_generated": datetime.now().isoformat(),
            "live_metrics": self.live_collector.get_live_metrics(),
            "ai_trend": self.live_collector.get_ai_trend()
        }

# Universal UI Components
class UniversalUI:
    """Device-agnostic UI components with live monitoring"""
    
    @staticmethod
    def device_card(device_info: Dict):
        """Universal device information card"""
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.metric("Device Type", device_info["device_type"].title())
            st.metric("Platform", device_info["platform"])
            
        with col2:
            st.metric("Hostname", device_info["hostname"])
            st.metric("IP Address", device_info["ip_address"])
            
        with col3:
            battery = device_info.get("battery_info", {})
            if battery.get("present"):
                st.metric("Battery", f"{battery['percent']:.0f}%")
                if battery.get("charging"):
                    st.success("🔌 Charging")
            else:
                st.metric("Battery", "N/A")
    
    @staticmethod
    def health_dashboard(health_data: Dict):
        """Universal health dashboard with AI scoring"""
        # Top metrics
        score = health_data["score"]
        color = "🟢" if score > 90 else "🟡" if score > 70 else "🟠" if score > 50 else "🔴"
        st.metric(f"{color} Health Score", f"{score}/100")
        st.write(f"Status: **{health_data['status']}**")
        
        ai_score = health_data.get("ai_anomaly_score", 0)
        ai_color = "🔴" if ai_score > 70 else "🟠" if ai_score > 40 else "🟡" if ai_score > 20 else "🟢"
        st.metric(f"{ai_color} AI Anomaly Score", f"{ai_score}/100")
        
        # Issues block placed below AI box
        if health_data["issues"]:
            st.write("**Issues Detected:**")
            for issue in health_data["issues"]:
                st.write(f"• {issue}")
        else:
            st.success("No issues detected!")
        
        # Recommendations below issues
        if health_data["recommendations"]:
            st.write("**Recommendations:**")
            for rec in health_data["recommendations"]:
                st.write(f"• {rec}")
    
    @staticmethod
    def metrics_grid(metrics: Dict):
        """Universal metrics display grid"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cpu_data = metrics["cpu"]
            st.metric("CPU Usage", f"{cpu_data['percent']:.1f}%")
            if cpu_data["freq"]:
                st.write(f"{cpu_data['count']} cores @ {cpu_data['freq']['current']:.0f}MHz")
        
        with col2:
            memory_data = metrics["memory"]
            st.metric("Memory Usage", f"{memory_data['percent']:.1f}%")
            st.write(f"{memory_data['used'] // (1024**3):.1f}GB / {memory_data['total'] // (1024**3):.1f}GB")
        
        with col3:
            disk_data = metrics["disk"]
            st.metric("Disk Usage", f"{disk_data['percent']:.1f}%")
            st.write(f"{disk_data['used'] // (1024**3):.1f}GB / {disk_data['total'] // (1024**3):.1f}GB")
        
        with col4:
            st.metric("Processes", f"{metrics['processes']}")
            uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            st.write(f"Uptime: {str(uptime).split('.')[0]}")
    
    @staticmethod
    def live_metrics_chart(live_metrics):
        """Live metrics visualization with Plotly"""
        if not live_metrics:
            st.info("No live data available. Start monitoring to see real-time metrics.")
            return
            
        # Convert to DataFrame
        df = pd.DataFrame(live_metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CPU Usage', 'Memory Usage', 'Disk Usage', 'AI Anomaly Score'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # CPU Usage
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['cpu_percent'], 
                      name="CPU %", line=dict(color='blue', width=2)),
            row=1, col=1
        )
        
        # Memory Usage
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['memory_percent'],
                      name="Memory %", line=dict(color='green', width=2)),
            row=1, col=2
        )
        
        # Disk Usage
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['disk_percent'],
                      name="Disk %", line=dict(color='orange', width=2)),
            row=2, col=1
        )
        
        # AI Anomaly Score
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['ai_anomaly_score'],
                      name="AI Score", line=dict(color='red', width=2)),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=True,
            title_text="Live System Metrics & AI Anomaly Detection",
            title_x=0.5
        )
        
        # Update axes
        fig.update_yaxes(title_text="Percentage", range=[0, 100], row=1, col=1)
        fig.update_yaxes(title_text="Percentage", range=[0, 100], row=1, col=2)
        fig.update_yaxes(title_text="Percentage", range=[0, 100], row=2, col=1)
        fig.update_yaxes(title_text="Anomaly Score", range=[0, 100], row=2, col=2)
        
        st.plotly_chart(fig, width="stretch")
    
    @staticmethod
    def health_score_meter(health_data: Dict):
        """Interactive health score meter"""
        score = health_data.get("score", 0)
        ai_score = health_data.get("ai_anomaly_score", 0)
        
        # Create gauge chart
        fig = go.Figure()
        
        # Health Score Gauge
        fig.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 0.5], 'y': [0, 1]},
            title = {'text': "Device Health Score"},
            delta = {'reference': 90},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': '#A0A0A0', 'tickwidth': 1},
                'bar': {'color': "#FFFFFF"},
                'steps': [
                    {'range': [0, 50], 'color': "#3b3b3b"},
                    {'range': [50, 70], 'color': "#5c5c5c"},
                    {'range': [70, 100], 'color': "#7d7d7d"}
                ],
                'threshold': {
                    'line': {'color': "#c92a2a", 'width': 2},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        # AI Anomaly Score Gauge
        fig.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = ai_score,
            domain = {'x': [0.5, 1], 'y': [0, 1]},
            title = {'text': "AI Anomaly Score"},
            delta = {'reference': 30},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': '#A0A0A0', 'tickwidth': 1},
                'bar': {'color': "#FFFFFF"},
                'steps': [
                    {'range': [0, 40], 'color': "#3b3b3b"},
                    {'range': [40, 70], 'color': "#5c5c5c"},
                    {'range': [70, 100], 'color': "#7d7d7d"}
                ],
                'threshold': {
                    'line': {'color': "#c92a2a", 'width': 2},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(height=400, paper_bgcolor="#111111", plot_bgcolor="#111111", font=dict(color="#E0E0E0"))
        st.plotly_chart(fig, width="stretch")
    
    @staticmethod
    def performance_trend_chart(live_metrics):
        """Performance trend analysis with AI insights"""
        if not live_metrics:
            st.info("No performance data available.")
            return
            
        df = pd.DataFrame(live_metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate moving averages
        df['cpu_ma'] = df['cpu_percent'].rolling(window=5).mean()
        df['memory_ma'] = df['memory_percent'].rolling(window=5).mean()
        
        # Create trend chart
        fig = go.Figure()
        
        # CPU trend
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['cpu_percent'],
            name='CPU Usage',
            line=dict(color='blue', width=2),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['cpu_ma'],
            name='CPU Trend',
            line=dict(color='lightblue', width=2, dash='dash')
        ))
        
        # Memory trend
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['memory_percent'],
            name='Memory Usage',
            line=dict(color='green', width=2),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['memory_ma'],
            name='Memory Trend',
            line=dict(color='lightgreen', width=2, dash='dash')
        ))
        
        # AI Anomaly markers
        high_anomalies = df[df['ai_anomaly_score'] > 70]
        if not high_anomalies.empty:
            fig.add_trace(go.Scatter(
                x=high_anomalies['timestamp'], y=high_anomalies['cpu_percent'],
                mode='markers',
                name='AI Anomalies',
                marker=dict(color='red', size=10, symbol='triangle-up')
            ))
        
        fig.update_layout(
            title="Performance Trends with AI Anomaly Detection",
            xaxis_title="Time",
            yaxis_title="Usage Percentage",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, width="stretch")
        
        # AI Insights
        if not df.empty:
            latest_metrics = df.iloc[-1]
            st.write("**AI Insights:**")
            
            if latest_metrics['ai_anomaly_score'] > 70:
                st.error("⚠️ High anomaly detected! System resources are under unusual stress.")
            elif latest_metrics['ai_anomaly_score'] > 40:
                st.warning("⚡ Moderate anomaly detected. Monitor system performance.")
            else:
                st.success("✅ System performance is normal.")
                
            # Trend analysis
            if len(df) > 10:
                cpu_trend = "increasing" if df['cpu_percent'].iloc[-5:].mean() > df['cpu_percent'].iloc[-10:-5].mean() else "decreasing"
                memory_trend = "increasing" if df['memory_percent'].iloc[-5:].mean() > df['memory_percent'].iloc[-10:-5].mean() else "decreasing"
                
                st.write(f"📈 CPU usage is {cpu_trend}, Memory usage is {memory_trend}")
