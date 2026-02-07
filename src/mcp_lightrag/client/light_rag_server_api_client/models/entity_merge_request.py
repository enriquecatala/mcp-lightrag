from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EntityMergeRequest")


@_attrs_define
class EntityMergeRequest:
    """
    Attributes:
        entities_to_change (list[str]): List of entity names to be merged and deleted. These are typically duplicate or
            misspelled entities.
        entity_to_change_into (str): Target entity name that will receive all relationships from the source entities.
            This entity will be preserved.
    """

    entities_to_change: list[str]
    entity_to_change_into: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entities_to_change = self.entities_to_change

        entity_to_change_into = self.entity_to_change_into

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entities_to_change": entities_to_change,
                "entity_to_change_into": entity_to_change_into,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entities_to_change = cast(list[str], d.pop("entities_to_change"))

        entity_to_change_into = d.pop("entity_to_change_into")

        entity_merge_request = cls(
            entities_to_change=entities_to_change,
            entity_to_change_into=entity_to_change_into,
        )

        entity_merge_request.additional_properties = d
        return entity_merge_request

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
