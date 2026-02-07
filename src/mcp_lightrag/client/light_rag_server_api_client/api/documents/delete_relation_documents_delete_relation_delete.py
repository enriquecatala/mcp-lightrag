from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_relation_request import DeleteRelationRequest
from ...models.deletion_result import DeletionResult
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DeleteRelationRequest,
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
        "url": "/documents/delete_relation",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeletionResult | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeletionResult.from_dict(response.json())

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
) -> Response[DeletionResult | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DeleteRelationRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[DeletionResult | HTTPValidationError]:
    """Delete Relation

     Delete a relationship between two entities from the knowledge graph.

    Args:
        request (DeleteRelationRequest): The request body containing the source and target entity names.

    Returns:
        DeletionResult: An object containing the outcome of the deletion process.

    Raises:
        HTTPException: If the relation is not found (404) or an error occurs (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteRelationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletionResult | HTTPValidationError]
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
    body: DeleteRelationRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> DeletionResult | HTTPValidationError | None:
    """Delete Relation

     Delete a relationship between two entities from the knowledge graph.

    Args:
        request (DeleteRelationRequest): The request body containing the source and target entity names.

    Returns:
        DeletionResult: An object containing the outcome of the deletion process.

    Raises:
        HTTPException: If the relation is not found (404) or an error occurs (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteRelationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletionResult | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DeleteRelationRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[DeletionResult | HTTPValidationError]:
    """Delete Relation

     Delete a relationship between two entities from the knowledge graph.

    Args:
        request (DeleteRelationRequest): The request body containing the source and target entity names.

    Returns:
        DeletionResult: An object containing the outcome of the deletion process.

    Raises:
        HTTPException: If the relation is not found (404) or an error occurs (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteRelationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletionResult | HTTPValidationError]
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
    body: DeleteRelationRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> DeletionResult | HTTPValidationError | None:
    """Delete Relation

     Delete a relationship between two entities from the knowledge graph.

    Args:
        request (DeleteRelationRequest): The request body containing the source and target entity names.

    Returns:
        DeletionResult: An object containing the outcome of the deletion process.

    Raises:
        HTTPException: If the relation is not found (404) or an error occurs (500).

    Args:
        api_key_header_value (None | str | Unset):
        body (DeleteRelationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletionResult | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
