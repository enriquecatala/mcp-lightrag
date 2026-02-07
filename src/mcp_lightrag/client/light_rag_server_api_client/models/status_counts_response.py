from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status_counts_response_status_counts import (
        StatusCountsResponseStatusCounts,
    )


T = TypeVar("T", bound="StatusCountsResponse")


@_attrs_define
class StatusCountsResponse:
    """Response model for document status counts

    Attributes:
        status_counts: Count of documents by status

        Example:
            {'status_counts': {'FAILED': 5, 'PENDING': 10, 'PREPROCESSED': 5, 'PROCESSED': 130, 'PROCESSING': 5}}

        Attributes:
            status_counts (StatusCountsResponseStatusCounts): Count of documents by status
    """

    status_counts: StatusCountsResponseStatusCounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status_counts = self.status_counts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status_counts": status_counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status_counts_response_status_counts import (
            StatusCountsResponseStatusCounts,
        )

        d = dict(src_dict)
        status_counts = StatusCountsResponseStatusCounts.from_dict(
            d.pop("status_counts")
        )

        status_counts_response = cls(
            status_counts=status_counts,
        )

        status_counts_response.additional_properties = d
        return status_counts_response

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
