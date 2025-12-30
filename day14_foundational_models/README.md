# Day 14: Foundational Models

**LangChain Academy - Module 1, Lesson 1.1**

## 📚 What You'll Learn

- Initialize and invoke chat models
- Customize model parameters (temperature)
- Use different model providers (OpenAI, Anthropic, Google)
- Create agents with `create_agent()`
- Pass conversation history
- Stream responses in real-time

## 🗂️ Files

1. **01_basic_model.py** - Basic model initialization and invocation
2. **02_model_temperature.py** - Customizing model with temperature
3. **03_different_providers.py** - Using OpenAI, Anthropic, Google models
4. **04_agents.py** - Creating and using agents
5. **05_conversation_history.py** - Passing conversation history
6. **06_streaming.py** - Streaming output word-by-word

## 🎯 Key Concepts

### Model vs Agent
- **Model**: Just the AI brain (`init_chat_model()`)
- **Agent**: AI + tools + memory (`create_agent()`)

### Temperature
- `temperature=0.0` → Predictable, deterministic responses
- `temperature=1.0` → Creative, varied responses

### Message Types
- `HumanMessage` → User input
- `AIMessage` → AI responses

### Streaming
- `agent.stream()` → Get responses word-by-word in real-time
- `stream_mode="messages"` → Stream message chunks

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day14_foundational_models
python 01_basic_model.py
python 02_model_temperature.py
python 03_different_providers.py
python 04_agents.py
python 05_conversation_history.py
python 06_streaming.py
```

## 📖 Related Resources

- [LangChain Chat Models Docs](https://docs.langchain.com/oss/python/integrations/chat)
- [Model Providers](https://docs.langchain.com/oss/python/integrations/providers/all_providers)
