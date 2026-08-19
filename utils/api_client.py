import requests


def _url(base_url, path):
    return base_url.rstrip("/") + "/" + path.lstrip("/")


def api_get(path, base_url, timeout=20):
    try:
        r = requests.get(_url(base_url, path), timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        return {"_error": str(e), "status_code": getattr(e.response, "status_code", None)}
    except ValueError as e:
        return {"_error": f"Invalid JSON response: {e}"}


def api_post(path, base_url, payload=None, timeout=45):
    try:
        r = requests.post(_url(base_url, path), json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        detail = None
        if getattr(e, "response", None) is not None:
            try:
                detail = e.response.json().get("detail")
            except Exception:
                detail = e.response.text
        return {"_error": detail or str(e), "status_code": getattr(e.response, "status_code", None)}
    except ValueError as e:
        return {"_error": f"Invalid JSON response: {e}"}


def backend_health(base_url):
    try:
        r = requests.get(_url(base_url, "/health"), timeout=3)
        return r.ok
    except requests.RequestException:
        return False
