from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.clear_cache_response_status import ClearCacheResponseStatus

T = TypeVar("T", bound="ClearCacheResponse")


@_attrs_define
class ClearCacheResponse:
    """Response model for cache clearing operation

    Attributes:
        status: Status of the clear operation
        message: Detailed message describing the operation result

        Example:
            {'message': "Successfully cleared cache for modes: ['default', 'naive']", 'status': 'success'}

        Attributes:
            status (ClearCacheResponseStatus): Status of the clear operation
            message (str): Message describing the operation result
    """

    status: ClearCacheResponseStatus
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ClearCacheResponseStatus(d.pop("status"))

        message = d.pop("message")

        clear_cache_response = cls(
            status=status,
            message=message,
        )

        clear_cache_response.additional_properties = d
        return clear_cache_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
