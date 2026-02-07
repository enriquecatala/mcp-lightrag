from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.query_data_response_data import QueryDataResponseData
    from ..models.query_data_response_metadata import QueryDataResponseMetadata


T = TypeVar("T", bound="QueryDataResponse")


@_attrs_define
class QueryDataResponse:
    """
    Attributes:
        status (str): Query execution status
        message (str): Status message
        data (QueryDataResponseData): Query result data containing entities, relationships, chunks, and references
        metadata (QueryDataResponseMetadata): Query metadata including mode, keywords, and processing information
    """

    status: str
    message: str
    data: QueryDataResponseData
    metadata: QueryDataResponseMetadata
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        message = self.message

        data = self.data.to_dict()

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "message": message,
                "data": data,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_data_response_data import QueryDataResponseData
        from ..models.query_data_response_metadata import QueryDataResponseMetadata

        d = dict(src_dict)
        status = d.pop("status")

        message = d.pop("message")

        data = QueryDataResponseData.from_dict(d.pop("data"))

        metadata = QueryDataResponseMetadata.from_dict(d.pop("metadata"))

        query_data_response = cls(
            status=status,
            message=message,
            data=data,
            metadata=metadata,
        )

        query_data_response.additional_properties = d
        return query_data_response

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
