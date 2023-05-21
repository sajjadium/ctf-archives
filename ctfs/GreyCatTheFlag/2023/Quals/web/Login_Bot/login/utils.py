from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    """Check if the target URL is safe to redirect to. Only works for within Flask request context."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc