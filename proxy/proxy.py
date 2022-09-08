import base64
import ipaddress
import json
import os
import random

import httpx
from fastapi import FastAPI, Request, Response

_ENV_VAR_PREFIX = "PR6XY_"

ipv6_block = os.environ.get(_ENV_VAR_PREFIX + "IPV6_BLOCK")

if ipv6_block:
    network = ipaddress.IPv6Network(ipv6_block)
    size = int(network[-1]) - int(network[0]) + 1


def get_ip(use_ipv6: bool = False) -> str:
    if ipv6_block and use_ipv6:
        random_index = random.randint(0, size)
        return str(network[random_index])
    return "0.0.0.0"


def process_ip_info(internal_params: dict) -> str:
    if "ip" in internal_params:
        return internal_params["ip"]
    return get_ip(internal_params.get("use_ipv6", False))


app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/get_random_ip")
async def get_random_ip(use_ipv6: bool = False):
    return get_ip(use_ipv6)


@app.get("/")
async def get(request: Request, internal_params: str) -> Response:
    internal_params = json.loads(internal_params)

    if not internal_params["headers"].get("Content-Type") and request.headers.get(
        "Content-Type"
    ):
        internal_params["headers"]["Content-Type"] = request.headers.get("Content-Type")

    async with httpx.AsyncHTTPTransport(
        local_address=process_ip_info(internal_params)
    ) as transport:
        async with httpx.AsyncClient(transport=transport) as client:
            try:
                response = await client.get(
                    internal_params["url"],
                    params=internal_params["params"],
                    headers=internal_params["headers"],
                    follow_redirects=True,
                )
            except Exception:
                return Response(status_code=500, headers={"X-Pr6xy-Failed": "true"})

            headers_header_data = base64.b64encode(
                json.dumps(dict(response.headers)).encode()
            ).decode("utf-8")
            headers = {
                "X-Returned-Headers": headers_header_data,
            }

            return Response(
                status_code=response.status_code,
                content=response.content,
                headers=headers,
            )


@app.post("/")
async def post(request: Request, internal_params: str) -> Response:
    internal_params = json.loads(internal_params)

    if not internal_params["headers"].get("Content-Type"):
        internal_params["headers"]["Content-Type"] = request.headers.get("Content-Type")

    async with httpx.AsyncHTTPTransport(
        local_address=get_ip(internal_params["use_ipv6"])
    ) as transport:
        async with httpx.AsyncClient(transport=transport) as client:
            try:
                response = await client.post(
                    internal_params["url"],
                    params=internal_params["params"],
                    headers=internal_params["headers"],
                    content=await request.body(),
                    follow_redirects=True,
                )
            except Exception:
                return Response(status_code=500, headers={"X-Pr6xy-Failed": "true"})

            headers_header_data = base64.b64encode(
                json.dumps(dict(response.headers)).encode()
            ).decode("utf-8")
            headers = {
                "X-Returned-Headers": headers_header_data,
            }

            return Response(
                status_code=response.status_code,
                content=response.content,
                headers=headers,
            )
