import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b-instruct")

def analyze_policy_and_infrastructure(audit_results: dict) -> str:
    prompt = f"""
You are a Principal Cloud Governance Architect and Enterprise Security Lead specialized in banking compliance frameworks (ISO/IEC 27001:2022, DORA, PCI-DSS, CIS Benchmarks, and Rev 6 Security Baselines).
Analyze the following multi-cloud inventory and policy initiatives data:

{json.dumps(audit_results, indent=2)}

Your absolute directives:
1. **Policy Initiatives Review (First):** Analyze how policy initiatives/sets are implemented or missing. If custom or weak initiatives are detected, explain the security gaps referencing specific compliance standards (ISO 27001, DORA, PCI, CIS, Rev 6). If initiatives are totally missing, design a proper multi-tier structure (Tenant Root -> Management Groups -> Subscriptions) following best practices.
2. **Resource & Technical Debt Analysis (Second):** Evaluate how resources align or drift from those policies and regulatory frameworks.
3. **Actionable Remediation Code:** Provide exact production-ready remediation code (e.g., Azure Policy definitions, Terraform modules, or compliance guardrails) mapped to regulatory requirements.

Write the output strictly in English, highly technical and rigorous.
"""
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    try:
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=120)
        return response.json().get("response", "Error") if response.status_code == 200 else f"Ollama Error: {response.text}"
    except Exception as e:
        return f"Connection error: {str(e)}"