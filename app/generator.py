# generator.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import ToolMessage, AIMessage

from llm import llm
from unplash import fetch_image_from_unsplash

# Bind tools to LLM
llm_with_tools = llm.bind_tools([fetch_image_from_unsplash])

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder("messages"),
    ]
)

# Agent flow
agent = RunnableSequence(prompt, llm_with_tools)


def execute_tool(tool_call):
    if tool_call["name"] == "fetch_image_from_unsplash":
        return fetch_image_from_unsplash.run(tool_call["args"]["query"])


if __name__ == "__main__":
    user_input = "Describe a serene mountain lake at sunrise and show me a matching image."

    # FIRST CALL → user → assistant issues tool call
    messages = [
        ("human", user_input)
    ]

    response1 = agent.invoke({"messages": messages})

    # Extract full assistant message (includes tool_calls)
    ai_msg = AIMessage(
        content=response1.content,
        tool_calls=response1.tool_calls
    )
    messages.append(ai_msg)

    # If tool call exists
    if response1.tool_calls:

        for call in response1.tool_calls:
            result = execute_tool(call)

            tool_msg = ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )

            messages.append(tool_msg)

        # SECOND CALL → (assistant final answer)
        response2 = agent.invoke({"messages": messages})

        print("\nFinal Output:\n", response2)

    else:
        print("\nFinal Output:\n", response1)
