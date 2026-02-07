from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docs_statuses_response_statuses import DocsStatusesResponseStatuses


T = TypeVar("T", bound="DocsStatusesResponse")


@_attrs_define
class DocsStatusesResponse:
    """Response model for document statuses

    Attributes:
        statuses: Dictionary mapping document status to lists of document status responses

        Example:
            {'statuses': {'PENDING': [{'content_length': 5000, 'content_summary': 'Pending document', 'created_at':
                '2025-03-31T10:00:00', 'file_path': 'pending_doc.pdf', 'id': 'doc_123', 'status': 'pending', 'track_id':
                'upload_20250331_100000_abc123', 'updated_at': '2025-03-31T10:00:00'}], 'PREPROCESSED': [{'chunks_count': 10,
                'content_length': 7200, 'content_summary': 'Document pending final indexing', 'created_at':
                '2025-03-31T09:30:00', 'file_path': 'preprocessed_doc.pdf', 'id': 'doc_789', 'status': 'preprocessed',
                'track_id': 'upload_20250331_093000_xyz789', 'updated_at': '2025-03-31T09:35:00'}], 'PROCESSED':
                [{'chunks_count': 8, 'content_length': 8000, 'content_summary': 'Processed document', 'created_at':
                '2025-03-31T09:00:00', 'file_path': 'processed_doc.pdf', 'id': 'doc_456', 'metadata': {'author': 'John Doe'},
                'status': 'processed', 'track_id': 'insert_20250331_090000_def456', 'updated_at': '2025-03-31T09:05:00'}]}}

        Attributes:
            statuses (DocsStatusesResponseStatuses | Unset): Dictionary mapping document status to lists of document status
                responses
    """

    statuses: DocsStatusesResponseStatuses | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        statuses: dict[str, Any] | Unset = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = self.statuses.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if statuses is not UNSET:
            field_dict["statuses"] = statuses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docs_statuses_response_statuses import (
            DocsStatusesResponseStatuses,
        )

        d = dict(src_dict)
        _statuses = d.pop("statuses", UNSET)
        statuses: DocsStatusesResponseStatuses | Unset
        if isinstance(_statuses, Unset):
            statuses = UNSET
        else:
            statuses = DocsStatusesResponseStatuses.from_dict(_statuses)

        docs_statuses_response = cls(
            statuses=statuses,
        )

        docs_statuses_response.additional_properties = d
        return docs_statuses_response

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
