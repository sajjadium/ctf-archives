import collections
import asyncio
import traceback
from urllib.parse import unquote

from reader.core import InvalidRequest, MethodNotAllowed, Request
from reader.routes import list_files

BUFFER_SIZE = 8196


async def parse_request(reader: asyncio.StreamReader):
    print("Recv req")
    req = (await reader.read(BUFFER_SIZE)).decode("utf8")
    first_line, rest = req.split("\r\n", 1)

    # Don't care about protocol, assume HTTP/1.1
    print("Parse req")
    method, path, _ = first_line.split(" ")

    print("Recv header")
    header_buffer = rest
    while "\r\n\r\n" not in header_buffer:
        request = (await reader.read(BUFFER_SIZE)).decode("utf8")
        header_buffer += request

    print("Parse header")
    # Should be a multidict, but we'll just assume every key is unique
    headers = {}
    for header in header_buffer.split("\r\n"):
        if not header.strip():
            break

        key, value = header.strip().split(":", 1)
        headers[key] = value

    if method == "GET":
        return Request(method, path, "")

    if method != "POST":
        raise MethodNotAllowed("Cannot use method: " + method)

    content_length = int(headers.get("Content-Length", "0"))
    if content_length <= 0:
        raise InvalidRequest("Invalid Content-Length")

    print("Parsing data, if available")
    data_buffer: collections.deque[str] = collections.deque(maxlen=content_length)

    # There might be leftover from header buffer, restore it
    _, data = header_buffer.split("\r\n\r\n", 1)
    if unquote(data).startswith("fname=/"):
        raise InvalidRequest("Can't do that.")

    data_buffer.extend(data)
    data_len = len(data)
    while data_len < content_length:
        body = (await reader.read(BUFFER_SIZE)).decode("utf8")
        if unquote(body).startswith("fname=/"):
            raise InvalidRequest("Can't do that.")

        data_buffer.extend(list(body))
        data_len += len(body)

    return Request(method, path, unquote("".join(list(data_buffer))))


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("New request")
    try:
        request = await asyncio.wait_for(parse_request(reader), timeout=5)
        if request.method in ("GET", "POST") and request.path == "/":
            response = await list_files(request)
        else:
            raise InvalidRequest("Invalid request")

        status = 200
        status_message = "OK"
    except InvalidRequest as e:
        status = 400
        status_message = "Bad Request"
        response = str(e)
    except MethodNotAllowed as e:
        status = 405
        status_message = "Method Not Allowed"
        response = str(e)
    except TimeoutError:
        status = 408
        status_message = "Timeout"
        response = "Timed out"
    except BaseException as e:
        traceback.print_exc()
        status = 500
        status_message = "Internal Server Error"
        response = str(e)

    try:
        writer.write(f"HTTP/1.1 {status} {status_message}\n".encode())
        writer.write(f"Content-Length: {len(response)}\n".encode())
        writer.write(f"Content-Type: text/html\n".encode())
        writer.write("\n".encode())
        writer.write(response.encode())
        await writer.drain()
        writer.close()
    except:
        pass
