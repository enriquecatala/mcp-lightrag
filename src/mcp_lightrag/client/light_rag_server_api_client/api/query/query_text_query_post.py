from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.query_request import QueryRequest
from ...models.query_response import QueryResponse
from ...models.query_text_query_post_response_400 import QueryTextQueryPostResponse400
from ...models.query_text_query_post_response_500 import QueryTextQueryPostResponse500
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
        "url": "/query",
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
    | QueryResponse
    | QueryTextQueryPostResponse400
    | QueryTextQueryPostResponse500
    | None
):
    if response.status_code == 200:
        response_200 = QueryResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = QueryTextQueryPostResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = QueryTextQueryPostResponse500.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    HTTPValidationError
    | QueryResponse
    | QueryTextQueryPostResponse400
    | QueryTextQueryPostResponse500
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
    | QueryResponse
    | QueryTextQueryPostResponse400
    | QueryTextQueryPostResponse500
]:
    r"""Query Text

     Comprehensive RAG query endpoint with non-streaming response. Parameter \"stream\" is ignored.

    This endpoint performs Retrieval-Augmented Generation (RAG) queries using various modes
    to provide intelligent responses based on your knowledge base.

    **Query Modes:**
    - **local**: Focuses on specific entities and their direct relationships
    - **global**: Analyzes broader patterns and relationships across the knowledge graph
    - **hybrid**: Combines local and global approaches for comprehensive results
    - **naive**: Simple vector similarity search without knowledge graph
    - **mix**: Integrates knowledge graph retrieval with vector search (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples:**

    Basic query:
    ```json
    {
        \"query\": \"What is machine learning?\",
        \"mode\": \"mix\"
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

    Advanced query with references:
    ```json
    {
        \"query\": \"Explain neural networks\",
        \"mode\": \"hybrid\",
        \"include_references\": true,
        \"response_type\": \"Multiple Paragraphs\",
        \"top_k\": 10
    }
    ```

    Conversation with history:
    ```json
    {
        \"query\": \"Can you give me more details?\",
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is AI?\"},
            {\"role\": \"assistant\", \"content\": \"AI is artificial intelligence...\"}
        ]
    }
    ```

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        QueryResponse: JSON response containing:
            - **response**: The generated answer to your query
            - **references**: Source citations (if include_references=True)

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QueryResponse | QueryTextQueryPostResponse400 | QueryTextQueryPostResponse500]
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
    | QueryResponse
    | QueryTextQueryPostResponse400
    | QueryTextQueryPostResponse500
    | None
):
    r"""Query Text

     Comprehensive RAG query endpoint with non-streaming response. Parameter \"stream\" is ignored.

    This endpoint performs Retrieval-Augmented Generation (RAG) queries using various modes
    to provide intelligent responses based on your knowledge base.

    **Query Modes:**
    - **local**: Focuses on specific entities and their direct relationships
    - **global**: Analyzes broader patterns and relationships across the knowledge graph
    - **hybrid**: Combines local and global approaches for comprehensive results
    - **naive**: Simple vector similarity search without knowledge graph
    - **mix**: Integrates knowledge graph retrieval with vector search (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples:**

    Basic query:
    ```json
    {
        \"query\": \"What is machine learning?\",
        \"mode\": \"mix\"
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

    Advanced query with references:
    ```json
    {
        \"query\": \"Explain neural networks\",
        \"mode\": \"hybrid\",
        \"include_references\": true,
        \"response_type\": \"Multiple Paragraphs\",
        \"top_k\": 10
    }
    ```

    Conversation with history:
    ```json
    {
        \"query\": \"Can you give me more details?\",
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is AI?\"},
            {\"role\": \"assistant\", \"content\": \"AI is artificial intelligence...\"}
        ]
    }
    ```

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        QueryResponse: JSON response containing:
            - **response**: The generated answer to your query
            - **references**: Source citations (if include_references=True)

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QueryResponse | QueryTextQueryPostResponse400 | QueryTextQueryPostResponse500
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
    | QueryResponse
    | QueryTextQueryPostResponse400
    | QueryTextQueryPostResponse500
]:
    r"""Query Text

     Comprehensive RAG query endpoint with non-streaming response. Parameter \"stream\" is ignored.

    This endpoint performs Retrieval-Augmented Generation (RAG) queries using various modes
    to provide intelligent responses based on your knowledge base.

    **Query Modes:**
    - **local**: Focuses on specific entities and their direct relationships
    - **global**: Analyzes broader patterns and relationships across the knowledge graph
    - **hybrid**: Combines local and global approaches for comprehensive results
    - **naive**: Simple vector similarity search without knowledge graph
    - **mix**: Integrates knowledge graph retrieval with vector search (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples:**

    Basic query:
    ```json
    {
        \"query\": \"What is machine learning?\",
        \"mode\": \"mix\"
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

    Advanced query with references:
    ```json
    {
        \"query\": \"Explain neural networks\",
        \"mode\": \"hybrid\",
        \"include_references\": true,
        \"response_type\": \"Multiple Paragraphs\",
        \"top_k\": 10
    }
    ```

    Conversation with history:
    ```json
    {
        \"query\": \"Can you give me more details?\",
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is AI?\"},
            {\"role\": \"assistant\", \"content\": \"AI is artificial intelligence...\"}
        ]
    }
    ```

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        QueryResponse: JSON response containing:
            - **response**: The generated answer to your query
            - **references**: Source citations (if include_references=True)

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QueryResponse | QueryTextQueryPostResponse400 | QueryTextQueryPostResponse500]
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
    | QueryResponse
    | QueryTextQueryPostResponse400
    | QueryTextQueryPostResponse500
    | None
):
    r"""Query Text

     Comprehensive RAG query endpoint with non-streaming response. Parameter \"stream\" is ignored.

    This endpoint performs Retrieval-Augmented Generation (RAG) queries using various modes
    to provide intelligent responses based on your knowledge base.

    **Query Modes:**
    - **local**: Focuses on specific entities and their direct relationships
    - **global**: Analyzes broader patterns and relationships across the knowledge graph
    - **hybrid**: Combines local and global approaches for comprehensive results
    - **naive**: Simple vector similarity search without knowledge graph
    - **mix**: Integrates knowledge graph retrieval with vector search (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples:**

    Basic query:
    ```json
    {
        \"query\": \"What is machine learning?\",
        \"mode\": \"mix\"
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

    Advanced query with references:
    ```json
    {
        \"query\": \"Explain neural networks\",
        \"mode\": \"hybrid\",
        \"include_references\": true,
        \"response_type\": \"Multiple Paragraphs\",
        \"top_k\": 10
    }
    ```

    Conversation with history:
    ```json
    {
        \"query\": \"Can you give me more details?\",
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is AI?\"},
            {\"role\": \"assistant\", \"content\": \"AI is artificial intelligence...\"}
        ]
    }
    ```

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        QueryResponse: JSON response containing:
            - **response**: The generated answer to your query
            - **references**: Source citations (if include_references=True)

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QueryResponse | QueryTextQueryPostResponse400 | QueryTextQueryPostResponse500
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
