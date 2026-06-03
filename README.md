# AI Digest

A fortnightly digest for AI product managers and consultants — covering what's shipped, what's worth knowing, and what's worth reading. Generated with Claude and web search, runs automatically every other Friday.

---

## What's in each issue

| Section | What it covers |
|---|---|
| **TL;DR** | 4–6 opinionated takeaways from the fortnight |
| **🔧 Engineering & Model Releases** | What shipped across the major labs — capabilities, benchmarks, pricing |
| **🧠 AI Product Management & Frameworks** | Frameworks for building and shipping AI products; transformation methodologies |
| **🚀 What's Being Built** | Products, apps, and enterprise deployments across all scales — from indie tools to Big Four rollouts |
| **📐 ML & Technical Fundamentals** | The full ML stack — not just agentic AI. RAG, fine-tuning, embeddings, evaluation, classical ML |
| **💼 Jobs & Hiring** | AI job market trends, salary signals, and 4–6 companies actively hiring (startups, fintech, consulting) |
| **⚖️ Regulatory & Governance** | EU AI Act, UK AI Safety, US policy — with deadlines |
| **📚 Worth Reading** | Curated blogs, papers, newsletters, and one book recommendation per issue |
| **🔬 Technical Deep Dive** | One topic explored properly — reasoning, multimodal, inference, alignment |

---

## Setup

### Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
git clone https://github.com/YOUR_USERNAME/ai-digest.git
cd ai-digest
pip install anthropic
```

### Run locally

```bash
export ANTHROPIC_API_KEY=your_key_here
python digest.py
```

Output saves to `~/Documents/AI_Digests/` as both `.md` and `.html`.

To save somewhere specific:

```bash
python digest.py --output-dir ./digests
```

---

## Automated runs (GitHub Actions)

The digest runs automatically every other Friday at 08:00 UTC via GitHub Actions. Generated files are committed to the `digests/` folder in this repo.

### Setup

1. Fork or clone this repo
2. Go to **Settings → Secrets and variables → Actions**
3. Add a secret: `ANTHROPIC_API_KEY` = your Anthropic API key
4. The workflow (`.github/workflows/digest.yml`) handles the rest

To trigger a run manually: **Actions → Generate Fortnightly AI Digest → Run workflow**.

---

## Cost

Each run makes ~15–20 web searches and generates ~4,000–6,000 tokens of output using `claude-sonnet-4-20250514`.

| Component | Estimate per run |
|---|---|
| Input tokens (system prompt + search results) | ~8,000–12,000 tokens |
| Output tokens | ~4,000–6,000 tokens |
| Web search tool calls | 15–20 searches |
| **Estimated cost per issue** | **~$0.15–$0.30** |
| **Annual cost (26 issues)** | **~$4–$8** |

GitHub Actions is free for public repos and included in the free tier for private repos (2,000 minutes/month — each digest run takes under 5 minutes).

---

## Digests archive

Generated digests live in [`digests/`](./digests/). Each issue is saved as both markdown and HTML.

---

## Customisation

The prompt in `digest.py` controls everything. Key things to adjust:

- **Reader persona** (line ~30): update if your role or focus shifts
- **Worth Reading sources**: add or remove specific blogs/newsletters in the search strategy
- **ML Fundamentals topics**: the prompt rotates across techniques — you can weight towards areas you want to build depth in
- **Run cadence**: edit the cron in `.github/workflows/digest.yml` — `0 8 * * 5` is every Friday at 08:00 UTC; the week parity check makes it fortnightly

---

## Structure

```
ai-digest/
├── digest.py                    # Main generator
├── .github/
│   └── workflows/
│       └── digest.yml           # GitHub Actions schedule
├── digests/                     # Generated issues (auto-committed)
│   ├── ai_digest_20260606.md
│   └── ai_digest_20260606.html
└── README.md
```
