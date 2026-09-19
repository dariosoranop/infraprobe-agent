import argparse
from rich.console import Console
from rich.panel import Panel
from modules.multi_cloud_scanner import run_cloud_policy_audit
from modules.debt_analyzer import analyze_policy_and_infrastructure
from modules.reporter import save_report

console = Console()

def main():
    parser = argparse.ArgumentParser(description="InfraProbe-Agent: Governance & Regulatory Compliance Auditor")
    parser.add_argument("--provider", required=True, choices=["azure", "aws", "gcp"])
    parser.add_argument("--target-id", required=True)
    args = parser.parse_args()

    console.print(Panel(f"[bold cyan]Starting Regulatory Compliance Audit for {args.provider.upper()}[/bold cyan] | Target: {args.target_id}"))

    console.print("[yellow][*] Scanning Policy Initiatives & Resource State...[/yellow]")
    audit_data = run_cloud_policy_audit(args.provider, args.target_id)
    
    console.print("[yellow][*] Running Local AI Governance & Compliance Analysis...[/yellow]")
    analysis = analyze_policy_and_infrastructure(audit_data)
    
    save_report(args.provider, args.target_id, analysis)
    console.print(Panel("[bold green]Compliance audit workflow successfully completed.[/bold green]"))

if __name__ == "__main__":
    main()