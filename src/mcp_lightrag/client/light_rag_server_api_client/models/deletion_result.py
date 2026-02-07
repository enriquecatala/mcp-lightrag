from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.deletion_result_status import DeletionResultStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeletionResult")


@_attrs_define
class DeletionResult:
    """
    Attributes:
        status (DeletionResultStatus):
        doc_id (str):
        message (str):
        status_code (int | Unset):  Default: 200.
        file_path (None | str | Unset):
    """

    status: DeletionResultStatus
    doc_id: str
    message: str
    status_code: int | Unset = 200
    file_path: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        doc_id = self.doc_id

        message = self.message

        status_code = self.status_code

        file_path: None | str | Unset
        if isinstance(self.file_path, Unset):
            file_path = UNSET
        else:
            file_path = self.file_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "doc_id": doc_id,
                "message": message,
            }
        )
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if file_path is not UNSET:
            field_dict["file_path"] = file_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = DeletionResultStatus(d.pop("status"))

        doc_id = d.pop("doc_id")

        message = d.pop("message")

        status_code = d.pop("status_code", UNSET)

        def _parse_file_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_path = _parse_file_path(d.pop("file_path", UNSET))

        deletion_result = cls(
            status=status,
            doc_id=doc_id,
            message=message,
            status_code=status_code,
            file_path=file_path,
        )

        deletion_result.additional_properties = d
        return deletion_result

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
