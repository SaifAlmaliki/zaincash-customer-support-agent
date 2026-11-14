from langchain_core.messages import AIMessage


def raw(input_tokens=100, output_tokens=20, **metadata):
    return AIMessage("", usage_metadata={"input_tokens": input_tokens, "output_tokens": output_tokens,
                                         "total_tokens": input_tokens + output_tokens},
                     response_metadata=metadata)
