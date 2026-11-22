"""Upload a UTF-8 TXT file as multipart/form-data.

Example:
    python tools/file-upload.py notes.txt --url https://example.com/upload ^
        --format txt --size-limit 1048576

The size limit is in bytes. Use an authorized endpoint; this script does not
provide authentication. Plain HTTP is permitted only for loopback testing.
"""

import argparse
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4


def positive_size(value: str) -> int:
    try:
        size = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("size limit must be a positive integer in bytes") from error
    if not 0 < size < sys.maxsize:
        raise argparse.ArgumentTypeError("size limit must be a positive integer in bytes")
    return size


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload a UTF-8 TXT file.")
    parser.add_argument("file", type=Path, help="File to upload.")
    parser.add_argument("--url", required=True, help="Authorized multipart upload endpoint.")
    parser.add_argument("--format", required=True, choices=("txt",), help="Allowed file format.")
    parser.add_argument(
        "--size-limit", required=True, type=positive_size, metavar="BYTES",
        help="Maximum file size in bytes.",
    )
    args = parser.parse_args()

    try:
        url = urlsplit(args.url)
        if (
            not url.hostname
            or url.username is not None
            or url.password is not None
            or url.fragment
            or (url.scheme != "https" and not (
                url.scheme == "http" and url.hostname in ("localhost", "127.0.0.1", "::1")
            ))
        ):
            raise ValueError("URL must be HTTPS, or HTTP on localhost, without credentials or a fragment")
        if args.file.suffix.lower() != f".{args.format}":
            raise ValueError(f"file must have a .{args.format} extension")
        if not args.file.is_file():
            raise ValueError("file must be a readable regular file")
        with args.file.open("rb") as source:
            data = source.read(args.size_limit + 1)
        if len(data) > args.size_limit:
            raise ValueError("file exceeds the size limit")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("file must contain valid UTF-8 text") from error
        if not text.strip() or "\0" in text:
            raise ValueError("file must contain non-empty text without NUL characters")

        boundary = uuid4().hex
        filename = quote(args.file.name, safe="")
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            "Content-Type: text/plain; charset=utf-8\r\n\r\n"
        ).encode("ascii") + data + f"\r\n--{boundary}--\r\n".encode("ascii")
        request = Request(
            args.url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with build_opener(NoRedirect()).open(request, timeout=30) as response:
            if not 200 <= response.status < 300:
                raise ValueError(f"upload failed with HTTP status {response.status}")
            print(f"Upload succeeded (HTTP {response.status}).")
    except HTTPError as error:
        parser.exit(1, f"Error: upload failed with HTTP status {error.code}.\n")
    except (OSError, URLError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
