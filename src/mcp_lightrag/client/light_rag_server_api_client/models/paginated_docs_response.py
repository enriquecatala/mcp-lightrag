from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.doc_status_response import DocStatusResponse
    from ..models.paginated_docs_response_status_counts import (
        PaginatedDocsResponseStatusCounts,
    )
    from ..models.pagination_info import PaginationInfo


T = TypeVar("T", bound="PaginatedDocsResponse")


@_attrs_define
class PaginatedDocsResponse:
    """Response model for paginated document queries

    Attributes:
        documents: List of documents for the current page
        pagination: Pagination information
        status_counts: Count of documents by status for all documents

        Example:
            {'documents': [{'chunks_count': 12, 'content_length': 15240, 'content_summary': 'Research paper on machine
                learning', 'created_at': '2025-03-31T12:34:56', 'file_path': 'research_paper.pdf', 'id': 'doc_123456',
                'metadata': {'author': 'John Doe', 'year': 2025}, 'status': 'PROCESSED', 'track_id':
                'upload_20250729_170612_abc123', 'updated_at': '2025-03-31T12:35:30'}], 'pagination': {'has_next': True,
                'has_prev': False, 'page': 1, 'page_size': 50, 'total_count': 150, 'total_pages': 3}, 'status_counts':
                {'FAILED': 5, 'PENDING': 10, 'PREPROCESSED': 5, 'PROCESSED': 130, 'PROCESSING': 5}}

        Attributes:
            documents (list[DocStatusResponse]): List of documents for the current page
            pagination (PaginationInfo): Pagination information

                Attributes:
                    page: Current page number
                    page_size: Number of items per page
                    total_count: Total number of items
                    total_pages: Total number of pages
                    has_next: Whether there is a next page
                    has_prev: Whether there is a previous page Example: {'has_next': True, 'has_prev': False, 'page': 1,
                'page_size': 50, 'total_count': 150, 'total_pages': 3}.
            status_counts (PaginatedDocsResponseStatusCounts): Count of documents by status for all documents
    """

    documents: list[DocStatusResponse]
    pagination: PaginationInfo
    status_counts: PaginatedDocsResponseStatusCounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)

        pagination = self.pagination.to_dict()

        status_counts = self.status_counts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documents": documents,
                "pagination": pagination,
                "status_counts": status_counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doc_status_response import DocStatusResponse
        from ..models.paginated_docs_response_status_counts import (
            PaginatedDocsResponseStatusCounts,
        )
        from ..models.pagination_info import PaginationInfo

        d = dict(src_dict)
        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = DocStatusResponse.from_dict(documents_item_data)

            documents.append(documents_item)

        pagination = PaginationInfo.from_dict(d.pop("pagination"))

        status_counts = PaginatedDocsResponseStatusCounts.from_dict(
            d.pop("status_counts")
        )

        paginated_docs_response = cls(
            documents=documents,
            pagination=pagination,
            status_counts=status_counts,
        )

        paginated_docs_response.additional_properties = d
        return paginated_docs_response

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
