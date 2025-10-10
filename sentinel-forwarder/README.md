# OCI Function → Azure Sentinel (Log Analytics) Forwarder

This sample OCI Function (Python) pulls JSON from a sample REST API and forwards it into Microsoft Sentinel via the **Azure Log Analytics HTTP Data Collector API**.

## Configure

Set these **Function** environment variables in the OCI Console:

- `WORKSPACE_ID` — your Log Analytics Workspace ID (a GUID)
- `SHARED_KEY` — your Workspace **Primary Key** (Base64)
- `LOG_TYPE` — custom table prefix (e.g., `OciSentinelDemo`). Azure table will appear as `OciSentinelDemo_CL`
- `SAMPLE_API_URL` — a public JSON endpoint to pull (default: `https://jsonplaceholder.typicode.com/todos?_limit=5`)

> Tip: For production, store `SHARED_KEY` in OCI Vault and read it securely from the function.

## Verify

After invoking the function, query in Azure Logs (Kusto):

```kusto
OciSentinelDemo_CL | take 10
```

You should see columns like `source_s`, `title_s`, `completed_b`, `id_d`, and `time_t`.
