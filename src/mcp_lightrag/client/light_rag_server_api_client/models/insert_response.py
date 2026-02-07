from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.insert_response_status import InsertResponseStatus

T = TypeVar("T", bound="InsertResponse")


@_attrs_define
class InsertResponse:
    """Response model for document insertion operations

    Attributes:
        status: Status of the operation (success, duplicated, partial_success, failure)
        message: Detailed message describing the operation result
        track_id: Tracking ID for monitoring processing status

        Example:
            {'message': "File 'document.pdf' uploaded successfully. Processing will continue in background.", 'status':
                'success', 'track_id': 'upload_20250729_170612_abc123'}

        Attributes:
            status (InsertResponseStatus): Status of the operation
            message (str): Message describing the operation result
            track_id (str): Tracking ID for monitoring processing status
    """

    status: InsertResponseStatus
    message: str
    track_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message = self.message

        track_id = self.track_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
                "track_id": track_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = InsertResponseStatus(d.pop("status"))

        message = d.pop("message")

        track_id = d.pop("track_id")

        insert_response = cls(
            status=status,
            message=message,
            track_id=track_id,
        )

        insert_response.additional_properties = d
        return insert_response

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
