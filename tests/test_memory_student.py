from __future__ import annotations

from types import SimpleNamespace

from src.memory_student import StudentMemory


class GraphStub:
    def __init__(self, responses=None):
        self.calls = []
        self.responses = list(responses or [SimpleNamespace()])

    def search(self, **kwargs):
        self.calls.append(kwargs)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_long_term_combines_context_block_and_user_facts(monkeypatch):
    graph = GraphStub(
        [SimpleNamespace(edges=[SimpleNamespace(fact="Python", valid_at="now", invalid_at=None)])]
    )
    client = SimpleNamespace(
        thread=SimpleNamespace(
            get_user_context=lambda **kwargs: SimpleNamespace(context="Current user context")
        ),
        graph=graph,
    )
    primed = []
    monkeypatch.setattr(
        "src.memory_student.prime_eval_thread",
        lambda *args: primed.append(args),
    )

    text = StudentMemory(client).retrieve_long_term("user-1", "thread-1", "preference")

    assert primed
    assert "Current user context" in text
    assert "FACT: Python" in text
    assert graph.calls[0]["user_id"] == "user-1"
    assert graph.calls[0]["scope"] == "edges"
    assert graph.calls[0]["limit"] == 20


def test_episodic_search_is_user_scoped_and_caps_query():
    graph = GraphStub([SimpleNamespace(episodes=[SimpleNamespace(content="ASYNC-FIX-20", metadata={})])])
    client = SimpleNamespace(graph=graph)

    text = StudentMemory(client).retrieve_episodic("user-1", "word " * 120)

    assert "ASYNC-FIX-20" in text
    assert graph.calls[0]["user_id"] == "user-1"
    assert graph.calls[0]["scope"] == "episodes"
    assert len(graph.calls[0]["query"]) <= 400


def test_semantic_search_falls_back_to_nodes():
    graph = GraphStub(
        [RuntimeError("episodes unavailable"), SimpleNamespace(nodes=[SimpleNamespace(name="Rule", summary="Idempotency-Key")])]
    )
    client = SimpleNamespace(graph=graph)

    text = StudentMemory(client).retrieve_semantic("shared-kb", "payment retry")

    assert "Idempotency-Key" in text
    assert [call["scope"] for call in graph.calls] == ["episodes", "nodes"]
    assert all(call["graph_id"] == "shared-kb" for call in graph.calls)


def test_assemble_context_uses_layer_priority_and_budget():
    memory = StudentMemory(SimpleNamespace())

    merged, breakdown = memory.assemble_context(
        {
            "semantic": "shared rule",
            "short_term": "recent turn",
            "long_term": "user preference",
            "episodic": "past outcome",
        }
    )

    assert merged.index("<SHORT_TERM>") < merged.index("<LONG_TERM>")
    assert merged.index("<LONG_TERM>") < merged.index("<EPISODIC>")
    assert merged.index("<EPISODIC>") < merged.index("<SEMANTIC>")
    assert breakdown["short_term"]["limit_tokens"] == 800
    assert breakdown["long_term"]["limit_tokens"] == 320
    assert breakdown["episodic"]["limit_tokens"] == 240
    assert breakdown["semantic"]["limit_tokens"] == 240
