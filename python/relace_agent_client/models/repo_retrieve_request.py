from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RepoRetrieveRequest")


@_attrs_define
class RepoRetrieveRequest:
    """
    Attributes:
        query (str):
        filter_ (Union[None, Unset, str]):
        include_content (Union[Unset, bool]):  Default: False.
        score_threshold (Union[Unset, float]):  Default: 0.3.
        token_limit (Union[Unset, int]):  Default: 30000.
    """

    query: str
    filter_: Union[None, Unset, str] = UNSET
    include_content: Union[Unset, bool] = False
    score_threshold: Union[Unset, float] = 0.3
    token_limit: Union[Unset, int] = 30000
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        filter_: Union[None, Unset, str]
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = self.filter_

        include_content = self.include_content

        score_threshold = self.score_threshold

        token_limit = self.token_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if include_content is not UNSET:
            field_dict["include_content"] = include_content
        if score_threshold is not UNSET:
            field_dict["score_threshold"] = score_threshold
        if token_limit is not UNSET:
            field_dict["token_limit"] = token_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        def _parse_filter_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        include_content = d.pop("include_content", UNSET)

        score_threshold = d.pop("score_threshold", UNSET)

        token_limit = d.pop("token_limit", UNSET)

        repo_retrieve_request = cls(
            query=query,
            filter_=filter_,
            include_content=include_content,
            score_threshold=score_threshold,
            token_limit=token_limit,
        )

        repo_retrieve_request.additional_properties = d
        return repo_retrieve_request

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
