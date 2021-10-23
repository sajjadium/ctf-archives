#!/usr/bin/python3
import sys
import time
import FastCgiClient
import re
from os import path,environ,getcwd

readCounter = 0
statusCodeDescs = {
    200 : "OK",
    405 : "Method Not Allowed",
    400 : "Bad request",
    412 : "Payload Too Large"
}
def sendResponse(html,statusCode):
    buf = ""
    buf+= f"HTTP/1.1 {statusCode} {statusCodeDescs[statusCode]}\r\n"
    buf+= f"Content-Length: {len(html)}\r\n"
    buf+= f"Content-Type: text/plain\r\n"
    buf+= f"\r\n"
    buf+= html
    print(buf,end="")
    exit()

def readn(n):
    global readCounter
    readed = 0
    buf = ""
    while(len(buf) != n):
        readedChr = sys.stdin.read(1)
        buf += readedChr 
        if(readedChr == ""):
            time.sleep(0.01)
    readCounter += len(buf)
    if(readCounter > 1000):
        sendResponse("HTTP request too big.",412)
    return buf

def readMethod():
    method = readn(3)
    if(method != "GET"):
        sendResponse("Method not allowed.",405)
    return method

def readURL():
    url = ""
    readn(1)
    while(True):
        readedChar = readn(1)
        if(readedChar == " "):
            break
        url += readedChar
    if( len(url) == 0 or len(url) > 200):
        sendResponse("Bad request.",400)
    return url

def readHTTPVersion():
    HTTPVersion = ""
    buf = ""
    while(True):
        buf += readn(1)
        if(buf[-2:] == "\r\n"):
            break
    HTTPVersion = buf[:-2]
    if(HTTPVersion != "HTTP/1.1"):
        sendResponse("Bad request.",400)
    return HTTPVersion

def readHeaders():
    headers = []

    end = False
    while(True):
        headerName = ""
        headerValue = ""
        while(True):
            readedChar = readn(1)
            if(readedChar == ":"):
                break
            headerName += readedChar
            if(headerName == "\r\n"):
                end = True
                break
        if(end == True):
            break
        buf = ""
        while(True):
            buf += readn(1)
            if(buf[-2:] == "\r\n"):
                break
        headerValue = buf[:-2]
        headers.append((re.sub(r'[^A-Z0-9_]', "", headerName.strip().upper().replace("-","_")),headerValue.strip()))
    return headers

if(__name__ == '__main__'):
    method = readMethod()
    url = readURL()
    protocol = readHTTPVersion()
    headers = readHeaders()
    query_string = ""
    path_info = ""
    script_filename = ""
    script_name = ""
    document_root = f"{getcwd()}/host/default"

    if("?" in url):
        query_string = url[url.index("?")+1:] 
        url = url[:url.index("?")]

    if(".php" not in url):
        url = "/index.php"

    phpExtIdx = url.index(".php")
    script_name = url[:phpExtIdx+4]
    path_info = url[phpExtIdx+4:]

    hostHeader = ""
    for header in headers:
        if(header[0] == "HOST"):
            hostHeader = header[1]

    #Virtual host support!
    if(path.isdir(path.normpath(f"{getcwd()}/host/{hostHeader}"))):
        document_root = f"{getcwd()}/host/{hostHeader}"

    script_filename = path.normpath(document_root+script_name)
    params = {
        'GATEWAY_INTERFACE': 'FastCGI/1.0',
        'REQUEST_METHOD': method,
        'SCRIPT_FILENAME': script_filename,
        'SCRIPT_NAME': script_name,
        'QUERY_STRING': query_string,
        'REQUEST_URI': url,
        'DOCUMENT_ROOT': document_root,
        'SERVER_PROTOCOL': protocol,
        'SERVER_SOFTWARE': 'mws',
        'REMOTE_ADDR': environ["REMOTE_HOST"],
        'SERVER_NAME': "mws",
        'CONTENT_TYPE': "",
        'CONTENT_LENGTH': "",
    }

    for header in headers:
        if("PROXY" not in header[0] and "LENGTH" not in header[0]):
            params[f"HTTP_{header[0]}"] = header[1]
    client = FastCgiClient.FastCGIClient(sys.argv[1])
    response = client.request(params, "")
    sendResponse(response[response.index(b"\r\n\r\n")+4:].decode('utf-8'),200)
