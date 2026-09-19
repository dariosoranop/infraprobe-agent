# InfraProbe-Agent 🛡️🤖

**InfraProbe-Agent** is a production-grade, highly hardened multi-cloud security, compliance, and governance auditor engineered explicitly for financial institutions and enterprise banking environments.

It bridges the gap between cloud infrastructure and regulatory compliance, performing deep multi-cloud scans aligned with **ISO/IEC 27001:2022, DORA (Digital Operational Resilience Act), PCI-DSS, CIS Benchmarks, and Rev 6 Security Baselines**.

---

## 🏛️ Why Banks Need Cloud Policy Compliance Auditing

Moving workloads to cloud platforms (Microsoft Azure, AWS, or Google Cloud) does not transfer regulatory accountability. Under the **Shared Responsibility Model**, financial institutions remain entirely liable for data security, configuration drift, and continuous compliance.

Furthermore, banks never apply cloud configurations as a monolithic standard. Internal Security & Governance teams define custom **Policy Initiatives** (grouped compliance rules), selectively enabling, overriding, or disabling controls based on risk appetite.

### Core Intelligence Workflow
InfraProbe-Agent follows a strict hierarchical governance workflow to evaluate and remediate infrastructure:
1. **Policy Initiatives & Governance Review (First):** Inspects how policy initiatives, security frameworks, and guardrails are implemented across the tenant or account. It detects overrides, disabled controls, and compliance gaps.
2. **Enterprise Hierarchy Blueprinting (Fallback):** If proper policy frameworks or management structures are missing, the agent designs an enterprise-grade hierarchy (Tenant Root -> Management Groups -> Subscriptions / Organizational Units) following cloud best practices.
3. **Resource-Level Drift Detection (Subsequent):** Maps underlying infrastructure resources against active policies to catch misconfigurations.
4. **Local AI Remediation:** Leverages local, offline quantized LLMs to generate vertical, production-ready remediation code (Terraform, CloudFormation, or JSON Policy definitions).

---

## 🔒 Regulatory & Security Alignment

InfraProbe-Agent is architected to satisfy rigorous internal and external audit requirements:
* **ISO/IEC 27001:2022:** Verifies asset management, access controls, and secure configuration baselines.
* **DORA:** Evaluates digital operational resilience, ICT risk management, and redundancy drift.
* **PCI-DSS:** Detects public data exposures, insecure storage, and unsegmented network paths.
* **CIS Benchmarks:** Ensures both cloud services and underlying host operating systems adhere to hardening guidelines.
* **Rev 6 Baselines:** Enforces strict internal enterprise security baselines required by major European banking groups.

---

## 🚀 Deployment Options

To comply with strict corporate security policies (where containerization like Docker may be completely banned in legacy banking environments), the agent supports **two independent deployment models**:

1. **Native Linux Binary & Systemd Service** (For hardened RHEL/Rocky Linux VMs with strict CIS Benchmarks where Docker is forbidden).
2. **Hardened Docker Container** (For cloud-native environments permitting rootless containers).

---

## 📁 Repository Structure

```text
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
```

---

## ⚙️ Configuration & Prerequisites (`.env` and Credentials)

Before launching the agent, make sure to address the following runtime prerequisites:
* **Environment Variables (`.env`):** Copy `.env.example` to `.env` and configure your local Ollama endpoint and model name:
  ```env
  OLLAMA_HOST=http://localhost:11434
  MODEL_NAME=qwen2.5:7b-instruct
  ```
* **Execution Credentials:** When running under restricted system accounts (such as the non-root Systemd user `infraprobe` or rootless Docker containers), interactive login tokens (e.g., `az login`) will not be inherited automatically. Ensure that either Managed Identities, Service Principals, or proper IAM instance profiles are correctly configured on the execution host.

---

## 🔄 What Happens When You Execute the Agent? (The 6-Step Workflow)

Once you run the agent with the required parameters, it operates completely autonomously following an end-to-end execution pipeline:

1. **Bootstrap & Air-Gap Safety Verification:** The agent initializes, prints the execution banner, and activates hardcoded security circuit breakers (`verify_air_gap_safety`) to block any unauthorized network egress, allowing connections strictly toward official cloud management endpoints.
2. **Policy Initiatives & Governance Scan:** It queries native cloud policy APIs (such as Azure Policy Insights, AWS Config, or GCP Org Policies) to map active policies, disabled rules, overrides, and initial compliance gaps.
3. **Hierarchical Governance Analysis & Fallback:** It reviews the organizational layout. If structural governance gaps or missing policy structures are found, the agent engages its architectural logic to blueprint a proper multi-tier layout (e.g., Tenant Root -> Management Groups -> Subscriptions).
4. **Underlying Resource-Level Audit:** It compiles a secure, read-only inventory of cloud resources (VMs, storage accounts, network configurations) correlated to the evaluated policies.
5. **Local AI Remediation & Code Generation:** It packages the structured findings and sends them securely to your offline, quantized local LLM (Ollama). The model analyzes the gaps against regulatory standards (ISO 27001, DORA, PCI, CIS, Rev 6) and outputs precise, production-ready remediation code (Terraform blocks or JSON policies).
6. **Automated Report Generation & Saving:** It automatically creates a `reports/` directory and persists a comprehensive Markdown audit report containing timestamps, scope IDs, risk assessments, and code solutions ready for security reviewers.

---

## 🛠️ How to Use and Launch

### Method A: Native Linux Binary & Systemd Service (No Docker)
*Ideal for secure, CIS-hardened RHEL / Rocky Linux VMs inside strict banking environments.*

1. **Build the standalone binary** (on an authorized build machine with matching architecture):
   ```bash
   chmod +x build_binary.sh
   ./build_binary.sh
   ```
2. **Deploy to the target banking VM:**
   * Copy the generated `dist/infraprobe-agent` binary to `/opt/infraprobe-agent/`.
   * Create a dedicated service user and directory:
     ```bash
     sudo useradd -r -s /bin/false infraprobe
     sudo mkdir -p /opt/infraprobe-agent/reports
     sudo chown -R infraprobe:infraprobe /opt/infraprobe-agent
     ```
3. **Configure and start the Systemd service:**
   ```bash
   sudo cp infraprobe.service /etc/systemd/system/infraprobe.service
   sudo systemctl daemon-reload
   sudo systemctl enable --now infraprobe.service
   ```

### Method B: Hardened Docker Container
*For environments where containerization is permitted.*

1. **Build the image:**
   ```bash
   docker build -t infraprobe-agent .
   ```
2. **Run the container (Rootless, isolated):**
   ```bash
   docker run --rm --read-only \
     -v ~/.azure:/home/appuser/.azure:ro \
     -e OLLAMA_HOST="http://host.docker.internal:11434" \
     infraprobe-agent \
     --provider azure --target-id "<YOUR-SUBSCRIPTION-ID>"
   ```

---

## 💻 Provider-Specific Execution (CLI)

### 1. Microsoft Azure
```bash
python main.py --provider azure --target-id "<YOUR-AZURE-SUBSCRIPTION-ID>"
```

### 2. Amazon Web Services (AWS)
```bash
python main.py --provider aws --target-id "<YOUR-AWS-ACCOUNT-ID>"
```

### 3. Google Cloud Platform (GCP)
```bash
python main.py --provider gcp --target-id "<YOUR-GCP-ORG-OR-PROJECT-ID>"
```