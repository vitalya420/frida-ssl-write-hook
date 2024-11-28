
import gzip


def is_completed_http_response(http_response: bytes):
    headers_buff, body = http_response.split(b'\r\n\r\n', 1)
    headers_str = headers_buff.decode("utf-8")
    header_lines = headers_str.split("\r\n")

    status_line = header_lines[0]
    http_version, status_code, *status_phrase = status_line.split(" ")
    status_code = int(status_code)
    status_phrase = " ".join(status_phrase)

    headers_dict = {}
    for line in header_lines[1:]:
        if line:
            key, value = line.split(": ", 1)
            headers_dict[key.lower()] = value
    
    return int(headers_dict.get('content-length', 0)) == len(body)

def parse_http_response(http_response: bytes):
    headers_buff, body = http_response.split(b'\r\n\r\n', 1)
    headers_str = headers_buff.decode("utf-8")
    header_lines = headers_str.split("\r\n")

    status_line = header_lines[0]
    http_version, status_code, *status_phrase = status_line.split(" ")
    status_code = int(status_code)
    status_phrase = " ".join(status_phrase)

    headers_dict = {}
    for line in header_lines[1:]:
        if line:
            key, value = line.split(": ", 1)
            headers_dict[key.lower()] = value

    
    content_encoding = headers_dict.get('content-encoding', None)
    if content_encoding == 'gzip':
        body = gzip.decompress(body)
        print(body)