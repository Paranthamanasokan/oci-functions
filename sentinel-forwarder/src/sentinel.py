# Helper for Azure Log Analytics HTTP Data Collector API
# Docs: https://learn.microsoft.com/en-us/rest/api/loganalytics/create-request

import base64
import hashlib
import hmac
import json
import datetime
import request

def _build_signature(workspace_id: str, shared_key_b64: str, date_str: str, content_length: int,
                     method: str = "POST", content_type: str = "application/json", resource: str = "/api/logs") -> str:
    string_to_sign = f"{method}\n{content_length}\n{content_type}\nx-ms-date:{date_str}\n{resource}"
    bytes_to_sign = string_to_sign.encode("utf-8")
    decoded_key = base64.b64decode(shared_key_b64)
    hashed = hmac.new(decoded_key, bytes_to_sign, hashlib.sha256).digest()
    signature = base64.b64encode(hashed).decode()
    return f"SharedKey {workspace_id}:{signature}"

def post_data(workspace_id: str, shared_key_b64: str, log_type: str, records: list, time_field: str = "time",
              api_version: str = "2016-04-01", timeout: int = 10) -> int:
    post_body = json.dumps(records)
    content_length = len(post_body)
    rfc1123date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    signature = _build_signature(workspace_id, shared_key_b64, rfc1123date, content_length)
    uri = f"https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version={api_version}"

    headers = {
        "Content-Type": "application/json",
        "Log-Type": log_type,
        "x-ms-date": rfc1123date,
        "Authorization": signature,
        "time-generated-field": time_field
    }

    resp = requests.post(uri, data=post_body, headers=headers, timeout=timeout)
    # 200 means accepted, 202 sometimes returned as well; raise for other errors
    if resp.status_code not in (200, 202):
        raise RuntimeError(f"Sentinel ingest failed: HTTP {resp.status_code} - {resp.text}")
    return resp.status_code
