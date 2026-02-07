from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.relation_update_request_updated_data import (
        RelationUpdateRequestUpdatedData,
    )


T = TypeVar("T", bound="RelationUpdateRequest")


@_attrs_define
class RelationUpdateRequest:
    """
    Attributes:
        source_id (str):
        target_id (str):
        updated_data (RelationUpdateRequestUpdatedData):
    """

    source_id: str
    target_id: str
    updated_data: RelationUpdateRequestUpdatedData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_id = self.source_id

        target_id = self.target_id

        updated_data = self.updated_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_id": source_id,
                "target_id": target_id,
                "updated_data": updated_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.relation_update_request_updated_data import (
            RelationUpdateRequestUpdatedData,
        )

        d = dict(src_dict)
        source_id = d.pop("source_id")

        target_id = d.pop("target_id")

        updated_data = RelationUpdateRequestUpdatedData.from_dict(d.pop("updated_data"))

        relation_update_request = cls(
            source_id=source_id,
            target_id=target_id,
            updated_data=updated_data,
        )

        relation_update_request.additional_properties = d
        return relation_update_request

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
