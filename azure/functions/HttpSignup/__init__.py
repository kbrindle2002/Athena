import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        name = body.get("name")
        email = body.get("email")
        return func.HttpResponse(
            json.dumps({"status": "ok", "user": {"name": name, "email": email}}),
            mimetype="application/json",
            status_code=200,
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=400,
        )
