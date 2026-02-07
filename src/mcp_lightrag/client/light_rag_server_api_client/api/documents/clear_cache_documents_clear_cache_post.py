from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clear_cache_request import ClearCacheRequest
from ...models.clear_cache_response import ClearCacheResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ClearCacheRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_api_key_header_value: None | str | Unset
    if isinstance(api_key_header_value, Unset):
        json_api_key_header_value = UNSET
    else:
        json_api_key_header_value = api_key_header_value
    params["api_key_header_value"] = json_api_key_header_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/documents/clear_cache",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClearCacheResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ClearCacheResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClearCacheResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ClearCacheRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[ClearCacheResponse | HTTPValidationError]:
    """Clear Cache

     Clear all cache data from the LLM response cache storage.

    This endpoint clears all cached LLM responses regardless of mode.
    The request body is accepted for API compatibility but is ignored.

    Args:
        request (ClearCacheRequest): The request body (ignored for compatibility).

    Returns:
        ClearCacheResponse: A response object containing the status and message.

    Raises:
        HTTPException: If an error occurs during cache clearing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (ClearCacheRequest): Request model for clearing cache

            This model is kept for API compatibility but no longer accepts any parameters.
            All cache will be cleared regardless of the request content.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClearCacheResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ClearCacheRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> ClearCacheResponse | HTTPValidationError | None:
    """Clear Cache

     Clear all cache data from the LLM response cache storage.

    This endpoint clears all cached LLM responses regardless of mode.
    The request body is accepted for API compatibility but is ignored.

    Args:
        request (ClearCacheRequest): The request body (ignored for compatibility).

    Returns:
        ClearCacheResponse: A response object containing the status and message.

    Raises:
        HTTPException: If an error occurs during cache clearing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (ClearCacheRequest): Request model for clearing cache

            This model is kept for API compatibility but no longer accepts any parameters.
            All cache will be cleared regardless of the request content.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClearCacheResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ClearCacheRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[ClearCacheResponse | HTTPValidationError]:
    """Clear Cache

     Clear all cache data from the LLM response cache storage.

    This endpoint clears all cached LLM responses regardless of mode.
    The request body is accepted for API compatibility but is ignored.

    Args:
        request (ClearCacheRequest): The request body (ignored for compatibility).

    Returns:
        ClearCacheResponse: A response object containing the status and message.

    Raises:
        HTTPException: If an error occurs during cache clearing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (ClearCacheRequest): Request model for clearing cache

            This model is kept for API compatibility but no longer accepts any parameters.
            All cache will be cleared regardless of the request content.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClearCacheResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ClearCacheRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> ClearCacheResponse | HTTPValidationError | None:
    """Clear Cache

     Clear all cache data from the LLM response cache storage.

    This endpoint clears all cached LLM responses regardless of mode.
    The request body is accepted for API compatibility but is ignored.

    Args:
        request (ClearCacheRequest): The request body (ignored for compatibility).

    Returns:
        ClearCacheResponse: A response object containing the status and message.

    Raises:
        HTTPException: If an error occurs during cache clearing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (ClearCacheRequest): Request model for clearing cache

            This model is kept for API compatibility but no longer accepts any parameters.
            All cache will be cleared regardless of the request content.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClearCacheResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
