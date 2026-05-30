import subprocess
import re
import time
import os

class AndroidMonitor:
    def __init__(self):
        self.device_id = None
        self.connected = False
        self.permission_cache = {} # Cache for permissions to speed up loops
        # Common Package to Name Mapping
        self.app_labels = {
            "com.whatsapp": "WhatsApp",
            "com.instagram.android": "Instagram",
            "com.facebook.katana": "Facebook",
            "com.snapchat.android": "Snapchat",
            "com.google.android.youtube": "YouTube",
            "com.google.android.gm": "Gmail",
            "com.android.chrome": "Chrome",
            "com.android.camera": "Camera",
            "com.sec.android.app.camera": "Camera (Samsung)",
            "com.google.android.GoogleCamera": "Pixel Camera",
            "com.apple.camera": "Camera (iOS-like)",
            "org.telegram.messenger": "Telegram",
            "com.twitter.android": "X (Twitter)",
            "com.zhiliaoapp.musically": "TikTok",
            "com.linkedin.android": "LinkedIn",
            "com.google.android.apps.maps": "Google Maps",
            "com.spotify.music": "Spotify",
            "com.netflix.mediaclient": "Netflix",
            "com.openai.chatgpt": "ChatGPT",
            "com.amazon.mShop.android.shopping": "Amazon Shopping"
        }
        self.check_connection()

    def run_adb_command(self, command, timeout=10):
        """Run an ADB command and return the output."""
        try:
            full_cmd = f"adb {command}"
            if self.device_id:
                full_cmd = f"adb -s {self.device_id} {command}"
            
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"ADB Command Failed: {e}")
            return None

    def run_adb_raw(self, command, timeout=10):
        """Run ADB without binding to a specific device."""
        try:
            full_cmd = f"adb {command}"
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"ADB Raw Command Failed: {e}")
            return None

    def check_connection(self):
        """Check if an Android device is connected."""
        devices = self.run_adb_command("devices")
        if devices:
            lines = devices.split('\n')
            # Handle potential daemon start messages by finding the "List of devices" line
            start_index = 0
            for i, line in enumerate(lines):
                if "List of devices attached" in line:
                    start_index = i + 1
                    break
            
            for line in lines[start_index:]:
                if "\tdevice" in line:
                    self.device_id = line.split('\t')[0]
                    self.connected = True
                    return True
        
        self.connected = False
        # Do not clear device_id immediately to allow re-connection attempts to same device if needed,
        # but since we use run_adb_raw now, it doesn't matter.
        return False

    def connect_wireless(self, ip, port="5555"):
        result = self.run_adb_raw(f"connect {ip}:{port}")
        if result and ("connected to" in result or "already connected" in result):
            self.check_connection()
            return True, result
        return False, result

    def pair_wireless(self, host, port, code):
        result = self.run_adb_raw(f"pair {host}:{port} {code}")
        if result and ("Successfully paired" in result or "Paired devices:" in result):
            return True, result
        return False, result

    def get_device_info(self):
        if not self.connected: return {"model": "Unknown", "manufacturer": "Unknown", "version": "Unknown"}
        model = self.run_adb_command("shell getprop ro.product.model")
        manufacturer = self.run_adb_command("shell getprop ro.product.manufacturer")
        version = self.run_adb_command("shell getprop ro.build.version.release")
        return {
            "model": model or "Unknown",
            "manufacturer": manufacturer or "Unknown",
            "version": version or "Unknown"
        }

    def get_app_label(self, package_name):
        """Returns a human-readable name for the package."""
        if not package_name: return "Unknown"
          
        # 1. Check dictionary
        if package_name in self.app_labels:
            return self.app_labels[package_name]
        
        # 2. Try simple formatting
        parts = package_name.split('.')
        if len(parts) >= 2:
            # e.g. com.camerasides.insashot -> Insashot
            return parts[-1].capitalize()
            
        return package_name

    def get_installed_apps(self, show_system=False):
        if not self.connected: return []
        
        cmd = "shell pm list packages -3" # 3rd party only by default
        if show_system:
            cmd = "shell pm list packages"
            
        output = self.run_adb_command(cmd)
        if not output: return []
        
        apps = []
        lines = output.split('\n')
        for line in lines:
            if line.startswith('package:'):
                pkg = line.replace('package:', '').strip()
                apps.append(pkg)
        return apps

    def get_permissions(self, package_name):
        if not self.connected: return []
        
        # Check cache first
        if package_name in self.permission_cache:
            return self.permission_cache[package_name]

        output = self.run_adb_command(f"shell dumpsys package {package_name}")
        if not output: return []
        
        perms = []
        # Parse requested permissions
        parsing_perms = False
        for line in output.split('\n'):
            line = line.strip()
            if "requested permissions:" in line.lower():
                parsing_perms = True
                continue
            if parsing_perms:
                if line.endswith(":") or line == "":
                    parsing_perms = False
                else:
                    perm = line.split(":")[0].strip()
                    if perm.startswith("android.permission."):
                        perms.append(perm)
        
        result = list(set(perms))
        self.permission_cache[package_name] = result # Cache it
        return result

    def get_app_process_state(self, package_name):
        """Checks if app is Foreground, Background, or Cached/Stopped."""
        if not self.connected: return "Unknown"
        
        # Check procstats or activity for process state
        # A simple check: `pidof`
        pid_out = self.run_adb_command(f"shell pidof {package_name}")
        if not pid_out:
            return "Stopped/Cached"
            
        # If PID exists, check if it's top activity
        activity_out = self.run_adb_command("shell dumpsys activity activities")
        if activity_out and f"mResumedActivity: ActivityRecord{{{{.* {package_name}/" in activity_out: # Simplified regex match logic
             # Better check using simple string containment for speed
             if f"{package_name}/" in activity_out and "mResumedActivity" in activity_out:
                 return "Foreground"
        
        return "Background"

    def get_active_sensors(self):
        """
        Detects active usage of Microphone, Camera, and GPS using optimized batch command.
        """
        if not self.connected: return {"mic": [], "camera": [], "gps": []}
        
        active = {"mic": [], "camera": [], "gps": []}
        
        # OPTIMIZATION: Combine multiple dumpsys commands into one adb shell call
        # Separator: "___DIV___"
        cmd = 'shell "dumpsys activity activities; echo ___DIV___; dumpsys audio; echo ___DIV___; dumpsys media.camera; echo ___DIV___; dumpsys location"'
        combined_output = self.run_adb_command(cmd, timeout=20)
        
        if not combined_output: return active
        
        parts = combined_output.split("___DIV___")
        if len(parts) < 4: return active
        
        activity_out = parts[0]
        audio_out = parts[1]
        camera_out = parts[2]
        loc_out = parts[3]
        
        # --- 1. Identify Foreground App ---
        fg_app = None
        fg_pid = None
        # Improved regex to capture package and potential PID/Process info if available nearby (simplified for now)
        match = re.search(r"mResumedActivity: ActivityRecord\{[^ ]+ [^ ]+ ([a-zA-Z0-9._]+)/", activity_out)
        if match:
            fg_app = match.group(1)
        
        # --- 2. Microphone Detection ---
        matches = re.findall(r"source:[^ ]+ package:([a-zA-Z0-9._]+)", audio_out)
        active["mic"].extend(matches)
        matches2 = re.findall(r"client:.*name=([a-zA-Z0-9._]+)", audio_out)
        active["mic"].extend(matches2)
        matches3 = re.findall(r"(?i)AudioRecord[^\\n]*package:([a-zA-Z0-9._]+)", audio_out)
        active["mic"].extend(matches3)
        matches4 = re.findall(r"(?i)AudioRecordClient.*package:([a-zA-Z0-9._]+)", audio_out)
        active["mic"].extend(matches4)

        # Check AppOps for Foreground App (Mic + Camera + Location)
        if fg_app:
            # We also get the PID here to help with Camera detection fallback
            ops_cmd = f'shell "pidof {fg_app}; echo ___OPS_DIV___; appops get {fg_app} RECORD_AUDIO; echo ___OPS_DIV___; appops get {fg_app} CAMERA; echo ___OPS_DIV___; appops get {fg_app} FINE_LOCATION; echo ___OPS_DIV___; appops get {fg_app} COARSE_LOCATION"'
            ops_out_full = self.run_adb_command(ops_cmd)
            
            if ops_out_full:
                ops_parts = ops_out_full.split("___OPS_DIV___")
                if len(ops_parts) >= 5:
                    pid_out = ops_parts[0].strip()
                    mic_ops = ops_parts[1]
                    cam_ops = ops_parts[2]
                    loc_ops = ops_parts[3]
                    coarse_loc_ops = ops_parts[4]
                    
                    if pid_out.replace(' ', '').isdigit():
                        # Take the first PID if multiple
                        fg_pid = pid_out.split()[0]
                    
                    # Mic AppOps Check
                    if "running" in mic_ops.lower():
                        active["mic"].append(fg_app)
                        
                    # Camera AppOps Check
                    if "running" in cam_ops.lower():
                        active["camera"].append(fg_app)
                        
                    # Location AppOps Check
                    if "running" in loc_ops.lower() or "running" in coarse_loc_ops.lower():
                        active["gps"].append(fg_app)

        # Broader AppOps scan for RECORD_AUDIO and LOCATION across apps
        appops_out = self.run_adb_command("shell dumpsys appops")
        if appops_out:
            for line in appops_out.splitlines():
                if "RECORD_AUDIO" in line or "FINE_LOCATION" in line or "COARSE_LOCATION" in line or "MONITOR_LOCATION" in line:
                    ll = line.lower()
                    if ("running" in ll) or ("isrunning" in ll):
                        pkg = None
                        m = re.search(r"pkg=([a-zA-Z0-9._-]+)", line)
                        if m:
                            pkg = m.group(1)
                        else:
                            m2 = re.search(r"package[:=]?\\s*([a-zA-Z0-9._-]+)", line)
                            if m2:
                                pkg = m2.group(1)
                        if pkg:
                            if "RECORD_AUDIO" in line:
                                active["mic"].append(pkg)
                            if "FINE_LOCATION" in line or "COARSE_LOCATION" in line or "MONITOR_LOCATION" in line:
                                active["gps"].append(pkg)
        installed = self.get_installed_apps()
        for pkg in installed[:50]:
            mic_ops = self.run_adb_command(f"shell appops get {pkg} RECORD_AUDIO")
            if mic_ops and ("running" in mic_ops.lower() or "isRunning" in mic_ops):
                active["mic"].append(pkg)

        # --- 3. Camera Detection (Enhanced) ---
        # 1. Regex for "Client name: com.package"
        matches = re.findall(r"Client name: ([a-zA-Z0-9._]+)", camera_out)
        active["camera"].extend(matches)
        
        # 2. Regex for "Client Package Name: com.package"
        matches2 = re.findall(r"Client Package Name: ([a-zA-Z0-9._]+)", camera_out)
        active["camera"].extend(matches2)

        # 3. Regex for "Client: com.package (PID)"
        matches3 = re.findall(r"Client: ([a-zA-Z0-9._]+) \(PID", camera_out)
        active["camera"].extend(matches3)

        # Check by PID if we have the FG PID
        if fg_pid and fg_pid in camera_out:
             active["camera"].append(fg_app)
        
        # Check if FG App Package Name is present in Camera Dump (strong heuristic for active usage)
        if fg_app and fg_app in camera_out:
             # Ensure it's not just in "History" (if possible, but simplified for now)
             # Usually active clients are listed first or in a separate section.
             # To be safe, we add it. False positives are better than False negatives for spyware detection.
             active["camera"].append(fg_app)



        # --- 4. GPS Detection ---
        # Refined regex for active listeners in dumpsys location
        # Typical format: "Receiver[... Package: com.example ...]"
        # or "Location Request... from com.example"
        
        # 1. Active Listeners (strong signal)
        matches = re.findall(r"Receiver\[.*?Package: ([a-zA-Z0-9._]+)", loc_out)
        active["gps"].extend(matches)
        
        # 2. Location Requests (strong signal if recent)
        matches2 = re.findall(r"Location Request.*?from ([a-zA-Z0-9._]+)", loc_out)
        active["gps"].extend(matches2)
        
        # 3. Fallback: simple Package match if not already covered, but be careful
        # Only if we found nothing else, to avoid historical noise
        if not active["gps"]:
             matches3 = re.findall(r"Package: ([a-zA-Z0-9._]+)", loc_out)
             # Filter matches3 to avoid excessively old history if possible
             # For now, we take them but this is the "broad" check
             active["gps"].extend(matches3)

        # Deduplicate
        active["mic"] = list(set(active["mic"]))
        active["camera"] = list(set(active["camera"]))
        active["gps"] = list(set(active["gps"]))
        
        return active

    def stop_app(self, package_name):
        """Force stops an app (Kill)."""
        if not self.connected: return False
        self.run_adb_command(f"shell am force-stop {package_name}")
        return True

    def quarantine_app(self, package_name):
        """Disables the app (Quarantine)."""
        if not self.connected: return False
        # pm disable-user --user 0 <pkg>
        res = self.run_adb_command(f"shell pm disable-user --user 0 {package_name}")
        return res is not None
    
    def get_app_open_ports(self, package_name, limit=200):
        """Scan open/active ports used by a specific app via its PID."""
        if not self.connected or not package_name: return []
        pid_out = self.run_adb_command(f"shell pidof {package_name}")
        if not pid_out: return []
        pid = pid_out.strip().split()[0]
        results = []
        protos = ["tcp", "udp", "tcp6", "udp6"]
        
        def parse_hex_port(h):
            try:
                return int(h, 16)
            except Exception:
                return None
        
        for proto in protos:
            out = self.run_adb_command(f"shell cat /proc/{pid}/net/{proto}")
            if not out: 
                continue
            lines = out.splitlines()
            if len(lines) <= 1: 
                continue
            for line in lines[1:]:
                parts = line.split()
                if len(parts) < 4:
                    continue
                local = parts[1]
                remote = parts[2]
                state = parts[3]  # hex state code, e.g. 0A for LISTEN
                try:
                    lport_hex = local.split(":")[1]
                    rport_hex = remote.split(":")[1]
                except Exception:
                    continue
                lp = parse_hex_port(lport_hex)
                rp = parse_hex_port(rport_hex)
                results.append({
                    "proto": proto,
                    "local_port": lp,
                    "remote_port": rp,
                    "state": state
                })
                if len(results) >= limit:
                    break
        # Deduplicate by proto+local_port+remote_port
        seen = set()
        unique = []
        for r in results:
            key = (r["proto"], r["local_port"], r["remote_port"], r["state"])
            if key in seen:
                continue
            seen.add(key)
            unique.append(r)
        return unique

    def get_dangerous_apps(self, limit=15):
        """Scans for apps with dangerous permission combinations."""
        if not self.connected: return []
        
        installed = self.get_installed_apps(show_system=False)
        # Limit to first N apps to prevent UI freezing
        installed = installed[:limit]
        
        dangerous_apps = []
        
        for app in installed:
            perms = self.get_permissions(app)
            risk_factors = []
            
            has_cam = "android.permission.CAMERA" in perms
            has_mic = "android.permission.RECORD_AUDIO" in perms
            has_loc = "android.permission.ACCESS_FINE_LOCATION" in perms
            has_overlay = "android.permission.SYSTEM_ALERT_WINDOW" in perms
            has_sms = "android.permission.READ_SMS" in perms
            has_contacts = "android.permission.READ_CONTACTS" in perms
            
            if has_cam and has_mic:
                risk_factors.append("Cam + Mic")
            if has_overlay and (has_sms or has_contacts):
                risk_factors.append("Overlay + Data Access")
            if has_loc and has_mic:
                risk_factors.append("Tracking + Eavesdropping")
                
            if risk_factors:
                dangerous_apps.append({
                    "package": app,
                    "label": self.get_app_label(app),
                    "risk_factors": risk_factors,
                    "permissions": perms
                })
                
        return dangerous_apps

    def get_exfiltration_insights(self, package_name):
        """Heuristic analysis for data collection/sending conditions and timing."""
        if not self.connected or not package_name:
            return {
                "is_collecting": False,
                "is_sending": False,
                "conditions": [],
                "when_next": "Unknown"
            }
        conditions = []
        try:
            perms = set(self.get_permissions(package_name))
        except Exception:
            perms = set()
        collecting_perms = {"android.permission.RECORD_AUDIO", "android.permission.CAMERA",
                            "android.permission.ACCESS_FINE_LOCATION", "android.permission.READ_CONTACTS",
                            "android.permission.READ_SMS"}
        is_collecting = len(perms.intersection(collecting_perms)) > 0
        try:
            net_active = self.is_app_network_active(package_name)
        except Exception:
            net_active = None
        is_sending = bool(net_active)
        # Detect device conditions
        try:
            power_out = self.run_adb_command("shell dumpsys power")
            if power_out and ("state=OFF" in power_out or "Display Power: state=OFF" in power_out):
                conditions.append("screen_off")
        except Exception:
            pass
        try:
            batt_out = self.run_adb_command("shell dumpsys battery")
            if batt_out:
                if "AC powered: true" in batt_out or "USB powered: true" in batt_out or "Wireless powered: true" in batt_out:
                    conditions.append("charging")
        except Exception:
            pass
        try:
            conn_out = self.run_adb_command("shell dumpsys connectivity")
            if conn_out:
                if "WIFI" in conn_out or "wifi" in conn_out:
                    conditions.append("wifi")
                if "MOBILE" in conn_out or "cellular" in conn_out or "mobile" in conn_out:
                    conditions.append("mobile_data")
        except Exception:
            pass
        # Jobs/alarms to guess next send window
        when_next = "Unknown"
        try:
            jobs_out = self.run_adb_command("shell dumpsys jobscheduler")
            if jobs_out and package_name in jobs_out:
                # Simple heuristic: look for 'next run' or 'interval'
                m = re.search(r"next run in (\d+)s", jobs_out)
                if m:
                    when_next = f"In {m.group(1)} seconds (scheduled job)"
                else:
                    m2 = re.search(r"interval=(\d+)ms", jobs_out)
                    if m2:
                        when_next = f"Repeats every {int(m2.group(1))//1000}s (scheduled job)"
        except Exception:
            pass
        if when_next == "Unknown":
            try:
                alarm_out = self.run_adb_command("shell dumpsys alarm")
                if alarm_out and package_name in alarm_out:
                    if "RTC" in alarm_out or "ELAPSED" in alarm_out:
                        when_next = "Has pending alarms (timed send likely)"
            except Exception:
                pass
        return {
            "is_collecting": is_collecting,
            "is_sending": is_sending,
            "conditions": conditions,
            "when_next": when_next
        }

    def get_battery_status(self):
        """Return Android device battery percent and charging state using dumpsys battery."""
        if not self.connected:
            return None
        try:
            out = self.run_adb_command("shell dumpsys battery")
            if not out:
                return None
            percent = None
            scale = 100
            charging = False
            for line in out.splitlines():
                line = line.strip()
                if line.startswith("level:"):
                    try:
                        percent = int(line.split(":")[1].strip())
                    except:
                        pass
                elif line.startswith("scale:"):
                    try:
                        scale = int(line.split(":")[1].strip())
                    except:
                        pass
                elif "AC powered:" in line or "USB powered:" in line or "Wireless powered:" in line:
                    if "true" in line.lower():
                        charging = True
            if percent is None:
                # Fallback parse using regex
                m = re.search(r"level:\s*(\d+)", out)
                if m:
                    percent = int(m.group(1))
            # Normalize percent by scale if available
            if percent is not None and scale and scale != 100:
                try:
                    percent = int((percent / scale) * 100)
                except:
                    pass
            if percent is None:
                return None
            return {"percent": max(0, min(100, percent)), "charging": charging}
        except Exception:
            return None
