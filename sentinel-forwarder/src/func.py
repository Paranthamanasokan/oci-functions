import io
import os
import json
import datetime
import requests
from fdk import response
from .sentinel import post_data

def handler(ctx, data: io.BytesIO = None):
    # Read configuration from environment variables
    workspace_id = os.environ.get("WORKSPACE_ID")
    shared_key = os.environ.get("SHARED_KEY")
    log_type = os.environ.get("LOG_TYPE", "OciSentinelDemo")
    sample_api_url = os.environ.get("SAMPLE_API_URL", "https://jsonplaceholder.typicode.com/todos?_limit=5")

    # Validate required config
    missing = [k for k in ["WORKSPACE_ID", "SHARED_KEY"] if os.environ.get(k) in (None, "")]
    if missing:
        return response.Response(
            ctx,
            status_code=500,
            response_data=json.dumps({"error": f"Missing required env vars: {', '.join(missing)}"}),
            headers={"Content-Type": "application/json"}
        )

    # Pull sample data (replace with your real data source later)
    try:
        r = requests.get(sample_api_url, timeout=10)
        r.raise_for_status()
        rows = r.json()
    except Exception as e:
        return response.Response(
            ctx,
            status_code=502,
            response_data=json.dumps({"error": f"Failed to fetch sample API: {str(e)}"}),
            headers={"Content-Type": "application/json"}
        )

    # Normalize rows into a simple list of dicts and stamp event time
    now_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    # Some public sample APIs return an object; ensure we have a list
    if isinstance(rows, dict):
        rows = [rows]
    events = []
    for item in rows[:1000]:  # keep payloads small
        evt = {
            "time": now_iso,   # used by 'time-generated-field'
            "source": "oci-function-demo",
            "title": item.get("title") if isinstance(item, dict) else str(item),
            "id": item.get("id") if isinstance(item, dict) else None,
            "completed": item.get("completed") if isinstance(item, dict) else None
        }
        events.append(evt)

    # Send to Azure Sentinel (Log Analytics)
    try:
        status = post_data(workspace_id, shared_key, log_type, events, time_field="time")
        out = {"sent": len(events), "status": status, "log_type": log_type}
        code = 200
    except Exception as e:
        out = {"error": f"Failed to send to Sentinel: {str(e)}"}
        code = 500

    return response.Response(
        ctx,
        status_code=code,
        response_data=json.dumps(out),
        headers={"Content-Type": "application/json"}
    )
