from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    label: str,
    max_depth: int | Unset = 3,
    max_nodes: int | Unset = 1000,
    api_key_header_value: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["label"] = label

    params["max_depth"] = max_depth

    params["max_nodes"] = max_nodes

    json_api_key_header_value: None | str | Unset
    if isinstance(api_key_header_value, Unset):
        json_api_key_header_value = UNSET
    else:
        json_api_key_header_value = api_key_header_value
    params["api_key_header_value"] = json_api_key_header_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/graphs",
        "params": params,
    }

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
    label: str,
    max_depth: int | Unset = 3,
    max_nodes: int | Unset = 1000,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. Hops(path) to the staring node take precedence
        2. Followed by the degree of the nodes

    Args:
        label (str): Label of the starting node
        max_depth (int, optional): Maximum depth of the subgraph,Defaults to 3
        max_nodes: Maxiumu nodes to return

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int | Unset): Maximum depth of graph Default: 3.
        max_nodes (int | Unset): Maximum nodes to return Default: 1000.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        label=label,
        max_depth=max_depth,
        max_nodes=max_nodes,
        api_key_header_value=api_key_header_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    label: str,
    max_depth: int | Unset = 3,
    max_nodes: int | Unset = 1000,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. Hops(path) to the staring node take precedence
        2. Followed by the degree of the nodes

    Args:
        label (str): Label of the starting node
        max_depth (int, optional): Maximum depth of the subgraph,Defaults to 3
        max_nodes: Maxiumu nodes to return

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int | Unset): Maximum depth of graph Default: 3.
        max_nodes (int | Unset): Maximum nodes to return Default: 1000.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        label=label,
        max_depth=max_depth,
        max_nodes=max_nodes,
        api_key_header_value=api_key_header_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    label: str,
    max_depth: int | Unset = 3,
    max_nodes: int | Unset = 1000,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. Hops(path) to the staring node take precedence
        2. Followed by the degree of the nodes

    Args:
        label (str): Label of the starting node
        max_depth (int, optional): Maximum depth of the subgraph,Defaults to 3
        max_nodes: Maxiumu nodes to return

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int | Unset): Maximum depth of graph Default: 3.
        max_nodes (int | Unset): Maximum nodes to return Default: 1000.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        label=label,
        max_depth=max_depth,
        max_nodes=max_nodes,
        api_key_header_value=api_key_header_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    label: str,
    max_depth: int | Unset = 3,
    max_nodes: int | Unset = 1000,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Get Knowledge Graph

     Retrieve a connected subgraph of nodes where the label includes the specified label.
    When reducing the number of nodes, the prioritization criteria are as follows:
        1. Hops(path) to the staring node take precedence
        2. Followed by the degree of the nodes

    Args:
        label (str): Label of the starting node
        max_depth (int, optional): Maximum depth of the subgraph,Defaults to 3
        max_nodes: Maxiumu nodes to return

    Returns:
        Dict[str, List[str]]: Knowledge graph for label

    Args:
        label (str): Label to get knowledge graph for
        max_depth (int | Unset): Maximum depth of graph Default: 3.
        max_nodes (int | Unset): Maximum nodes to return Default: 1000.
        api_key_header_value (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            label=label,
            max_depth=max_depth,
            max_nodes=max_nodes,
            api_key_header_value=api_key_header_value,
        )
    ).parsed
