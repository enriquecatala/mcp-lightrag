from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteDocRequest")


@_attrs_define
class DeleteDocRequest:
    """
    Attributes:
        doc_ids (list[str]): The IDs of the documents to delete.
        delete_file (bool | Unset): Whether to delete the corresponding file in the upload directory. Default: False.
        delete_llm_cache (bool | Unset): Whether to delete cached LLM extraction results for the documents. Default:
            False.
    """

    doc_ids: list[str]
    delete_file: bool | Unset = False
    delete_llm_cache: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        doc_ids = self.doc_ids

        delete_file = self.delete_file

        delete_llm_cache = self.delete_llm_cache

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "doc_ids": doc_ids,
            }
        )
        if delete_file is not UNSET:
            field_dict["delete_file"] = delete_file
        if delete_llm_cache is not UNSET:
            field_dict["delete_llm_cache"] = delete_llm_cache

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        doc_ids = cast(list[str], d.pop("doc_ids"))

        delete_file = d.pop("delete_file", UNSET)

        delete_llm_cache = d.pop("delete_llm_cache", UNSET)

        delete_doc_request = cls(
            doc_ids=doc_ids,
            delete_file=delete_file,
            delete_llm_cache=delete_llm_cache,
        )

        delete_doc_request.additional_properties = d
        return delete_doc_request

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
