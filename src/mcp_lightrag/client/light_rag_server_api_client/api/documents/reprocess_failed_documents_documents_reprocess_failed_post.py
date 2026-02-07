from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.reprocess_response import ReprocessResponse
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
        "url": "/documents/reprocess_failed",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ReprocessResponse | None:
    if response.status_code == 200:
        response_200 = ReprocessResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ReprocessResponse]:
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
) -> Response[HTTPValidationError | ReprocessResponse]:
    """Reprocess Failed Documents

     Reprocess failed and pending documents.

    This endpoint triggers the document processing pipeline which automatically
    picks up and reprocesses documents in the following statuses:
    - FAILED: Documents that failed during previous processing attempts
    - PENDING: Documents waiting to be processed
    - PROCESSING: Documents with abnormally terminated processing (e.g., server crashes)

    This is useful for recovering from server crashes, network errors, LLM service
    outages, or other temporary failures that caused document processing to fail.

    The processing happens in the background and can be monitored by checking the
    pipeline status. The reprocessed documents retain their original track_id from
    initial upload, so use their original track_id to monitor progress.

    Returns:
        ReprocessResponse: Response with status and message.
            track_id is always empty string because reprocessed documents retain
            their original track_id from initial upload.

    Raises:
        HTTPException: If an error occurs while initiating reprocessing (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReprocessResponse]
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
) -> HTTPValidationError | ReprocessResponse | None:
    """Reprocess Failed Documents

     Reprocess failed and pending documents.

    This endpoint triggers the document processing pipeline which automatically
    picks up and reprocesses documents in the following statuses:
    - FAILED: Documents that failed during previous processing attempts
    - PENDING: Documents waiting to be processed
    - PROCESSING: Documents with abnormally terminated processing (e.g., server crashes)

    This is useful for recovering from server crashes, network errors, LLM service
    outages, or other temporary failures that caused document processing to fail.

    The processing happens in the background and can be monitored by checking the
    pipeline status. The reprocessed documents retain their original track_id from
    initial upload, so use their original track_id to monitor progress.

    Returns:
        ReprocessResponse: Response with status and message.
            track_id is always empty string because reprocessed documents retain
            their original track_id from initial upload.

    Raises:
        HTTPException: If an error occurs while initiating reprocessing (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReprocessResponse
    """

    return sync_detailed(
        client=client,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReprocessResponse]:
    """Reprocess Failed Documents

     Reprocess failed and pending documents.

    This endpoint triggers the document processing pipeline which automatically
    picks up and reprocesses documents in the following statuses:
    - FAILED: Documents that failed during previous processing attempts
    - PENDING: Documents waiting to be processed
    - PROCESSING: Documents with abnormally terminated processing (e.g., server crashes)

    This is useful for recovering from server crashes, network errors, LLM service
    outages, or other temporary failures that caused document processing to fail.

    The processing happens in the background and can be monitored by checking the
    pipeline status. The reprocessed documents retain their original track_id from
    initial upload, so use their original track_id to monitor progress.

    Returns:
        ReprocessResponse: Response with status and message.
            track_id is always empty string because reprocessed documents retain
            their original track_id from initial upload.

    Raises:
        HTTPException: If an error occurs while initiating reprocessing (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReprocessResponse]
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
) -> HTTPValidationError | ReprocessResponse | None:
    """Reprocess Failed Documents

     Reprocess failed and pending documents.

    This endpoint triggers the document processing pipeline which automatically
    picks up and reprocesses documents in the following statuses:
    - FAILED: Documents that failed during previous processing attempts
    - PENDING: Documents waiting to be processed
    - PROCESSING: Documents with abnormally terminated processing (e.g., server crashes)

    This is useful for recovering from server crashes, network errors, LLM service
    outages, or other temporary failures that caused document processing to fail.

    The processing happens in the background and can be monitored by checking the
    pipeline status. The reprocessed documents retain their original track_id from
    initial upload, so use their original track_id to monitor progress.

    Returns:
        ReprocessResponse: Response with status and message.
            track_id is always empty string because reprocessed documents retain
            their original track_id from initial upload.

    Raises:
        HTTPException: If an error occurs while initiating reprocessing (500).

    Args:
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReprocessResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
