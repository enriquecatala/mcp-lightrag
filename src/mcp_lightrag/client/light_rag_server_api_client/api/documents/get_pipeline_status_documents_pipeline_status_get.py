from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.pipeline_status_response import PipelineStatusResponse
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
        "url": "/documents/pipeline_status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PipelineStatusResponse | None:
    if response.status_code == 200:
        response_200 = PipelineStatusResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PipelineStatusResponse]:
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
) -> Response[HTTPValidationError | PipelineStatusResponse]:
    """Get Pipeline Status

     Get the current status of the document indexing pipeline.

    This endpoint returns information about the current state of the document processing pipeline,
    including the processing status, progress information, and history messages.

    Returns:
        PipelineStatusResponse: A response object containing:
            - autoscanned (bool): Whether auto-scan has started
            - busy (bool): Whether the pipeline is currently busy
            - job_name (str): Current job name (e.g., indexing files/indexing texts)
            - job_start (str, optional): Job start time as ISO format string
            - docs (int): Total number of documents to be indexed
            - batchs (int): Number of batches for processing documents
            - cur_batch (int): Current processing batch
            - request_pending (bool): Flag for pending request for processing
            - latest_message (str): Latest message from pipeline processing
            - history_messages (List[str], optional): List of history messages (limited to latest 1000
    entries,
              with truncation message if more than 1000 messages exist)

    Raises:
        HTTPException: If an error occurs while retrieving pipeline status (500)

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PipelineStatusResponse]
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
) -> HTTPValidationError | PipelineStatusResponse | None:
    """Get Pipeline Status

     Get the current status of the document indexing pipeline.

    This endpoint returns information about the current state of the document processing pipeline,
    including the processing status, progress information, and history messages.

    Returns:
        PipelineStatusResponse: A response object containing:
            - autoscanned (bool): Whether auto-scan has started
            - busy (bool): Whether the pipeline is currently busy
            - job_name (str): Current job name (e.g., indexing files/indexing texts)
            - job_start (str, optional): Job start time as ISO format string
            - docs (int): Total number of documents to be indexed
            - batchs (int): Number of batches for processing documents
            - cur_batch (int): Current processing batch
            - request_pending (bool): Flag for pending request for processing
            - latest_message (str): Latest message from pipeline processing
            - history_messages (List[str], optional): List of history messages (limited to latest 1000
    entries,
              with truncation message if more than 1000 messages exist)

    Raises:
        HTTPException: If an error occurs while retrieving pipeline status (500)

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PipelineStatusResponse
    """

    return sync_detailed(
        client=client,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PipelineStatusResponse]:
    """Get Pipeline Status

     Get the current status of the document indexing pipeline.

    This endpoint returns information about the current state of the document processing pipeline,
    including the processing status, progress information, and history messages.

    Returns:
        PipelineStatusResponse: A response object containing:
            - autoscanned (bool): Whether auto-scan has started
            - busy (bool): Whether the pipeline is currently busy
            - job_name (str): Current job name (e.g., indexing files/indexing texts)
            - job_start (str, optional): Job start time as ISO format string
            - docs (int): Total number of documents to be indexed
            - batchs (int): Number of batches for processing documents
            - cur_batch (int): Current processing batch
            - request_pending (bool): Flag for pending request for processing
            - latest_message (str): Latest message from pipeline processing
            - history_messages (List[str], optional): List of history messages (limited to latest 1000
    entries,
              with truncation message if more than 1000 messages exist)

    Raises:
        HTTPException: If an error occurs while retrieving pipeline status (500)

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PipelineStatusResponse]
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
) -> HTTPValidationError | PipelineStatusResponse | None:
    """Get Pipeline Status

     Get the current status of the document indexing pipeline.

    This endpoint returns information about the current state of the document processing pipeline,
    including the processing status, progress information, and history messages.

    Returns:
        PipelineStatusResponse: A response object containing:
            - autoscanned (bool): Whether auto-scan has started
            - busy (bool): Whether the pipeline is currently busy
            - job_name (str): Current job name (e.g., indexing files/indexing texts)
            - job_start (str, optional): Job start time as ISO format string
            - docs (int): Total number of documents to be indexed
            - batchs (int): Number of batches for processing documents
            - cur_batch (int): Current processing batch
            - request_pending (bool): Flag for pending request for processing
            - latest_message (str): Latest message from pipeline processing
            - history_messages (List[str], optional): List of history messages (limited to latest 1000
    entries,
              with truncation message if more than 1000 messages exist)

    Raises:
        HTTPException: If an error occurs while retrieving pipeline status (500)

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PipelineStatusResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
