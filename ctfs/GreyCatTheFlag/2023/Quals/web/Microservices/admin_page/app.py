from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from requests import get
import os

load_dotenv()
admin_cookie = os.environ.get("ADMIN_COOKIE", "FAKE_COOKIE")

app = FastAPI()


@app.get("/")
async def index(request: Request):
    """
    The base service for admin site
    """

    # Currently Work in Progress
    requested_service = request.query_params.get("service", None)
    if requested_service is None:
        return {"message": "requested service is not found"}

    # Filter external parties who are not local
    if requested_service == "admin_page":
        return {"message": "admin page is currently not a requested service"}

    # Legit admin on localhost
    requested_url = request.query_params.get("url", None)
    if requested_url is None:
        return {"message": "URL is not found"}

    # Testing the URL with admin
    response = get(requested_url, cookies={"cookie": admin_cookie})
    return Response(response.content, response.status_code)
