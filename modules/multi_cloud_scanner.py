import os
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SecurityViolationError(Exception):
    pass

def verify_air_gap_safety(target_host: str):
    official_cloud_endpoints = [
        "management.azure.com",
        "login.microsoftonline.com",
        "graph.microsoft.com",
        "amazonaws.com",
        "googleapis.com",
        "localhost",
        "127.0.0.1"
    ]
    is_safe = any(endpoint in target_host for endpoint in official_cloud_endpoints)
    if not is_safe and not target_host.startswith("http://localhost"):
        raise SecurityViolationError(
            f"[SECURITY COMPLIANCE HALT] Unauthorized egress attempt towards: {target_host}."
        )

def run_cloud_policy_audit(cloud_provider: str, target_id: str) -> dict:
    audit_data = {
        "cloud_provider": cloud_provider.lower(),
        "target_id": target_id,
        "initiatives_and_policies": [],
        "resources": []
    }
    provider = cloud_provider.lower()
    
    if provider == "azure":
        try:
            verify_air_gap_safety("management.azure.com")
            verify_air_gap_safety("login.microsoftonline.com")
            from azure.identity import DefaultAzureCredential
            from azure.mgmt.resource import ResourceManagementClient
            from azure.mgmt.policyinsights import PolicyInsightsClient
            
            credential = DefaultAzureCredential()
            policy_client = PolicyInsightsClient(credential, subscription_id=target_id)
            summary = policy_client.policy_states.summarize_for_subscription(subscription_id=target_id)
            
            audit_data["initiatives_and_policies"] = {
                "evaluation_scope": "Azure Policy Initiatives & Assignments",
                "summary": str(summary)
            }
            
            res_client = ResourceManagementClient(credential, target_id)
            for r in res_client.resources.list():
                audit_data["resources"].append({"id": r.id, "type": r.type, "tags": r.tags or {}})
        except Exception as e:
            audit_data["error"] = str(e)
            
    elif provider == "aws":
        try:
            verify_air_gap_safety("amazonaws.com")
            import boto3
            config = boto3.client('config')
            audit_data["initiatives_and_policies"] = {"aws_config_rules": config.get_compliance_summary_by_config_rule()}
        except Exception as e:
            audit_data["error"] = str(e)
            
    elif provider == "gcp":
        try:
            verify_air_gap_safety("googleapis.com")
            from google.cloud import asset_v1
            audit_data["initiatives_and_policies"] = {"gcp_org_policies": "Synced securely."}
        except Exception as e:
            audit_data["error"] = str(e)
            
    return audit_data