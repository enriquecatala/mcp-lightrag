from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.query_data_query_data_post_response_400 import (
    QueryDataQueryDataPostResponse400,
)
from ...models.query_data_query_data_post_response_500 import (
    QueryDataQueryDataPostResponse500,
)
from ...models.query_data_response import QueryDataResponse
from ...models.query_request import QueryRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: QueryRequest,
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
        "url": "/query/data",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    HTTPValidationError
    | QueryDataQueryDataPostResponse400
    | QueryDataQueryDataPostResponse500
    | QueryDataResponse
    | None
):
    if response.status_code == 200:
        response_200 = QueryDataResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = QueryDataQueryDataPostResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = QueryDataQueryDataPostResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    HTTPValidationError
    | QueryDataQueryDataPostResponse400
    | QueryDataQueryDataPostResponse500
    | QueryDataResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: QueryRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[
    HTTPValidationError
    | QueryDataQueryDataPostResponse400
    | QueryDataQueryDataPostResponse500
    | QueryDataResponse
]:
    r"""Query Data

     Advanced data retrieval endpoint for structured RAG analysis.

    This endpoint provides raw retrieval results without LLM generation, perfect for:
    - **Data Analysis**: Examine what information would be used for RAG
    - **System Integration**: Get structured data for custom processing
    - **Debugging**: Understand retrieval behavior and quality
    - **Research**: Analyze knowledge graph structure and relationships

    **Key Features:**
    - No LLM generation - pure data retrieval
    - Complete structured output with entities, relationships, and chunks
    - Always includes references for citation
    - Detailed metadata about processing and keywords
    - Compatible with all query modes and parameters

    **Query Mode Behaviors:**
    - **local**: Returns entities and their direct relationships + related chunks
    - **global**: Returns relationship patterns across the knowledge graph
    - **hybrid**: Combines local and global retrieval strategies
    - **naive**: Returns only vector-retrieved text chunks (no knowledge graph)
    - **mix**: Integrates knowledge graph data with vector-retrieved chunks
    - **bypass**: Returns empty data arrays (used for direct LLM queries)

    **Data Structure:**
    - **entities**: Knowledge graph entities with descriptions and metadata
    - **relationships**: Connections between entities with weights and descriptions
    - **chunks**: Text segments from documents with source information
    - **references**: Citation information mapping reference IDs to file paths
    - **metadata**: Processing information, keywords, and query statistics

    **Usage Examples:**

    Analyze entity relationships:
    ```json
    {
        \"query\": \"machine learning algorithms\",
        \"mode\": \"local\",
        \"top_k\": 10
    }
    ```

    Explore global patterns:
    ```json
    {
        \"query\": \"artificial intelligence trends\",
        \"mode\": \"global\",
        \"max_relation_tokens\": 2000
    }
    ```

    Vector similarity search:
    ```json
    {
        \"query\": \"neural network architectures\",
        \"mode\": \"naive\",
        \"chunk_top_k\": 5
    }
    ```

    Bypass initial LLM call by providing high-level and low-level keywords:
    ```json
    {
        \"query\": \"What is Retrieval-Augmented-Generation?\",
        \"hl_keywords\": [\"machine learning\", \"information retrieval\", \"natural language
    processing\"],
        \"ll_keywords\": [\"retrieval augmented generation\", \"RAG\", \"knowledge base\"],
        \"mode\": \"mix\"
    }
    ```

    **Response Analysis:**
    - **Empty arrays**: Normal for certain modes (e.g., naive mode has no entities/relationships)
    - **Processing info**: Shows retrieval statistics and token usage
    - **Keywords**: High-level and low-level keywords extracted from query
    - **Reference mapping**: Links all data back to source documents

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The search query to analyze (min 3 characters)
            - **mode**: Retrieval strategy affecting data types returned
            - **top_k**: Number of top entities/relationships to retrieve
            - **chunk_top_k**: Number of text chunks to retrieve
            - **max_entity_tokens**: Token limit for entity context
            - **max_relation_tokens**: Token limit for relationship context
            - **max_total_tokens**: Overall token budget for retrieval

    Returns:
        QueryDataResponse: Structured JSON response containing:
            - **status**: \"success\" or \"failure\"
            - **message**: Human-readable status description
            - **data**: Complete retrieval results with entities, relationships, chunks, references
            - **metadata**: Query processing information and statistics

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., knowledge graph unavailable)

    Note:
        This endpoint always includes references regardless of the include_references parameter,
        as structured data analysis typically requires source attribution.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QueryDataQueryDataPostResponse400 | QueryDataQueryDataPostResponse500 | QueryDataResponse]
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
    body: QueryRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> (
    HTTPValidationError
    | QueryDataQueryDataPostResponse400
    | QueryDataQueryDataPostResponse500
    | QueryDataResponse
    | None
):
    r"""Query Data

     Advanced data retrieval endpoint for structured RAG analysis.

    This endpoint provides raw retrieval results without LLM generation, perfect for:
    - **Data Analysis**: Examine what information would be used for RAG
    - **System Integration**: Get structured data for custom processing
    - **Debugging**: Understand retrieval behavior and quality
    - **Research**: Analyze knowledge graph structure and relationships

    **Key Features:**
    - No LLM generation - pure data retrieval
    - Complete structured output with entities, relationships, and chunks
    - Always includes references for citation
    - Detailed metadata about processing and keywords
    - Compatible with all query modes and parameters

    **Query Mode Behaviors:**
    - **local**: Returns entities and their direct relationships + related chunks
    - **global**: Returns relationship patterns across the knowledge graph
    - **hybrid**: Combines local and global retrieval strategies
    - **naive**: Returns only vector-retrieved text chunks (no knowledge graph)
    - **mix**: Integrates knowledge graph data with vector-retrieved chunks
    - **bypass**: Returns empty data arrays (used for direct LLM queries)

    **Data Structure:**
    - **entities**: Knowledge graph entities with descriptions and metadata
    - **relationships**: Connections between entities with weights and descriptions
    - **chunks**: Text segments from documents with source information
    - **references**: Citation information mapping reference IDs to file paths
    - **metadata**: Processing information, keywords, and query statistics

    **Usage Examples:**

    Analyze entity relationships:
    ```json
    {
        \"query\": \"machine learning algorithms\",
        \"mode\": \"local\",
        \"top_k\": 10
    }
    ```

    Explore global patterns:
    ```json
    {
        \"query\": \"artificial intelligence trends\",
        \"mode\": \"global\",
        \"max_relation_tokens\": 2000
    }
    ```

    Vector similarity search:
    ```json
    {
        \"query\": \"neural network architectures\",
        \"mode\": \"naive\",
        \"chunk_top_k\": 5
    }
    ```

    Bypass initial LLM call by providing high-level and low-level keywords:
    ```json
    {
        \"query\": \"What is Retrieval-Augmented-Generation?\",
        \"hl_keywords\": [\"machine learning\", \"information retrieval\", \"natural language
    processing\"],
        \"ll_keywords\": [\"retrieval augmented generation\", \"RAG\", \"knowledge base\"],
        \"mode\": \"mix\"
    }
    ```

    **Response Analysis:**
    - **Empty arrays**: Normal for certain modes (e.g., naive mode has no entities/relationships)
    - **Processing info**: Shows retrieval statistics and token usage
    - **Keywords**: High-level and low-level keywords extracted from query
    - **Reference mapping**: Links all data back to source documents

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The search query to analyze (min 3 characters)
            - **mode**: Retrieval strategy affecting data types returned
            - **top_k**: Number of top entities/relationships to retrieve
            - **chunk_top_k**: Number of text chunks to retrieve
            - **max_entity_tokens**: Token limit for entity context
            - **max_relation_tokens**: Token limit for relationship context
            - **max_total_tokens**: Overall token budget for retrieval

    Returns:
        QueryDataResponse: Structured JSON response containing:
            - **status**: \"success\" or \"failure\"
            - **message**: Human-readable status description
            - **data**: Complete retrieval results with entities, relationships, chunks, references
            - **metadata**: Query processing information and statistics

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., knowledge graph unavailable)

    Note:
        This endpoint always includes references regardless of the include_references parameter,
        as structured data analysis typically requires source attribution.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QueryDataQueryDataPostResponse400 | QueryDataQueryDataPostResponse500 | QueryDataResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: QueryRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[
    HTTPValidationError
    | QueryDataQueryDataPostResponse400
    | QueryDataQueryDataPostResponse500
    | QueryDataResponse
]:
    r"""Query Data

     Advanced data retrieval endpoint for structured RAG analysis.

    This endpoint provides raw retrieval results without LLM generation, perfect for:
    - **Data Analysis**: Examine what information would be used for RAG
    - **System Integration**: Get structured data for custom processing
    - **Debugging**: Understand retrieval behavior and quality
    - **Research**: Analyze knowledge graph structure and relationships

    **Key Features:**
    - No LLM generation - pure data retrieval
    - Complete structured output with entities, relationships, and chunks
    - Always includes references for citation
    - Detailed metadata about processing and keywords
    - Compatible with all query modes and parameters

    **Query Mode Behaviors:**
    - **local**: Returns entities and their direct relationships + related chunks
    - **global**: Returns relationship patterns across the knowledge graph
    - **hybrid**: Combines local and global retrieval strategies
    - **naive**: Returns only vector-retrieved text chunks (no knowledge graph)
    - **mix**: Integrates knowledge graph data with vector-retrieved chunks
    - **bypass**: Returns empty data arrays (used for direct LLM queries)

    **Data Structure:**
    - **entities**: Knowledge graph entities with descriptions and metadata
    - **relationships**: Connections between entities with weights and descriptions
    - **chunks**: Text segments from documents with source information
    - **references**: Citation information mapping reference IDs to file paths
    - **metadata**: Processing information, keywords, and query statistics

    **Usage Examples:**

    Analyze entity relationships:
    ```json
    {
        \"query\": \"machine learning algorithms\",
        \"mode\": \"local\",
        \"top_k\": 10
    }
    ```

    Explore global patterns:
    ```json
    {
        \"query\": \"artificial intelligence trends\",
        \"mode\": \"global\",
        \"max_relation_tokens\": 2000
    }
    ```

    Vector similarity search:
    ```json
    {
        \"query\": \"neural network architectures\",
        \"mode\": \"naive\",
        \"chunk_top_k\": 5
    }
    ```

    Bypass initial LLM call by providing high-level and low-level keywords:
    ```json
    {
        \"query\": \"What is Retrieval-Augmented-Generation?\",
        \"hl_keywords\": [\"machine learning\", \"information retrieval\", \"natural language
    processing\"],
        \"ll_keywords\": [\"retrieval augmented generation\", \"RAG\", \"knowledge base\"],
        \"mode\": \"mix\"
    }
    ```

    **Response Analysis:**
    - **Empty arrays**: Normal for certain modes (e.g., naive mode has no entities/relationships)
    - **Processing info**: Shows retrieval statistics and token usage
    - **Keywords**: High-level and low-level keywords extracted from query
    - **Reference mapping**: Links all data back to source documents

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The search query to analyze (min 3 characters)
            - **mode**: Retrieval strategy affecting data types returned
            - **top_k**: Number of top entities/relationships to retrieve
            - **chunk_top_k**: Number of text chunks to retrieve
            - **max_entity_tokens**: Token limit for entity context
            - **max_relation_tokens**: Token limit for relationship context
            - **max_total_tokens**: Overall token budget for retrieval

    Returns:
        QueryDataResponse: Structured JSON response containing:
            - **status**: \"success\" or \"failure\"
            - **message**: Human-readable status description
            - **data**: Complete retrieval results with entities, relationships, chunks, references
            - **metadata**: Query processing information and statistics

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., knowledge graph unavailable)

    Note:
        This endpoint always includes references regardless of the include_references parameter,
        as structured data analysis typically requires source attribution.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QueryDataQueryDataPostResponse400 | QueryDataQueryDataPostResponse500 | QueryDataResponse]
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
    body: QueryRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> (
    HTTPValidationError
    | QueryDataQueryDataPostResponse400
    | QueryDataQueryDataPostResponse500
    | QueryDataResponse
    | None
):
    r"""Query Data

     Advanced data retrieval endpoint for structured RAG analysis.

    This endpoint provides raw retrieval results without LLM generation, perfect for:
    - **Data Analysis**: Examine what information would be used for RAG
    - **System Integration**: Get structured data for custom processing
    - **Debugging**: Understand retrieval behavior and quality
    - **Research**: Analyze knowledge graph structure and relationships

    **Key Features:**
    - No LLM generation - pure data retrieval
    - Complete structured output with entities, relationships, and chunks
    - Always includes references for citation
    - Detailed metadata about processing and keywords
    - Compatible with all query modes and parameters

    **Query Mode Behaviors:**
    - **local**: Returns entities and their direct relationships + related chunks
    - **global**: Returns relationship patterns across the knowledge graph
    - **hybrid**: Combines local and global retrieval strategies
    - **naive**: Returns only vector-retrieved text chunks (no knowledge graph)
    - **mix**: Integrates knowledge graph data with vector-retrieved chunks
    - **bypass**: Returns empty data arrays (used for direct LLM queries)

    **Data Structure:**
    - **entities**: Knowledge graph entities with descriptions and metadata
    - **relationships**: Connections between entities with weights and descriptions
    - **chunks**: Text segments from documents with source information
    - **references**: Citation information mapping reference IDs to file paths
    - **metadata**: Processing information, keywords, and query statistics

    **Usage Examples:**

    Analyze entity relationships:
    ```json
    {
        \"query\": \"machine learning algorithms\",
        \"mode\": \"local\",
        \"top_k\": 10
    }
    ```

    Explore global patterns:
    ```json
    {
        \"query\": \"artificial intelligence trends\",
        \"mode\": \"global\",
        \"max_relation_tokens\": 2000
    }
    ```

    Vector similarity search:
    ```json
    {
        \"query\": \"neural network architectures\",
        \"mode\": \"naive\",
        \"chunk_top_k\": 5
    }
    ```

    Bypass initial LLM call by providing high-level and low-level keywords:
    ```json
    {
        \"query\": \"What is Retrieval-Augmented-Generation?\",
        \"hl_keywords\": [\"machine learning\", \"information retrieval\", \"natural language
    processing\"],
        \"ll_keywords\": [\"retrieval augmented generation\", \"RAG\", \"knowledge base\"],
        \"mode\": \"mix\"
    }
    ```

    **Response Analysis:**
    - **Empty arrays**: Normal for certain modes (e.g., naive mode has no entities/relationships)
    - **Processing info**: Shows retrieval statistics and token usage
    - **Keywords**: High-level and low-level keywords extracted from query
    - **Reference mapping**: Links all data back to source documents

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The search query to analyze (min 3 characters)
            - **mode**: Retrieval strategy affecting data types returned
            - **top_k**: Number of top entities/relationships to retrieve
            - **chunk_top_k**: Number of text chunks to retrieve
            - **max_entity_tokens**: Token limit for entity context
            - **max_relation_tokens**: Token limit for relationship context
            - **max_total_tokens**: Overall token budget for retrieval

    Returns:
        QueryDataResponse: Structured JSON response containing:
            - **status**: \"success\" or \"failure\"
            - **message**: Human-readable status description
            - **data**: Complete retrieval results with entities, relationships, chunks, references
            - **metadata**: Query processing information and statistics

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., knowledge graph unavailable)

    Note:
        This endpoint always includes references regardless of the include_references parameter,
        as structured data analysis typically requires source attribution.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QueryDataQueryDataPostResponse400 | QueryDataQueryDataPostResponse500 | QueryDataResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
