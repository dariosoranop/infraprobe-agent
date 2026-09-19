import os
from datetime import datetime

def save_report(provider: str, target_id: str, analysis_content: str):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/governance_compliance_audit_{provider}_{target_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Multi-Cloud Governance & Regulatory Compliance Audit Report\n")
        f.write(f"**Provider:** `{provider.upper()}` | **Scope:** `{target_id}`\n")
        f.write(f"**Standards Covered:** ISO 27001:2022 | DORA | PCI-DSS | CIS Benchmarks | Rev 6\n\n---\n\n")
        f.write(analysis_content)
    print(f"\n[+] Compliance Report saved to: {filename}")