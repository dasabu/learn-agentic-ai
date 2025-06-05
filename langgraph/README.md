## Terminology

Agent workflows are represented as graphs:

- **State**: represents the current state of the application

- **Node**: python functions that represent agent logic. They receive the current **State** as input, do action and return a new (updated) **State**

- **Edge**: python functions that determine which **Node** to execute next based on the **State**. They can be conditional or fixed

***Nodes** do the work, **Edges** choose what to do next*

### Five steps:

1. Define the **State** class
2. Start the **Graph Build**
3. Create a **Node**
4. Create **Edges**
5. **Compile** the Graph

## State

State is **immutable**

```python
def my_counting_node(old_state: State) -> State:
    count = old_state.count
    count += 1
    new_state = State(count) # create new object
    return new_state
```

For each field in your State, you can specify a special function called a **Reducer**. When you return a new State, LangGraph uses reducer to combine these fields in the new State with the old State.

This enables LangGraph to run multiple nodes concurrently and combine State without overwriting.

---

### ⚠️ Super-Step & Checkpoint

- **Super-step**: can be considered a single iteration over the graph nodes. Nodes that run in parallel are part of the same super-step, while nodes that run sequentially belong to separate super-steps

- The graph describes one super-steps, one interaction between agents and tools to archive an outcome

- Every user interaction is a fresh `graph.invoke(state)` call

*The reducer handles updating state during a super-step but not between super-steps*

```
Define Graph (5 steps) -> Super-step (user question invoke the graph) -> Super-step (another question) -> ...
```

- **Checkpoint**: LangGraph uses checkpoints to keep track and preserve context between these super-steps. Checkpoint is a snapshot of the graph state saved at each super-step.