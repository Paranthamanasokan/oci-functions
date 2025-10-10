# Quick local test (no OCI) to verify import & event shaping only.
# It won't post to Sentinel unless you set env vars.
import os
from io import BytesIO
from src.func import handler

# set envs for local test if you want to actually post
# os.environ["WORKSPACE_ID"] = "<your_workspace_id>"
# os.environ["SHARED_KEY"] = "<your_primary_key_base64>"

resp = handler(None, BytesIO())
print(resp.body().decode() if hasattr(resp, "body") else resp)
