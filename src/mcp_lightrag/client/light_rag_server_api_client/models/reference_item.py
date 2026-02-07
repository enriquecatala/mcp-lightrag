from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReferenceItem")


@_attrs_define
class ReferenceItem:
    """A single reference item in query responses.

    Attributes:
        reference_id (str): Unique reference identifier
        file_path (str): Path to the source file
        content (list[str] | None | Unset): List of chunk contents from this file (only present when
            include_chunk_content=True)
    """

    reference_id: str
    file_path: str
    content: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference_id = self.reference_id

        file_path = self.file_path

        content: list[str] | None | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, list):
            content = self.content

        else:
            content = self.content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reference_id": reference_id,
                "file_path": file_path,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reference_id = d.pop("reference_id")

        file_path = d.pop("file_path")

        def _parse_content(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_0 = cast(list[str], data)

                return content_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        content = _parse_content(d.pop("content", UNSET))

        reference_item = cls(
            reference_id=reference_id,
            file_path=file_path,
            content=content,
        )

        reference_item.additional_properties = d
        return reference_item

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
