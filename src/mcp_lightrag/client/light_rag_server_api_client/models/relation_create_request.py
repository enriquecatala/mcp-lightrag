from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relation_create_request_relation_data import (
        RelationCreateRequestRelationData,
    )


T = TypeVar("T", bound="RelationCreateRequest")


@_attrs_define
class RelationCreateRequest:
    """
    Attributes:
        source_entity (str): Name of the source entity. This entity must already exist in the knowledge graph.
        target_entity (str): Name of the target entity. This entity must already exist in the knowledge graph.
        relation_data (RelationCreateRequestRelationData): Dictionary containing relationship properties. Common fields
            include 'description', 'keywords', and 'weight'.
    """

    source_entity: str
    target_entity: str
    relation_data: RelationCreateRequestRelationData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_entity = self.source_entity

        target_entity = self.target_entity

        relation_data = self.relation_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_entity": source_entity,
                "target_entity": target_entity,
                "relation_data": relation_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relation_create_request_relation_data import (
            RelationCreateRequestRelationData,
        )

        d = dict(src_dict)
        source_entity = d.pop("source_entity")

        target_entity = d.pop("target_entity")

        relation_data = RelationCreateRequestRelationData.from_dict(
            d.pop("relation_data")
        )

        relation_create_request = cls(
            source_entity=source_entity,
            target_entity=target_entity,
            relation_data=relation_data,
        )

        relation_create_request.additional_properties = d
        return relation_create_request

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
