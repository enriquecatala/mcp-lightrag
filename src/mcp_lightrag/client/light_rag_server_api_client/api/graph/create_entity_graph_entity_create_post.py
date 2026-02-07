from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.entity_create_request import EntityCreateRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: EntityCreateRequest,
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
        "url": "/graph/entity/create",
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
    body: EntityCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Create Entity

     Create a new entity in the knowledge graph

    This endpoint creates a new entity node in the knowledge graph with the specified
    properties. The system automatically generates vector embeddings for the entity
    to enable semantic search and retrieval.

    Request Body:
        entity_name (str): Unique name identifier for the entity
        entity_data (dict): Entity properties including:
            - description (str): Textual description of the entity
            - entity_type (str): Category/type of the entity (e.g., PERSON, ORGANIZATION, LOCATION)
            - source_id (str): Related chunk_id from which the description originates
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Entity 'Tesla' created successfully\",
            \"data\": {
                \"entity_name\": \"Tesla\",
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                ... (other entity properties)
            }
        }

    HTTP Status Codes:
        200: Entity created successfully
        400: Invalid request (e.g., missing required fields, duplicate entity)
        500: Internal server error

    Example Request:
        POST /graph/entity/create
        {
            \"entity_name\": \"Tesla\",
            \"entity_data\": {
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\"
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityCreateRequest):

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
    body: EntityCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Create Entity

     Create a new entity in the knowledge graph

    This endpoint creates a new entity node in the knowledge graph with the specified
    properties. The system automatically generates vector embeddings for the entity
    to enable semantic search and retrieval.

    Request Body:
        entity_name (str): Unique name identifier for the entity
        entity_data (dict): Entity properties including:
            - description (str): Textual description of the entity
            - entity_type (str): Category/type of the entity (e.g., PERSON, ORGANIZATION, LOCATION)
            - source_id (str): Related chunk_id from which the description originates
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Entity 'Tesla' created successfully\",
            \"data\": {
                \"entity_name\": \"Tesla\",
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                ... (other entity properties)
            }
        }

    HTTP Status Codes:
        200: Entity created successfully
        400: Invalid request (e.g., missing required fields, duplicate entity)
        500: Internal server error

    Example Request:
        POST /graph/entity/create
        {
            \"entity_name\": \"Tesla\",
            \"entity_data\": {
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\"
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityCreateRequest):

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
    body: EntityCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Create Entity

     Create a new entity in the knowledge graph

    This endpoint creates a new entity node in the knowledge graph with the specified
    properties. The system automatically generates vector embeddings for the entity
    to enable semantic search and retrieval.

    Request Body:
        entity_name (str): Unique name identifier for the entity
        entity_data (dict): Entity properties including:
            - description (str): Textual description of the entity
            - entity_type (str): Category/type of the entity (e.g., PERSON, ORGANIZATION, LOCATION)
            - source_id (str): Related chunk_id from which the description originates
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Entity 'Tesla' created successfully\",
            \"data\": {
                \"entity_name\": \"Tesla\",
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                ... (other entity properties)
            }
        }

    HTTP Status Codes:
        200: Entity created successfully
        400: Invalid request (e.g., missing required fields, duplicate entity)
        500: Internal server error

    Example Request:
        POST /graph/entity/create
        {
            \"entity_name\": \"Tesla\",
            \"entity_data\": {
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\"
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityCreateRequest):

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
    body: EntityCreateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Create Entity

     Create a new entity in the knowledge graph

    This endpoint creates a new entity node in the knowledge graph with the specified
    properties. The system automatically generates vector embeddings for the entity
    to enable semantic search and retrieval.

    Request Body:
        entity_name (str): Unique name identifier for the entity
        entity_data (dict): Entity properties including:
            - description (str): Textual description of the entity
            - entity_type (str): Category/type of the entity (e.g., PERSON, ORGANIZATION, LOCATION)
            - source_id (str): Related chunk_id from which the description originates
            - Additional custom properties as needed

    Response Schema:
        {
            \"status\": \"success\",
            \"message\": \"Entity 'Tesla' created successfully\",
            \"data\": {
                \"entity_name\": \"Tesla\",
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\",
                \"source_id\": \"chunk-123<SEP>chunk-456\"
                ... (other entity properties)
            }
        }

    HTTP Status Codes:
        200: Entity created successfully
        400: Invalid request (e.g., missing required fields, duplicate entity)
        500: Internal server error

    Example Request:
        POST /graph/entity/create
        {
            \"entity_name\": \"Tesla\",
            \"entity_data\": {
                \"description\": \"Electric vehicle manufacturer\",
                \"entity_type\": \"ORGANIZATION\"
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityCreateRequest):

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
