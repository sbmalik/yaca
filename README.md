# YACA
Yet Another Chat Agent 

## Design Decisions

1. Frontend: Basic HTML/CSS/JS with SSE for streaming to just view the response from Agent.
2. Backend: FastAPI for the API/Web-Server. 
3. Logging: Loguru for logging.
4. Configuration: Pydantic Settings for configuration.
5. Routing: LiteLLM for routing so we don't stuck with a single model provider. 
6. Orchestration: LangGraph for orchestrating the flow of the conversation.

## TODO List
[ ] Chat history 