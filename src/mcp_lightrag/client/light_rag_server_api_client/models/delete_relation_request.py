from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeleteRelationRequest")


@_attrs_define
class DeleteRelationRequest:
    """
    Attributes:
        source_entity (str): The name of the source entity.
        target_entity (str): The name of the target entity.
    """

    source_entity: str
    target_entity: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_entity = self.source_entity

        target_entity = self.target_entity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_entity": source_entity,
                "target_entity": target_entity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_entity = d.pop("source_entity")

        target_entity = d.pop("target_entity")

        delete_relation_request = cls(
            source_entity=source_entity,
            target_entity=target_entity,
        )

        delete_relation_request.additional_properties = d
        return delete_relation_request

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
