# CoALA: how language agents remember, decide and act

`REFERENCE ARCHITECTURE · coala-cognitive-architecture · 17 Oct 2026`

*A reference architecture for thinking about any LLM agent: three kinds of long-term memory, a working memory where the model reasons, an action space, and a decision cycle that ties them together. Explained with two diagrams and one worked example.*

| Domain | Level | Key concepts | Related demos |
|---|---|---|---|
| AI agents | Beginner | working memory · semantic · episodic · procedural memory · internal vs external actions · decision cycle | `/demos/rag-demo` |

---

## 1. In one picture

**CoALA**, short for *Cognitive Architectures for Language Agents* (Sumers et al., 2023), is a way to describe any LLM agent with the same few parts. The language model is not the whole agent; it's the reasoning engine inside it. Around it sit **memories** that hold information, **actions** that move information or change the world, and a **decision cycle** that chooses what to do next.

![Fig. 1: CoALA at a glance, adapted from Sumers et al. (2023): long-term memory, working memory and the action space.](figures/fig-01-coala-at-a-glance.svg)

*Fig. 1: CoALA at a glance, adapted from Sumers et al. (2023): long-term memory, working memory and the action space.*

> **The key idea.** If you can say which memory a component writes to, and which action reads from it, you can describe and compare any agent, from a 50-line RAG script to a multi-agent system.

## 2. Why it matters

Agent frameworks use the same words for different things. "Memory" might mean the chat history, a vector database or a fine-tuned model. "Planning" might be one prompt or a search over many. Without shared vocabulary, two designs are hard to compare and gaps are hard to spot.

CoALA gives each piece a role. Once every component has a role, three questions get easy:
- **What does this agent actually remember?**
- **What can it change?** Only its own memory, or the outside world too?
- **Who decides what happens next?** A fixed pipeline, or the model each turn?

## 3. The building blocks

**Working memory** is what the model sees right now: the goal, the retrieved context, recent turns and any scratch work. In practice, it's the prompt. It's small and rebuilt every cycle.

**Long-term memory** comes in three kinds:

| Memory | Holds | Everyday example |
| ------ | ----- | ---------------- |
| Semantic | Facts about the world or a domain | Documents in a vector store, a knowledge graph |
| Episodic | What happened before | Past conversations, logs of earlier attempts |
| Procedural | How to act | The system prompt, tool definitions, the agent's code, the model's weights |

**Actions** are either *internal*, working on the agent's own memories, or *external*, reaching outside it:

| Action | Kind | What it does |
| ------ | ---- | ------------ |
| Retrieval | Internal | Reads from long-term memory into working memory |
| Reasoning | Internal | The LLM processes working memory and writes results back to it |
| Learning | Internal | Writes to long-term memory: storing documents, saving an episode, updating a prompt |
| Grounding | External | Talks to a person, calls a tool or API, acts in an environment |

**The decision procedure** is the loop that picks which action to take, described next.

## 4. How it works

Each cycle has two stages, **planning** and **execution**:

1. **Propose.** The model suggests candidate actions, often after retrieving context.
2. **Evaluate.** Each candidate is scored, by the model, by rules or by a value estimate.
3. **Select.** One action is chosen. Simple agents skip straight here: there's only one option.
4. **Act.** The chosen action runs: an internal one, like retrieving or learning, or an external one, like replying or calling a tool.
5. **Observe.** The result goes back into working memory, and the next cycle starts. The loop ends when the goal is met or a budget runs out.

![Fig. 2: The decision cycle, adapted from Sumers et al. (2023): planning (propose → evaluate → select), then execution and observation.](figures/fig-02-decision-cycle.svg)

*Fig. 2: The decision cycle, adapted from Sumers et al. (2023): planning (propose → evaluate → select), then execution and observation.*

### A worked example: the RAG demo

A basic RAG chatbot is a small CoALA agent. Uploading a document is a **learning** action into **semantic** memory. Each question triggers a **retrieval** action that fills **working memory**, the model **reasons**, and the reply is a **grounding** action. Seen this way, what's missing is easy to spot: there's no episodic store (history lives only in the browser), and the agent never learns from conversations.

![Fig. 3: The RAG demo mapped onto CoALA: learning into semantic memory, retrieval into working memory, reasoning, then a reply. Episodic memory is only client-side.](figures/fig-03-rag-through-coala.svg)

*Fig. 3: The RAG demo mapped onto CoALA: learning into semantic memory, retrieval into working memory, reasoning, then a reply. Episodic memory is only client-side.*

## 5. Patterns & variations

| Pattern | What changes in CoALA terms | When to use it |
| ------- | --------------------------- | -------------- |
| Plain RAG | A fixed cycle: retrieve → reason → reply. No learning from chats | Q&A over a known body of documents |
| ReAct (Yao et al., 2022) | Reasoning and grounding alternate over several cycles; the model picks the next tool | Tasks that need several lookups or tool calls |
| Conversational memory | Adds an episodic store and retrieval from it | Assistants that should remember a user across sessions |
| Reflection (Park et al., 2023) | A learning action writes the agent's own conclusions into long-term memory | Long-running agents that improve from experience |
| Human-gated learning | Learning writes to a review queue; a person promotes items to semantic memory | Agents that speak for a person or a brand, where drift is unacceptable |

## 6. Pitfalls

| Pitfall | What you'll notice | Remedy |
| ------- | ------------------ | ------ |
| Everything in working memory | Prompts grow until they're slow, costly or truncated | Move history to episodic memory and retrieve only what's relevant |
| Unreviewed learning | The agent "remembers" false or injected facts | Gate writes to semantic memory; keep a review queue |
| Unbounded decision loops | Runaway tool calls and costs | Cap the cycles and tokens; force a final answer at the cap |
| Procedural memory edited ad hoc | Behaviour changes nobody can trace | Version prompts and tool definitions like code; record the version with each run |
| Episodic and semantic mixed together | Old chat snippets cited as facts | Separate stores, labelled sources, different retrieval rules |

## 7. Go further

- **See it built:** the [RAG demo](/demos/rag-demo) implements the agent in Fig. 3, with every stage visible in its UI.
- **Read the paper:** Sumers et al. (2023), listed below, covers the framework in depth, including how it relates to classic cognitive architectures.
- **Next on this desk:** explainers on agent harnesses and AI Ops will use the same vocabulary.

## Credits & sources

1. Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths. [*Cognitive Architectures for Language Agents*](https://arxiv.org/abs/2309.02427) (2023). The framework this page explains: the memory modules, the internal and external action space and the decision cycle. Fig. 1 and Fig. 2 are simplified, redrawn adaptations of the paper's framework, not copies.
2. Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. [*ReAct: Synergizing Reasoning and Acting in Language Models*](https://arxiv.org/abs/2210.03629) (2022). The reason-then-act pattern in the Patterns table.
3. Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein. [*Generative Agents: Interactive Simulacra of Human Behavior*](https://arxiv.org/abs/2304.03442) (2023). The reflection pattern, where an agent writes its own conclusions back into memory.

---

coala-cognitive-architecture · reference architecture · credits above.
