from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_doc_by_id_response import DeleteDocByIdResponse
from ...models.delete_doc_request import DeleteDocRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DeleteDocRequest,
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
        "method": "delete",
        "url": "/documents/delete_document",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteDocByIdResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeleteDocByIdResponse.from_dict(response.json())

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
) -> Response[DeleteDocByIdResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DeleteDocRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[DeleteDocByIdResponse | HTTPValidationError]:
    r"""Delete a document and all its associated data by its ID.

     Delete documents and all their associated data by their IDs using background processing.

    Deletes specific documents and all their associated data, including their status,
    text chunks, vector embeddings, and any related graph data. When requested,
    cached LLM extraction responses are removed after graph deletion/rebuild completes.
    The deletion process runs in the background to avoid blocking the client connection.

    This operation is irreversible and will interact with the pipeline status.

    Args:
        delete_request (DeleteDocRequest): The request containing the document IDs and deletion options.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        DeleteDocByIdResponse: The result of the deletion operation.
            - status=\"deletion_started\": The document deletion has been initiated in the background.
            - status=\"busy\": The pipeline is busy with another operation.

    Raises:
        HTTPException:
          - 500: If an unexpected internal error occurs during initialization.

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteDocRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDocByIdResponse | HTTPValidationError]
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
    body: DeleteDocRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> DeleteDocByIdResponse | HTTPValidationError | None:
    r"""Delete a document and all its associated data by its ID.

     Delete documents and all their associated data by their IDs using background processing.

    Deletes specific documents and all their associated data, including their status,
    text chunks, vector embeddings, and any related graph data. When requested,
    cached LLM extraction responses are removed after graph deletion/rebuild completes.
    The deletion process runs in the background to avoid blocking the client connection.

    This operation is irreversible and will interact with the pipeline status.

    Args:
        delete_request (DeleteDocRequest): The request containing the document IDs and deletion options.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        DeleteDocByIdResponse: The result of the deletion operation.
            - status=\"deletion_started\": The document deletion has been initiated in the background.
            - status=\"busy\": The pipeline is busy with another operation.

    Raises:
        HTTPException:
          - 500: If an unexpected internal error occurs during initialization.

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteDocRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteDocByIdResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DeleteDocRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[DeleteDocByIdResponse | HTTPValidationError]:
    r"""Delete a document and all its associated data by its ID.

     Delete documents and all their associated data by their IDs using background processing.

    Deletes specific documents and all their associated data, including their status,
    text chunks, vector embeddings, and any related graph data. When requested,
    cached LLM extraction responses are removed after graph deletion/rebuild completes.
    The deletion process runs in the background to avoid blocking the client connection.

    This operation is irreversible and will interact with the pipeline status.

    Args:
        delete_request (DeleteDocRequest): The request containing the document IDs and deletion options.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        DeleteDocByIdResponse: The result of the deletion operation.
            - status=\"deletion_started\": The document deletion has been initiated in the background.
            - status=\"busy\": The pipeline is busy with another operation.

    Raises:
        HTTPException:
          - 500: If an unexpected internal error occurs during initialization.

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteDocRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDocByIdResponse | HTTPValidationError]
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
    body: DeleteDocRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> DeleteDocByIdResponse | HTTPValidationError | None:
    r"""Delete a document and all its associated data by its ID.

     Delete documents and all their associated data by their IDs using background processing.

    Deletes specific documents and all their associated data, including their status,
    text chunks, vector embeddings, and any related graph data. When requested,
    cached LLM extraction responses are removed after graph deletion/rebuild completes.
    The deletion process runs in the background to avoid blocking the client connection.

    This operation is irreversible and will interact with the pipeline status.

    Args:
        delete_request (DeleteDocRequest): The request containing the document IDs and deletion options.
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        DeleteDocByIdResponse: The result of the deletion operation.
            - status=\"deletion_started\": The document deletion has been initiated in the background.
            - status=\"busy\": The pipeline is busy with another operation.

    Raises:
        HTTPException:
          - 500: If an unexpected internal error occurs during initialization.

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteDocRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteDocByIdResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
