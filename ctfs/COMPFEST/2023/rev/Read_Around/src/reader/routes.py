from jinja2 import Environment, PackageLoader, select_autoescape

from reader.core import InvalidRequest, Request
from reader.utils import get_content, get_filelist

env = Environment(loader=PackageLoader("reader"), autoescape=select_autoescape())
template = env.get_template("index.html")

async def list_files(request: Request | None = None):
    print("Request: ", request)
    content = None
    if request and request.data:
        # There can only be one parameter, and that is fname. Just ignore the rest.
        if not request.data.startswith("fname="):
            raise InvalidRequest("Malformed request")
        
        key, value = request.data.split("=", 1)
        if key == "fname":
            content = get_content(value)

    filelist = await get_filelist()
    return template.render(files=filelist, content=content)