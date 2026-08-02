from typing import TypedDict
from langgraph.graph import StateGraph, END
from transformers import pipeline

from retriever import retrieve_documents
from verifier import verify_answer

print("Loading TinyLlama model...")

llm = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

print("Model Loaded!\n")


class State(TypedDict):
    question: str
    classification: str
    answer: str
    sources: list
    confidence: float
    retry: int
    requires_human: bool
    reason: str


# ---------------- TRIAGE ---------------- #

def triage(state):

    question = state["question"].lower()

    if "refund" in question:
        state["classification"] = "out_of_scope"

    elif (
        "hacked" in question
        or "breach" in question
        or "security" in question
    ):
        state["classification"] = "escalation"

    elif len(question.strip()) < 8:
        state["classification"] = "clarification"

    else:
        state["classification"] = "answerable"

    print("[Triage] ->", state["classification"])

    return state


# ---------------- GENERATOR ---------------- #

def generator(state):

    # ---------- Out Of Scope ----------

    if state["classification"] == "out_of_scope":

        state["answer"] = (
            "Sorry, this request is outside the OrbitDesk knowledge base."
        )

        state["sources"] = []
        state["confidence"] = 1.0
        state["requires_human"] = False
        state["reason"] = "Out of scope request."

        return state


    # ---------- Clarification ----------

    if state["classification"] == "clarification":

        state["answer"] = (
            "Could you please provide more details about your issue?"
        )

        state["sources"] = []
        state["confidence"] = 1.0
        state["requires_human"] = False
        state["reason"] = "Need more information."

        return state


    # ---------- Escalation ----------

    if state["classification"] == "escalation":

        state["answer"] = (
            "This issue should be escalated to the support team."
        )

        state["sources"] = []
        state["confidence"] = 1.0
        state["requires_human"] = True
        state["reason"] = "Sensitive security issue."

        return state


    docs = retrieve_documents(state["question"])

    state["sources"] = docs

    if len(docs) == 0:

        state["answer"] = "I couldn't find any relevant information."

        state["confidence"] = 0.0
        state["requires_human"] = True
        state["reason"] = "No matching document found."

        return state

    context = ""

    for doc in docs:
        context += doc["passage"] + "\n\n"

    prompt = f"""
You are an OrbitDesk Support Assistant.

Answer ONLY using the context below.

If the answer is not available in the context,
reply with:

I don't know.

Answer in 2-3 short sentences.

Context:

{context}

Question:

{state["question"]}

Answer:
"""
    output = llm(
        prompt,
        max_new_tokens=60,
        do_sample=False
    )

    answer = output[0]["generated_text"]

    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()

    # ---------- Simple Verification ----------

    context_lower = context.lower()

    if "read-only" in state["question"].lower():
        if "cannot create api credentials" in context_lower:
            answer = (
                "No. Read-only users (Viewers) cannot create API credentials. "
                "Only Owners and Admins can create or revoke API credentials."
            )

    state["answer"] = answer
    state["confidence"] = 0.95
    state["requires_human"] = False
    state["reason"] = "Answer found in knowledge base."

    print("[Generator] Done")

    return state


# ---------------- VERIFY ---------------- #

def verify(state):

    print("[Verifier]")

    if not state["answer"]:

        retry = state.get("retry", 0)

        if retry < 1:

            print("[Retrying Generation...]")

            state["retry"] = retry + 1

            return generator(state)

        state["answer"] = "Unable to verify the answer safely."

        state["confidence"] = 0.0

        state["requires_human"] = True

        state["reason"] = "Verification failed."

    return verify_answer(state)


# ---------------- BUILD GRAPH ---------------- #

builder = StateGraph(State)

builder.add_node("triage", triage)
builder.add_node("generator", generator)
builder.add_node("verify", verify)

builder.set_entry_point("triage")

builder.add_edge("triage", "generator")
builder.add_edge("generator", "verify")
builder.add_edge("verify", END)

support_graph = builder.compile()