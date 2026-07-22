import { Article } from "../types/article";

export const news: Article[] = [
  {
    id: "openai-coding-model",

    title: "OpenAI Releases New Coding Model",

    summary: "A new model optimized for software engineering tasks.",

    content:
      "OpenAI introduced a new coding model with stronger repository-level reasoning and software engineering capabilities. The model is designed to better understand large codebases, assist with debugging, and perform repository-level reasoning across multiple files.",

    takeaway:
      "AI coding assistants are evolving from simple code completion tools toward repository-level software engineering assistants.",

    concepts: [
      "Repository-level Reasoning",
      "Transformer",
      "Large Language Model (LLM)",
    ],

    background:
      "Repository-level reasoning allows an AI model to understand relationships across an entire software project rather than analyzing only one file at a time. This enables more accurate code generation, debugging, and refactoring.",

    relatedNews: [
      {
        id: "cursor-agent",
        title: "Cursor Introduces AI Agent",
      },
      {
        id: "google-mcp-sdk",
        title: "Google Launches MCP SDK",
      },
    ],

    sources: [
      {
        name: "OpenAI",
        url: "https://openai.com/",
      },
      {
        name: "TechCrunch",
        url: "https://techcrunch.com/",
      },
    ],
  },

  {
    id: "google-mcp-sdk",

    title: "Google Launches MCP SDK",

    summary: "Google announces a new SDK supporting MCP.",

    content:
      "Google released a new SDK supporting the Model Context Protocol (MCP), making it easier for developers to build AI applications that interact with external tools and services.",

    takeaway:
      "Support from major companies suggests MCP is becoming an emerging industry standard.",

    concepts: [
      "Model Context Protocol (MCP)",
      "SDK",
      "AI Agents",
    ],

    background:
      "Model Context Protocol (MCP) is an open protocol that standardizes how AI models communicate with external tools, APIs, and data sources.",

    relatedNews: [
      {
        id: "openai-coding-model",
        title: "OpenAI Releases New Coding Model",
      },
      {
        id: "cursor-agent",
        title: "Cursor Introduces AI Agent",
      },
    ],

    sources: [
      {
        name: "Google Developers",
        url: "https://developers.google.com/",
      },
      {
        name: "Anthropic",
        url: "https://www.anthropic.com/",
      },
    ],
  },

  {
    id: "cursor-agent",

    title: "Cursor Introduces AI Agent",

    summary: "Cursor adds a new AI coding agent.",

    content:
      "Cursor introduced a new AI agent capable of understanding project context, planning coding tasks, and assisting developers with increasingly autonomous software engineering workflows.",

    takeaway:
      "Coding tools are gradually shifting from simple copilots to autonomous development agents.",

    concepts: [
      "AI Agent",
      "Code Generation",
      "Developer Tools",
    ],

    background:
      "Unlike traditional code completion tools, AI agents can reason over multiple steps, use external tools, and complete more complex engineering tasks autonomously.",

    relatedNews: [
      {
        id: "openai-coding-model",
        title: "OpenAI Releases New Coding Model",
      },
      {
        id: "google-mcp-sdk",
        title: "Google Launches MCP SDK",
      },
    ],

    sources: [
      {
        name: "Cursor",
        url: "https://www.cursor.com/",
      },
      {
        name: "Hacker News",
        url: "https://news.ycombinator.com/",
      },
    ],
  },
];