# pr6xy api documentation

## Endpoints
This application has three HTTP endpoints.

### GET /get_random_ip
This endpoint returns a string of an IP address. It takes one optional query parameter, `use_ipv6`, which is a boolean. If `use_ipv6` is true, the endpoint will return an IPv6 address. If `use_ipv6` is false or not provided, the endpoint will return an IPv4 address. For now, if it's an IPv4 address, it will be `0.0.0.0`.

### GET /
This endpoint is used to proxy GET requests. It takes one parameter, `internal_params`, which is a string. The string should be a JSON object with the following keys:
- `url`: A string. The URL to request.
- `use_ipv6`: A boolean. If true, the request will be made using a random IPv6 address. If false, the request will be made using a random IPv4 address. If not provided, the request will be made using an IPv4 address.
- `headers`: A JSON object. The headers to send with the request. If not specified here, the `Content-Type` header will be set to the header you sent to this endpoint. If you do not send a `Content-Type` header and do not specify it here, the `Content-Type` header will be not be set.
- `params`: A JSON object. The query parameters to send with the request.
- `ip`: A string. The IP address to use for the request. If not provided, a random IP will be used.

The raw data returned by the request will be returned by this endpoint. However, the headers will be returned as a Base64-encoded header named `X-Returned-Headers`. You'll need to do some logic with this if you want cookies to work properly, as the proxy does not handle that for you.

If there is an issue with the request, the server will respond with a 500 status code and no data. A `X-Pr6xy-Failed` header will be returned if the request failed. This should usually only happen when the URL is invalid, the server you are trying to request is down, or the service does not support IPv6 and you specified `use_ipv6` as true.

### POST /
This endpoint is used to proxy POST requests. You should send the raw data you want to POST. It takes one parameter, `internal_params`, which is a string. The string should be a JSON object with the following keys:
- `url`: A string. The URL to request.
- `use_ipv6`: A boolean. If true, the request will be made using a random IPv6 address. If false, the request will be made using a random IPv4 address. If not provided, the request will be made using an IPv4 address.
- `headers`: A JSON object. The headers to send with the request. If not specified here, the `Content-Type` header will be set to the header you sent to this endpoint. If you do not send a `Content-Type` header and do not specify it here, the `Content-Type` header will be not be set.
- `params`: A JSON object. The query parameters to send with the request.
- `ip`: A string. The IP address to use for the request. If not provided, a random IP will be used.

The raw data returned by the request will be returned by this endpoint. However, the headers will be returned as a Base64-encoded header named `X-Returned-Headers`. You'll need to do some logic with this if you want cookies to work properly, as the proxy does not handle that for you.

If there is an issue with the request, the server will respond with a 500 status code and no data. A `X-Pr6xy-Failed` header will be returned if the request failed. This should usually only happen when the URL is invalid, the server you are trying to request is down, or the service does not support IPv6 and you specified `use_ipv6` as true.