from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_pipeline_response import CancelPipelineResponse
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
        "method": "post",
        "url": "/documents/cancel_pipeline",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CancelPipelineResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CancelPipelineResponse.from_dict(response.json())

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
) -> Response[CancelPipelineResponse | HTTPValidationError]:
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
) -> Response[CancelPipelineResponse | HTTPValidationError]:
    r"""Cancel Pipeline

     Request cancellation of the currently running pipeline.

    This endpoint sets a cancellation flag in the pipeline status. The pipeline will:
    1. Check this flag at key processing points
    2. Stop processing new documents
    3. Cancel all running document processing tasks
    4. Mark all PROCESSING documents as FAILED with reason \"User cancelled\"

    The cancellation is graceful and ensures data consistency. Documents that have
    completed processing will remain in PROCESSED status.

    Returns:
        CancelPipelineResponse: Response with status and message
            - status=\"cancellation_requested\": Cancellation flag has been set
            - status=\"not_busy\": Pipeline is not currently running

    Raises:
        HTTPException: If an error occurs while setting cancellation flag (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelPipelineResponse | HTTPValidationError]
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
) -> CancelPipelineResponse | HTTPValidationError | None:
    r"""Cancel Pipeline

     Request cancellation of the currently running pipeline.

    This endpoint sets a cancellation flag in the pipeline status. The pipeline will:
    1. Check this flag at key processing points
    2. Stop processing new documents
    3. Cancel all running document processing tasks
    4. Mark all PROCESSING documents as FAILED with reason \"User cancelled\"

    The cancellation is graceful and ensures data consistency. Documents that have
    completed processing will remain in PROCESSED status.

    Returns:
        CancelPipelineResponse: Response with status and message
            - status=\"cancellation_requested\": Cancellation flag has been set
            - status=\"not_busy\": Pipeline is not currently running

    Raises:
        HTTPException: If an error occurs while setting cancellation flag (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelPipelineResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[CancelPipelineResponse | HTTPValidationError]:
    r"""Cancel Pipeline

     Request cancellation of the currently running pipeline.

    This endpoint sets a cancellation flag in the pipeline status. The pipeline will:
    1. Check this flag at key processing points
    2. Stop processing new documents
    3. Cancel all running document processing tasks
    4. Mark all PROCESSING documents as FAILED with reason \"User cancelled\"

    The cancellation is graceful and ensures data consistency. Documents that have
    completed processing will remain in PROCESSED status.

    Returns:
        CancelPipelineResponse: Response with status and message
            - status=\"cancellation_requested\": Cancellation flag has been set
            - status=\"not_busy\": Pipeline is not currently running

    Raises:
        HTTPException: If an error occurs while setting cancellation flag (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelPipelineResponse | HTTPValidationError]
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
) -> CancelPipelineResponse | HTTPValidationError | None:
    r"""Cancel Pipeline

     Request cancellation of the currently running pipeline.

    This endpoint sets a cancellation flag in the pipeline status. The pipeline will:
    1. Check this flag at key processing points
    2. Stop processing new documents
    3. Cancel all running document processing tasks
    4. Mark all PROCESSING documents as FAILED with reason \"User cancelled\"

    The cancellation is graceful and ensures data consistency. Documents that have
    completed processing will remain in PROCESSED status.

    Returns:
        CancelPipelineResponse: Response with status and message
            - status=\"cancellation_requested\": Cancellation flag has been set
            - status=\"not_busy\": Pipeline is not currently running

    Raises:
        HTTPException: If an error occurs while setting cancellation flag (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelPipelineResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
