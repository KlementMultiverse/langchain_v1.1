"""
LangChain Streaming Chain

Builds the LangChain chain for streaming responses from Groq
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import config


def create_chain():
    """
    Create LangChain streaming chain.

    Architecture:
    User Question → Prompt Template → Groq LLM → String Parser → Stream

    Returns:
        LangChain chain (supports .stream())
    """

    # Create Groq LLM (ultra-fast streaming!)
    llm = ChatGroq(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS,
        groq_api_key=config.GROQ_API_KEY,
        streaming=True  # Enable token-by-token streaming
    )

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", config.ASSISTANT_PROMPT),
        ("human", "{question}")
    ])

    # Create output parser (converts AIMessage to string)
    parser = StrOutputParser()

    # Build chain using LCEL (LangChain Expression Language)
    chain = prompt | llm | parser

    return chain


def stream_response(chain, question: str, callbacks: list):
    """
    Stream response from chain with callbacks.

    Args:
        chain: LangChain chain
        question: User's question
        callbacks: List of callback handlers

    Yields:
        Text chunks as they arrive
    """
    for chunk in chain.stream(
        {"question": question},
        config={"callbacks": callbacks}
    ):
        yield chunk
