from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.insert_response import InsertResponse
from ...models.insert_text_request import InsertTextRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: InsertTextRequest,
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
        "url": "/documents/text",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | InsertResponse | None:
    if response.status_code == 200:
        response_200 = InsertResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | InsertResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InsertTextRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InsertResponse]:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextRequest): Request model for inserting a single text document

            Attributes:
                text: The text content to be inserted into the RAG system
                file_source: Source of the text (optional) Example: {'file_source': 'Source of the
            text (optional)', 'text': 'This is a sample text to be inserted into the RAG system.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InsertResponse]
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
    body: InsertTextRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | InsertResponse | None:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextRequest): Request model for inserting a single text document

            Attributes:
                text: The text content to be inserted into the RAG system
                file_source: Source of the text (optional) Example: {'file_source': 'Source of the
            text (optional)', 'text': 'This is a sample text to be inserted into the RAG system.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InsertResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InsertTextRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InsertResponse]:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextRequest): Request model for inserting a single text document

            Attributes:
                text: The text content to be inserted into the RAG system
                file_source: Source of the text (optional) Example: {'file_source': 'Source of the
            text (optional)', 'text': 'This is a sample text to be inserted into the RAG system.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InsertResponse]
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
    body: InsertTextRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | InsertResponse | None:
    """Insert Text

     Insert text into the RAG system.

    This endpoint allows you to insert text data into the RAG system for later retrieval
    and use in generating responses.

    Args:
        request (InsertTextRequest): The request body containing the text to be inserted.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextRequest): Request model for inserting a single text document

            Attributes:
                text: The text content to be inserted into the RAG system
                file_source: Source of the text (optional) Example: {'file_source': 'Source of the
            text (optional)', 'text': 'This is a sample text to be inserted into the RAG system.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InsertResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
