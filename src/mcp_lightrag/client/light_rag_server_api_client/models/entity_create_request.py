from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.entity_create_request_entity_data import EntityCreateRequestEntityData


T = TypeVar("T", bound="EntityCreateRequest")


@_attrs_define
class EntityCreateRequest:
    """
    Attributes:
        entity_name (str): Unique name for the new entity
        entity_data (EntityCreateRequestEntityData): Dictionary containing entity properties. Common fields include
            'description' and 'entity_type'.
    """

    entity_name: str
    entity_data: EntityCreateRequestEntityData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity_name = self.entity_name

        entity_data = self.entity_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_name": entity_name,
                "entity_data": entity_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.entity_create_request_entity_data import (
            EntityCreateRequestEntityData,
        )

        d = dict(src_dict)
        entity_name = d.pop("entity_name")

        entity_data = EntityCreateRequestEntityData.from_dict(d.pop("entity_data"))

        entity_create_request = cls(
            entity_name=entity_name,
            entity_data=entity_data,
        )

        entity_create_request.additional_properties = d
        return entity_create_request

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
