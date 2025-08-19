from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.repo_agent_request_agent_inputs import RepoAgentRequestAgentInputs
    from ..models.repo_agent_request_overrides_type_0 import RepoAgentRequestOverridesType0


T = TypeVar("T", bound="RepoAgentRequest")


@_attrs_define
class RepoAgentRequest:
    """
    Attributes:
        agent_name (str):
        agent_inputs (RepoAgentRequestAgentInputs):
        overrides (Union['RepoAgentRequestOverridesType0', None, Unset]):
    """

    agent_name: str
    agent_inputs: "RepoAgentRequestAgentInputs"
    overrides: Union["RepoAgentRequestOverridesType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.repo_agent_request_overrides_type_0 import RepoAgentRequestOverridesType0

        agent_name = self.agent_name

        agent_inputs = self.agent_inputs.to_dict()

        overrides: Union[None, Unset, dict[str, Any]]
        if isinstance(self.overrides, Unset):
            overrides = UNSET
        elif isinstance(self.overrides, RepoAgentRequestOverridesType0):
            overrides = self.overrides.to_dict()
        else:
            overrides = self.overrides

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_name": agent_name,
                "agent_inputs": agent_inputs,
            }
        )
        if overrides is not UNSET:
            field_dict["overrides"] = overrides

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.repo_agent_request_agent_inputs import RepoAgentRequestAgentInputs
        from ..models.repo_agent_request_overrides_type_0 import RepoAgentRequestOverridesType0

        d = dict(src_dict)
        agent_name = d.pop("agent_name")

        agent_inputs = RepoAgentRequestAgentInputs.from_dict(d.pop("agent_inputs"))

        def _parse_overrides(data: object) -> Union["RepoAgentRequestOverridesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                overrides_type_0 = RepoAgentRequestOverridesType0.from_dict(data)

                return overrides_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RepoAgentRequestOverridesType0", None, Unset], data)

        overrides = _parse_overrides(d.pop("overrides", UNSET))

        repo_agent_request = cls(
            agent_name=agent_name,
            agent_inputs=agent_inputs,
            overrides=overrides,
        )

        repo_agent_request.additional_properties = d
        return repo_agent_request

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
