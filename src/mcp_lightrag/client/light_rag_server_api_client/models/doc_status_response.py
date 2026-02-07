from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.doc_status import DocStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.doc_status_response_metadata_type_0 import (
        DocStatusResponseMetadataType0,
    )


T = TypeVar("T", bound="DocStatusResponse")


@_attrs_define
class DocStatusResponse:
    """
    Example:
        {'chunks_count': 12, 'content_length': 15240, 'content_summary': 'Research paper on machine learning',
            'created_at': '2025-03-31T12:34:56', 'file_path': 'research_paper.pdf', 'id': 'doc_123456', 'metadata':
            {'author': 'John Doe', 'year': 2025}, 'status': 'processed', 'track_id': 'upload_20250729_170612_abc123',
            'updated_at': '2025-03-31T12:35:30'}

    Attributes:
        id (str): Document identifier
        content_summary (str): Summary of document content
        content_length (int): Length of document content in characters
        status (DocStatus): Document processing status
        created_at (str): Creation timestamp (ISO format string)
        updated_at (str): Last update timestamp (ISO format string)
        file_path (str): Path to the document file
        track_id (None | str | Unset): Tracking ID for monitoring progress
        chunks_count (int | None | Unset): Number of chunks the document was split into
        error_msg (None | str | Unset): Error message if processing failed
        metadata (DocStatusResponseMetadataType0 | None | Unset): Additional metadata about the document
    """

    id: str
    content_summary: str
    content_length: int
    status: DocStatus
    created_at: str
    updated_at: str
    file_path: str
    track_id: None | str | Unset = UNSET
    chunks_count: int | None | Unset = UNSET
    error_msg: None | str | Unset = UNSET
    metadata: DocStatusResponseMetadataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.doc_status_response_metadata_type_0 import (
            DocStatusResponseMetadataType0,
        )

        id = self.id

        content_summary = self.content_summary

        content_length = self.content_length

        status = self.status.value

        created_at = self.created_at

        updated_at = self.updated_at

        file_path = self.file_path

        track_id: None | str | Unset
        if isinstance(self.track_id, Unset):
            track_id = UNSET
        else:
            track_id = self.track_id

        chunks_count: int | None | Unset
        if isinstance(self.chunks_count, Unset):
            chunks_count = UNSET
        else:
            chunks_count = self.chunks_count

        error_msg: None | str | Unset
        if isinstance(self.error_msg, Unset):
            error_msg = UNSET
        else:
            error_msg = self.error_msg

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, DocStatusResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "content_summary": content_summary,
                "content_length": content_length,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "file_path": file_path,
            }
        )
        if track_id is not UNSET:
            field_dict["track_id"] = track_id
        if chunks_count is not UNSET:
            field_dict["chunks_count"] = chunks_count
        if error_msg is not UNSET:
            field_dict["error_msg"] = error_msg
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doc_status_response_metadata_type_0 import (
            DocStatusResponseMetadataType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        content_summary = d.pop("content_summary")

        content_length = d.pop("content_length")

        status = DocStatus(d.pop("status"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        file_path = d.pop("file_path")

        def _parse_track_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        track_id = _parse_track_id(d.pop("track_id", UNSET))

        def _parse_chunks_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        chunks_count = _parse_chunks_count(d.pop("chunks_count", UNSET))

        def _parse_error_msg(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_msg = _parse_error_msg(d.pop("error_msg", UNSET))

        def _parse_metadata(
            data: object,
        ) -> DocStatusResponseMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = DocStatusResponseMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DocStatusResponseMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        doc_status_response = cls(
            id=id,
            content_summary=content_summary,
            content_length=content_length,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            file_path=file_path,
            track_id=track_id,
            chunks_count=chunks_count,
            error_msg=error_msg,
            metadata=metadata,
        )

        doc_status_response.additional_properties = d
        return doc_status_response

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
