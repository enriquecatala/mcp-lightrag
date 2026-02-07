from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.status_counts_response import StatusCountsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    api_key_header_value: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_api_key_header_value: None | str | Unset
    if isinstance(api_key_header_value, Unset):
        json_api_key_header_value = UNSET
    else:
        json_api_key_header_value = api_key_header_value
    params["api_key_header_value"] = json_api_key_header_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/documents/status_counts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | StatusCountsResponse | None:
    if response.status_code == 200:
        response_200 = StatusCountsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | StatusCountsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | StatusCountsResponse]:
    """Get Document Status Counts

     Get counts of documents by status.

    This endpoint retrieves the count of documents in each processing status
    (PENDING, PROCESSING, PROCESSED, FAILED) for all documents in the system.

    Returns:
        StatusCountsResponse: A response object containing status counts

    Raises:
        HTTPException: If an error occurs while retrieving status counts (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | StatusCountsResponse]
    """

    kwargs = _get_kwargs(
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | StatusCountsResponse | None:
    """Get Document Status Counts

     Get counts of documents by status.

    This endpoint retrieves the count of documents in each processing status
    (PENDING, PROCESSING, PROCESSED, FAILED) for all documents in the system.

    Returns:
        StatusCountsResponse: A response object containing status counts

    Raises:
        HTTPException: If an error occurs while retrieving status counts (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | StatusCountsResponse
    """

    return sync_detailed(
        client=client,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | StatusCountsResponse]:
    """Get Document Status Counts

     Get counts of documents by status.

    This endpoint retrieves the count of documents in each processing status
    (PENDING, PROCESSING, PROCESSED, FAILED) for all documents in the system.

    Returns:
        StatusCountsResponse: A response object containing status counts

    Raises:
        HTTPException: If an error occurs while retrieving status counts (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | StatusCountsResponse]
    """

    kwargs = _get_kwargs(
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | StatusCountsResponse | None:
    """Get Document Status Counts

     Get counts of documents by status.

    This endpoint retrieves the count of documents in each processing status
    (PENDING, PROCESSING, PROCESSED, FAILED) for all documents in the system.

    Returns:
        StatusCountsResponse: A response object containing status counts

    Raises:
        HTTPException: If an error occurs while retrieving status counts (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | StatusCountsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
