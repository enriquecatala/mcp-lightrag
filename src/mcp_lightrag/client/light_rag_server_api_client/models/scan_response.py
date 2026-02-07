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

T = TypeVar("T", bound="ScanResponse")


@_attrs_define
class ScanResponse:
    """Response model for document scanning operation

    Attributes:
        status: Status of the scanning operation
        message: Optional message with additional details
        track_id: Tracking ID for monitoring scanning progress

        Example:
            {'message': 'Scanning process has been initiated in the background', 'status': 'scanning_started', 'track_id':
                'scan_20250729_170612_abc123'}

        Attributes:
            status (Literal['scanning_started']): Status of the scanning operation
            track_id (str): Tracking ID for monitoring scanning progress
            message (None | str | Unset): Additional details about the scanning operation
    """

    status: Literal["scanning_started"]
    track_id: str
    message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        track_id = self.track_id

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "track_id": track_id,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = cast(Literal["scanning_started"], d.pop("status"))
        if status != "scanning_started":
            raise ValueError(
                f"status must match const 'scanning_started', got '{status}'"
            )

        track_id = d.pop("track_id")

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        scan_response = cls(
            status=status,
            track_id=track_id,
            message=message,
        )

        scan_response.additional_properties = d
        return scan_response

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
