from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.doc_status_response import DocStatusResponse
    from ..models.track_status_response_status_summary import (
        TrackStatusResponseStatusSummary,
    )


T = TypeVar("T", bound="TrackStatusResponse")


@_attrs_define
class TrackStatusResponse:
    """Response model for tracking document processing status by track_id

    Attributes:
        track_id: The tracking ID
        documents: List of documents associated with this track_id
        total_count: Total number of documents for this track_id
        status_summary: Count of documents by status

        Example:
            {'documents': [{'chunks_count': 12, 'content_length': 15240, 'content_summary': 'Research paper on machine
                learning', 'created_at': '2025-03-31T12:34:56', 'file_path': 'research_paper.pdf', 'id': 'doc_123456',
                'metadata': {'author': 'John Doe', 'year': 2025}, 'status': 'PROCESSED', 'track_id':
                'upload_20250729_170612_abc123', 'updated_at': '2025-03-31T12:35:30'}], 'status_summary': {'PROCESSED': 1},
                'total_count': 1, 'track_id': 'upload_20250729_170612_abc123'}

        Attributes:
            track_id (str): The tracking ID
            documents (list[DocStatusResponse]): List of documents associated with this track_id
            total_count (int): Total number of documents for this track_id
            status_summary (TrackStatusResponseStatusSummary): Count of documents by status
    """

    track_id: str
    documents: list[DocStatusResponse]
    total_count: int
    status_summary: TrackStatusResponseStatusSummary
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        track_id = self.track_id

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)

        total_count = self.total_count

        status_summary = self.status_summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "track_id": track_id,
                "documents": documents,
                "total_count": total_count,
                "status_summary": status_summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doc_status_response import DocStatusResponse
        from ..models.track_status_response_status_summary import (
            TrackStatusResponseStatusSummary,
        )

        d = dict(src_dict)
        track_id = d.pop("track_id")

        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = DocStatusResponse.from_dict(documents_item_data)

            documents.append(documents_item)

        total_count = d.pop("total_count")

        status_summary = TrackStatusResponseStatusSummary.from_dict(
            d.pop("status_summary")
        )

        track_status_response = cls(
            track_id=track_id,
            documents=documents,
            total_count=total_count,
            status_summary=status_summary,
        )

        track_status_response.additional_properties = d
        return track_status_response

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
