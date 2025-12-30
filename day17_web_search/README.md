# Day 17: Web Search

**LangChain Academy - Module 1, Lesson 1.2**

## 📚 What You'll Learn

- Limitations of AI without web search
- Create web search tool with Tavily API
- Give AI access to real-time information
- Understand web search message flow

## 🗂️ Files

1. **01_without_web_search.py** - AI with outdated knowledge
2. **02_with_web_search.py** - AI with real-time web access

## 🎯 Key Concepts

### Why Web Search?
- AI training data has a cutoff date
- Cannot access current events/news
- Cannot get real-time information
- Web search solves this problem

### Tavily API
- LLM-friendly search service
- Returns structured, clean results
- 1000 free searches/month
- ~0.5-1 second response time

### Message Flow
```
HumanMessage("Who is mayor?")
→ AIMessage(tool_call: web_search)
→ ToolMessage(search results)
→ AIMessage("The mayor is...")
```

### Key Insight
AI automatically:
- Reads search results
- Understands content
- Reasons about information
- Formats clean answer

You don't parse JSON manually!

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day17_web_search
python 01_without_web_search.py
python 02_with_web_search.py
```

## 📖 API Keys Required

- `TAVILY_API_KEY` - Get free key at https://tavily.com
