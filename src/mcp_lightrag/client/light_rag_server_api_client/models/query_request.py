from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.query_request_mode import QueryRequestMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_request_conversation_history_type_0_item import (
        QueryRequestConversationHistoryType0Item,
    )


T = TypeVar("T", bound="QueryRequest")


@_attrs_define
class QueryRequest:
    """
    Attributes:
        query (str): The query text
        mode (QueryRequestMode | Unset): Query mode Default: QueryRequestMode.MIX.
        only_need_context (bool | None | Unset): If True, only returns the retrieved context without generating a
            response.
        only_need_prompt (bool | None | Unset): If True, only returns the generated prompt without producing a response.
        response_type (None | str | Unset): Defines the response format. Examples: 'Multiple Paragraphs', 'Single
            Paragraph', 'Bullet Points'.
        top_k (int | None | Unset): Number of top items to retrieve. Represents entities in 'local' mode and
            relationships in 'global' mode.
        chunk_top_k (int | None | Unset): Number of text chunks to retrieve initially from vector search and keep after
            reranking.
        max_entity_tokens (int | None | Unset): Maximum number of tokens allocated for entity context in unified token
            control system.
        max_relation_tokens (int | None | Unset): Maximum number of tokens allocated for relationship context in unified
            token control system.
        max_total_tokens (int | None | Unset): Maximum total tokens budget for the entire query context (entities +
            relations + chunks + system prompt).
        hl_keywords (list[str] | Unset): List of high-level keywords to prioritize in retrieval. Leave empty to use the
            LLM to generate the keywords.
        ll_keywords (list[str] | Unset): List of low-level keywords to refine retrieval focus. Leave empty to use the
            LLM to generate the keywords.
        conversation_history (list[QueryRequestConversationHistoryType0Item] | None | Unset): History messages are only
            sent to LLM for context, not used for retrieval. Format: [{'role': 'user/assistant', 'content': 'message'}].
        user_prompt (None | str | Unset): User-provided prompt for the query. If provided, this will be used instead of
            the default value from prompt template.
        enable_rerank (bool | None | Unset): Enable reranking for retrieved text chunks. If True but no rerank model is
            configured, a warning will be issued. Default is True.
        include_references (bool | None | Unset): If True, includes reference list in responses. Affects /query and
            /query/stream endpoints. /query/data always includes references. Default: True.
        include_chunk_content (bool | None | Unset): If True, includes actual chunk text content in references. Only
            applies when include_references=True. Useful for evaluation and debugging. Default: False.
        stream (bool | None | Unset): If True, enables streaming output for real-time responses. Only affects
            /query/stream endpoint. Default: True.
    """

    query: str
    mode: QueryRequestMode | Unset = QueryRequestMode.MIX
    only_need_context: bool | None | Unset = UNSET
    only_need_prompt: bool | None | Unset = UNSET
    response_type: None | str | Unset = UNSET
    top_k: int | None | Unset = UNSET
    chunk_top_k: int | None | Unset = UNSET
    max_entity_tokens: int | None | Unset = UNSET
    max_relation_tokens: int | None | Unset = UNSET
    max_total_tokens: int | None | Unset = UNSET
    hl_keywords: list[str] | Unset = UNSET
    ll_keywords: list[str] | Unset = UNSET
    conversation_history: (
        list[QueryRequestConversationHistoryType0Item] | None | Unset
    ) = UNSET
    user_prompt: None | str | Unset = UNSET
    enable_rerank: bool | None | Unset = UNSET
    include_references: bool | None | Unset = True
    include_chunk_content: bool | None | Unset = False
    stream: bool | None | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        only_need_context: bool | None | Unset
        if isinstance(self.only_need_context, Unset):
            only_need_context = UNSET
        else:
            only_need_context = self.only_need_context

        only_need_prompt: bool | None | Unset
        if isinstance(self.only_need_prompt, Unset):
            only_need_prompt = UNSET
        else:
            only_need_prompt = self.only_need_prompt

        response_type: None | str | Unset
        if isinstance(self.response_type, Unset):
            response_type = UNSET
        else:
            response_type = self.response_type

        top_k: int | None | Unset
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        chunk_top_k: int | None | Unset
        if isinstance(self.chunk_top_k, Unset):
            chunk_top_k = UNSET
        else:
            chunk_top_k = self.chunk_top_k

        max_entity_tokens: int | None | Unset
        if isinstance(self.max_entity_tokens, Unset):
            max_entity_tokens = UNSET
        else:
            max_entity_tokens = self.max_entity_tokens

        max_relation_tokens: int | None | Unset
        if isinstance(self.max_relation_tokens, Unset):
            max_relation_tokens = UNSET
        else:
            max_relation_tokens = self.max_relation_tokens

        max_total_tokens: int | None | Unset
        if isinstance(self.max_total_tokens, Unset):
            max_total_tokens = UNSET
        else:
            max_total_tokens = self.max_total_tokens

        hl_keywords: list[str] | Unset = UNSET
        if not isinstance(self.hl_keywords, Unset):
            hl_keywords = self.hl_keywords

        ll_keywords: list[str] | Unset = UNSET
        if not isinstance(self.ll_keywords, Unset):
            ll_keywords = self.ll_keywords

        conversation_history: list[dict[str, Any]] | None | Unset
        if isinstance(self.conversation_history, Unset):
            conversation_history = UNSET
        elif isinstance(self.conversation_history, list):
            conversation_history = []
            for conversation_history_type_0_item_data in self.conversation_history:
                conversation_history_type_0_item = (
                    conversation_history_type_0_item_data.to_dict()
                )
                conversation_history.append(conversation_history_type_0_item)

        else:
            conversation_history = self.conversation_history

        user_prompt: None | str | Unset
        if isinstance(self.user_prompt, Unset):
            user_prompt = UNSET
        else:
            user_prompt = self.user_prompt

        enable_rerank: bool | None | Unset
        if isinstance(self.enable_rerank, Unset):
            enable_rerank = UNSET
        else:
            enable_rerank = self.enable_rerank

        include_references: bool | None | Unset
        if isinstance(self.include_references, Unset):
            include_references = UNSET
        else:
            include_references = self.include_references

        include_chunk_content: bool | None | Unset
        if isinstance(self.include_chunk_content, Unset):
            include_chunk_content = UNSET
        else:
            include_chunk_content = self.include_chunk_content

        stream: bool | None | Unset
        if isinstance(self.stream, Unset):
            stream = UNSET
        else:
            stream = self.stream

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if only_need_context is not UNSET:
            field_dict["only_need_context"] = only_need_context
        if only_need_prompt is not UNSET:
            field_dict["only_need_prompt"] = only_need_prompt
        if response_type is not UNSET:
            field_dict["response_type"] = response_type
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if chunk_top_k is not UNSET:
            field_dict["chunk_top_k"] = chunk_top_k
        if max_entity_tokens is not UNSET:
            field_dict["max_entity_tokens"] = max_entity_tokens
        if max_relation_tokens is not UNSET:
            field_dict["max_relation_tokens"] = max_relation_tokens
        if max_total_tokens is not UNSET:
            field_dict["max_total_tokens"] = max_total_tokens
        if hl_keywords is not UNSET:
            field_dict["hl_keywords"] = hl_keywords
        if ll_keywords is not UNSET:
            field_dict["ll_keywords"] = ll_keywords
        if conversation_history is not UNSET:
            field_dict["conversation_history"] = conversation_history
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt
        if enable_rerank is not UNSET:
            field_dict["enable_rerank"] = enable_rerank
        if include_references is not UNSET:
            field_dict["include_references"] = include_references
        if include_chunk_content is not UNSET:
            field_dict["include_chunk_content"] = include_chunk_content
        if stream is not UNSET:
            field_dict["stream"] = stream

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_request_conversation_history_type_0_item import (
            QueryRequestConversationHistoryType0Item,
        )

        d = dict(src_dict)
        query = d.pop("query")

        _mode = d.pop("mode", UNSET)
        mode: QueryRequestMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = QueryRequestMode(_mode)

        def _parse_only_need_context(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        only_need_context = _parse_only_need_context(d.pop("only_need_context", UNSET))

        def _parse_only_need_prompt(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        only_need_prompt = _parse_only_need_prompt(d.pop("only_need_prompt", UNSET))

        def _parse_response_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        response_type = _parse_response_type(d.pop("response_type", UNSET))

        def _parse_top_k(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_chunk_top_k(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        chunk_top_k = _parse_chunk_top_k(d.pop("chunk_top_k", UNSET))

        def _parse_max_entity_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_entity_tokens = _parse_max_entity_tokens(d.pop("max_entity_tokens", UNSET))

        def _parse_max_relation_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_relation_tokens = _parse_max_relation_tokens(
            d.pop("max_relation_tokens", UNSET)
        )

        def _parse_max_total_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_total_tokens = _parse_max_total_tokens(d.pop("max_total_tokens", UNSET))

        hl_keywords = cast(list[str], d.pop("hl_keywords", UNSET))

        ll_keywords = cast(list[str], d.pop("ll_keywords", UNSET))

        def _parse_conversation_history(
            data: object,
        ) -> list[QueryRequestConversationHistoryType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                conversation_history_type_0 = []
                _conversation_history_type_0 = data
                for (
                    conversation_history_type_0_item_data
                ) in _conversation_history_type_0:
                    conversation_history_type_0_item = (
                        QueryRequestConversationHistoryType0Item.from_dict(
                            conversation_history_type_0_item_data
                        )
                    )

                    conversation_history_type_0.append(conversation_history_type_0_item)

                return conversation_history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                list[QueryRequestConversationHistoryType0Item] | None | Unset, data
            )

        conversation_history = _parse_conversation_history(
            d.pop("conversation_history", UNSET)
        )

        def _parse_user_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        def _parse_enable_rerank(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        enable_rerank = _parse_enable_rerank(d.pop("enable_rerank", UNSET))

        def _parse_include_references(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        include_references = _parse_include_references(
            d.pop("include_references", UNSET)
        )

        def _parse_include_chunk_content(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        include_chunk_content = _parse_include_chunk_content(
            d.pop("include_chunk_content", UNSET)
        )

        def _parse_stream(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        stream = _parse_stream(d.pop("stream", UNSET))

        query_request = cls(
            query=query,
            mode=mode,
            only_need_context=only_need_context,
            only_need_prompt=only_need_prompt,
            response_type=response_type,
            top_k=top_k,
            chunk_top_k=chunk_top_k,
            max_entity_tokens=max_entity_tokens,
            max_relation_tokens=max_relation_tokens,
            max_total_tokens=max_total_tokens,
            hl_keywords=hl_keywords,
            ll_keywords=ll_keywords,
            conversation_history=conversation_history,
            user_prompt=user_prompt,
            enable_rerank=enable_rerank,
            include_references=include_references,
            include_chunk_content=include_chunk_content,
            stream=stream,
        )

        query_request.additional_properties = d
        return query_request

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
