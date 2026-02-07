from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.track_status_response import TrackStatusResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    track_id: str,
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
        "url": "/documents/track_status/{track_id}".format(
            track_id=quote(str(track_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TrackStatusResponse | None:
    if response.status_code == 200:
        response_200 = TrackStatusResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TrackStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    track_id: str,
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | TrackStatusResponse]:
    """Get Track Status

     Get the processing status of documents by tracking ID.

    This endpoint retrieves all documents associated with a specific tracking ID,
    allowing users to monitor the processing progress of their uploaded files or inserted texts.

    Args:
        track_id (str): The tracking ID returned from upload, text, or texts endpoints

    Returns:
        TrackStatusResponse: A response object containing:
            - track_id: The tracking ID
            - documents: List of documents associated with this track_id
            - total_count: Total number of documents for this track_id

    Raises:
        HTTPException: If track_id is invalid (400) or an error occurs (500).

    Args:
        track_id (str):
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TrackStatusResponse]
    """

    kwargs = _get_kwargs(
        track_id=track_id,
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    track_id: str,
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | TrackStatusResponse | None:
    """Get Track Status

     Get the processing status of documents by tracking ID.

    This endpoint retrieves all documents associated with a specific tracking ID,
    allowing users to monitor the processing progress of their uploaded files or inserted texts.

    Args:
        track_id (str): The tracking ID returned from upload, text, or texts endpoints

    Returns:
        TrackStatusResponse: A response object containing:
            - track_id: The tracking ID
            - documents: List of documents associated with this track_id
            - total_count: Total number of documents for this track_id

    Raises:
        HTTPException: If track_id is invalid (400) or an error occurs (500).

    Args:
        track_id (str):
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TrackStatusResponse
    """

    return sync_detailed(
        track_id=track_id,
        client=client,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    track_id: str,
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | TrackStatusResponse]:
    """Get Track Status

     Get the processing status of documents by tracking ID.

    This endpoint retrieves all documents associated with a specific tracking ID,
    allowing users to monitor the processing progress of their uploaded files or inserted texts.

    Args:
        track_id (str): The tracking ID returned from upload, text, or texts endpoints

    Returns:
        TrackStatusResponse: A response object containing:
            - track_id: The tracking ID
            - documents: List of documents associated with this track_id
            - total_count: Total number of documents for this track_id

    Raises:
        HTTPException: If track_id is invalid (400) or an error occurs (500).

    Args:
        track_id (str):
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TrackStatusResponse]
    """

    kwargs = _get_kwargs(
        track_id=track_id,
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    track_id: str,
    *,
    client: AuthenticatedClient,
    api_key_header_value: None | str | Unset = UNSET,
) -> HTTPValidationError | TrackStatusResponse | None:
    """Get Track Status

     Get the processing status of documents by tracking ID.

    This endpoint retrieves all documents associated with a specific tracking ID,
    allowing users to monitor the processing progress of their uploaded files or inserted texts.

    Args:
        track_id (str): The tracking ID returned from upload, text, or texts endpoints

    Returns:
        TrackStatusResponse: A response object containing:
            - track_id: The tracking ID
            - documents: List of documents associated with this track_id
            - total_count: Total number of documents for this track_id

    Raises:
        HTTPException: If track_id is invalid (400) or an error occurs (500).

    Args:
        track_id (str):
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TrackStatusResponse
    """

    return (
        await asyncio_detailed(
            track_id=track_id,
            client=client,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
