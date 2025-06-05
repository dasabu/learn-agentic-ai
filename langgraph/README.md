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

