AGENT_PROMPT = """Context:
        {context}

        Available tools:
        {tool_descriptions}

        Based on the user's input and context, decide if you should use a tool or respond directly.        
        If you identify a action, respond with the tool name and the arguments for the tool.        
        If you decide to respond directly to the user then make the action "respond_to_user" with args as your response in the following format.

        Response Format:
        {response_format}
        
        Note:
        Only respond with the JSON object and nothing else.
        Do not add any additional text or explanations.

        """
        
SYSTEM_PROMPT = """You are a helpful assistant. You will be provided with a context and a list of available tools.
        Based on the user's input and context, decide if you should use a tool or respond directly.        
        If you identify a action, respond with the tool name and the arguments for the tool.        
        If you decide to respond directly to the user then make the action "respond_to_user" with args as your response in the following format.

        Response Format:
        {response_format}
        
        Note:
        Only respond with the JSON object and nothing else.
        Do not add any additional text or explanations.

        """