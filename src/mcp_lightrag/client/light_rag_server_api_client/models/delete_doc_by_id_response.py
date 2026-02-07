from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delete_doc_by_id_response_status import DeleteDocByIdResponseStatus

T = TypeVar("T", bound="DeleteDocByIdResponse")


@_attrs_define
class DeleteDocByIdResponse:
    """Response model for single document deletion operation.

    Attributes:
        status (DeleteDocByIdResponseStatus): Status of the deletion operation
        message (str): Message describing the operation result
        doc_id (str): The ID of the document to delete
    """

    status: DeleteDocByIdResponseStatus
    message: str
    doc_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message = self.message

        doc_id = self.doc_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
                "doc_id": doc_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = DeleteDocByIdResponseStatus(d.pop("status"))

        message = d.pop("message")

        doc_id = d.pop("doc_id")

        delete_doc_by_id_response = cls(
            status=status,
            message=message,
            doc_id=doc_id,
        )

        delete_doc_by_id_response.additional_properties = d
        return delete_doc_by_id_response

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
