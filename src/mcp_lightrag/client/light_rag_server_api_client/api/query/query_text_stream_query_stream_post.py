from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.query_request import QueryRequest
from ...models.query_text_stream_query_stream_post_response_400 import (
    QueryTextStreamQueryStreamPostResponse400,
)
from ...models.query_text_stream_query_stream_post_response_500 import (
    QueryTextStreamQueryStreamPostResponse500,
)
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
        "url": "/query/stream",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | HTTPValidationError
    | QueryTextStreamQueryStreamPostResponse400
    | QueryTextStreamQueryStreamPostResponse500
    | None
):
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 400:
        response_400 = QueryTextStreamQueryStreamPostResponse400.from_dict(
            response.json()
        )

        return response_400

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = QueryTextStreamQueryStreamPostResponse500.from_dict(
            response.json()
        )

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | HTTPValidationError
    | QueryTextStreamQueryStreamPostResponse400
    | QueryTextStreamQueryStreamPostResponse500
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
    Any
    | HTTPValidationError
    | QueryTextStreamQueryStreamPostResponse400
    | QueryTextStreamQueryStreamPostResponse500
]:
    r"""Query Text Stream

     Advanced RAG query endpoint with flexible streaming response.

    This endpoint provides the most flexible querying experience, supporting both real-time streaming
    and complete response delivery based on your integration needs.

    **Response Modes:**
    - Real-time response delivery as content is generated
    - NDJSON format: each line is a separate JSON object
    - First line: `{\"references\": [...]}` (if include_references=True)
    - Subsequent lines: `{\"response\": \"content chunk\"}`
    - Error handling: `{\"error\": \"error message\"}`

    > If stream parameter is False, or the query hit LLM cache, complete response delivered in a single
    streaming message.

    **Response Format Details**
    - **Content-Type**: `application/x-ndjson` (Newline-Delimited JSON)
    - **Structure**: Each line is an independent, valid JSON object
    - **Parsing**: Process line-by-line, each line is self-contained
    - **Headers**: Includes cache control and connection management

    **Query Modes (same as /query endpoint)**
    - **local**: Entity-focused retrieval with direct relationships
    - **global**: Pattern analysis across the knowledge graph
    - **hybrid**: Combined local and global strategies
    - **naive**: Vector similarity search only
    - **mix**: Integrated knowledge graph + vector retrieval (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples**

    Real-time streaming query:
    ```json
    {
        \"query\": \"Explain machine learning algorithms\",
        \"mode\": \"mix\",
        \"stream\": true,
        \"include_references\": true
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

    Complete response query:
    ```json
    {
        \"query\": \"What is deep learning?\",
        \"mode\": \"hybrid\",
        \"stream\": false,
        \"response_type\": \"Multiple Paragraphs\"
    }
    ```

    Conversation with context:
    ```json
    {
        \"query\": \"Can you elaborate on that?\",
        \"stream\": true,
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is neural network?\"},
            {\"role\": \"assistant\", \"content\": \"A neural network is...\"}
        ]
    }
    ```

    **Response Processing:**

    ```python
    async for line in response.iter_lines():
        data = json.loads(line)
        if \"references\" in data:
            # Handle references (first message)
            references = data[\"references\"]
        if \"response\" in data:
            # Handle content chunk
            content_chunk = data[\"response\"]
        if \"error\" in data:
            # Handle error
            error_message = data[\"error\"]
    ```

    **Error Handling:**
    - Streaming errors are delivered as `{\"error\": \"message\"}` lines
    - Non-streaming errors raise HTTP exceptions
    - Partial responses may be delivered before errors in streaming mode
    - Always check for error objects when processing streaming responses

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **stream**: Enable streaming (True) or complete response (False)
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context for multi-turn conversations
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        StreamingResponse: NDJSON streaming response containing:
            - **Streaming mode**: Multiple JSON objects, one per line
              - References object (if requested): `{\"references\": [...]}`
              - Content chunks: `{\"response\": \"chunk content\"}`
              - Error objects: `{\"error\": \"error message\"}`
            - **Non-streaming mode**: Single JSON object
              - Complete response: `{\"references\": [...], \"response\": \"complete content\"}`

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Note:
        This endpoint is ideal for applications requiring flexible response delivery.
        Use streaming mode for real-time interfaces and non-streaming for batch processing.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | QueryTextStreamQueryStreamPostResponse400 | QueryTextStreamQueryStreamPostResponse500]
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
    Any
    | HTTPValidationError
    | QueryTextStreamQueryStreamPostResponse400
    | QueryTextStreamQueryStreamPostResponse500
    | None
):
    r"""Query Text Stream

     Advanced RAG query endpoint with flexible streaming response.

    This endpoint provides the most flexible querying experience, supporting both real-time streaming
    and complete response delivery based on your integration needs.

    **Response Modes:**
    - Real-time response delivery as content is generated
    - NDJSON format: each line is a separate JSON object
    - First line: `{\"references\": [...]}` (if include_references=True)
    - Subsequent lines: `{\"response\": \"content chunk\"}`
    - Error handling: `{\"error\": \"error message\"}`

    > If stream parameter is False, or the query hit LLM cache, complete response delivered in a single
    streaming message.

    **Response Format Details**
    - **Content-Type**: `application/x-ndjson` (Newline-Delimited JSON)
    - **Structure**: Each line is an independent, valid JSON object
    - **Parsing**: Process line-by-line, each line is self-contained
    - **Headers**: Includes cache control and connection management

    **Query Modes (same as /query endpoint)**
    - **local**: Entity-focused retrieval with direct relationships
    - **global**: Pattern analysis across the knowledge graph
    - **hybrid**: Combined local and global strategies
    - **naive**: Vector similarity search only
    - **mix**: Integrated knowledge graph + vector retrieval (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples**

    Real-time streaming query:
    ```json
    {
        \"query\": \"Explain machine learning algorithms\",
        \"mode\": \"mix\",
        \"stream\": true,
        \"include_references\": true
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

    Complete response query:
    ```json
    {
        \"query\": \"What is deep learning?\",
        \"mode\": \"hybrid\",
        \"stream\": false,
        \"response_type\": \"Multiple Paragraphs\"
    }
    ```

    Conversation with context:
    ```json
    {
        \"query\": \"Can you elaborate on that?\",
        \"stream\": true,
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is neural network?\"},
            {\"role\": \"assistant\", \"content\": \"A neural network is...\"}
        ]
    }
    ```

    **Response Processing:**

    ```python
    async for line in response.iter_lines():
        data = json.loads(line)
        if \"references\" in data:
            # Handle references (first message)
            references = data[\"references\"]
        if \"response\" in data:
            # Handle content chunk
            content_chunk = data[\"response\"]
        if \"error\" in data:
            # Handle error
            error_message = data[\"error\"]
    ```

    **Error Handling:**
    - Streaming errors are delivered as `{\"error\": \"message\"}` lines
    - Non-streaming errors raise HTTP exceptions
    - Partial responses may be delivered before errors in streaming mode
    - Always check for error objects when processing streaming responses

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **stream**: Enable streaming (True) or complete response (False)
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context for multi-turn conversations
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        StreamingResponse: NDJSON streaming response containing:
            - **Streaming mode**: Multiple JSON objects, one per line
              - References object (if requested): `{\"references\": [...]}`
              - Content chunks: `{\"response\": \"chunk content\"}`
              - Error objects: `{\"error\": \"error message\"}`
            - **Non-streaming mode**: Single JSON object
              - Complete response: `{\"references\": [...], \"response\": \"complete content\"}`

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Note:
        This endpoint is ideal for applications requiring flexible response delivery.
        Use streaming mode for real-time interfaces and non-streaming for batch processing.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | QueryTextStreamQueryStreamPostResponse400 | QueryTextStreamQueryStreamPostResponse500
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
    Any
    | HTTPValidationError
    | QueryTextStreamQueryStreamPostResponse400
    | QueryTextStreamQueryStreamPostResponse500
]:
    r"""Query Text Stream

     Advanced RAG query endpoint with flexible streaming response.

    This endpoint provides the most flexible querying experience, supporting both real-time streaming
    and complete response delivery based on your integration needs.

    **Response Modes:**
    - Real-time response delivery as content is generated
    - NDJSON format: each line is a separate JSON object
    - First line: `{\"references\": [...]}` (if include_references=True)
    - Subsequent lines: `{\"response\": \"content chunk\"}`
    - Error handling: `{\"error\": \"error message\"}`

    > If stream parameter is False, or the query hit LLM cache, complete response delivered in a single
    streaming message.

    **Response Format Details**
    - **Content-Type**: `application/x-ndjson` (Newline-Delimited JSON)
    - **Structure**: Each line is an independent, valid JSON object
    - **Parsing**: Process line-by-line, each line is self-contained
    - **Headers**: Includes cache control and connection management

    **Query Modes (same as /query endpoint)**
    - **local**: Entity-focused retrieval with direct relationships
    - **global**: Pattern analysis across the knowledge graph
    - **hybrid**: Combined local and global strategies
    - **naive**: Vector similarity search only
    - **mix**: Integrated knowledge graph + vector retrieval (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples**

    Real-time streaming query:
    ```json
    {
        \"query\": \"Explain machine learning algorithms\",
        \"mode\": \"mix\",
        \"stream\": true,
        \"include_references\": true
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

    Complete response query:
    ```json
    {
        \"query\": \"What is deep learning?\",
        \"mode\": \"hybrid\",
        \"stream\": false,
        \"response_type\": \"Multiple Paragraphs\"
    }
    ```

    Conversation with context:
    ```json
    {
        \"query\": \"Can you elaborate on that?\",
        \"stream\": true,
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is neural network?\"},
            {\"role\": \"assistant\", \"content\": \"A neural network is...\"}
        ]
    }
    ```

    **Response Processing:**

    ```python
    async for line in response.iter_lines():
        data = json.loads(line)
        if \"references\" in data:
            # Handle references (first message)
            references = data[\"references\"]
        if \"response\" in data:
            # Handle content chunk
            content_chunk = data[\"response\"]
        if \"error\" in data:
            # Handle error
            error_message = data[\"error\"]
    ```

    **Error Handling:**
    - Streaming errors are delivered as `{\"error\": \"message\"}` lines
    - Non-streaming errors raise HTTP exceptions
    - Partial responses may be delivered before errors in streaming mode
    - Always check for error objects when processing streaming responses

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **stream**: Enable streaming (True) or complete response (False)
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context for multi-turn conversations
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        StreamingResponse: NDJSON streaming response containing:
            - **Streaming mode**: Multiple JSON objects, one per line
              - References object (if requested): `{\"references\": [...]}`
              - Content chunks: `{\"response\": \"chunk content\"}`
              - Error objects: `{\"error\": \"error message\"}`
            - **Non-streaming mode**: Single JSON object
              - Complete response: `{\"references\": [...], \"response\": \"complete content\"}`

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Note:
        This endpoint is ideal for applications requiring flexible response delivery.
        Use streaming mode for real-time interfaces and non-streaming for batch processing.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | QueryTextStreamQueryStreamPostResponse400 | QueryTextStreamQueryStreamPostResponse500]
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
    Any
    | HTTPValidationError
    | QueryTextStreamQueryStreamPostResponse400
    | QueryTextStreamQueryStreamPostResponse500
    | None
):
    r"""Query Text Stream

     Advanced RAG query endpoint with flexible streaming response.

    This endpoint provides the most flexible querying experience, supporting both real-time streaming
    and complete response delivery based on your integration needs.

    **Response Modes:**
    - Real-time response delivery as content is generated
    - NDJSON format: each line is a separate JSON object
    - First line: `{\"references\": [...]}` (if include_references=True)
    - Subsequent lines: `{\"response\": \"content chunk\"}`
    - Error handling: `{\"error\": \"error message\"}`

    > If stream parameter is False, or the query hit LLM cache, complete response delivered in a single
    streaming message.

    **Response Format Details**
    - **Content-Type**: `application/x-ndjson` (Newline-Delimited JSON)
    - **Structure**: Each line is an independent, valid JSON object
    - **Parsing**: Process line-by-line, each line is self-contained
    - **Headers**: Includes cache control and connection management

    **Query Modes (same as /query endpoint)**
    - **local**: Entity-focused retrieval with direct relationships
    - **global**: Pattern analysis across the knowledge graph
    - **hybrid**: Combined local and global strategies
    - **naive**: Vector similarity search only
    - **mix**: Integrated knowledge graph + vector retrieval (recommended)
    - **bypass**: Direct LLM query without knowledge retrieval

    conversation_history parameteris sent to LLM only, does not affect retrieval results.

    **Usage Examples**

    Real-time streaming query:
    ```json
    {
        \"query\": \"Explain machine learning algorithms\",
        \"mode\": \"mix\",
        \"stream\": true,
        \"include_references\": true
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

    Complete response query:
    ```json
    {
        \"query\": \"What is deep learning?\",
        \"mode\": \"hybrid\",
        \"stream\": false,
        \"response_type\": \"Multiple Paragraphs\"
    }
    ```

    Conversation with context:
    ```json
    {
        \"query\": \"Can you elaborate on that?\",
        \"stream\": true,
        \"conversation_history\": [
            {\"role\": \"user\", \"content\": \"What is neural network?\"},
            {\"role\": \"assistant\", \"content\": \"A neural network is...\"}
        ]
    }
    ```

    **Response Processing:**

    ```python
    async for line in response.iter_lines():
        data = json.loads(line)
        if \"references\" in data:
            # Handle references (first message)
            references = data[\"references\"]
        if \"response\" in data:
            # Handle content chunk
            content_chunk = data[\"response\"]
        if \"error\" in data:
            # Handle error
            error_message = data[\"error\"]
    ```

    **Error Handling:**
    - Streaming errors are delivered as `{\"error\": \"message\"}` lines
    - Non-streaming errors raise HTTP exceptions
    - Partial responses may be delivered before errors in streaming mode
    - Always check for error objects when processing streaming responses

    Args:
        request (QueryRequest): The request object containing query parameters:
            - **query**: The question or prompt to process (min 3 characters)
            - **mode**: Query strategy - \"mix\" recommended for best results
            - **stream**: Enable streaming (True) or complete response (False)
            - **include_references**: Whether to include source citations
            - **response_type**: Format preference (e.g., \"Multiple Paragraphs\")
            - **top_k**: Number of top entities/relations to retrieve
            - **conversation_history**: Previous dialogue context for multi-turn conversations
            - **max_total_tokens**: Token budget for the entire response

    Returns:
        StreamingResponse: NDJSON streaming response containing:
            - **Streaming mode**: Multiple JSON objects, one per line
              - References object (if requested): `{\"references\": [...]}`
              - Content chunks: `{\"response\": \"chunk content\"}`
              - Error objects: `{\"error\": \"error message\"}`
            - **Non-streaming mode**: Single JSON object
              - Complete response: `{\"references\": [...], \"response\": \"complete content\"}`

    Raises:
        HTTPException:
            - 400: Invalid input parameters (e.g., query too short, invalid mode)
            - 500: Internal processing error (e.g., LLM service unavailable)

    Note:
        This endpoint is ideal for applications requiring flexible response delivery.
        Use streaming mode for real-time interfaces and non-streaming for batch processing.

    Args:
        api_key_header_value (None | str | Unset):
        body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | QueryTextStreamQueryStreamPostResponse400 | QueryTextStreamQueryStreamPostResponse500
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
