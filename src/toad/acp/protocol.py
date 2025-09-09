from typing import TypedDict, Required, Literal


# https://agentclientprotocol.com/protocol/schema#clientcapabilities
class ClientCapabilities(TypedDict, total=False):
    fs: Required[dict[str, bool]]
    terminal: bool


# https://agentclientprotocol.com/protocol/schema#promptcapabilities
class PromptCapabilities(TypedDict):
    audio: bool
    embeddedContent: bool
    image: bool


# https://agentclientprotocol.com/protocol/schema#agentcapabilities
class AgentCapabilities(TypedDict):
    loadSession: bool
    promptCapabilities: PromptCapabilities


class AuthMethod(TypedDict, total=False):
    description: str | None
    id: Required[str]
    name: Required[str]


class InitializeResponse(TypedDict):
    agentCapabilities: AgentCapabilities
    authMethods: list[AuthMethod]
    protocolVersion: Required[int]


class EnvVariable(TypedDict):
    name: str
    value: str


# https://agentclientprotocol.com/protocol/schema#mcpserver
class McpServer(TypedDict):
    args: list[str]
    command: str
    env: list[EnvVariable]
    name: str


class NewSessionResponse(TypedDict):
    sessionId: str


# https://modelcontextprotocol.io/specification/2025-06-18/server/resources#annotations
class Annotations(TypedDict):
    audience: list[str]
    priority: float
    lastModified: str


class TextContent(TypedDict, total=False):
    type: Required[str]
    text: Required[str]
    annotations: Annotations


class ImageContent(TypedDict, total=False):
    type: Required[str]
    data: Required[str]
    mimeType: Required[str]
    url: str
    annotations: Annotations


class AudioContent(TypedDict, total=False):
    type: Required[str]
    data: Required[str]
    mimeType: Required[str]
    Annotations: Annotations


class EmbeddedResourceText(TypedDict, total=False):
    uri: Required[str]
    text: Required[str]
    mimeType: str


class EmbeddedResourceBlob(TypedDict, total=False):
    uri: Required[str]
    blob: Required[str]
    mimeType: str


# https://agentclientprotocol.com/protocol/content#embedded-resource
class EmbeddedResourceContent(TypedDict, total=False):
    type: Required[str]
    resource: EmbeddedResourceText | EmbeddedResourceBlob


class ResourceLinkContent(TypedDict, total=False):
    annotations: Annotations | None
    description: str | None
    mimeType: str | None
    name: Required[str]
    size: int | None
    title: str | None
    type: Required[str]
    uri: Required[str]


type ContentBlock = (
    TextContent
    | ImageContent
    | AudioContent
    | EmbeddedResourceContent
    | ResourceLinkContent
)


class UserMessageChunk(TypedDict):
    content: ContentBlock
    sessionUpdate: str


class AgentMessageChunk(TypedDict):
    content: ContentBlock
    sessionUpdate: str


class AgentThoughtChunk(TypedDict):
    content: ContentBlock
    sessionUpdate: str


class ToolCallContentContent(TypedDict):
    content: ContentBlock
    type: str


class ToolCallContentDiff(TypedDict, total=False):
    newText: Required[str]
    oldText: str
    path: Required[str]
    type: Required[str]


class ToolCallContentTerminal(TypedDict, total=False):
    terminalId: str
    type: str


# https://agentclientprotocol.com/protocol/schema#toolcallcontent
type ToolCallContent = (
    ToolCallContentContent | ToolCallContentDiff | ToolCallContentTerminal
)

# https://agentclientprotocol.com/protocol/schema#toolkind
type ToolKind = Literal[
    "read",
    "edit",
    "delete",
    "move",
    "search",
    "execute",
    "think",
    "fetch",
    "switch_mode",
    "other",
]

type ToolCallStatus = Literal["pending", "in_progress", "completed", "failed"]


class ToolCallLocation(TypedDict, total=False):
    line: int | None
    path: Required[str]


type ToolCallId = str


class ToolCall(TypedDict):
    content: list[ToolCallContent]
    kind: ToolKind
    locations: list[ToolCallLocation]
    rawInput: dict
    rawOutput: dict
    sessionUpdate: Required[str]
    status: ToolCallStatus
    title: str
    toolCallId: ToolCallId


class ToolCallUpdate(TypedDict, total=False):
    content: list | None
    kind: ToolKind | None
    locations: list | None
    rawInput: dict
    rawOutput: dict
    sessionUpdate: Required[str]
    status: ToolCallStatus | None
    title: str | None
    toolCallId: ToolCallId


class PlanEntry(TypedDict, total=False):
    content: Required[str]
    priority: Literal["high", "medium", "low"]
    status: Literal["pending", "in_progress", "completed"]


# https://agentclientprotocol.com/protocol/schema#param-plan
class Plan(TypedDict, total=False):
    entries: Required[list[PlanEntry]]
    sessionUpdate: str


class AvailableCommandInput(TypedDict, total=False):
    hint: Required[str]


class AvailableCommand(TypedDict, total=False):
    description: Required[str]
    input: AvailableCommandInput | None
    name: Required[str]


class AvailableCommandsUpdate(TypedDict, total=False):
    availableCommands: Required[list[AvailableCommand]]
    sessionUpdate: Required[str]


class CurrentModeUpdate(TypedDict, total=False):
    currentModeId: Required[str]
    sessionUpdate: Required[str]


type SessionUpdate = (
    UserMessageChunk
    | AgentMessageChunk
    | AgentThoughtChunk
    | ToolCall
    | ToolCallUpdate
    | Plan
    | AvailableCommandsUpdate
    | CurrentModeUpdate
)


class SessionNotification(TypedDict):
    sessionId: str
    update: SessionUpdate
