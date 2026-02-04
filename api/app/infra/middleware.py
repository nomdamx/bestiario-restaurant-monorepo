from flask import request
from .request_context import set_context, RequestContext
import re
 
def ctx_middleware():
    auth_header = request.headers.get("Authorization")
    accept_header = request.headers.get("Accept")
    set_context(
        RequestContext(
            user_token = get_user_token_from_header(auth_header),
            version_api = extract_api_version(accept_header)
        )
    )

def get_user_token_from_header(auth_header: str | None):
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    return auth_header.replace("Bearer ", "").strip()


API_VENDOR = "restaurant-api"
DEFAULT_VERSION = "v1"

def extract_api_version(accept_header: str | None) -> str:
    if not accept_header:
        return DEFAULT_VERSION
    
    matches = re.findall(
        rf"application/vnd\.{API_VENDOR}\.(v\d+)\+json",
        accept_header.lower()
    )
    return matches[0] if matches else DEFAULT_VERSION