from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PaginationInfo")


@_attrs_define
class PaginationInfo:
    """Pagination information

    Attributes:
        page: Current page number
        page_size: Number of items per page
        total_count: Total number of items
        total_pages: Total number of pages
        has_next: Whether there is a next page
        has_prev: Whether there is a previous page

        Example:
            {'has_next': True, 'has_prev': False, 'page': 1, 'page_size': 50, 'total_count': 150, 'total_pages': 3}

        Attributes:
            page (int): Current page number
            page_size (int): Number of items per page
            total_count (int): Total number of items
            total_pages (int): Total number of pages
            has_next (bool): Whether there is a next page
            has_prev (bool): Whether there is a previous page
    """

    page: int
    page_size: int
    total_count: int
    total_pages: int
    has_next: bool
    has_prev: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        page_size = self.page_size

        total_count = self.total_count

        total_pages = self.total_pages

        has_next = self.has_next

        has_prev = self.has_prev

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page = d.pop("page")

        page_size = d.pop("page_size")

        total_count = d.pop("total_count")

        total_pages = d.pop("total_pages")

        has_next = d.pop("has_next")

        has_prev = d.pop("has_prev")

        pagination_info = cls(
            page=page,
            page_size=page_size,
            total_count=total_count,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev,
        )

        pagination_info.additional_properties = d
        return pagination_info

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
