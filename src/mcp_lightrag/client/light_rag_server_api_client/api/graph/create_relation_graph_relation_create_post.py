from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.relation_create_request import RelationCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: RelationCreateRequest,
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
        "url": "/graph/relation/create",
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
    body: RelationCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Create Relation

     Create a new relationship between two entities in the knowledge graph

    This endpoint establishes an undirected relationship between two existing entities.
    The provided source/target order is accepted for convenience, but the backend
    stored edge is undirected and may be returned with the entities swapped.
    Both entities must already exist in the knowledge graph. The system automatically
    generates vector embeddings for the relationship to enable semantic search and graph traversal.

    Prerequisites:
        - Both source_entity and target_entity must exist in the knowledge graph
        - Use /graph/entity/create to create entities first if they don't exist

    Request Body:
        source_entity (str): Name of the source entity (relationship origin)
        target_entity (str): Name of the target entity (relationship destination)
        relation_data (dict): Relationship properties including:
            - description (str): Textual description of the relationship
            - keywords (str): Comma-separated keywords describing the relationship type
            - source_id (str): Related chunk_id from which the description originates
            - weight (float): Relationship strength/importance (default: 1.0)
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Relation created successfully between 'Elon Musk' and 'Tesla'\",
            \"data\": {
                \"src_id\": \"Elon Musk\",
                \"tgt_id\": \"Tesla\",
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                \"weight\": 1.0,
                ... (other relationship properties)
            }
        }

    HTTP Status Codes:
        200: Relationship created successfully
        400: Invalid request (e.g., missing entities, invalid data, duplicate relationship)
        500: Internal server error

    Example Request:
        POST /graph/relation/create
        {
            \"source_entity\": \"Elon Musk\",
            \"target_entity\": \"Tesla\",
            \"relation_data\": {
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"weight\": 1.0
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (RelationCreateRequest):

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
    body: RelationCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Create Relation

     Create a new relationship between two entities in the knowledge graph

    This endpoint establishes an undirected relationship between two existing entities.
    The provided source/target order is accepted for convenience, but the backend
    stored edge is undirected and may be returned with the entities swapped.
    Both entities must already exist in the knowledge graph. The system automatically
    generates vector embeddings for the relationship to enable semantic search and graph traversal.

    Prerequisites:
        - Both source_entity and target_entity must exist in the knowledge graph
        - Use /graph/entity/create to create entities first if they don't exist

    Request Body:
        source_entity (str): Name of the source entity (relationship origin)
        target_entity (str): Name of the target entity (relationship destination)
        relation_data (dict): Relationship properties including:
            - description (str): Textual description of the relationship
            - keywords (str): Comma-separated keywords describing the relationship type
            - source_id (str): Related chunk_id from which the description originates
            - weight (float): Relationship strength/importance (default: 1.0)
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Relation created successfully between 'Elon Musk' and 'Tesla'\",
            \"data\": {
                \"src_id\": \"Elon Musk\",
                \"tgt_id\": \"Tesla\",
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                \"weight\": 1.0,
                ... (other relationship properties)
            }
        }

    HTTP Status Codes:
        200: Relationship created successfully
        400: Invalid request (e.g., missing entities, invalid data, duplicate relationship)
        500: Internal server error

    Example Request:
        POST /graph/relation/create
        {
            \"source_entity\": \"Elon Musk\",
            \"target_entity\": \"Tesla\",
            \"relation_data\": {
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"weight\": 1.0
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (RelationCreateRequest):

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
    body: RelationCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Create Relation

     Create a new relationship between two entities in the knowledge graph

    This endpoint establishes an undirected relationship between two existing entities.
    The provided source/target order is accepted for convenience, but the backend
    stored edge is undirected and may be returned with the entities swapped.
    Both entities must already exist in the knowledge graph. The system automatically
    generates vector embeddings for the relationship to enable semantic search and graph traversal.

    Prerequisites:
        - Both source_entity and target_entity must exist in the knowledge graph
        - Use /graph/entity/create to create entities first if they don't exist

    Request Body:
        source_entity (str): Name of the source entity (relationship origin)
        target_entity (str): Name of the target entity (relationship destination)
        relation_data (dict): Relationship properties including:
            - description (str): Textual description of the relationship
            - keywords (str): Comma-separated keywords describing the relationship type
            - source_id (str): Related chunk_id from which the description originates
            - weight (float): Relationship strength/importance (default: 1.0)
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Relation created successfully between 'Elon Musk' and 'Tesla'\",
            \"data\": {
                \"src_id\": \"Elon Musk\",
                \"tgt_id\": \"Tesla\",
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                \"weight\": 1.0,
                ... (other relationship properties)
            }
        }

    HTTP Status Codes:
        200: Relationship created successfully
        400: Invalid request (e.g., missing entities, invalid data, duplicate relationship)
        500: Internal server error

    Example Request:
        POST /graph/relation/create
        {
            \"source_entity\": \"Elon Musk\",
            \"target_entity\": \"Tesla\",
            \"relation_data\": {
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"weight\": 1.0
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (RelationCreateRequest):

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
    body: RelationCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Create Relation

     Create a new relationship between two entities in the knowledge graph

    This endpoint establishes an undirected relationship between two existing entities.
    The provided source/target order is accepted for convenience, but the backend
    stored edge is undirected and may be returned with the entities swapped.
    Both entities must already exist in the knowledge graph. The system automatically
    generates vector embeddings for the relationship to enable semantic search and graph traversal.

    Prerequisites:
        - Both source_entity and target_entity must exist in the knowledge graph
        - Use /graph/entity/create to create entities first if they don't exist

    Request Body:
        source_entity (str): Name of the source entity (relationship origin)
        target_entity (str): Name of the target entity (relationship destination)
        relation_data (dict): Relationship properties including:
            - description (str): Textual description of the relationship
            - keywords (str): Comma-separated keywords describing the relationship type
            - source_id (str): Related chunk_id from which the description originates
            - weight (float): Relationship strength/importance (default: 1.0)
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Relation created successfully between 'Elon Musk' and 'Tesla'\",
            \"data\": {
                \"src_id\": \"Elon Musk\",
                \"tgt_id\": \"Tesla\",
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                \"weight\": 1.0,
                ... (other relationship properties)
            }
        }

    HTTP Status Codes:
        200: Relationship created successfully
        400: Invalid request (e.g., missing entities, invalid data, duplicate relationship)
        500: Internal server error

    Example Request:
        POST /graph/relation/create
        {
            \"source_entity\": \"Elon Musk\",
            \"target_entity\": \"Tesla\",
            \"relation_data\": {
                \"description\": \"Elon Musk is the CEO of Tesla\",
                \"keywords\": \"CEO, founder\",
                \"weight\": 1.0
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (RelationCreateRequest):

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
