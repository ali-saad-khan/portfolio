"""Certification data. Rendered by build_site.py (/certifications page, home section, about page).
Images are optimised copies of the certificate files in assets/images/certificates/<slug>.webp (see make_cert_images.py)."""

FA = "FreeAcademy.ai"
FA_URL = "https://freeacademy.ai/verify/"
NOV = "November 3, 2026"
OCT = "October 2026"

CATEGORIES = [
    ("ai-agents", "AI Agents & Tool Use", "Building, orchestrating and understanding autonomous AI agents in Python and TypeScript, plus the Model Context Protocol."),
    ("claude-ai-coding", "Claude & AI-Assisted Engineering", "Using Claude and agentic coding tools in a real engineering workflow: planning, specs, code review and prompt design."),
    ("llm-foundations", "LLM Foundations & Prompting", "How large language models and reasoning models work, and how to steer them with prompt and context engineering."),
    ("rag-data", "RAG, Vector Search & Data", "Retrieval-augmented generation, embeddings and vector databases for AI features on a real full stack."),
    ("ai-security", "AI Safety & Security", "Using AI responsibly at work and applying it to defensive cybersecurity such as phishing analysis."),
    ("n8n", "n8n Workflow Automation", "Four n8n Academy certificates on workflow automation, API integrations and AI agents, built on a self-hosted n8n."),
]

# (slug, category, title, issuer, issued, lessons, credential_id, verify_url, image, description, skills)
def fa(slug, cat, title, lessons, cid, desc, skills, img):
    return dict(slug=slug, cat=cat, title=title, issuer=FA, issued=NOV, lessons=lessons, cid="FA-2026-" + cid,
                url=FA_URL + "FA-2026-" + cid, img=img, desc=desc, skills=skills)

CERTS = [
    fa("ai-agents-nodejs-typescript", "ai-agents", "AI Agents with Node.js & TypeScript", 8, "AANT-9Z2HLP",
       "Build AI agents in TypeScript on Node.js: tool calling, agent loops and typed integrations that slot into a JavaScript or Next.js back end.",
       ["AI agents", "Node.js", "TypeScript", "Tool calling"], "AI Agents Node.js TypeScript"),
    fa("agentic-ai-python-langchain", "ai-agents", "Agentic AI with Python & LangChain", 10, "AAPL-LFR238",
       "Design agentic workflows in Python with LangChain: chains, tools, memory and multi-step reasoning for task-solving agents.",
       ["Agentic AI", "Python", "LangChain", "Memory"], "Agentic AI Python Langchain"),
    fa("first-ai-agent-python", "ai-agents", "Build Your First AI Agent in Python", 7, "MFAA-848F6D",
       "Hands-on build of a first working AI agent in Python: the model, the loop, tools and how to keep behaviour predictable.",
       ["AI agents", "Python", "LLM APIs"], "First AI Agent Python"),
    fa("how-ai-agents-work", "ai-agents", "How AI Agents Work", 5, "MHAA-SEL37B",
       "The architecture behind AI agents: planning, tool use, memory and the trade-offs that decide whether an agent is reliable in production.",
       ["Agent architecture", "Planning", "Tool use"], "How AI Agents Work"),
    fa("ai-browsers-computer-use-agents", "ai-agents", "AI Browsers & Computer Use Agents", 9, "ABCU-WNDQDA",
       "Agents that operate browsers and computers: how computer-use models see and act on a UI, and where the risks and limits are.",
       ["Computer use", "Browser agents", "Automation"], "AI Browsers Computer Use Agents"),
    fa("mcp-model-context-protocol", "ai-agents", "MCP: Model Context Protocol", 12, "MMCP-9M5NUN",
       "Connect AI models to tools and data through the Model Context Protocol: servers, tools, resources and secure integration patterns.",
       ["MCP", "Tool integration", "AI infrastructure"], "MCP Model Context Protocol"),

    fa("claude-code-ai-powered-coding", "claude-ai-coding", "Claude Code: AI-Powered Coding", 14, "CCAP-81WCQ2",
       "Day-to-day software development with Claude Code: exploring codebases, making multi-file changes, running tests and iterating with an AI pair.",
       ["Claude Code", "AI pair programming", "Refactoring"], "Claude Code AI Powered Coding"),
    fa("claude-code-complete-guide", "claude-ai-coding", "Claude Code: Complete Guide", 10, "CCCG-QPDUR5",
       "A full tour of Claude Code: configuration, memory files, permissions, slash commands, hooks and workflows for larger projects.",
       ["Claude Code", "Workflows", "Developer tooling"], "Claude Code Complete Guide"),
    fa("claude-code-review", "claude-ai-coding", "Claude Code Review", 6, "MCCR-O5RMQZ",
       "Using Claude to review code: catching bugs, security issues and design problems, and turning review findings into fixes.",
       ["Code review", "Claude", "Quality"], "Claude Code Review"),
    fa("spec-driven-development-ai-coding-agents", "claude-ai-coding", "Spec-Driven Development with AI Coding Agents", 7, "SDDA-JN6IS0",
       "Write clear specifications first and let coding agents implement against them, so AI-generated code stays reviewable and on target.",
       ["Spec-driven development", "Coding agents", "Planning"], "Spec Driven Development AI Coding Agents"),
    fa("prompt-engineering-claude", "claude-ai-coding", "Prompt Engineering with Claude", 26, "PEC-0HAXUA",
       "A 26-lesson course on prompting Claude: structure, examples, roles, output formats and evaluation for dependable results.",
       ["Prompt engineering", "Claude", "Structured output"], "Prompt Engineering Claude"),

    fa("advanced-prompt-engineering", "llm-foundations", "Advanced Prompt Engineering", 10, "APE-UCAKR6",
       "Advanced techniques for complex tasks: decomposition, chain-of-thought, self-checking, prompt chaining and testing prompts like code.",
       ["Prompt engineering", "Chaining", "Evaluation"], "Advanced Prompt Engineering"),
    fa("context-engineering", "llm-foundations", "Context Engineering", 5, "MCE-YTWGK1",
       "Deciding what goes into a model's context window and when: retrieval, summarisation and memory for accurate, cost-aware AI features.",
       ["Context engineering", "Context windows", "Memory"], "Context Engineering"),
    fa("how-llms-work", "llm-foundations", "How LLMs Work", 6, "MHLW-2QK8TV",
       "Tokens, embeddings, attention and sampling: a clear mental model of how large language models generate text and why they fail.",
       ["LLMs", "Transformers", "Tokens"], "How LLMs Work"),
    fa("reasoning-models-explained", "llm-foundations", "Reasoning Models Explained", 5, "MRME-69ASXX",
       "What reasoning models do differently, when extra thinking time pays off, and how to prompt and budget for them.",
       ["Reasoning models", "Test-time compute", "Prompting"], "Reasoning Models Explained"),
    fa("machine-learning-fundamentals", "llm-foundations", "Machine Learning Fundamentals", 35, "MLF-SMS5W1",
       "The largest course in the set, at 35 lessons: core machine learning concepts, model training and evaluation that underpin modern AI.",
       ["Machine learning", "Model evaluation", "Data"], "Machine Learning Fundamentals"),

    fa("full-stack-rag-nextjs-supabase-gemini", "rag-data", "Full-Stack RAG with Next.js, Supabase & Gemini", 17, "FRNS-9SL43K",
       "Build a retrieval-augmented generation app end to end: Next.js front end, Supabase Postgres with pgvector, and Gemini for answers.",
       ["RAG", "Next.js", "Supabase", "Gemini"], "Full-Stack RAG Next.js Supabase Gemini"),
    fa("vector-databases-ai", "rag-data", "Vector Databases for AI", 17, "VDA-1LHTVU",
       "Embeddings, similarity search and indexing: how vector databases work and how to choose and tune one for semantic search.",
       ["Vector databases", "Embeddings", "Semantic search"], "Vector Databases AI"),

    fa("hands-on-ai-cybersecurity-phishing-labs", "ai-security", "Hands-On AI for Cybersecurity: Phishing Labs", 12, "HOAF-Z5DVV2",
       "Micro practical labs applying AI to defensive security, with phishing detection and analysis as the running example.",
       ["Cybersecurity", "Phishing detection", "AI labs"], "Hands On AI For Cybersecurity Micro Practical Labs Phishing"),
    fa("using-ai-safely-at-work", "ai-security", "Using AI Safely at Work", 6, "MUAS-W5LZK0",
       "Practical rules for AI at work: protecting sensitive data, spotting hallucinations, and staying within policy and privacy limits.",
       ["AI safety", "Data privacy", "Responsible AI"], "Using AI Safely At Work"),
]

def n8n(slug, title, desc, url, img, skills):
    return dict(slug=slug, cat="n8n", title=title, issuer="n8n Academy", issued=OCT, lessons=None, cid=None, url=url, img=img, desc=desc, skills=skills)

CERTS += [
    n8n("n8n-quickstart", "n8n Quickstart", "Scheduled workflows with filtering, merging and data tables; API reports converted to CSV; error-monitoring alerts; an AI agent with memory and tools on a local LLM (Ollama).",
        "https://lnkd.in/d6CFXna7", "n8n quick start certification", ["n8n", "Scheduling", "AI agent", "Ollama"]),
    n8n("n8n-essentials-first-workflows", "Essentials: Your First Workflows", "Webhook, schedule, polling and chat triggers; data transformation and expressions; IF branching; CSV reports sent to an API with header authentication.",
        "https://lnkd.in/dWrmwFJj", "Essentials: Your First Workflows", ["Webhooks", "Expressions", "Header auth"]),
    n8n("n8n-integrations-apis", "Integrations: APIs & Connected Workflows", "API pipelines with pagination, merging and routing; authenticated webhook workflows with Data Tables and sub-workflows.",
        "https://lnkd.in/dpfMNHTs", "Integrations: APIs & Connected Workflows", ["REST APIs", "Pagination", "Sub-workflows"]),
    n8n("n8n-in-practice-ai-testing", "In Practice: AI, Testing & Best Practices", "AI feedback pipeline with classification and structured output, an AI agent with tools, retry and error workflows, and debugging a broken workflow.",
        "https://lnkd.in/dYj2ncZD", "In Practice: AI, Testing & Best Practices", ["AI agents", "Error handling", "Debugging"]),
]
CMAP = {c["slug"]: c for c in CERTS}
FEATURED = ["full-stack-rag-nextjs-supabase-gemini", "claude-code-complete-guide", "mcp-model-context-protocol", "agentic-ai-python-langchain", "prompt-engineering-claude", "n8n-in-practice-ai-testing"]
TOTAL = len(CERTS)
FA_COUNT = sum(1 for c in CERTS if c["issuer"] == FA)
LESSONS = sum(c["lessons"] or 0 for c in CERTS)
