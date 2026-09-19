#!/bin/bash
set -e

echo "[*] Cleaning previous builds..."
rm -rf build/ dist/ *.spec
#!/bin/bash
set -e

echo "[*] Cleaning previous builds..."
rm -rf build/ dist/ *.spec

echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Compiling standalone Linux binary with explicit hidden imports..."
pyinstaller --onefile \
  --name infraprobe-agent \
  --hidden-import=azure.identity \
  --hidden-import=azure.mgmt.resource \
  --hidden-import=azure.mgmt.policyinsights \
  --hidden-import=boto3 \
  --hidden-import=botocore \
  --hidden-import=google.cloud.asset \
  --hidden-import=rich \
  main.py

echo "[✔] Build completed successfully. Binary located in dist/infraprobe-agent"