from typing import TypedDict
from uuid import UUID

from langgraph.graph import END, StateGraph
from opentelemetry import trace

from app.domain.mentor.memory import MemoryStore
from app.domain.mentor.prompts import MENTOR_SYSTEM_PROMPT
from app.domain.mentor.provider import ProviderChain

tracer = trace.get_tracer(__name__)


class MentorState(TypedDict):
    user_id: UUID
    message: str
    mode: str
    context: list[str]
    answer: str


class AIOrchestrator:
    def __init__(self, provider: ProviderChain | None = None, memory: MemoryStore | None = None) -> None:
        self.provider = provider or ProviderChain()
        self.memory = memory or MemoryStore()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(MentorState)
        graph.add_node("retrieve_memory", self._retrieve_memory)
        graph.add_node("generate", self._generate)
        graph.set_entry_point("retrieve_memory")
        graph.add_edge("retrieve_memory", "generate")
        graph.add_edge("generate", END)
        return graph.compile()

    def _retrieve_memory(self, state: MentorState) -> MentorState:
        with tracer.start_as_current_span("ai_orchestrator.retrieve_memory"):
            state["context"] = self.memory.search(state["user_id"], state["message"])
            return state

    def _generate(self, state: MentorState) -> MentorState:
        with tracer.start_as_current_span("ai_orchestrator.generate") as span:
            span.set_attribute("mentor.mode", state["mode"])
            context = "\n".join(f"- {item}" for item in state["context"]) or "- No stored memory facts yet."
            messages = [
                {"role": "system", "content": MENTOR_SYSTEM_PROMPT},
                {"role": "user", "content": f"Mode: {state['mode']}\nMemory:\n{context}\n\nUser message:\n{state['message']}"},
            ]
            state["answer"] = self.provider.generate(messages)
            return state

    def mentor_chat(self, user_id: UUID, message: str, mode: str) -> str:
        result = self.graph.invoke({"user_id": user_id, "message": message, "mode": mode, "context": [], "answer": ""})
        self.memory.store_fact(user_id, f"Mentor exchange: {message} -> {result['answer'][:500]}", "mentor_chat")
        return result["answer"]
