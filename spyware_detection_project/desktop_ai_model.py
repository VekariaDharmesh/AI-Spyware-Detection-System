import os
import json
import warnings
import re

class DesktopThreatModel:
    def __init__(self, api_key: str | None = None, model_path: str | None = None):
        """Desktop threat model wrapper.
        - Uses local heuristic analysis instead of remote API.
        - Backwards compatible with existing init signature.
        """
        self.is_configured = True # Always true now as we use local logic
        self.model_path = model_path or "model.pkl"
        
        # Known Suspicious Keywords
        self.suspicious_keywords = [
            "keylog", "spy", "stealer", "rat", "trojan", "miner", "hack", "crack", 
            "powershell -w hidden", "nc -e", "metasploit", "cobalt", "empire",
            "xmrig", "blackcat", "mimikatz"
        ]
        
        # High Risk System Processes (if running from unexpected locations or user)
        self.system_impersonators = [
            "svchost.exe", "explorer.exe", "winlogon.exe", "lsass.exe", "csrss.exe"
        ]

    def analyze_process(self, process_info):
        """
        Analyze a process using Local Heuristic AI.
        process_info: dict containing name, pid, cpu, memory, etc.
        """
        score = 0
        reasons = []
        is_threat = False
        
        name = process_info.get('name', 'Unknown').lower()
        cmdline = process_info.get('cmdline', '').lower()
        cpu = process_info.get('cpu_percent', 0)
        mem = process_info.get('memory_percent', 0)
        
        # 1. Keyword Analysis
        for kw in self.suspicious_keywords:
            if kw in name or kw in cmdline:
                score += 50
                reasons.append(f"Suspicious keyword '{kw}' detected")
                is_threat = True

        # 2. Resource Anomaly
        if cpu > 80:
            score += 20
            reasons.append("Abnormal high CPU usage")
        if mem > 80:
            score += 15
            reasons.append("Abnormal high Memory usage")
            
        # 3. System Impersonation Check (Simple)
        # If it's a python script pretending to be system, etc.
        if any(imp in name for imp in self.system_impersonators):
            # In a real scenario we'd check path, but here we just check if it's not the actual system process
            # For this simplified model, we flag if it has high resource usage while being a system process
            if cpu > 50:
                score += 30
                reasons.append(f"System process '{name}' showing high activity")

        # 4. Network Activity (Inferred from connections if passed, or just cmdline)
        if "nc " in cmdline or "netcat" in cmdline or "socket" in cmdline:
             score += 40
             reasons.append("Potential reverse shell command")

        # Cap score
        score = min(score, 100)
        
        # Determine Level
        if score > 75: level = "Critical"
        elif score > 50: level = "High"
        elif score > 20: level = "Medium"
        else: level = "Low"
        
        if not reasons:
            reasons.append("Normal behavior")

        return {
            "risk_score": score,
            "risk_level": level,
            "reason": "; ".join(reasons),
            "is_threat": is_threat or score > 70
        }

    # Legacy methods for compatibility
    def train_model(self, save_path=None):
        path = save_path or self.model_path or "model.pkl"
        try:
            with open(path, "w") as f:
                f.write("local-heuristic-model")
        except Exception:
            pass
        return path

    def predict(self, features):
        try:
            cpu, mem, open_files, net_conns, is_root, suspicious_name = features
        except Exception:
            return 0.5
        risk = 0.0
        risk += max(0.0, min(cpu / 100.0, 1.0)) * 0.3
        risk += max(0.0, min(mem / 100.0, 1.0)) * 0.2
        risk += max(0.0, min(open_files / 50.0, 1.0)) * 0.1
        risk += max(0.0, min(net_conns / 20.0, 1.0)) * 0.2
        risk += (0.1 if is_root else 0.0)
        risk += (0.3 if suspicious_name else 0.0)
        return max(0.0, min(risk, 1.0))
