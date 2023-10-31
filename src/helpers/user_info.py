# Get user IP address from request
def get_user_ip(request) -> str | None:
    # Used when accesed behind Reverse Proxy
    ip = request.headers.get("X-Forwarded-For")
    # More than one IP may be returned
    if ip:
        ip = ip.split(", ")[0]
    # Used if hosted without Reverse Proxy
    else:
        ip = request.client.host

    return ip or None
