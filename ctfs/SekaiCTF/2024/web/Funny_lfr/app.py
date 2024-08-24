from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import FileResponse


async def download(request):
    return FileResponse(request.query_params.get("file"))


app = Starlette(routes=[Route("/", endpoint=download)])
