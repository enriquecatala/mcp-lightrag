from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.documents_request import DocumentsRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_docs_response import PaginatedDocsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DocumentsRequest,
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
        "url": "/documents/paginated",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedDocsResponse | None:
    if response.status_code == 200:
        response_200 = PaginatedDocsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PaginatedDocsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DocumentsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedDocsResponse]:
    """Get Documents Paginated

     Get documents with pagination support.

    This endpoint retrieves documents with pagination, filtering, and sorting capabilities.
    It provides better performance for large document collections by loading only the
    requested page of data.

    Args:
        request (DocumentsRequest): The request body containing pagination parameters

    Returns:
        PaginatedDocsResponse: A response object containing:
            - documents: List of documents for the current page
            - pagination: Pagination information (page, total_count, etc.)
            - status_counts: Count of documents by status for all documents

    Raises:
        HTTPException: If an error occurs while retrieving documents (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DocumentsRequest): Request model for paginated document queries

            Attributes:
                status_filter: Filter by document status, None for all statuses
                page: Page number (1-based)
                page_size: Number of documents per page (10-200)
                sort_field: Field to sort by ('created_at', 'updated_at', 'id', 'file_path')
                sort_direction: Sort direction ('asc' or 'desc') Example: {'page': 1, 'page_size': 50,
            'sort_direction': 'desc', 'sort_field': 'updated_at', 'status_filter': 'PROCESSED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedDocsResponse]
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
    body: DocumentsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedDocsResponse | None:
    """Get Documents Paginated

     Get documents with pagination support.

    This endpoint retrieves documents with pagination, filtering, and sorting capabilities.
    It provides better performance for large document collections by loading only the
    requested page of data.

    Args:
        request (DocumentsRequest): The request body containing pagination parameters

    Returns:
        PaginatedDocsResponse: A response object containing:
            - documents: List of documents for the current page
            - pagination: Pagination information (page, total_count, etc.)
            - status_counts: Count of documents by status for all documents

    Raises:
        HTTPException: If an error occurs while retrieving documents (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DocumentsRequest): Request model for paginated document queries

            Attributes:
                status_filter: Filter by document status, None for all statuses
                page: Page number (1-based)
                page_size: Number of documents per page (10-200)
                sort_field: Field to sort by ('created_at', 'updated_at', 'id', 'file_path')
                sort_direction: Sort direction ('asc' or 'desc') Example: {'page': 1, 'page_size': 50,
            'sort_direction': 'desc', 'sort_field': 'updated_at', 'status_filter': 'PROCESSED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedDocsResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DocumentsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedDocsResponse]:
    """Get Documents Paginated

     Get documents with pagination support.

    This endpoint retrieves documents with pagination, filtering, and sorting capabilities.
    It provides better performance for large document collections by loading only the
    requested page of data.

    Args:
        request (DocumentsRequest): The request body containing pagination parameters

    Returns:
        PaginatedDocsResponse: A response object containing:
            - documents: List of documents for the current page
            - pagination: Pagination information (page, total_count, etc.)
            - status_counts: Count of documents by status for all documents

    Raises:
        HTTPException: If an error occurs while retrieving documents (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DocumentsRequest): Request model for paginated document queries

            Attributes:
                status_filter: Filter by document status, None for all statuses
                page: Page number (1-based)
                page_size: Number of documents per page (10-200)
                sort_field: Field to sort by ('created_at', 'updated_at', 'id', 'file_path')
                sort_direction: Sort direction ('asc' or 'desc') Example: {'page': 1, 'page_size': 50,
            'sort_direction': 'desc', 'sort_field': 'updated_at', 'status_filter': 'PROCESSED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedDocsResponse]
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
    body: DocumentsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedDocsResponse | None:
    """Get Documents Paginated

     Get documents with pagination support.

    This endpoint retrieves documents with pagination, filtering, and sorting capabilities.
    It provides better performance for large document collections by loading only the
    requested page of data.

    Args:
        request (DocumentsRequest): The request body containing pagination parameters

    Returns:
        PaginatedDocsResponse: A response object containing:
            - documents: List of documents for the current page
            - pagination: Pagination information (page, total_count, etc.)
            - status_counts: Count of documents by status for all documents

    Raises:
        HTTPException: If an error occurs while retrieving documents (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DocumentsRequest): Request model for paginated document queries

            Attributes:
                status_filter: Filter by document status, None for all statuses
                page: Page number (1-based)
                page_size: Number of documents per page (10-200)
                sort_field: Field to sort by ('created_at', 'updated_at', 'id', 'file_path')
                sort_direction: Sort direction ('asc' or 'desc') Example: {'page': 1, 'page_size': 50,
            'sort_direction': 'desc', 'sort_field': 'updated_at', 'status_filter': 'PROCESSED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedDocsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
