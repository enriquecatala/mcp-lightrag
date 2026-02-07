from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_item import ReferenceItem


T = TypeVar("T", bound="QueryResponse")


@_attrs_define
class QueryResponse:
    """
    Attributes:
        response (str): The generated response
        references (list[ReferenceItem] | None | Unset): Reference list (Disabled when include_references=False,
            /query/data always includes references.)
    """

    response: str
    references: list[ReferenceItem] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response

        references: list[dict[str, Any]] | None | Unset
        if isinstance(self.references, Unset):
            references = UNSET
        elif isinstance(self.references, list):
            references = []
            for references_type_0_item_data in self.references:
                references_type_0_item = references_type_0_item_data.to_dict()
                references.append(references_type_0_item)

        else:
            references = self.references

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "response": response,
            }
        )
        if references is not UNSET:
            field_dict["references"] = references

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_item import ReferenceItem

        d = dict(src_dict)
        response = d.pop("response")

        def _parse_references(data: object) -> list[ReferenceItem] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                references_type_0 = []
                _references_type_0 = data
                for references_type_0_item_data in _references_type_0:
                    references_type_0_item = ReferenceItem.from_dict(
                        references_type_0_item_data
                    )

                    references_type_0.append(references_type_0_item)

                return references_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ReferenceItem] | None | Unset, data)

        references = _parse_references(d.pop("references", UNSET))

        query_response = cls(
            response=response,
            references=references,
        )

        query_response.additional_properties = d
        return query_response

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
