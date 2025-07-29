{
    "_id": "688921d09933921ff68fcae2",
    "api_key": "sk-default-05hTTebADbZQbZXbnkaDRHRxi4iMvK6g",
    "name": "Anurag Portfolio Assistant",
    "description": "AI Agent: Anurag Portfolio Assistant",
    "agent_role": null,
    "agent_instructions": null,
    "agent_goal": null,
    "agent_context": null,
    "agent_output": null,
    "examples": null,
    "features": [
        {
            "type": "KNOWLEDGE_BASE",
            "config": {
                "lyzr_rag": {
                    "rag_id": "688921cf27bf591f1e85a633",
                    "params": {
                        "top_k": 5
                    }
                }
            },
            "priority": 0
        },
        {
            "type": "MEMORY",
            "config": {
                "max_messages_context_count": 10
            },
            "priority": 1
        }
    ],
    "tools": [],
    "tool_usage_description": null,
    "response_format": {},
    "provider_id": "OpenAI",
    "model": "gpt-4o-mini",
    "top_p": "1",
    "temperature": "0.2",
    "managed_agents": null,
    "version": "3",
    "created_at": "2025-07-29T19:32:32.766000",
    "updated_at": "2025-07-29T19:32:33.618000",
    "llm_credential_id": "lyzr_openai"
}