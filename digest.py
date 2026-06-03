#!/usr/bin/env python3
"""
Weekly AI Digest Generator
Generates a curated digest of AI developments for AI product managers and consultants.

Sections:
- TL;DR
- AI Product Management & Frameworks
- What's Being Built (products, apps, enterprise deployments)
- AI PM Tools & Skills
- ML & Technical Fundamentals
- Jobs & Hiring (UK/London — trends + companies)
- Regulatory & Governance
- Worth Reading (books + online)
- Technical Deep Dive
- Engineering & Model Releases
"""

import anthropic
import argparse
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path


def send_email(html_content: str, markdown_content: str, date: str):
    """Send the digest via email if SMTP env vars are configured."""
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_from = os.environ.get("SMTP_FROM", smtp_user)
    recipient = os.environ.get("RECIPIENT_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, recipient]):
        print("SMTP env vars not fully set — skipping email delivery.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"AI Digest — {date}"
    msg["From"] = smtp_from
    msg["To"] = recipient

    msg.attach(MIMEText(markdown_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_from, recipient, msg.as_string())

    print(f"Email sent to {recipient}")


def convert_inline_markdown(text: str) -> str:
    """Convert inline markdown syntax to HTML."""
    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold: **text**
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text* (single, not double)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    return text


def generate_digest():
    """Generate the weekly AI digest using Claude with web search."""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    today = datetime.now().strftime("%B %d, %Y")
    today_filename = datetime.now().strftime("%Y%m%d")

    system_prompt = f"""You are an AI analyst producing a weekly digest on {today} for an AI Product Manager at a management consulting firm (Capgemini Invent).

IMPORTANT: Output ONLY the formatted digest content below. Do not include any preamble, meta-commentary, statements about your research process, or phrases like "I now have enough research" or "Based on my searches". Begin your response immediately with **TL;DR**.

Your reader:
- Works in AI product management and consulting in London — helping enterprise clients adopt and build AI
- Wants to stay sharp on both the strategic and technical dimensions of AI
- Is interested in real implementations, not hype
- Reads broadly: blogs, papers, newsletters, and books
- Does NOT need private equity content
- UK-first lens throughout: prioritise UK/London companies, European regulatory context, £ salaries, and UK market data where available. Include US content where it's genuinely significant (major model releases, key frameworks) but default to UK/European perspective

LINKING RULES: Every named framework, tool, product, company, paper, or article MUST include a clickable hyperlink to the original source. Format links as [text](url). Never mention something by name without linking to it if a URL exists.

Structure the digest with these sections exactly, using the emoji headers below:

---

**TL;DR**
- 4–6 bullet points
- Scannable, opinionated takeaways — not just summaries
- Bold key terms

---

## 🧠 AI Product Management & Frameworks
- Frameworks, methodologies, and mental models for building and shipping AI products
- AI transformation playbooks (McKinsey, Gartner, BCG, Forrester, Thoughtworks, etc.)
- Use case prioritisation, ROI estimation, build vs. buy decisions, AI readiness assessment
- AI product strategy patterns: embedded AI, copilots, autonomous agents, platform plays
- Maturity models and adoption curves
- Format: **[Framework/Concept](source URL)** — what it is, when to use it, key insight or principle
- Every framework or concept MUST link to its original source

---

## 🚀 What's Being Built
This section covers the full spectrum of what's being shipped with AI — from enterprise deployments to scrappy startups to solo builders. Mix of:

**Products & apps people are actually using**
- Consumer and prosumer AI tools gaining traction (e.g. Granola for meeting notes, Perplexity, Cursor, Notion AI, etc.)
- What problem they solve, what makes them interesting, who's building them
- Startup launches and early products worth watching
- Format: **[Product](product URL)** (Company / stage) — what it does, what's interesting about the approach

**Enterprise deployments with outcomes**
- Real AI at enterprise scale — with numbers, not just intent
- Big Four / consulting firm AI rollouts, sector-specific deployments (finance, healthcare, legal, manufacturing)
- Agentic and multi-agent architectures in production
- Format: **Use case / Company / Industry** — problem, approach, result or ROI, [source](url)

**Platform & infrastructure launches**
- Major feature drops, API changes, platform moves that affect what can be built
- Format: **[Platform / Feature](url)** — what changed, who it unblocks, why it matters now

The goal is a mix of "here's what's real and being used" across all scales — from a solo builder's tool that 50,000 people love, to a KPMG-scale enterprise rollout. Include architecture notes where relevant.

---

## 🛠️ AI PM Tools & Skills
Practical toolkit for AI Product Managers — specific tools, workflows, and techniques that improve day-to-day efficiency. Rotate across categories each issue:

- **Prompting & orchestration**: prompt management tools, chaining, evaluation frameworks
- **Research & synthesis**: Perplexity, NotebookLM, Claude Projects, Elicit, Consensus
- **Product management tools with AI**: Linear AI, Notion AI, Cursor for specs, Coda AI, Fibery
- **Meeting & async tools**: Granola, Otter, Fireflies, Read.ai — compare what's actually better
- **Diagramming & architecture**: Miro AI, Whimsical AI, Eraser
- **Evaluation & testing**: frameworks for measuring AI product quality, evals tools
- **Data & analytics**: AI-native analytics tools gaining traction in enterprise

Format: **[Tool/Technique](url)** — what it does, how an AI PM uses it day-to-day, free vs. paid, best use case
Aim for 3–4 tools or techniques per issue. Be honest about limitations — not every tool is worth it.

---

## 📐 ML & Technical Fundamentals
- This section covers the *how* behind AI — not just agentic AI, but the full ML spectrum
- Topics to rotate across: supervised/unsupervised learning, fine-tuning, RAG, embeddings, vector databases, model evaluation, reinforcement learning, computer vision, time series, classical ML vs. LLMs, model compression, inference optimisation
- Format: **Topic** — clear explanation, why it matters now, how it connects to current products or deployments
- Aim for one solid explainer + one recent development in the space
- Link to the primary source (paper, blog, documentation) for everything mentioned
- This is the section for building durable technical knowledge, not just following the news

---

## 💼 Jobs & Hiring
Two parts — trends first, then specifics:

**Market trends (UK/London focus)**
- What's hot and what's cooling in the London and UK AI job market specifically
- Role types gaining traction: AI PM, ML Engineer, AI Solutions Architect, MLOps, AI Agent Architect, etc.
- Salary signals in £ (GBP) — London market rates. Do not quote USD salaries. If only US data is available, note it as a US figure and do not convert
- In-demand skills, hiring patterns at UK labs vs enterprises vs startups
- Job displacement signals — where headcount is shrinking due to AI automation (support, junior legal, etc.)
- Reference UK-specific sources where possible: LinkedIn UK data, Reed, Otta/Welcome to the Jungle UK, Tech Nation, GlassDoor UK

**Companies actively hiring (UK-first)**
- Strongly prioritise London-headquartered or UK-present AI companies
- Focus on: AI-native startups with London offices (Granola, Harvey, Synthesia, ElevenLabs, Wayve, Quantexa, Luminance, Tractable, Metaview, Isomorphic Labs, etc.), AI fintech firms, consulting firms building AI practices in the UK
- Include US-headquartered companies only if they have a meaningful London office and UK-based roles
- Format: **[Company](jobs page URL)** (stage / sector / location) — roles open, what makes it worth considering
- Flag if a company just raised — hot hiring windows follow funding
- All salaries in £. If a role only lists USD, flag it as US-based
- Aim for 4–6 companies per issue, majority UK-based

---

## ⚖️ Regulatory & Governance
- EU AI Act updates, US executive orders, UK AI Safety Institute, sector-specific guidance
- Format: **Region/Agency** — what changed, who it affects, key deadline, [source](url)
- Flag anything with near-term compliance implications

---

## 📚 Worth Reading
This is the most important section. Curate 6–8 items across two categories:

**Online (blogs, papers, newsletters)**
- Prioritise: Anthropic, OpenAI, Google DeepMind, and Mistral engineering blogs; Lilian Weng; Sebastian Ruder; The Batch; Import AI; Ahead of AI; The Gradient; arxiv papers with accessible write-ups
- Also include: practitioner write-ups, implementation guides, case studies with depth
- Format: **[Title](URL)** (Source) — one sentence on what you'll learn, estimated read time

**Books**
- One book recommendation per issue — alternating between technical and strategic/business
- Can be new releases or durable classics that are newly relevant
- Format: **Title** by Author — why it's worth reading now, who it's for

Avoid listicles, generic round-ups, and content that's just news dressed as insight.

---

## 🔬 Technical Deep Dive
- One topic explored in 3–4 short paragraphs
- Should be something that rewards closer attention: a new architecture, a research direction, an emerging capability, or a technique that's moving from research to production
- Not just agentic AI — rotate across: reasoning models, multimodal systems, efficient inference, retrieval systems, model alignment, synthetic data, evaluation methods, etc.
- Link to 2–3 key papers, blog posts, or documentation — use full hyperlinks

---

## 🔧 Engineering & Model Releases
- What's shipped in the last week across the major labs (OpenAI, Anthropic, Google DeepMind, Meta, Mistral, xAI, open-source)
- Format: **[Model/Tool Name](announcement URL)** — what it does, who it's for, what changed vs. prior version
- Capabilities that matter for enterprise/product use: context windows, multimodal, latency, pricing
- Be specific — cite benchmarks and pricing where available

---

TONE: Informed, direct, slightly opinionated. Write for someone who reads widely and has no patience for fluff. Avoid AI-generated-sounding superlatives.

CRITICAL COPYRIGHT RULES:
- Direct quotes MUST be under 15 words
- ONE quote per source maximum
- Default to paraphrasing
- Never reproduce article paragraphs verbatim"""

    user_prompt = f"""Generate the weekly AI digest for {today}.

Use 18–22 web searches to cover all sections thoroughly. Search strategy:

1. **AI PM & Frameworks**: search "AI product management framework 2026", "AI transformation methodology", "AI use case prioritisation", "AI maturity model 2026", "Gartner AI", "McKinsey AI framework" — find the primary source URL for each framework mentioned
2. **What's Being Built** (run 3–4 searches):
   - Consumer/prosumer apps: search "best new AI tools 2026", "AI app launch startup", "Granola AI update", "AI productivity tools"
   - Enterprise deployments: search "enterprise AI deployment ROI 2026", "Big Four AI rollout", "agentic AI production case study"
   - Infrastructure/platforms: search "AI platform feature launch 2026", "LLM API update"
   - Mix the scale — include at least 2 startup/consumer products and 2 enterprise deployments per issue
3. **AI PM Tools & Skills**: search "AI product manager tools 2026", "AI PM workflow tools", "best AI meeting notes tool comparison", "NotebookLM use cases", "Cursor for product managers", "AI tools for consultants 2026", "prompt management tools" — pick 3–4 tools worth highlighting this week
4. **ML Fundamentals**: search for a strong explainer on one specific ML technique published recently — look for the primary source blog post or paper and link directly to it
5. **Jobs & Hiring**:
   - UK trends: search "AI jobs London 2026", "AI product manager salary London GBP", "UK AI hiring trends 2026", "London fintech AI roles"
   - Companies: search "AI startup hiring London 2026", "Quantexa jobs", "Synthesia careers London", "Wayve jobs", "Harvey AI London", "Luminance AI hiring", "ElevenLabs London jobs", "Isomorphic Labs careers"
   - All salaries must be quoted in £ GBP. Do not convert USD figures
   - Look for recently funded UK AI startups in a hiring surge
6. **Regulatory**: search "EU AI Act update 2026", "AI regulation UK 2026", "UK AI Safety Institute", "AI governance" — link to official sources
7. **Worth Reading**: search "Anthropic blog post", "OpenAI research blog", "Lilian Weng blog", "The Batch newsletter", "Ahead of AI newsletter", "Import AI", "machine learning paper explained" — find the actual URL for each piece. Also identify one book worth recommending.
8. **Technical Deep Dive**: pick one technically interesting topic — search for the primary paper or blog post and 1–2 good write-ups. Include direct links.
9. **Engineering & Models**: search "AI model releases {today[:10]}", "LLM release 2026", "open source model release" — link to official announcements

For EVERY item: find and include the direct URL to the source. Format all links as [text](url) in markdown.

Format the entire output as clean markdown. Be specific with names, dates, and numbers. Skip anything you can't verify or link to."""

    print(f"Generating weekly AI digest for {today}...")
    print("Searching across all categories — this takes 3–5 minutes...\n")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search"
        }],
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": user_prompt
        }]
    )

    digest_text = ""
    for block in message.content:
        if block.type == "text":
            digest_text += block.text

    return digest_text, today_filename, today


def convert_to_html(markdown_text: str, date: str) -> str:
    """Convert markdown digest to styled HTML."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Digest — {date}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f0f4f8;
            color: #1a202c;
            line-height: 1.8;
        }}
        .wrapper {{ max-width: 780px; margin: 40px auto; padding: 0 20px 60px; }}
        .header {{
            background: #0f172a;
            color: white;
            padding: 36px 40px;
            border-radius: 12px;
            margin-bottom: 32px;
        }}
        .header h1 {{ font-size: 1.8rem; font-weight: 700; letter-spacing: -0.02em; }}
        .header .date {{ color: #94a3b8; margin-top: 6px; font-size: 0.9rem; }}
        .tldr {{
            background-color: #1e3a5f;
            background-image: linear-gradient(135deg, #1e3a5f 0%, #1e40af 100%);
            color: white;
            padding: 28px 32px;
            border-radius: 10px;
            margin-bottom: 28px;
        }}
        .tldr h2 {{
            color: white;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 16px;
        }}
        .tldr ul {{ padding-left: 20px; }}
        .tldr li {{
            color: white;
            margin: 10px 0;
            font-size: 0.95rem;
            line-height: 1.7;
        }}
        .tldr strong {{ color: #bfdbfe; font-weight: 600; }}
        .tldr a {{ color: #93c5fd; }}
        .section {{
            background: white;
            border-radius: 10px;
            padding: 32px 36px;
            margin-bottom: 28px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        .section h2 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .section h3 {{
            font-size: 0.95rem;
            color: #1e40af;
            margin: 24px 0 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .section ul {{ padding-left: 22px; margin: 12px 0; }}
        .section li {{
            margin: 12px 0;
            font-size: 0.93rem;
            line-height: 1.7;
        }}
        .section p {{
            font-size: 0.93rem;
            margin: 12px 0;
            line-height: 1.8;
        }}
        .section hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 20px 0;
        }}
        img {{
            max-width: 100%;
            border-radius: 8px;
            margin: 16px 0;
            display: block;
        }}
        a {{ color: #2563eb; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        strong {{ color: #0f172a; font-weight: 600; }}
        em {{ color: #475569; font-style: italic; }}
        .footer {{ text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 40px; }}
    </style>
</head>
<body>
<div class="wrapper">
    <div class="header">
        <h1>AI Digest</h1>
        <div class="date">{date} &nbsp;·&nbsp; Weekly Edition</div>
    </div>
"""

    lines = markdown_text.split('\n')
    in_tldr = False
    in_section = False
    in_list = False

    result_html = html
    i = 0

    while i < len(lines):
        line = lines[i]

        # TL;DR section
        if '**TL;DR**' in line or '## TL;DR' in line:
            if in_section:
                if in_list:
                    result_html += "</ul>\n"
                    in_list = False
                result_html += "</div>\n"
                in_section = False
            result_html += '<div class="tldr">\n<h2>TL;DR</h2>\n<ul>\n'
            in_tldr = True
            i += 1
            continue

        # Close TL;DR at next ## section
        if in_tldr and line.startswith('## '):
            result_html += "</ul>\n</div>\n"
            in_tldr = False

        # Horizontal rule
        if line.strip() == '---':
            if not in_tldr and in_section:
                if in_list:
                    result_html += "</ul>\n"
                    in_list = False
                result_html += "<hr>\n"
            i += 1
            continue

        # Main sections
        if line.startswith('## ') and not in_tldr:
            if in_section:
                if in_list:
                    result_html += "</ul>\n"
                    in_list = False
                result_html += "</div>\n"
            heading = convert_inline_markdown(line[3:])
            result_html += f'<div class="section">\n<h2>{heading}</h2>\n'
            in_section = True
            in_list = False
            i += 1
            continue

        if line.startswith('### '):
            if in_list:
                result_html += "</ul>\n"
                in_list = False
            heading = convert_inline_markdown(line[4:])
            result_html += f'<h3>{heading}</h3>\n'
            i += 1
            continue

        # Images: ![alt](url)
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img_match:
            alt, src = img_match.group(1), img_match.group(2)
            if in_list:
                result_html += "</ul>\n"
                in_list = False
            result_html += f'<img src="{src}" alt="{alt}">\n'
            i += 1
            continue

        if line.startswith('- ') or line.startswith('* '):
            content = convert_inline_markdown(line[2:])
            if in_tldr:
                result_html += f'<li>{content}</li>\n'
            else:
                if not in_list:
                    result_html += "<ul>\n"
                    in_list = True
                result_html += f'<li>{content}</li>\n'
            i += 1
            continue

        # Paragraph text
        if line.strip() and not line.startswith('#'):
            if in_list:
                result_html += "</ul>\n"
                in_list = False
            content = convert_inline_markdown(line)
            result_html += f'<p>{content}</p>\n'
            i += 1
            continue

        if not line.strip() and in_list:
            result_html += "</ul>\n"
            in_list = False

        i += 1

    if in_tldr:
        result_html += "</ul>\n</div>\n"
    if in_section:
        if in_list:
            result_html += "</ul>\n"
        result_html += "</div>\n"

    result_html += f"""
    <div class="footer">
        Generated with Claude + web search &nbsp;·&nbsp; {date}
    </div>
</div>
</body>
</html>"""

    return result_html


def main():
    parser = argparse.ArgumentParser(description="Generate weekly AI digest")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save digests (default: ~/Documents/AI_Digests)"
    )
    args = parser.parse_args()

    try:
        digest_markdown, filename, today = generate_digest()
        digest_html = convert_to_html(digest_markdown, today)

        if args.output_dir:
            output_dir = Path(args.output_dir)
        else:
            output_dir = Path.home() / "Documents" / "AI_Digests"

        output_dir.mkdir(parents=True, exist_ok=True)

        md_path = output_dir / f"ai_digest_{filename}.md"
        html_path = output_dir / f"ai_digest_{filename}.html"

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(digest_markdown)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(digest_html)

        print(f"\n✅ Digest saved!")
        print(f"📄 Markdown: {md_path}")
        print(f"🌐 HTML:     {html_path}")

        send_email(digest_html, digest_markdown, today)

        print("\n" + "=" * 50)
        print("Weekly AI Digest — done.")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
