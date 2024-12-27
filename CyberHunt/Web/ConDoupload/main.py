import glob
import importlib
from pathlib import Path as Pathlib
from fastapi import FastAPI, HTTPException, Response, Request
from module.errorhandler import add_error_handler
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from collections import OrderedDict
from fastapi.middleware.cors import CORSMiddleware
import re
from fastapi.staticfiles import StaticFiles

CSP: dict[str, str | list[str]] = {
    "default-src": "'self'",
    "connect-src": ["*"],
    "script-src": ["'self'", "'unsafe-inline'"],
    "style-src-elem": [
        # For SWAGGER UI
        "'self'",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.4/jquery.min.js",
        "https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    ],
}


def parse_policy(policy: dict[str, str | list[str]] | str) -> str:
    """Parse a given policy dict to string."""
    if isinstance(policy, str):
        # parse the string into a policy dict
        policy_string = policy
        policy = OrderedDict()

        for policy_part in policy_string.split(";"):
            policy_parts = policy_part.strip().split(" ")
            policy[policy_parts[0]] = " ".join(policy_parts[1:])

    policies = []
    for section, content in policy.items():
        if not isinstance(content, str):
            content = " ".join(content)
        policy_part = f"{section} {content}"

        policies.append(policy_part)

    parsed_policy = "; ".join(policies)

    return parsed_policy


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    def __init__(self, app: FastAPI, csp: bool = True) -> None:
        """Init SecurityHeadersMiddleware.

        :param app: FastAPI instance
        :param no_csp: If no CSP should be used;
            defaults to :py:obj:`False`
        """
        super().__init__(app)
        self.csp = csp

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch of the middleware.

        :param request: Incoming request
        :param call_next: Function to process the request
        :return: Return response coming from from processed request
        """
        headers = {
            "Content-Security-Policy": "" if not self.csp else parse_policy(CSP),
        }
        response = await call_next(request)
        response.headers.update(headers)

        return response
    
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SecurityHeadersMiddleware, csp=True)


for module_filename in glob.glob("./routes/*"):
    if module_filename.endswith(".py"):
        module_name = f"routes.{module_filename.split('/')[-1][:-3]}"
        module = importlib.import_module(module_name)
        app.include_router(module.app)

add_error_handler(app)

def sanitize_path(string):
    pattern = r'(\A/)|(\.\.)'
    replaced_string = re.sub(pattern, '', string)
    if re.search(pattern, replaced_string):
        return sanitize_path(replaced_string)
    return replaced_string


@app.get("/uploads/{path:path}")
async def static_file(path: str):
    if (filepath := (Pathlib("uploads")/sanitize_path(path))).exists():
        return Response(filepath.read_bytes())
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/healthcheck")
async def health_check():
    return {"message": "ok"}


