from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.entity_update_request import EntityUpdateRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: EntityUpdateRequest,
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
        "url": "/graph/entity/edit",
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
    body: EntityUpdateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Update Entity

     Update an entity's properties in the knowledge graph

    This endpoint allows updating entity properties, including renaming entities.
    When renaming to an existing entity name, the behavior depends on allow_merge:

    Args:
        request (EntityUpdateRequest): Request containing:
            - entity_name (str): Name of the entity to update
            - updated_data (Dict[str, Any]): Dictionary of properties to update
            - allow_rename (bool): Whether to allow entity renaming (default: False)
            - allow_merge (bool): Whether to merge into existing entity when renaming
                                 causes name conflict (default: False)

    Returns:
        Dict with the following structure:
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\" | \"Entity merged successfully into
    'target_name'\",
            \"data\": {
                \"entity_name\": str,        # Final entity name
                \"description\": str,        # Entity description
                \"entity_type\": str,        # Entity type
                \"source_id\": str,         # Source chunk IDs
                ...                       # Other entity properties
            },
            \"operation_summary\": {
                \"merged\": bool,           # Whether entity was merged into another
                \"merge_status\": str,      # \"success\" | \"failed\" | \"not_attempted\"
                \"merge_error\": str | None, # Error message if merge failed
                \"operation_status\": str,  # \"success\" | \"partial_success\" | \"failure\"
                \"target_entity\": str | None, # Target entity name if renaming/merging
                \"final_entity\": str,      # Final entity name after operation
                \"renamed\": bool           # Whether entity was renamed
            }
        }

    operation_status values explained:
        - \"success\": All operations completed successfully
            * For simple updates: entity properties updated
            * For renames: entity renamed successfully
            * For merges: non-name updates applied AND merge completed

        - \"partial_success\": Update succeeded but merge failed
            * Non-name property updates were applied successfully
            * Merge operation failed (entity not merged)
            * Original entity still exists with updated properties
            * Use merge_error for failure details

        - \"failure\": Operation failed completely
            * If merge_status == \"failed\": Merge attempted but both update and merge failed
            * If merge_status == \"not_attempted\": Regular update failed
            * No changes were applied to the entity

    merge_status values explained:
        - \"success\": Entity successfully merged into target entity
        - \"failed\": Merge operation was attempted but failed
        - \"not_attempted\": No merge was attempted (normal update/rename)

    Behavior when renaming to an existing entity:
        - If allow_merge=False: Raises ValueError with 400 status (default behavior)
        - If allow_merge=True: Automatically merges the source entity into the existing target entity,
                              preserving all relationships and applying non-name updates first

    Example Request (simple update):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Tesla\",
            \"updated_data\": {\"description\": \"Updated description\"},
            \"allow_rename\": false,
            \"allow_merge\": false
        }

    Example Response (simple update success):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"not_attempted\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": null,
                \"final_entity\": \"Tesla\",
                \"renamed\": false
            }
        }

    Example Request (rename with auto-merge):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Elon Msk\",
            \"updated_data\": {
                \"entity_name\": \"Elon Musk\",
                \"description\": \"Corrected description\"
            },
            \"allow_rename\": true,
            \"allow_merge\": true
        }

    Example Response (merge success):
        {
            \"status\": \"success\",
            \"message\": \"Entity merged successfully into 'Elon Musk'\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": true,
                \"merge_status\": \"success\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Musk\",
                \"renamed\": true
            }
        }

    Example Response (partial success - update succeeded but merge failed):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },  # Data reflects updated \"Elon Msk\" entity
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"failed\",
                \"merge_error\": \"Target entity locked by another operation\",
                \"operation_status\": \"partial_success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Msk\",  # Original entity still exists
                \"renamed\": true
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityUpdateRequest):

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
    body: EntityUpdateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Update Entity

     Update an entity's properties in the knowledge graph

    This endpoint allows updating entity properties, including renaming entities.
    When renaming to an existing entity name, the behavior depends on allow_merge:

    Args:
        request (EntityUpdateRequest): Request containing:
            - entity_name (str): Name of the entity to update
            - updated_data (Dict[str, Any]): Dictionary of properties to update
            - allow_rename (bool): Whether to allow entity renaming (default: False)
            - allow_merge (bool): Whether to merge into existing entity when renaming
                                 causes name conflict (default: False)

    Returns:
        Dict with the following structure:
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\" | \"Entity merged successfully into
    'target_name'\",
            \"data\": {
                \"entity_name\": str,        # Final entity name
                \"description\": str,        # Entity description
                \"entity_type\": str,        # Entity type
                \"source_id\": str,         # Source chunk IDs
                ...                       # Other entity properties
            },
            \"operation_summary\": {
                \"merged\": bool,           # Whether entity was merged into another
                \"merge_status\": str,      # \"success\" | \"failed\" | \"not_attempted\"
                \"merge_error\": str | None, # Error message if merge failed
                \"operation_status\": str,  # \"success\" | \"partial_success\" | \"failure\"
                \"target_entity\": str | None, # Target entity name if renaming/merging
                \"final_entity\": str,      # Final entity name after operation
                \"renamed\": bool           # Whether entity was renamed
            }
        }

    operation_status values explained:
        - \"success\": All operations completed successfully
            * For simple updates: entity properties updated
            * For renames: entity renamed successfully
            * For merges: non-name updates applied AND merge completed

        - \"partial_success\": Update succeeded but merge failed
            * Non-name property updates were applied successfully
            * Merge operation failed (entity not merged)
            * Original entity still exists with updated properties
            * Use merge_error for failure details

        - \"failure\": Operation failed completely
            * If merge_status == \"failed\": Merge attempted but both update and merge failed
            * If merge_status == \"not_attempted\": Regular update failed
            * No changes were applied to the entity

    merge_status values explained:
        - \"success\": Entity successfully merged into target entity
        - \"failed\": Merge operation was attempted but failed
        - \"not_attempted\": No merge was attempted (normal update/rename)

    Behavior when renaming to an existing entity:
        - If allow_merge=False: Raises ValueError with 400 status (default behavior)
        - If allow_merge=True: Automatically merges the source entity into the existing target entity,
                              preserving all relationships and applying non-name updates first

    Example Request (simple update):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Tesla\",
            \"updated_data\": {\"description\": \"Updated description\"},
            \"allow_rename\": false,
            \"allow_merge\": false
        }

    Example Response (simple update success):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"not_attempted\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": null,
                \"final_entity\": \"Tesla\",
                \"renamed\": false
            }
        }

    Example Request (rename with auto-merge):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Elon Msk\",
            \"updated_data\": {
                \"entity_name\": \"Elon Musk\",
                \"description\": \"Corrected description\"
            },
            \"allow_rename\": true,
            \"allow_merge\": true
        }

    Example Response (merge success):
        {
            \"status\": \"success\",
            \"message\": \"Entity merged successfully into 'Elon Musk'\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": true,
                \"merge_status\": \"success\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Musk\",
                \"renamed\": true
            }
        }

    Example Response (partial success - update succeeded but merge failed):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },  # Data reflects updated \"Elon Msk\" entity
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"failed\",
                \"merge_error\": \"Target entity locked by another operation\",
                \"operation_status\": \"partial_success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Msk\",  # Original entity still exists
                \"renamed\": true
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityUpdateRequest):

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
    body: EntityUpdateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Update Entity

     Update an entity's properties in the knowledge graph

    This endpoint allows updating entity properties, including renaming entities.
    When renaming to an existing entity name, the behavior depends on allow_merge:

    Args:
        request (EntityUpdateRequest): Request containing:
            - entity_name (str): Name of the entity to update
            - updated_data (Dict[str, Any]): Dictionary of properties to update
            - allow_rename (bool): Whether to allow entity renaming (default: False)
            - allow_merge (bool): Whether to merge into existing entity when renaming
                                 causes name conflict (default: False)

    Returns:
        Dict with the following structure:
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\" | \"Entity merged successfully into
    'target_name'\",
            \"data\": {
                \"entity_name\": str,        # Final entity name
                \"description\": str,        # Entity description
                \"entity_type\": str,        # Entity type
                \"source_id\": str,         # Source chunk IDs
                ...                       # Other entity properties
            },
            \"operation_summary\": {
                \"merged\": bool,           # Whether entity was merged into another
                \"merge_status\": str,      # \"success\" | \"failed\" | \"not_attempted\"
                \"merge_error\": str | None, # Error message if merge failed
                \"operation_status\": str,  # \"success\" | \"partial_success\" | \"failure\"
                \"target_entity\": str | None, # Target entity name if renaming/merging
                \"final_entity\": str,      # Final entity name after operation
                \"renamed\": bool           # Whether entity was renamed
            }
        }

    operation_status values explained:
        - \"success\": All operations completed successfully
            * For simple updates: entity properties updated
            * For renames: entity renamed successfully
            * For merges: non-name updates applied AND merge completed

        - \"partial_success\": Update succeeded but merge failed
            * Non-name property updates were applied successfully
            * Merge operation failed (entity not merged)
            * Original entity still exists with updated properties
            * Use merge_error for failure details

        - \"failure\": Operation failed completely
            * If merge_status == \"failed\": Merge attempted but both update and merge failed
            * If merge_status == \"not_attempted\": Regular update failed
            * No changes were applied to the entity

    merge_status values explained:
        - \"success\": Entity successfully merged into target entity
        - \"failed\": Merge operation was attempted but failed
        - \"not_attempted\": No merge was attempted (normal update/rename)

    Behavior when renaming to an existing entity:
        - If allow_merge=False: Raises ValueError with 400 status (default behavior)
        - If allow_merge=True: Automatically merges the source entity into the existing target entity,
                              preserving all relationships and applying non-name updates first

    Example Request (simple update):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Tesla\",
            \"updated_data\": {\"description\": \"Updated description\"},
            \"allow_rename\": false,
            \"allow_merge\": false
        }

    Example Response (simple update success):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"not_attempted\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": null,
                \"final_entity\": \"Tesla\",
                \"renamed\": false
            }
        }

    Example Request (rename with auto-merge):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Elon Msk\",
            \"updated_data\": {
                \"entity_name\": \"Elon Musk\",
                \"description\": \"Corrected description\"
            },
            \"allow_rename\": true,
            \"allow_merge\": true
        }

    Example Response (merge success):
        {
            \"status\": \"success\",
            \"message\": \"Entity merged successfully into 'Elon Musk'\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": true,
                \"merge_status\": \"success\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Musk\",
                \"renamed\": true
            }
        }

    Example Response (partial success - update succeeded but merge failed):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },  # Data reflects updated \"Elon Msk\" entity
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"failed\",
                \"merge_error\": \"Target entity locked by another operation\",
                \"operation_status\": \"partial_success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Msk\",  # Original entity still exists
                \"renamed\": true
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityUpdateRequest):

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
    body: EntityUpdateRequest,
    api_key_header_value: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Update Entity

     Update an entity's properties in the knowledge graph

    This endpoint allows updating entity properties, including renaming entities.
    When renaming to an existing entity name, the behavior depends on allow_merge:

    Args:
        request (EntityUpdateRequest): Request containing:
            - entity_name (str): Name of the entity to update
            - updated_data (Dict[str, Any]): Dictionary of properties to update
            - allow_rename (bool): Whether to allow entity renaming (default: False)
            - allow_merge (bool): Whether to merge into existing entity when renaming
                                 causes name conflict (default: False)

    Returns:
        Dict with the following structure:
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\" | \"Entity merged successfully into
    'target_name'\",
            \"data\": {
                \"entity_name\": str,        # Final entity name
                \"description\": str,        # Entity description
                \"entity_type\": str,        # Entity type
                \"source_id\": str,         # Source chunk IDs
                ...                       # Other entity properties
            },
            \"operation_summary\": {
                \"merged\": bool,           # Whether entity was merged into another
                \"merge_status\": str,      # \"success\" | \"failed\" | \"not_attempted\"
                \"merge_error\": str | None, # Error message if merge failed
                \"operation_status\": str,  # \"success\" | \"partial_success\" | \"failure\"
                \"target_entity\": str | None, # Target entity name if renaming/merging
                \"final_entity\": str,      # Final entity name after operation
                \"renamed\": bool           # Whether entity was renamed
            }
        }

    operation_status values explained:
        - \"success\": All operations completed successfully
            * For simple updates: entity properties updated
            * For renames: entity renamed successfully
            * For merges: non-name updates applied AND merge completed

        - \"partial_success\": Update succeeded but merge failed
            * Non-name property updates were applied successfully
            * Merge operation failed (entity not merged)
            * Original entity still exists with updated properties
            * Use merge_error for failure details

        - \"failure\": Operation failed completely
            * If merge_status == \"failed\": Merge attempted but both update and merge failed
            * If merge_status == \"not_attempted\": Regular update failed
            * No changes were applied to the entity

    merge_status values explained:
        - \"success\": Entity successfully merged into target entity
        - \"failed\": Merge operation was attempted but failed
        - \"not_attempted\": No merge was attempted (normal update/rename)

    Behavior when renaming to an existing entity:
        - If allow_merge=False: Raises ValueError with 400 status (default behavior)
        - If allow_merge=True: Automatically merges the source entity into the existing target entity,
                              preserving all relationships and applying non-name updates first

    Example Request (simple update):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Tesla\",
            \"updated_data\": {\"description\": \"Updated description\"},
            \"allow_rename\": false,
            \"allow_merge\": false
        }

    Example Response (simple update success):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"not_attempted\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": null,
                \"final_entity\": \"Tesla\",
                \"renamed\": false
            }
        }

    Example Request (rename with auto-merge):
        POST /graph/entity/edit
        {
            \"entity_name\": \"Elon Msk\",
            \"updated_data\": {
                \"entity_name\": \"Elon Musk\",
                \"description\": \"Corrected description\"
            },
            \"allow_rename\": true,
            \"allow_merge\": true
        }

    Example Response (merge success):
        {
            \"status\": \"success\",
            \"message\": \"Entity merged successfully into 'Elon Musk'\",
            \"data\": { ... },
            \"operation_summary\": {
                \"merged\": true,
                \"merge_status\": \"success\",
                \"merge_error\": null,
                \"operation_status\": \"success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Musk\",
                \"renamed\": true
            }
        }

    Example Response (partial success - update succeeded but merge failed):
        {
            \"status\": \"success\",
            \"message\": \"Entity updated successfully\",
            \"data\": { ... },  # Data reflects updated \"Elon Msk\" entity
            \"operation_summary\": {
                \"merged\": false,
                \"merge_status\": \"failed\",
                \"merge_error\": \"Target entity locked by another operation\",
                \"operation_status\": \"partial_success\",
                \"target_entity\": \"Elon Musk\",
                \"final_entity\": \"Elon Msk\",  # Original entity still exists
                \"renamed\": true
            }
        }

    Args:
        api_key_header_value (None | str | Unset):
        body (EntityUpdateRequest):

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
