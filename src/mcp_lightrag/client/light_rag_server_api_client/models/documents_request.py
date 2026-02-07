from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.doc_status import DocStatus
from ..models.documents_request_sort_direction import DocumentsRequestSortDirection
from ..models.documents_request_sort_field import DocumentsRequestSortField
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentsRequest")


@_attrs_define
class DocumentsRequest:
    """Request model for paginated document queries

    Attributes:
        status_filter: Filter by document status, None for all statuses
        page: Page number (1-based)
        page_size: Number of documents per page (10-200)
        sort_field: Field to sort by ('created_at', 'updated_at', 'id', 'file_path')
        sort_direction: Sort direction ('asc' or 'desc')

        Example:
            {'page': 1, 'page_size': 50, 'sort_direction': 'desc', 'sort_field': 'updated_at', 'status_filter': 'PROCESSED'}

        Attributes:
            status_filter (DocStatus | None | Unset): Filter by document status, None for all statuses
            page (int | Unset): Page number (1-based) Default: 1.
            page_size (int | Unset): Number of documents per page (10-200) Default: 50.
            sort_field (DocumentsRequestSortField | Unset): Field to sort by Default: DocumentsRequestSortField.UPDATED_AT.
            sort_direction (DocumentsRequestSortDirection | Unset): Sort direction Default:
                DocumentsRequestSortDirection.DESC.
    """

    status_filter: DocStatus | None | Unset = UNSET
    page: int | Unset = 1
    page_size: int | Unset = 50
    sort_field: DocumentsRequestSortField | Unset = DocumentsRequestSortField.UPDATED_AT
    sort_direction: DocumentsRequestSortDirection | Unset = (
        DocumentsRequestSortDirection.DESC
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status_filter: None | str | Unset
        if isinstance(self.status_filter, Unset):
            status_filter = UNSET
        elif isinstance(self.status_filter, DocStatus):
            status_filter = self.status_filter.value
        else:
            status_filter = self.status_filter

        page = self.page

        page_size = self.page_size

        sort_field: str | Unset = UNSET
        if not isinstance(self.sort_field, Unset):
            sort_field = self.sort_field.value

        sort_direction: str | Unset = UNSET
        if not isinstance(self.sort_direction, Unset):
            sort_direction = self.sort_direction.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status_filter is not UNSET:
            field_dict["status_filter"] = status_filter
        if page is not UNSET:
            field_dict["page"] = page
        if page_size is not UNSET:
            field_dict["page_size"] = page_size
        if sort_field is not UNSET:
            field_dict["sort_field"] = sort_field
        if sort_direction is not UNSET:
            field_dict["sort_direction"] = sort_direction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_status_filter(data: object) -> DocStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_filter_type_0 = DocStatus(data)

                return status_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DocStatus | None | Unset, data)

        status_filter = _parse_status_filter(d.pop("status_filter", UNSET))

        page = d.pop("page", UNSET)

        page_size = d.pop("page_size", UNSET)

        _sort_field = d.pop("sort_field", UNSET)
        sort_field: DocumentsRequestSortField | Unset
        if isinstance(_sort_field, Unset):
            sort_field = UNSET
        else:
            sort_field = DocumentsRequestSortField(_sort_field)

        _sort_direction = d.pop("sort_direction", UNSET)
        sort_direction: DocumentsRequestSortDirection | Unset
        if isinstance(_sort_direction, Unset):
            sort_direction = UNSET
        else:
            sort_direction = DocumentsRequestSortDirection(_sort_direction)

        documents_request = cls(
            status_filter=status_filter,
            page=page,
            page_size=page_size,
            sort_field=sort_field,
            sort_direction=sort_direction,
        )

        documents_request.additional_properties = d
        return documents_request

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
