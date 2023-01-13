#!/usr/bin/env python3

import socket
from os import path
from base64 import b64decode
from urllib.parse import unquote_plus
from typing import Union, Tuple, Dict

from threading import Thread

BUFF_SIZE = 8192

# Equivalent to CRLF, named NEWLINE for clarity
NEWLINE = "\r\n"

HTTP_REQ_HEADER_END = (NEWLINE + NEWLINE).encode("utf-8")

# This class is 100% built for you. It uses slightly fancier versions of code like we saw in class.
# YOU WILL NEED TO READ (at least) THE DOCSTRINGS AND FUNCTION NAMES HERE!
class Request:
    """Holds the data which a client sends in a request

    `method` is a string of the HTTP method which the client's request was in.
    For example: GET or POST.

    `headers` is a dictionary of all lowercase key to value pairs. For Example:
      - accept: 'text/html'
      - accept-charset: 'UTF-8'

    `content` is a possibly empty string of whatever content was included in the
    client's request.
    """

    def __init__(self, start_line: str, headers: Dict[str, str], content: str):
        self.method, self.path, *_ = start_line.split()
        # remove leading "/" from the path
        self.path = self.path[1:]
        self.headers = headers
        self.content = content

# provided complete
def recv_until_crlfs(sock) -> Request:
    def to_tuple(kvstr: str) -> Tuple[str, str]:
        k, v = kvstr.split(":", 1)
        # we could have capitalized header or all lowercase, normalize it
        # so we can do a proper lookup
        return (k.lower(), v)

    header_data = b""
    content = b""
    content_bytes_read = 0
    while True:
        data = sock.recv(BUFF_SIZE)
        if not data:
            break
        # Request headers end with two CRLFs
        if HTTP_REQ_HEADER_END in data:
            header_end_idx = data.find(HTTP_REQ_HEADER_END)
            header_data += data[:header_end_idx]
            # How much content did we prematurely recieve from the client
            content_bytes_read = max(0, len(data) - header_end_idx - 4)
            content += data[header_end_idx + 4 :]
            break
        header_data += data
    # read the rest of the content that we need to based on content-length
    headers = header_data.decode("utf-8")
    header_list = headers.split(NEWLINE)
    header_kvs = dict(map(to_tuple, header_list[1:]))
    if content_bytes_read != 0:
        if "content-length" not in header_kvs:
            # No content length header... keep reading until end
            while True:
                data = sock.recv(BUFF_SIZE)
                if not data:
                    break
                content += data
        else:
            content_len = int(header_kvs["content-length"])
            to_recv = max(0, content_len - content_bytes_read)
            content += sock.recv(to_recv)
    return Request(header_list[0], header_kvs, content.decode("utf-8"))


# Let's define some functions to help us deal with files, since reading them
# and returning their data is going to be a very common operation.
# Both functions are provided complete and correct.

def get_file_contents(file_name: str) -> str:
    """Returns the text content of `file_name`"""
    with open(file_name, "r") as f:
        return f.read()


def get_file_binary_contents(file_name: str) -> bytes:
    """Returns the binary content of `file_name`"""
    with open(file_name, "rb") as f:
        return f.read()


# This set will hold all of the resources which you want to be gated behind some
# form of authorization. For the purposes of this assignment, keeping only
# private.html is good enough.
# You should not need to change this.
private_files = set(["private.html"])


def has_permission(file_name: str) -> bool:
    """Returns `True` if the `file_name` in the private_files"""
    return file_name in private_files


def file_exists(file_name: str) -> bool:
    """Returns `True` if `file_name` exists, this is just a wrapper for the
    os.path.exists function so that it's more visible"""
    return path.exists(file_name)


# Some files should be read in plain text, whereas others should be read
# as binary. To maintain a mapping from file types to their expected form, we
# have a `set` that maintains membership of file extensions expected in binary.
# We've defined a starting point for this set, which you may add to as
# necessary.
# TODO: Finish this set with all relevant files types that should be read in
# binary
binary_type_files = set(["jpg", "jpeg", "png", "mp3", "woff", "ttf"]) # "png", "mp3", woff, ttf

def should_return_binary(file_extension: str) -> bool:
    """
    Returns `True` if the file with `file_extension` should be sent back as
    binary.
    """
    return file_extension in binary_type_files


# For a client to know what sort of file you're returning, it must have what's
# called a MIME type. We will maintain a `dictionary` mapping file extensions
# to their MIME type so that we may easily access the correct type when
# responding to requests.
# TODO: Finish this dictionary with all required MIME types
MimeType = str
Response = bytes
mime_types: Dict[str, MimeType] = {
    "html": "text/html",
    "css" : "text/css",
    "js"  : "text/javascript",
    "mp3" : "audio/mpeg",
    # fonts
    "woff": "font/woff",
    "ttf" : "font/ttf",
    # images
    "jpg" : "image/jpeg",
    "png" : "image/png",
    "jpeg": "image/jpeg"
}


def get_file_mime_type(file_extension: str) -> MimeType:
    """
    Returns the MIME type for `file_extension` if present, otherwise
    returns the MIME type for plain text.
    """
    if file_extension not in mime_types:
        return "text/plain"
    return mime_types[file_extension]


# TODO: This is not completely built -- you will need to finish it, or replace it with comperable behavior.
class ResponseBuilder:
    """
    This class is here for your use if you want to use it. This follows
    the builder design pattern to assist you in forming a response. An
    example of its use is in the `method_not_allowed` function.
    """

    def __init__(self):
        """
        Initialize the parts of a response to nothing (I.E. by default -- no response)
        """
        self.headers = []
        self.status = None
        self.content = None

    def add_header(self, header_key: str, header_value: Union[str, int]) -> None:
        """Adds a new header to the response"""
        self.headers.append(f"{header_key}: {header_value}")

    def set_status(self, status_code: Union[str, int], status_message: str) -> None:
        """Sets the status of the response"""
        self.status = f"HTTP/1.1 {status_code} {status_message}"

    def set_content(self, content: Union[str, bytes]) -> None:
        """Sets `self.content` to the bytes of the content"""
        if isinstance(content, (bytes, bytearray)):
            self.content = content
        else:
            self.content = content.encode("utf-8")

    def build(self) -> bytes:
        """
        Returns the utf-8 bytes of the response.

        Uses the `self.status`, `self.headers`, and `self.content` to form
        an HTTP response in valid formatting per w3c specifications, which
        can be seen here:
          https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html

        Where CRLF is our `NEWLINE` constant.
        """
        # TODO: this        
        response = self.status + NEWLINE
        for header in self.headers:
          response = response + str(header) + NEWLINE
          
        response = response + NEWLINE
        response = response.encode('utf-8')

        if self.content != None:
          response = response + self.content
        # else:
        #   response = response.encode('utf-8')
        print(response)
        return response


class HTTPServer:
    """
    Our actual HTTP server which will service GET, POST, and HEAD requests.
    """

    def __init__(self, host="localhost", port=9001, directory="."):
        print(f"Server started. Listening at http://{host}:{port}/")
        self.host = host
        self.port = port
        self.working_dir = directory

        self.setup_socket()
        self.accept()

        self.teardown_socket()

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(128)

    def teardown_socket(self):
        if self.sock:
            self.sock.shutdown()
            self.sock.close()

    def accept(self):
        while True:
            (client, address) = self.sock.accept()
            th = Thread(target=self.accept_request, args=(client, address))
            th.start()

    def accept_request(self, client_sock, client_addr):
        req = recv_until_crlfs(client_sock)

        response = self.process_response(req)
        client_sock.send(response)

        # clean up
        client_sock.shutdown(1)
        client_sock.close()

    def process_response(self, request: Request) -> bytes:
        if request.method == "GET":
            return self.get_request(request)
        if request.method == "POST":
            return self.post_request(request)
        if request.method == "HEAD":
            return self.head_request(request)
        return self.method_not_allowed()

    # TODO: Write the response to a GET request
    def get_request(self, request: Request) -> Response:
        """
        Responds to a GET request with the associated bytes.

        If the request is to redirect to a url (first item in URI),
        responds with a redirect request with HTTP 307 (Temporary Redirect)
        status code and a location header

        If the request is to a file that does not exist, returns
        a `NOT FOUND` error.

        If the request is to a file that is supposed to be private, have the
        client go through the authentication steps in order to access it.

        Otherwise, we must read the requested file's content, either
        in binary or text depending on `should_return_binary` and
        send it back with a status set and appropriate mime type
        depending on `get_file_mime_type`.
        """        
        size = 0
        mime_type = ""
        data = ""
        builder = ResponseBuilder()
        
        keys = list(request.headers.keys())
        values = list(request.headers.values())
        # append all the requested headers 
        for i in range(len(keys)):
          builder.add_header(keys[i], values[i])

        # redirect
        if request.path.startswith("redirect"):
          if request.path == "redirect":
            redirect = "MyServer.html"
            extension = redirect[redirect.index('.')+1:]
            mime_type = get_file_mime_type(extension)
            data = get_file_contents(redirect)
            size = len(bytes(data, 'utf-8'))
            builder.set_status("307", "Temporary Redirect")
            builder.add_header("Content-Length", size)
            builder.add_header("Content-Type", mime_type+'; charset=UTF-8')
            builder.add_header("Connection", "close")
            builder.set_content(data)
          else:
            idx = request.path.index("=")
            # referenced from: https://docs.python.org/3/library/urllib.parse.html
            search = unquote_plus(request.path[idx+1:])
            builder.set_status("307", "Temporary Redirect")
            builder.add_header("Location", "https://www.youtube.com/results?search_query="+search)
            builder.add_header("Connection", "close")
          return builder.build()

        # 404
        elif not file_exists(request.path):
          return self.resource_not_found()
        
        # get files
        else:
          if has_permission(request.path):
            # print(request.path, 'is private')
            try:
              authorize = str(b64decode(request.headers['authorization'][7:]))
              password = authorize[authorize.index(':')+1:-1]
              username = authorize[2:authorize.index(':')]

              if username == 'admin' and password == 'password':
                extension = request.path[request.path.index('.')+1:]
                mime_type = get_file_mime_type(extension)
                data = get_file_contents(request.path)
                size = len(bytes(data,'utf-8'))
                
                builder.set_status("200", "OK")
                
              else:
                unauthorized = "401.html"
                extension = unauthorized[unauthorized.index('.')+1:]
                mime_type = get_file_mime_type(extension)
                data = get_file_contents(unauthorized)
                size = len(bytes(data,'utf-8'))
                
                builder.set_status("401", "Unauthorized")
            except:
              unauthorized = "401.html"
              extension = unauthorized[unauthorized.index('.')+1:]
              mime_type = get_file_mime_type(extension)
              data = get_file_contents(unauthorized)
              size = len(bytes(data,'utf-8'))
              
              builder.set_status("401", "Unauthorized")
              # referenced from: basic access authentication - wikipidia 
              builder.add_header("WWW-Authenticate", "Basic realm='admin:password'")
          else:
            extension = request.path[request.path.index('.')+1:]
            mime_type = get_file_mime_type(extension)
            if should_return_binary(extension):  # if true, it should be jpg etc
              data = get_file_binary_contents(request.path)            
            else:
              data = bytes(get_file_contents(request.path), 'utf-8')
            size = len(data)
            builder.set_status("200", "OK")

          builder.add_header("Content-Length", size)
          builder.add_header("Content-Type", mime_type+'; charset=UTF-8')
          builder.add_header("Connection", "close")
          builder.set_content(data)

          return builder.build()            
  
    # TODO: Write the response to a POST request
    def post_request(self, request: Request) -> Response:
        """
        Responds to a POST request with an HTML page with keys and values
        echoed per the requirements writeup.

        A post request through the form will send over key value pairs
        through "x-www-form-urlencoded" format. You may learn more about
        that here:
          https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
        You /do not/ need to check the POST request's Content-Type to
        verify the encoding used (although a real server would).

        From the request, each key and value should be extracted. A row in
        the HTML table will hold a single key-value pair. With the key having
        the first column and the value the second. If a request sent n
        key-value pairs, the HTML page returned should contain a table like:

        | key 1 | val 1 |
        | key 2 | val 2 |
        | ...   | ...   |
        | key n | val n |

        Care should be taken in forming values with spaces. Since the request
        was urlencoded, it will need to be decoded using
        `urllib.parse.unquote_plus`.
        """
        builder = ResponseBuilder()
        builder.set_status('200', 'OK')
        param = ""
        # set table 
        result = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>POST request</title></head><body><table>'

        if request.content != "":
          param = unquote_plus(request.content)
        else:
          param = unquote_plus(request.path)
          # check if parameter exist
          if '?' in param:
            param = param[param.index('?')+1:]
          else:
            result = result + "</table></body></html>"
            size = len(bytes(result,'utf-8'))
            mime_type = get_file_mime_type("html")
            
            builder.add_header("Content-Length", size)
            builder.add_header("Content-Type", mime_type+'; charset=UTF-8')
            builder.add_header("Connection", "close")
            builder.set_content(result)

            return builder.build()
          
        
        keys = []
        values = []
        while '=' in param:
          i = param.index('=')
          if '&' in param:
            j = param.index('&')
          else:
            j = -1

          # slicing
          if j != -1:
            key = param[:i]
            value = param[i+1:j]
            param = param[j+1:]
          else:
            key = param[:i]
            value = param[i+1:]
            param = ""
          
          keys.append(key)
          values.append(value)

        builder.set_status('200', 'OK')
        
        for i in range(len(keys)):
          result = result + f"<tr><td>{keys[i]}</td><td>{values[i]}</td></tr>"
        result = result + "</table></body></html>"

        size = len(bytes(result,'utf-8'))
        mime_type = get_file_mime_type("html")
        
        builder.add_header("Content-Length", size)
        builder.add_header("Content-Type", mime_type+'; charset=UTF-8')
        builder.add_header("Connection", "close")
        builder.set_content(result)

        return builder.build()
        
    # TODO: Write the head request function
    def head_request(self, request: Request) -> Response:
        """
        Responds to a HEAD request with the exact same requirements as a GET
        request, but should not contain any content.

        HINT: you can _remove_ content from a ResponseBuilder...
        """
        header = self.get_request(request)
        # referenced from: https://realpython.com/lessons/operations-bytes-objects/
        idx = self.get_request(request).find(b'\r\n\r\n')
        head = header[:idx+4]
        return head

    def method_not_allowed(self) -> Response:
        """
        Returns 405 not allowed status and gives allowed methods.

        TODO: If (and only if)  you are not going to complete the `ResponseBuilder`,
        This must be rewritten.
        """
        builder = ResponseBuilder()
        builder.set_status("405", "METHOD NOT ALLOWED")
        allowed = ", ".join(["GET", "POST", "HEAD"])
        builder.add_header("Allow", allowed)
        builder.add_header("Connection", "close")
        return builder.build()

    # TODO: Write 404 error
    def resource_not_found(self) -> Response:
        """
        Returns 404 not found status and sends back our 404.html page.
        """
        builder = ResponseBuilder()
        mime_type = get_file_mime_type("html")
        data = get_file_contents("404.html")
        size = len(bytes(data, 'utf-8'))
        builder.set_status("404", "Not Found")
        builder.add_header("Content-Length", size)
        builder.add_header("Content-Type", mime_type+'; charset=UTF-8')
        builder.add_header("Connection", 'close')
        builder.set_content(data)
        return builder.build()


if __name__ == "__main__":
    HTTPServer()
