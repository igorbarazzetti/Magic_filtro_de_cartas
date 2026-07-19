from __future__ import annotations

from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response


app = FastAPI(title="Magic MTG Finder Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRYFALL_BASE = "https://api.scryfall.com"
FRONTEND_FILE = Path(__file__).resolve().parents[1] / "magic-mtg-landing.html"
TIMEOUT_SECONDS = 20.0


async def _proxy_request(request: Request, path: str) -> Response:
    query = dict(request.query_params)
    target = f"{SCRYFALL_BASE}/{path.lstrip('/')}"
    timeout = httpx.Timeout(timeout=TIMEOUT_SECONDS)

    async with httpx.AsyncClient(timeout=timeout) as client:
        upstream = await client.get(target, params=query)

    content = upstream.content
    headers = {
        "content-type": upstream.headers.get("content-type", "application/json; charset=utf-8"),
        "cache-control": upstream.headers.get("cache-control", "no-cache"),
    }

    return Response(
        content=content,
        status_code=upstream.status_code,
        headers=headers,
    )


@app.get("/api/health")
async def api_health() -> dict:
    return {"ok": True, "service": "magic-mtg-landing-proxy"}


@app.api_route("/api/scryfall/{path:path}", methods=["GET"])
async def scryfall_proxy(path: str, request: Request) -> Response:
    return await _proxy_request(request, path)


@app.get("/")
@app.get("/magic-mtg-landing.html")
async def serve_frontend():
    return FileResponse(FRONTEND_FILE)


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    # Single-page fallback to keep direct links working.
    if full_path.startswith("api/"):
        return JSONResponse(
            status_code=404,
            content={"error": "Not Found"},
        )
    if FRONTEND_FILE.exists():
        return FileResponse(FRONTEND_FILE)
    return JSONResponse(status_code=404, content={"error": "File not found"})
