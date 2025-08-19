import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.repo_log_item_event_type import RepoLogItemEventType

if TYPE_CHECKING:
    from ..models.agent_event import AgentEvent
    from ..models.build_event import BuildEvent
    from ..models.committed_event import CommittedEvent
    from ..models.deployed_event import DeployedEvent
    from ..models.done_event import DoneEvent
    from ..models.prompt_error_event import PromptErrorEvent
    from ..models.repo_agent_request import RepoAgentRequest
    from ..models.started_event import StartedEvent
    from ..models.test_event import TestEvent
    from ..models.tool_event import ToolEvent


T = TypeVar("T", bound="RepoLogItem")


@_attrs_define
class RepoLogItem:
    """
    Attributes:
        timestamp (datetime.datetime):
        event_type (RepoLogItemEventType):
        event (Union['AgentEvent', 'BuildEvent', 'CommittedEvent', 'DeployedEvent', 'DoneEvent', 'PromptErrorEvent',
            'RepoAgentRequest', 'StartedEvent', 'TestEvent', 'ToolEvent']):
    """

    timestamp: datetime.datetime
    event_type: RepoLogItemEventType
    event: Union[
        "AgentEvent",
        "BuildEvent",
        "CommittedEvent",
        "DeployedEvent",
        "DoneEvent",
        "PromptErrorEvent",
        "RepoAgentRequest",
        "StartedEvent",
        "TestEvent",
        "ToolEvent",
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_event import AgentEvent
        from ..models.build_event import BuildEvent
        from ..models.committed_event import CommittedEvent
        from ..models.deployed_event import DeployedEvent
        from ..models.prompt_error_event import PromptErrorEvent
        from ..models.repo_agent_request import RepoAgentRequest
        from ..models.started_event import StartedEvent
        from ..models.test_event import TestEvent
        from ..models.tool_event import ToolEvent

        timestamp = self.timestamp.isoformat()

        event_type = self.event_type.value

        event: dict[str, Any]
        if isinstance(self.event, RepoAgentRequest):
            event = self.event.to_dict()
        elif isinstance(self.event, PromptErrorEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, StartedEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, AgentEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, ToolEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, CommittedEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, BuildEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, TestEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, DeployedEvent):
            event = self.event.to_dict()
        else:
            event = self.event.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "event_type": event_type,
                "event": event,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_event import AgentEvent
        from ..models.build_event import BuildEvent
        from ..models.committed_event import CommittedEvent
        from ..models.deployed_event import DeployedEvent
        from ..models.done_event import DoneEvent
        from ..models.prompt_error_event import PromptErrorEvent
        from ..models.repo_agent_request import RepoAgentRequest
        from ..models.started_event import StartedEvent
        from ..models.test_event import TestEvent
        from ..models.tool_event import ToolEvent

        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        event_type = RepoLogItemEventType(d.pop("event_type"))

        def _parse_event(
            data: object,
        ) -> Union[
            "AgentEvent",
            "BuildEvent",
            "CommittedEvent",
            "DeployedEvent",
            "DoneEvent",
            "PromptErrorEvent",
            "RepoAgentRequest",
            "StartedEvent",
            "TestEvent",
            "ToolEvent",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_0 = RepoAgentRequest.from_dict(data)

                return event_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_1 = PromptErrorEvent.from_dict(data)

                return event_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_2 = StartedEvent.from_dict(data)

                return event_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_3 = AgentEvent.from_dict(data)

                return event_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_4 = ToolEvent.from_dict(data)

                return event_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_5 = CommittedEvent.from_dict(data)

                return event_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_6 = BuildEvent.from_dict(data)

                return event_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_7 = TestEvent.from_dict(data)

                return event_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_8 = DeployedEvent.from_dict(data)

                return event_type_8
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            event_type_9 = DoneEvent.from_dict(data)

            return event_type_9

        event = _parse_event(d.pop("event"))

        repo_log_item = cls(
            timestamp=timestamp,
            event_type=event_type,
            event=event,
        )

        repo_log_item.additional_properties = d
        return repo_log_item

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
