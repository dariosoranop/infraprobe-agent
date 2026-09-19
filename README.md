# infraprobe-agent

InfraProbe-Agent is a production-grade, highly hardened multi-cloud security, compliance, and governance auditor engineered explicitly for financial institutions and enterprise banking environments.

It bridges the gap between cloud infrastructure and regulatory compliance, performing deep multi-cloud scans aligned with ISO/IEC 27001:2022, DORA (Digital Operational Resilience Act), PCI-DSS, CIS Benchmarks, and Rev 6 Security Baselines.


# Why Banks Need Cloud Policy Compliance Auditing

Moving workloads to cloud platforms (Microsoft Azure, AWS, or Google Cloud) does not transfer regulatory accountability. Under the Shared Responsibility Model, financial institutions remain entirely liable for data security, configuration drift, and continuous compliance.

Furthermore, banks never apply cloud configurations as a monolithic standard. Internal Security & Governance teams define custom Policy Initiatives (grouped compliance rules), selectively enabling, overriding, or disabling controls based on risk appetite.

Core Intelligence Workflow
InfraProbe-Agent follows a strict hierarchical governance workflow to evaluate and remediate infrastructure:

Policy Initiatives & Governance Review (First): Inspects how policy initiatives, security frameworks, and guardrails are implemented across the tenant or account. It detects overrides, disabled controls, and compliance gaps.

Enterprise Hierarchy Blueprinting (Fallback): If proper policy frameworks or management structures are missing, the agent designs an enterprise-grade hierarchy (Tenant Root -> Management Groups -> Subscriptions / Organizational Units) following cloud best practices.

Resource-Level Drift Detection (Subsequent): Maps underlying infrastructure resources against active policies to catch misconfigurations.

Local AI Remediation: Leverages local, offline quantized LLMs to generate vertical, production-ready remediation code (Terraform, CloudFormation, or JSON Policy definitions).


# Regulatory & Security Alignment

InfraProbe-Agent is architected to satisfy rigorous internal and external audit requirements:

ISO/IEC 27001:2022: Verifies asset management, access controls, and secure configuration baselines.

DORA: Evaluates digital operational resilience, ICT risk management, and redundancy drift.

PCI-DSS: Detects public data exposures, insecure storage, and unsegmented network paths.

CIS Benchmarks: Ensures both cloud services and underlying host operating systems adhere to hardening guidelines.

Rev 6 Baselines: Enforces strict internal enterprise security baselines required by major European banking groups.


# Deployment Options 

To comply with strict corporate security policies (where containerization like Docker may be completely banned in legacy banking environments), the agent supports two independent deployment models:

Native Linux Binary & Systemd Service (For hardened RHEL/Rocky Linux VMs with strict CIS Benchmarks where Docker is forbidden).

Hardened Docker Container (For cloud-native environments permitting rootless containers).

infraprobe-agent/
├── .env.example
├── Dockerfile
├── README.md
├── requirements.txt
├── main.py
├── infraprobe.service
├── build_binary.sh
└── modules/
    ├── __init__.py
    ├── multi_cloud_scanner.py
    ├── debt_analyzer.py
    └── reporter.py
