from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.insert_response import InsertResponse
from ...models.insert_texts_request import InsertTextsRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: InsertTextsRequest,
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
        "url": "/documents/texts",
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
    body: InsertTextsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InsertResponse]:
    """Insert Texts

     Insert multiple texts into the RAG system.

    This endpoint allows you to insert multiple text entries into the RAG system
    in a single request.

    Args:
        request (InsertTextsRequest): The request body containing the list of texts.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextsRequest): Request model for inserting multiple text documents

            Attributes:
                texts: List of text contents to be inserted into the RAG system
                file_sources: Sources of the texts (optional) Example: {'file_sources': ['First file
            source (optional)'], 'texts': ['This is the first text to be inserted.', 'This is the
            second text to be inserted.']}.

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
    body: InsertTextsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | InsertResponse | None:
    """Insert Texts

     Insert multiple texts into the RAG system.

    This endpoint allows you to insert multiple text entries into the RAG system
    in a single request.

    Args:
        request (InsertTextsRequest): The request body containing the list of texts.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextsRequest): Request model for inserting multiple text documents

            Attributes:
                texts: List of text contents to be inserted into the RAG system
                file_sources: Sources of the texts (optional) Example: {'file_sources': ['First file
            source (optional)'], 'texts': ['This is the first text to be inserted.', 'This is the
            second text to be inserted.']}.

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
    body: InsertTextsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InsertResponse]:
    """Insert Texts

     Insert multiple texts into the RAG system.

    This endpoint allows you to insert multiple text entries into the RAG system
    in a single request.

    Args:
        request (InsertTextsRequest): The request body containing the list of texts.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextsRequest): Request model for inserting multiple text documents

            Attributes:
                texts: List of text contents to be inserted into the RAG system
                file_sources: Sources of the texts (optional) Example: {'file_sources': ['First file
            source (optional)'], 'texts': ['This is the first text to be inserted.', 'This is the
            second text to be inserted.']}.

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
    body: InsertTextsRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | InsertResponse | None:
    """Insert Texts

     Insert multiple texts into the RAG system.

    This endpoint allows you to insert multiple text entries into the RAG system
    in a single request.

    Args:
        request (InsertTextsRequest): The request body containing the list of texts.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        InsertResponse: A response object containing the status of the operation.

    Raises:
        HTTPException: If an error occurs during text processing (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (InsertTextsRequest): Request model for inserting multiple text documents

            Attributes:
                texts: List of text contents to be inserted into the RAG system
                file_sources: Sources of the texts (optional) Example: {'file_sources': ['First file
            source (optional)'], 'texts': ['This is the first text to be inserted.', 'This is the
            second text to be inserted.']}.

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
