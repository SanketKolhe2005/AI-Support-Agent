def verify_answer(state):
    
    if state["sources"]:
        return state

    state["answer"] = "Unable to answer from the knowledge base."

    state["confidence"] = 0.0

    return state