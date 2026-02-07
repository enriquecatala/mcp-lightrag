from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.entity_merge_request import EntityMergeRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: EntityMergeRequest,
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
        "url": "/graph/entities/merge",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: EntityMergeRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Merge Entities

     Merge multiple entities into a single entity, preserving all relationships

    This endpoint consolidates duplicate or misspelled entities while preserving the entire
    graph structure. It's particularly useful for cleaning up knowledge graphs after document
    processing or correcting entity name variations.

    What the Merge Operation Does:
        1. Deletes the specified source entities from the knowledge graph
        2. Transfers all relationships from source entities to the target entity
        3. Intelligently merges duplicate relationships (if multiple sources have the same relationship)
        4. Updates vector embeddings for accurate retrieval and search
        5. Preserves the complete graph structure and connectivity
        6. Maintains relationship properties and metadata

    Use Cases:
        - Fixing spelling errors in entity names (e.g., \"Elon Msk\" -> \"Elon Musk\")
        - Consolidating duplicate entities discovered after document processing
        - Merging name variations (e.g., \"NY\", \"New York\", \"New York City\")
        - Cleaning up the knowledge graph for better query performance
        - Standardizing entity names across the knowledge base

    Request Body:
        entities_to_change (list[str]): List of entity names to be merged and deleted
        entity_to_change_into (str): Target entity that will receive all relationships

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Successfully merged 2 entities into 'Elon Musk'\",
            \"data\": {
                \"merged_entity\": \"Elon Musk\",
                \"deleted_entities\": [\"Elon Msk\", \"Ellon Musk\"],
                \"relationships_transferred\": 15,
                ... (merge operation details)
            }
        }

    HTTP Status Codes:
        200: Entities merged successfully
        400: Invalid request (e.g., empty entity list, target entity doesn't exist)
        500: Internal server error

    Example Request:
        POST /graph/entities/merge
        {
            \"entities_to_change\": [\"Elon Msk\", \"Ellon Musk\"],
            \"entity_to_change_into\": \"Elon Musk\"
        }

    Note:
        - The target entity (entity_to_change_into) must exist in the knowledge graph
        - Source entities will be permanently deleted after the merge
        - This operation cannot be undone, so verify entity names before merging

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityMergeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
    body: EntityMergeRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Merge Entities

     Merge multiple entities into a single entity, preserving all relationships

    This endpoint consolidates duplicate or misspelled entities while preserving the entire
    graph structure. It's particularly useful for cleaning up knowledge graphs after document
    processing or correcting entity name variations.

    What the Merge Operation Does:
        1. Deletes the specified source entities from the knowledge graph
        2. Transfers all relationships from source entities to the target entity
        3. Intelligently merges duplicate relationships (if multiple sources have the same relationship)
        4. Updates vector embeddings for accurate retrieval and search
        5. Preserves the complete graph structure and connectivity
        6. Maintains relationship properties and metadata

    Use Cases:
        - Fixing spelling errors in entity names (e.g., \"Elon Msk\" -> \"Elon Musk\")
        - Consolidating duplicate entities discovered after document processing
        - Merging name variations (e.g., \"NY\", \"New York\", \"New York City\")
        - Cleaning up the knowledge graph for better query performance
        - Standardizing entity names across the knowledge base

    Request Body:
        entities_to_change (list[str]): List of entity names to be merged and deleted
        entity_to_change_into (str): Target entity that will receive all relationships

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Successfully merged 2 entities into 'Elon Musk'\",
            \"data\": {
                \"merged_entity\": \"Elon Musk\",
                \"deleted_entities\": [\"Elon Msk\", \"Ellon Musk\"],
                \"relationships_transferred\": 15,
                ... (merge operation details)
            }
        }

    HTTP Status Codes:
        200: Entities merged successfully
        400: Invalid request (e.g., empty entity list, target entity doesn't exist)
        500: Internal server error

    Example Request:
        POST /graph/entities/merge
        {
            \"entities_to_change\": [\"Elon Msk\", \"Ellon Musk\"],
            \"entity_to_change_into\": \"Elon Musk\"
        }

    Note:
        - The target entity (entity_to_change_into) must exist in the knowledge graph
        - Source entities will be permanently deleted after the merge
        - This operation cannot be undone, so verify entity names before merging

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityMergeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: EntityMergeRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Merge Entities

     Merge multiple entities into a single entity, preserving all relationships

    This endpoint consolidates duplicate or misspelled entities while preserving the entire
    graph structure. It's particularly useful for cleaning up knowledge graphs after document
    processing or correcting entity name variations.

    What the Merge Operation Does:
        1. Deletes the specified source entities from the knowledge graph
        2. Transfers all relationships from source entities to the target entity
        3. Intelligently merges duplicate relationships (if multiple sources have the same relationship)
        4. Updates vector embeddings for accurate retrieval and search
        5. Preserves the complete graph structure and connectivity
        6. Maintains relationship properties and metadata

    Use Cases:
        - Fixing spelling errors in entity names (e.g., \"Elon Msk\" -> \"Elon Musk\")
        - Consolidating duplicate entities discovered after document processing
        - Merging name variations (e.g., \"NY\", \"New York\", \"New York City\")
        - Cleaning up the knowledge graph for better query performance
        - Standardizing entity names across the knowledge base

    Request Body:
        entities_to_change (list[str]): List of entity names to be merged and deleted
        entity_to_change_into (str): Target entity that will receive all relationships

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Successfully merged 2 entities into 'Elon Musk'\",
            \"data\": {
                \"merged_entity\": \"Elon Musk\",
                \"deleted_entities\": [\"Elon Msk\", \"Ellon Musk\"],
                \"relationships_transferred\": 15,
                ... (merge operation details)
            }
        }

    HTTP Status Codes:
        200: Entities merged successfully
        400: Invalid request (e.g., empty entity list, target entity doesn't exist)
        500: Internal server error

    Example Request:
        POST /graph/entities/merge
        {
            \"entities_to_change\": [\"Elon Msk\", \"Ellon Musk\"],
            \"entity_to_change_into\": \"Elon Musk\"
        }

    Note:
        - The target entity (entity_to_change_into) must exist in the knowledge graph
        - Source entities will be permanently deleted after the merge
        - This operation cannot be undone, so verify entity names before merging

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityMergeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
    body: EntityMergeRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Merge Entities

     Merge multiple entities into a single entity, preserving all relationships

    This endpoint consolidates duplicate or misspelled entities while preserving the entire
    graph structure. It's particularly useful for cleaning up knowledge graphs after document
    processing or correcting entity name variations.

    What the Merge Operation Does:
        1. Deletes the specified source entities from the knowledge graph
        2. Transfers all relationships from source entities to the target entity
        3. Intelligently merges duplicate relationships (if multiple sources have the same relationship)
        4. Updates vector embeddings for accurate retrieval and search
        5. Preserves the complete graph structure and connectivity
        6. Maintains relationship properties and metadata

    Use Cases:
        - Fixing spelling errors in entity names (e.g., \"Elon Msk\" -> \"Elon Musk\")
        - Consolidating duplicate entities discovered after document processing
        - Merging name variations (e.g., \"NY\", \"New York\", \"New York City\")
        - Cleaning up the knowledge graph for better query performance
        - Standardizing entity names across the knowledge base

    Request Body:
        entities_to_change (list[str]): List of entity names to be merged and deleted
        entity_to_change_into (str): Target entity that will receive all relationships

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Successfully merged 2 entities into 'Elon Musk'\",
            \"data\": {
                \"merged_entity\": \"Elon Musk\",
                \"deleted_entities\": [\"Elon Msk\", \"Ellon Musk\"],
                \"relationships_transferred\": 15,
                ... (merge operation details)
            }
        }

    HTTP Status Codes:
        200: Entities merged successfully
        400: Invalid request (e.g., empty entity list, target entity doesn't exist)
        500: Internal server error

    Example Request:
        POST /graph/entities/merge
        {
            \"entities_to_change\": [\"Elon Msk\", \"Ellon Musk\"],
            \"entity_to_change_into\": \"Elon Musk\"
        }

    Note:
        - The target entity (entity_to_change_into) must exist in the knowledge graph
        - Source entities will be permanently deleted after the merge
        - This operation cannot be undone, so verify entity names before merging

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityMergeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
