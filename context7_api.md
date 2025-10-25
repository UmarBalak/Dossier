## Context7 API

### What Context7 Does

Context7 provides **real-time, accurate code documentation** from popular libraries to prevent AI from generating outdated or wrong code.

### Two Main Functions

**Search**
- Finds which libraries are available in Context7's database
- Think of it as browsing a catalog
- Returns library names, IDs, and quality scores

**Get Docs**
- Retrieves actual code examples from a specific library
- Filters results based on your topic (like "authentication" or "SSR")
- Returns most relevant snippets first

### Two Output Formats

**JSON Format**
- Gives you structured data with all the details
- Each snippet includes: title, description, code, relevance score, source link
- Best for: Building apps that need to process documentation programmatically

**TXT Format**  
- Gives you clean, readable markdown text
- Same content, just formatted for humans
- Best for: Feeding directly to AI assistants or reading yourself

### Important Rules

**Library Paths**: Must use full format like "fastapi/fastapi", not just "fastapi"

**Only Indexed Libraries**: Context7 only has popular, publicly submitted libraries - your private repos won't work

**Snippets Are Curated**: You don't get the entire documentation - just the most relevant code examples selected by AI

**Topic Filters Everything**: When you specify a topic, both JSON and TXT get filtered the same way

**Relevance Matters**: Results are ranked 0.0 to 1.0 based on how well they match your query

### How It Works Behind the Scenes

Context7 uses **semantic search** (like Google for code) to find the best matching examples. It scores each snippet based on how well it answers your question (80%) and code quality (20%). Everything is cached for speed and updated regularly to stay current.

### Why Use It

Prevents outdated code examples, eliminates API hallucinations, and gives version-specific documentation - all automatically.