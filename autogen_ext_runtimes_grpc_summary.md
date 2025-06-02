# autogen_ext.runtimes.grpc.GrpcWorkerAgentRuntime Summary

## Overview

The `GrpcWorkerAgentRuntime` class is an agent runtime for running remote or cross-language agents.

Agent messaging uses protobufs from `agent_worker.proto` and CloudEvent from `cloudevent.proto`.

Cross-language agents will additionally require all agents use shared protobuf schemas for any message types that are sent between agents.

## Parameters

*   `host_address` (str): The address of the gRPC host.
*   `tracer_provider` (Optional[TracerProvider], optional): The tracer provider for tracing. Defaults to None.
*   `extra_grpc_config` (Optional[Sequence[Tuple[str, Any]]], optional): Extra gRPC configuration. Defaults to None.
*   `payload_serialization_format` (str, optional): The serialization format for the payload. Defaults to `JSON_DATA_CONTENT_TYPE`.

## Methods

*   `add_message_serializer(serializer: MessageSerializer[Any] | Sequence[MessageSerializer[Any]])`: Add a new message serialization serializer to the runtime.
*   `add_subscription(subscription: Subscription)`: Add a new subscription that the runtime should fulfill when processing published messages.
*   `agent_load_state(agent: AgentId, state: Mapping[str, Any])`: Load the state of a single agent.
*   `agent_metadata(agent: AgentId)`: Get the metadata for an agent.
*   `agent_save_state(agent: AgentId)`: Save the state of a single agent.
*   `get(id_or_type: AgentId | AgentType | str, /, key: str = 'default', *, lazy: bool = True)`:
*   `load_state(state: Mapping[str, Any])`: Load the state of the entire runtime, including all hosted agents.
*   `publish_message(message: Any, topic_id: TopicId, *, sender: AgentId | None = None, cancellation_token: CancellationToken | None = None, message_id: str | None = None)`: Publish a message to all agents in the given namespace.
*   `register_factory(type: str | AgentType, agent_factory: Callable[[], T | Awaitable[T]], *, expected_class: type[T] | None = None)`: Register an agent factory with the runtime associated with a specific type.
*   `remove_subscription(id: str)`: Remove a subscription from the runtime.
*   `save_state()`: Save the state of the entire runtime, including all hosted agents.
*   `send_message(message: Any, recipient: AgentId, *, sender: AgentId | None = None, cancellation_token: CancellationToken | None = None, message_id: str | None = None)`: Send a message to an agent and get a response.
*   `start()`: Start the runtime in a background task.
*   `stop()`: Stop the runtime immediately.
*   `stop_when_signal(signals: Sequence[Signals] = (signal.SIGTERM, signal.SIGINT))`: Stop the runtime when a signal is received.
*   `try_get_underlying_agent_instance(id: AgentId, type: Type[T] = Agent)`: Try to get the underlying agent instance by name and namespace.

## Classes

*   `GrpcWorkerAgentRuntimeHost(address: str, extra_grpc_config: Sequence[Tuple[str, Any]] | None = None)`: Hosts the gRPC server.
    *   `start()`: Start the server in a background task.
    *   `stop(grace: int = 5)`: Stop the server.
    *   `stop_when_signal(grace: int = 5, signals: Sequence[Signals] = (signal.SIGTERM, signal.SIGINT))`: Stop the server when a signal is received.
*   `GrpcWorkerAgentRuntimeHostServicer`: A gRPC servicer that hosts message delivery service for agents.
    *   `AddSubscription(request: AddSubscriptionRequest, context: ServicerContext[AddSubscriptionRequest, AddSubscriptionResponse])`:
    *   `GetSubscriptions(request: GetSubscriptionsRequest, context: ServicerContext[GetSubscriptionsRequest, GetSubscriptionsResponse])`:
    *   `OpenChannel(request_iterator: AsyncIterator[Message], context: ServicerContext[Message, Message])`:
    *   `OpenControlChannel(request_iterator: AsyncIterator[ControlMessage], context: ServicerContext[ControlMessage, ControlMessage])`:
    *   `RegisterAgent(request: RegisterAgentTypeRequest, context: ServicerContext[RegisterAgentTypeRequest, RegisterAgentTypeResponse])`:
    *   `RemoveSubscription(request: RemoveSubscriptionRequest, context: ServicerContext[RemoveSubscriptionRequest, RemoveSubscriptionResponse])`:

[Previous](autogen_ext.cache_store.redis.html)

[Next](autogen_ext.auth.azure.html)
