from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReprocessResponse")


@_attrs_define
class ReprocessResponse:
    """Response model for reprocessing failed documents operation

    Attributes:
        status: Status of the reprocessing operation
        message: Message describing the operation result
        track_id: Always empty string. Reprocessed documents retain their original track_id.

        Example:
            {'message': 'Reprocessing of failed documents has been initiated in background', 'status':
                'reprocessing_started', 'track_id': ''}

        Attributes:
            status (Literal['reprocessing_started']): Status of the reprocessing operation
            message (str): Human-readable message describing the operation
            track_id (str | Unset): Always empty string. Reprocessed documents retain their original track_id from initial
                upload. Default: ''.
    """

    status: Literal["reprocessing_started"]
    message: str
    track_id: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        message = self.message

        track_id = self.track_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
            }
        )
        if track_id is not UNSET:
            field_dict["track_id"] = track_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = cast(Literal["reprocessing_started"], d.pop("status"))
        if status != "reprocessing_started":
            raise ValueError(
                f"status must match const 'reprocessing_started', got '{status}'"
            )

        message = d.pop("message")

        track_id = d.pop("track_id", UNSET)

        reprocess_response = cls(
            status=status,
            message=message,
            track_id=track_id,
        )

        reprocess_response.additional_properties = d
        return reprocess_response

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
