from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entity_update_request_updated_data import (
        EntityUpdateRequestUpdatedData,
    )


T = TypeVar("T", bound="EntityUpdateRequest")


@_attrs_define
class EntityUpdateRequest:
    """
    Attributes:
        entity_name (str):
        updated_data (EntityUpdateRequestUpdatedData):
        allow_rename (bool | Unset):  Default: False.
        allow_merge (bool | Unset):  Default: False.
    """

    entity_name: str
    updated_data: EntityUpdateRequestUpdatedData
    allow_rename: bool | Unset = False
    allow_merge: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity_name = self.entity_name

        updated_data = self.updated_data.to_dict()

        allow_rename = self.allow_rename

        allow_merge = self.allow_merge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_name": entity_name,
                "updated_data": updated_data,
            }
        )
        if allow_rename is not UNSET:
            field_dict["allow_rename"] = allow_rename
        if allow_merge is not UNSET:
            field_dict["allow_merge"] = allow_merge

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.entity_update_request_updated_data import (
            EntityUpdateRequestUpdatedData,
        )

        d = dict(src_dict)
        entity_name = d.pop("entity_name")

        updated_data = EntityUpdateRequestUpdatedData.from_dict(d.pop("updated_data"))

        allow_rename = d.pop("allow_rename", UNSET)

        allow_merge = d.pop("allow_merge", UNSET)

        entity_update_request = cls(
            entity_name=entity_name,
            updated_data=updated_data,
            allow_rename=allow_rename,
            allow_merge=allow_merge,
        )

        entity_update_request.additional_properties = d
        return entity_update_request

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
