import azure.functions as func
from azure.data.tables import TableServiceClient
from datetime import datetime
import json, os

# ------------------------------------------------------------------
#  Settings
# ------------------------------------------------------------------
CONN  = os.environ["AzureWebJobsStorage"]   # storage conn string injected by Azure
TABLE = "AthenaBetaSignups"                 # table auto-created if missing

# ------------------------------------------------------------------
#  Main HTTP entry point
# ------------------------------------------------------------------
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # 1) Parse body as JSON if possible, else read form fields
        if req.headers.get("content-type", "").startswith("application/json"):
            data = req.get_json()
        else:
            data = {k: v for k, v in req.form.items()}

        name  = (data.get("name")  or "").strip()
        email = (data.get("email") or "").strip()

        if not (name and email):
            raise ValueError("name and email required")

        # 2) Store in Azure Table Storage
        svc   = TableServiceClient.from_connection_string(CONN)
        table = svc.get_table_client(TABLE)
        table.create_table_if_not_exists()

        entity = {
            "PartitionKey": "signup",
            "RowKey": str(datetime.utcnow().timestamp()),
            "name":  name,
            "email": email
        }
        table.create_entity(entity)

        # 3) Success response
        return func.HttpResponse(
            json.dumps({"ok": True}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        # 4) Error response
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
