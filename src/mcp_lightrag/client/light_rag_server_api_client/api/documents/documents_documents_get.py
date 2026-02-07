from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.docs_statuses_response import DocsStatusesResponse
from ...models.http_validation_error import HTTPValidationError
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
        "url": "/documents",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DocsStatusesResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DocsStatusesResponse.from_dict(response.json())

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
) -> Response[DocsStatusesResponse | HTTPValidationError]:
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
) -> Response[DocsStatusesResponse | HTTPValidationError]:
    """Documents

     Get the status of all documents in the system. This endpoint is deprecated; use /documents/paginated
    instead.
    To prevent excessive resource consumption, a maximum of 1,000 records is returned.

    This endpoint retrieves the current status of all documents, grouped by their
    processing status (PENDING, PROCESSING, PREPROCESSED, PROCESSED, FAILED). The results are
    limited to 1000 total documents with fair distribution across all statuses.

    Returns:
        DocsStatusesResponse: A response object containing a dictionary where keys are
                            DocStatus values and values are lists of DocStatusResponse
                            objects representing documents in each status category.
                            Maximum 1000 documents total will be returned.

    Raises:
        HTTPException: If an error occurs while retrieving document statuses (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocsStatusesResponse | HTTPValidationError]
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
) -> DocsStatusesResponse | HTTPValidationError | None:
    """Documents

     Get the status of all documents in the system. This endpoint is deprecated; use /documents/paginated
    instead.
    To prevent excessive resource consumption, a maximum of 1,000 records is returned.

    This endpoint retrieves the current status of all documents, grouped by their
    processing status (PENDING, PROCESSING, PREPROCESSED, PROCESSED, FAILED). The results are
    limited to 1000 total documents with fair distribution across all statuses.

    Returns:
        DocsStatusesResponse: A response object containing a dictionary where keys are
                            DocStatus values and values are lists of DocStatusResponse
                            objects representing documents in each status category.
                            Maximum 1000 documents total will be returned.

    Raises:
        HTTPException: If an error occurs while retrieving document statuses (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocsStatusesResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[DocsStatusesResponse | HTTPValidationError]:
    """Documents

     Get the status of all documents in the system. This endpoint is deprecated; use /documents/paginated
    instead.
    To prevent excessive resource consumption, a maximum of 1,000 records is returned.

    This endpoint retrieves the current status of all documents, grouped by their
    processing status (PENDING, PROCESSING, PREPROCESSED, PROCESSED, FAILED). The results are
    limited to 1000 total documents with fair distribution across all statuses.

    Returns:
        DocsStatusesResponse: A response object containing a dictionary where keys are
                            DocStatus values and values are lists of DocStatusResponse
                            objects representing documents in each status category.
                            Maximum 1000 documents total will be returned.

    Raises:
        HTTPException: If an error occurs while retrieving document statuses (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocsStatusesResponse | HTTPValidationError]
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
) -> DocsStatusesResponse | HTTPValidationError | None:
    """Documents

     Get the status of all documents in the system. This endpoint is deprecated; use /documents/paginated
    instead.
    To prevent excessive resource consumption, a maximum of 1,000 records is returned.

    This endpoint retrieves the current status of all documents, grouped by their
    processing status (PENDING, PROCESSING, PREPROCESSED, PROCESSED, FAILED). The results are
    limited to 1000 total documents with fair distribution across all statuses.

    Returns:
        DocsStatusesResponse: A response object containing a dictionary where keys are
                            DocStatus values and values are lists of DocStatusResponse
                            objects representing documents in each status category.
                            Maximum 1000 documents total will be returned.

    Raises:
        HTTPException: If an error occurs while retrieving document statuses (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocsStatusesResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
