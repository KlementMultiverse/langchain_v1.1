# Complete LangChain Learning Curriculum

**Version:** December 2025 (LangChain 1.1.0+, LangGraph 1.0)

**Last Updated:** December 16, 2025

**Status:** 🔒 LOCKED - Complete this curriculum without changes

---

## 🎯 Philosophy

**"Collaborative Learning - The Next Genesis Learning"**

1. Master fundamentals before advanced topics
2. Build real projects (no vibe coding)
3. Each day builds on previous
4. Aligned with LangChain 1.1+ (December 2025)

---

## 📚 Complete Learning Path

### **PHASE 1: LangChain Foundations (Days 1-7)** ✅ COMPLETE

| Day | Topic | Status | What You Built | Key Concepts |
|-----|-------|--------|----------------|--------------|
| **Day 1** | Messages | ✅ Complete | `day1_messages.py` | Message types, roles, conversation structure |
| **Day 2** | Chat Models | ✅ Complete | `day2_first_ai_call.py` | Connect to LLM, basic conversations |
| **Day 3** | Chains | ✅ Complete | `day3_simple_chain.py`<br>`day3_parser_chain.py` | LCEL, prompt templates, output parsers |
| **Day 4** | Basic Tools | ✅ Complete | `day4_calculator_tool.py` | Tool definition, binding, execution |
| **Day 5** | Memory | ✅ Complete | `day5_memory_chat.py` | Conversation memory, context management |
| **Day 6** | RAG Systems | ✅ Complete | 3 iterations (see below) | Document loading, chunking, vector search |
| **Day 7** | Structured Output | ✅ Complete | `07_ai_resume_extractor/` | Pydantic, validation, production patterns |

#### Day 6 RAG Iterations (Complete):
- ✅ Iteration 1: Basic RAG + Memory
- ✅ Iteration 2: Text Splitters + Chunking
- ✅ Iteration 3: Vector Embeddings + ChromaDB
- 📝 Note: Iterations 4-5 (multi-doc, hybrid search) → integrate in later projects

---

### **PHASE 2: Advanced LangChain (Days 8-14)** 🔄 IN PROGRESS

**Goal:** Master all LangChain 1.1 features before agents

---

#### **Day 8: Streaming & Callbacks** ⭐ NEXT!

**Location:** `day8_streaming_callbacks/`

**Why This First:**
- User experience (real-time feedback)
- Monitoring & debugging
- Production requirement
- Used in ALL future projects

**Programs to Build:**
```
day8_streaming_callbacks/
├── 01_basic_streaming.py          # Stream tokens one by one
├── 02_callback_handlers.py        # Monitor LLM behavior
├── 03_cost_tracking.py            # Track token usage & costs
├── 04_streaming_with_chains.py    # Stream in complex chains
├── 05_real_time_chat.py           # Build responsive chat interface
├── README.md                       # Complete documentation
└── requirements.txt                # No new dependencies!
```

**Key Concepts:**
- Token-by-token streaming
- Custom callback handlers
- Cost monitoring
- Real-time user experience
- Production logging

**Learning Outcomes:**
- Stream any LLM response
- Monitor LLM behavior in real-time
- Track costs per request
- Build responsive UIs
- Debug LLM issues efficiently

---

#### **Day 9: LCEL Advanced (Runnables)**

**Location:** `day9_lcel_advanced/`

**Why This Matters:**
- Foundation for LangGraph
- Complex workflow building blocks
- Parallel execution
- LangChain 1.1 core feature

**Programs to Build:**
```
day9_lcel_advanced/
├── 01_runnable_passthrough.py     # Pass data through chains
├── 02_runnable_lambda.py          # Custom transformations
├── 03_parallel_execution.py       # Run tasks in parallel
├── 04_branching_logic.py          # Conditional routing
├── 05_complex_chain.py            # Combine all patterns
└── README.md
```

**Key Concepts:**
- RunnablePassthrough (data flow)
- RunnableLambda (custom logic)
- RunnableParallel (concurrent execution)
- RunnableBranch (conditional routing)
- Chain composition

**Learning Outcomes:**
- Build complex workflows
- Execute tasks in parallel
- Add custom logic to chains
- Route based on conditions
- Prepare for LangGraph

---

#### **Day 10: Prompt Engineering Deep Dive**

**Location:** `day10_prompt_engineering/`

**Why This Matters:**
- Prompt = Programming language for LLMs
- Quality in = Quality out
- Production prompts are engineered
- Reusable prompt patterns

**Programs to Build:**
```
day10_prompt_engineering/
├── 01_few_shot_prompting.py       # Examples in prompts
├── 02_chat_templates.py           # System/user/assistant roles
├── 03_partial_prompts.py          # Template variables
├── 04_prompt_composition.py       # Combine prompts
├── 05_production_patterns.py      # Real-world templates
└── README.md
```

**Key Concepts:**
- Few-shot learning (examples)
- Chat prompt templates
- Partial variables
- Prompt composition
- System messages
- Prompt optimization

**Learning Outcomes:**
- Write effective prompts
- Use examples to guide LLM
- Build reusable templates
- Compose complex prompts
- Production prompt patterns

---

#### **Day 11: Document Loaders & Processing**

**Location:** `day11_document_loaders/`

**Why This Matters:**
- Real data comes in many formats
- Web scraping for live data
- API integration
- Data transformation pipelines

**Programs to Build:**
```
day11_document_loaders/
├── 01_csv_excel_loaders.py        # Tabular data
├── 02_json_yaml_loaders.py        # Structured data
├── 03_web_scraping.py             # Live web data
├── 04_api_loaders.py              # External APIs
├── 05_data_transformers.py        # Clean & transform
└── README.md
```

**Key Concepts:**
- CSV/Excel loading
- JSON/YAML parsing
- Web scraping (BeautifulSoup)
- API integration
- Data transformers
- Processing pipelines

**Learning Outcomes:**
- Load any file format
- Scrape websites
- Integrate APIs
- Transform data
- Build data pipelines

---

#### **Day 12: Output Parsers & Validation**

**Location:** `day12_output_parsers/`

**Why This Matters:**
- LLMs are unpredictable
- Need robust parsing
- Retry on failures
- Production reliability

**Programs to Build:**
```
day12_output_parsers/
├── 01_structured_parsers.py       # Parse to structures
├── 02_retry_parsers.py            # Handle failures
├── 03_custom_parsers.py           # Build your own
├── 04_validation_chains.py        # Validate output
├── 05_error_handling.py           # Production patterns
└── README.md
```

**Key Concepts:**
- PydanticOutputParser (you know this!)
- OutputFixingParser (retry)
- RetryOutputParser (retry with context)
- Custom parsers
- Validation strategies
- Error handling

**Learning Outcomes:**
- Parse any LLM output
- Handle parsing failures
- Build custom parsers
- Validate output
- Production error handling

---

#### **Day 13: Caching & Performance**

**Location:** `day13_caching_performance/`

**Why This Matters:**
- Speed matters
- Cost optimization
- User experience
- Production efficiency

**Programs to Build:**
```
day13_caching_performance/
├── 01_llm_caching.py              # Cache LLM responses
├── 02_embedding_caching.py        # Cache embeddings
├── 03_semantic_caching.py         # Similar queries
├── 04_cost_optimization.py        # Reduce API costs
├── 05_performance_benchmarks.py   # Measure improvements
└── README.md
```

**Key Concepts:**
- LLM response caching
- Embedding caching
- Semantic caching (similar queries)
- Cache invalidation
- Cost tracking
- Performance metrics

**Learning Outcomes:**
- Implement caching strategies
- Optimize API costs
- Speed up responses
- Measure performance
- Production optimization

---

#### **Day 14: Advanced Retrievers**

**Location:** `day14_advanced_retrievers/`

**Why This Matters:**
- RAG beyond basics
- Specialized retrieval strategies
- Query understanding
- Production RAG patterns

**Programs to Build:**
```
day14_advanced_retrievers/
├── 01_self_query_retriever.py     # LLM generates structured queries
├── 02_multi_vector_retriever.py   # Multiple vectors per document
├── 03_ensemble_retriever.py       # Combine multiple retrievers
├── 04_parent_document_retriever.py # Store small chunks, retrieve large
├── 05_contextual_compression.py   # Filter retrieved docs
└── README.md
```

**Key Concepts:**
- Self-query retrievers (LLM writes structured query)
- Multi-vector retrievers (summaries, hypothetical questions)
- Ensemble retrievers (hybrid search - keyword + semantic)
- Parent document retrievers (chunking strategy)
- Contextual compression (post-retrieval filtering)
- Time-weighted retrievers (recency matters)

**Learning Outcomes:**
- Advanced RAG strategies
- Query understanding with LLM
- Hybrid search techniques
- Optimize retrieval quality
- Production RAG patterns

**Real-World Use Cases:**
- Self-query: "Find docs about Python from last month"
- Multi-vector: Generate questions a doc answers, search those
- Ensemble: Combine BM25 (keyword) + semantic search
- Parent: Search small chunks, return full context
- Compression: Only return relevant sentences from docs

---

#### **Day 15: Query Construction**

**Location:** `day15_query_construction/`

**Why This Matters:**
- Convert natural language → structured queries
- Database access with LLMs
- Graph database queries
- API query construction

**Programs to Build:**
```
day15_query_construction/
├── 01_text_to_sql.py              # Natural language → SQL
├── 02_sql_chain.py                # Question answering over databases
├── 03_text_to_cypher.py           # Natural language → Cypher (Neo4j)
├── 04_api_query_construction.py   # Build API queries
├── 05_structured_search.py        # Combine with metadata filters
└── README.md
```

**Key Concepts:**
- Text-to-SQL (LLM generates SQL queries)
- SQL database chains
- Text-to-Cypher (for graph databases)
- API query builders
- Metadata filtering
- Query validation

**Learning Outcomes:**
- LLM → SQL translation
- Safe database querying
- Graph database integration
- Structured data access
- Query safety & validation

**Production Pattern:**
```python
# User asks: "Show me all customers from California who spent over $1000"
# LLM generates: SELECT * FROM customers WHERE state='CA' AND total_spent > 1000
# Execute query safely
# Return natural language answer
```

---

#### **Day 16: Model Profiles & Capabilities** 🆕 (LangChain 1.1 Feature!)

**Location:** `day16_model_profiles/`

**Why This Matters:**
- **NEW in LangChain 1.1** (Dec 2, 2025)
- Models now expose capabilities
- Feature detection
- Provider-specific behavior
- Dynamic adaptation

**Programs to Build:**
```
day14_model_profiles/
├── 01_model_profiles.py           # Explore .profile attribute
├── 02_feature_detection.py        # Check capabilities
├── 03_provider_strategies.py      # Provider-specific logic
├── 04_dynamic_routing.py          # Route based on features
├── 05_production_patterns.py      # Use profiles in production
└── README.md
```

**Key Concepts:**
- `.profile` attribute (NEW!)
- Feature detection
- Structured output capabilities
- Function calling support
- JSON mode detection
- Provider-specific behavior
- Dynamic model selection

**Learning Outcomes:**
- Use model profiles
- Detect supported features
- Adapt to model capabilities
- Provider-specific logic
- Dynamic model routing

**LangChain 1.1 Update:**
```python
# NEW in LangChain 1.1
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen3:4b")

# Check what this model can do!
print(model.profile)  # Shows: structured_output, json_mode, etc.

# Dynamic behavior based on capabilities
if model.profile.supports_structured_output:
    structured_llm = model.with_structured_output(MyModel)
else:
    # Fallback to parsing
    structured_llm = model | output_parser
```

---

### **PHASE 3: LangGraph & Modern Agents (Days 17-22)** 📅 UPCOMING

**⚠️ IMPORTANT:** LangChain 1.1 deprecates old Agent/AgentExecutor!

**NEW WAY (Dec 2025):**
- LangGraph 1.0 is now standard
- No more `AgentExecutor`
- State machines instead
- Production-ready from day 1

---

#### **Day 17: LangGraph Basics** (The New Agent Framework!)

**Location:** `day17_langgraph_basics/`

**Why LangGraph?**
- **LangGraph 1.0 released** (Nov 2025)
- Replaces old Agent system
- State machines for workflows
- Production-grade from start

**Programs to Build:**
```
day15_langgraph_basics/
├── 01_state_machines.py           # Basic state concept
├── 02_nodes_and_edges.py          # Graph components
├── 03_conditional_routing.py      # Dynamic flow
├── 04_simple_agent.py             # First LangGraph agent
├── 05_agent_with_tools.py         # Tools in LangGraph
└── README.md
```

**Key Concepts:**
- State (data flowing through graph)
- Nodes (functions/operations)
- Edges (connections)
- Conditional edges (routing)
- Graph compilation
- Agent patterns

**Learning Outcomes:**
- Build state machines
- Create nodes and edges
- Conditional routing
- First LangGraph agent
- Replace old AgentExecutor

**Migration Note:**
```python
# ❌ OLD WAY (Deprecated in LangChain 1.1)
from langchain.agents import AgentExecutor

# ✅ NEW WAY (LangChain 1.1+)
from langgraph.prebuilt import create_react_agent
# OR
from langchain.agents import ...  # New agent module
```

---

#### **Day 18: ReACT Agents with LangGraph**

**Location:** `day18_react_agents/`

**What is ReACT?**
- Reasoning + Acting
- Think → Act → Observe → Repeat
- Standard agent pattern

**Programs to Build:**
```
day16_react_agents/
├── 01_simple_react.py             # Basic ReACT pattern
├── 02_multi_tool_agent.py         # Multiple tools
├── 03_agent_with_memory.py        # Stateful agents
├── 04_error_handling.py           # Production reliability
├── 05_production_agent.py         # Complete system
└── README.md
```

**Key Concepts:**
- ReACT pattern (Reason + Act)
- Tool selection
- Observation processing
- Multi-step reasoning
- Agent memory
- Error recovery

**Learning Outcomes:**
- Build ReACT agents
- Multi-tool selection
- Stateful agents
- Handle failures
- Production agents

---

#### **Day 19: Multi-Agent Systems**

**Location:** `day19_multi_agent/`

**Why Multi-Agent?**
- Complex tasks need specialization
- Agents collaborate
- Divide and conquer
- Production scalability

**Programs to Build:**
```
day17_multi_agent/
├── 01_agent_communication.py      # Agents talk to each other
├── 02_hierarchical_agents.py      # Manager + workers
├── 03_collaborative_agents.py     # Peer-to-peer
├── 04_agent_coordination.py       # Orchestration
├── 05_production_system.py        # Complete multi-agent app
└── README.md
```

**Key Concepts:**
- Agent communication
- Hierarchical structure
- Collaborative patterns
- Coordination strategies
- Shared state
- Conflict resolution

**Learning Outcomes:**
- Build multi-agent systems
- Coordinate agents
- Hierarchical patterns
- Agent collaboration
- Production orchestration

---

#### **Day 20: Evaluation & Testing**

**Location:** `day20_evaluation_testing/`

**Why This Matters:**
- How do you know your LLM app works?
- Measure quality objectively
- Regression testing
- Benchmark creation

**Programs to Build:**
```
day20_evaluation_testing/
├── 01_llm_evaluation.py           # Evaluate LLM outputs
├── 02_rag_evaluation.py           # Test RAG quality
├── 03_agent_testing.py            # Test agent behavior
├── 04_benchmark_creation.py       # Create test suites
├── 05_langsmith_evals.py          # LangSmith integration
└── README.md
```

**Key Concepts:**
- LLM-as-judge (evaluate with another LLM)
- RAGAS metrics (RAG evaluation)
- Ground truth datasets
- A/B testing
- Regression tests
- LangSmith evaluation

**Learning Outcomes:**
- Test LLM applications
- Measure RAG quality
- Create benchmarks
- Prevent regressions
- Production testing

---

#### **Day 21: LangServe & Deployment**

**Location:** `day21_langserve_deployment/`

**Why This Matters:**
- Deploy chains as APIs
- Production serving
- REST endpoints
- Client integration

**Programs to Build:**
```
day21_langserve_deployment/
├── 01_simple_langserve.py         # Deploy a chain
├── 02_rag_api.py                  # RAG as API
├── 03_streaming_api.py            # Streaming endpoints
├── 04_client_integration.py       # Call from Python
├── 05_production_deploy.py        # Docker + production
└── README.md
```

**Key Concepts:**
- LangServe framework
- REST API generation
- Streaming endpoints
- Client libraries
- Docker deployment
- Production patterns

**Learning Outcomes:**
- Deploy chains as APIs
- Create REST endpoints
- Streaming responses
- Client integration
- Production deployment

---

#### **Day 22: Production Agent Deployment**

**Location:** `day22_production_agents/`

**Why This Matters:**
- Agents in production are different
- Monitoring required
- Safety constraints
- Cost management

**Programs to Build:**
```
day18_production_agents/
├── 01_monitoring.py               # Track agent behavior
├── 02_safety_constraints.py       # Prevent bad actions
├── 03_cost_management.py          # Budget limits
├── 04_logging_observability.py    # Debug production
├── 05_deployment_patterns.py      # Deploy safely
└── README.md
```

**Key Concepts:**
- Agent monitoring
- Safety constraints
- Cost budgets
- Observability
- Error recovery
- Rollback strategies

**Learning Outcomes:**
- Deploy agents safely
- Monitor in production
- Set safety limits
- Manage costs
- Debug live agents

---

### **PHASE 4: Advanced Topics (Days 23-30)** 📅 FUTURE

**Topics to Cover:**

**Day 23:** LangSmith (Observability & Monitoring)
- Tracing LLM calls
- Debugging chains
- Performance monitoring
- Cost analytics

**Day 24:** Advanced RAG Techniques
- Query rewriting
- Re-ranking
- HyDE (Hypothetical Document Embeddings)
- Multi-query strategies

**Day 25:** Multimodal AI
- Image + Text
- Audio processing
- Vision models
- Multimodal RAG

**Day 26:** Custom Agent Architectures
- Planning agents
- Reflection agents
- Tool-making agents
- Meta-agents

**Day 27:** Vector Database Deep Dive
- ChromaDB advanced features
- Pinecone integration
- Weaviate integration
- Performance tuning & optimization

**Day 28:** Security & Safety
- Prompt injection prevention
- Output filtering
- Rate limiting
- Content moderation

**Day 29:** Production Best Practices
- Monitoring & alerting
- Error handling patterns
- Scaling strategies
- Cost optimization

**Day 30:** Capstone Project
- Build complete production system
- All concepts integrated
- Full deployment
- Portfolio showcase piece

---

## 📊 Progress Tracking

**Use:** `LEARNING_TRACKER.md` for detailed progress

### Current Status (December 16, 2025):

**Phase 1:** ✅ 100% Complete (Days 1-7)
**Phase 2:** 🔄 0% Complete (Days 8-16) - Starting Day 8
**Phase 3:** 📅 Not Started (Days 17-22)
**Phase 4:** 📅 Not Started (Days 23-30)

---

## 🔄 Version Notes

### December 2025 Updates:

**LangChain 1.1.0 (Released Dec 2, 2025):**
- ✅ Added Day 14: Model Profiles (NEW feature)
- ✅ Updated Day 15+: LangGraph 1.0 (NO MORE AgentExecutor)
- ✅ Migration notes for deprecated features
- ✅ Production patterns aligned with 1.1

**LangGraph 1.0 (Released Nov 2025):**
- ✅ Standard agent framework
- ✅ Replaces old agent system
- ✅ Production-ready from start

---

## 🎯 Key Principles

1. **Complete Phase 1 before Phase 2** - Fundamentals matter
2. **Complete Phase 2 before Phase 3** - No shortcuts to agents
3. **Build every program** - No skipping, no copy-paste
4. **Test everything** - Run and understand each program
5. **Document learnings** - Update LEARNING_TRACKER.md

---

## 📝 Daily Workflow

**Every Learning Session:**

1. Read day's README
2. Understand concepts BEFORE coding
3. Build program 1 → test → understand
4. Build program 2 → test → understand
5. Continue through all programs
6. Update LEARNING_TRACKER.md
7. Document key learnings

**No Vibe Coding:** Understand every line you type!

---

## 🚀 After Completion

**You Will Be Able To:**
- ✅ Build production LangChain applications
- ✅ Create autonomous AI agents
- ✅ Deploy multi-agent systems
- ✅ Optimize for cost and performance
- ✅ Monitor and debug in production
- ✅ Handle real-world complexity

**Career Ready:**
- LangChain Engineer
- AI Agent Developer
- LLM Application Developer
- Production AI Systems Engineer

---

## 🔒 Curriculum Lock

**This curriculum is LOCKED as of December 16, 2025.**

**Do NOT change until completion.**

**Changes allowed ONLY if:**
- LangChain releases breaking changes
- Major deprecations announced
- Security issues discovered

**Otherwise:** Follow this path exactly!

---

## 📚 Resources

**Official Docs:**
- LangChain: https://python.langchain.com/
- LangGraph: https://langchain-ai.github.io/langgraph/
- LangSmith: https://docs.smith.langchain.com/

**Our Files:**
- Main README: `README.md`
- Progress Tracker: `LEARNING_TRACKER.md`
- Agentic Curriculum: `AGENTIC_MASTERY_CURRICULUM_2025.md`
- Pseudocode Examples: `PSEUDOCODE_EXAMPLES.md`

---

**Created:** December 16, 2025
**Version:** 2.0.0 (Updated with complete topics)
**Status:** 🔒 LOCKED
**Total Days:** 30 days (4 phases)
**Next:** Day 8 - Streaming & Callbacks

---

*"Not vibe coding. Real mastery. One day at a time."*
