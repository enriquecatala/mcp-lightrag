from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InsertTextsRequest")


@_attrs_define
class InsertTextsRequest:
    """Request model for inserting multiple text documents

    Attributes:
        texts: List of text contents to be inserted into the RAG system
        file_sources: Sources of the texts (optional)

        Example:
            {'file_sources': ['First file source (optional)'], 'texts': ['This is the first text to be inserted.', 'This is
                the second text to be inserted.']}

        Attributes:
            texts (list[str]): The texts to insert
            file_sources (list[str] | Unset): Sources of the texts
    """

    texts: list[str]
    file_sources: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        texts = self.texts

        file_sources: list[str] | Unset = UNSET
        if not isinstance(self.file_sources, Unset):
            file_sources = self.file_sources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "texts": texts,
            }
        )
        if file_sources is not UNSET:
            field_dict["file_sources"] = file_sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        texts = cast(list[str], d.pop("texts"))

        file_sources = cast(list[str], d.pop("file_sources", UNSET))

        insert_texts_request = cls(
            texts=texts,
            file_sources=file_sources,
        )

        insert_texts_request.additional_properties = d
        return insert_texts_request

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
