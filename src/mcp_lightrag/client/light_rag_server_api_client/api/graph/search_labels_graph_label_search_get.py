from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    limit: int | Unset = 50,
    api_key_header_value: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["limit"] = limit

    json_api_key_header_value: None | str | Unset
    if isinstance(api_key_header_value, Unset):
        json_api_key_header_value = UNSET
    else:
        json_api_key_header_value = api_key_header_value
    params["api_key_header_value"] = json_api_key_header_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/graph/label/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 50,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Search Labels

     Search labels with fuzzy matching

    Args:
        q (str): Search query string
        limit (int): Maximum number of results to return (default: 50, max: 100)

    Returns:
        List[str]: List of matching labels sorted by relevance

    Args:
        q (str): Search query string
        limit (int | Unset): Maximum number of search results to return Default: 50.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        q=q,
        limit=limit,
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 50,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Search Labels

     Search labels with fuzzy matching

    Args:
        q (str): Search query string
        limit (int): Maximum number of results to return (default: 50, max: 100)

    Returns:
        List[str]: List of matching labels sorted by relevance

    Args:
        q (str): Search query string
        limit (int | Unset): Maximum number of search results to return Default: 50.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        q=q,
        limit=limit,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 50,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Search Labels

     Search labels with fuzzy matching

    Args:
        q (str): Search query string
        limit (int): Maximum number of results to return (default: 50, max: 100)

    Returns:
        List[str]: List of matching labels sorted by relevance

    Args:
        q (str): Search query string
        limit (int | Unset): Maximum number of search results to return Default: 50.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        q=q,
        limit=limit,
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 50,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Search Labels

     Search labels with fuzzy matching

    Args:
        q (str): Search query string
        limit (int): Maximum number of results to return (default: 50, max: 100)

    Returns:
        List[str]: List of matching labels sorted by relevance

    Args:
        q (str): Search query string
        limit (int | Unset): Maximum number of search results to return Default: 50.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            limit=limit,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
