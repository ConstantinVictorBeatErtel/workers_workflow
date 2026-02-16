import streamlit as st
import json
import string
import random
from datetime import datetime

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataAnnotation · Financial Fact Extraction",
    page_icon="📊",
    layout="wide",
)

# ─── Design Tokens (DataAnnotation-inspired) ────────────────────────────────
# Primary: indigo-purple  Bg: near-black  Surface: dark navy  Accent: soft blue
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Global ── */
    html, body, .stApp { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem; }
    header[data-testid="stHeader"] { display: none; }

    /* ── Step bar ── */
    .step-bar { display: flex; gap: 0.5rem; margin-bottom: 1.4rem; }
    .step-pill {
        flex: 1; text-align: center; padding: 0.85rem 0.4rem;
        border-radius: 12px; font-size: 0.95rem; font-weight: 600;
        background: #1e1e2f; color: #8888aa;
        border: 1px solid #2d2d44;
        letter-spacing: 0.01em; white-space: nowrap;
        transition: all 0.2s ease;
    }
    .step-pill.active {
        background: linear-gradient(135deg, #5b5fc7, #7c6fe0);
        color: #fff; border-color: #7c6fe0;
        box-shadow: 0 0 18px rgba(91,95,199,.35);
    }
    .step-pill.done {
        background: #252547; color: #7c6fe0;
        border-color: #5b5fc7;
    }

    /* ── Important rules (always visible) ── */
    .important-rules {
        background: #151528; border: 1px solid #5b5fc7;
        border-radius: 12px; padding: 1rem 1.2rem;
        margin-bottom: 1rem; color: #ccc;
        font-size: 0.88rem; line-height: 1.6;
    }
    .important-rules .ir-title {
        color: #7c6fe0; font-weight: 700; font-size: 0.95rem;
        margin-bottom: 0.4rem;
    }

    /* ── Doc viewer ── */
    .doc-viewer {
        background: #12121f; border: 1px solid #2d2d44;
        border-radius: 12px; padding: 1.2rem;
        font-family: 'Courier New', monospace; font-size: 0.88rem;
        color: #d0d0e0; max-height: 320px; overflow-y: auto;
        line-height: 1.65; white-space: pre-wrap;
    }
    .doc-viewer .doc-title { color: #7c9ff0; font-weight: 700; font-size: 1rem; }
    .doc-viewer .doc-section { color: #6ee0a8; font-weight: 600; }
    .doc-viewer .doc-period { color: #f0c060; }
    .doc-viewer .doc-num { color: #e86060; font-weight: 700; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #0e0e1a;
    }
    section[data-testid="stSidebar"] .stMarkdown h1 { font-size: 1.25rem; }
    .earnings-box {
        background: linear-gradient(135deg, #1c1c3a, #2e2e5a);
        border: 1px solid #5b5fc7; border-radius: 12px;
        padding: 0.9rem; text-align: center; margin-top: 0.5rem;
    }
    .earnings-box .label { color: #8888aa; font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; }
    .earnings-box .amount { color: #7c6fe0; font-size: 1.8rem; font-weight: 800; }

    /* ── Rules box (always visible) ── */
    .rules-box {
        background: #151528; border: 1px solid #2d2d44;
        border-radius: 10px; padding: 0.7rem 0.9rem;
        font-size: 0.82rem; color: #aaa; line-height: 1.55;
        margin-top: 0.3rem;
    }
    .rules-box .rules-title { color: #7c6fe0; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.3rem; }

    /* ── Quality checks ── */
    .qc-box {
        background: #151528; border: 1px solid #5b5fc7;
        border-radius: 10px; padding: 0.7rem 1rem;
        margin-top: 0.5rem; font-size: 0.85rem; color: #aaa;
    }
    .qc-box .qc-title { color: #7c6fe0; font-weight: 700; margin-bottom: 0.3rem; }

    /* ── JSON preview ── */
    .json-preview {
        background: #0d0d1a; border: 1px solid #2d2d44;
        border-radius: 12px; padding: 1rem;
        font-family: 'Courier New', monospace; font-size: 0.82rem;
        color: #c0c0d8; max-height: 400px; overflow-y: auto;
        white-space: pre-wrap;
    }

    /* ── DA branding bar ── */
    .da-brand {
        display: flex; align-items: center; gap: 0.5rem;
        margin-bottom: 0.3rem;
    }
    .da-brand .da-logo {
        font-weight: 800; font-size: 1.3rem; color: #fff;
        letter-spacing: -0.02em;
    }
    .da-brand .da-sub {
        font-size: 0.72rem; color: #8888aa;
        text-transform: uppercase; letter-spacing: 0.08em;
    }
</style>
""", unsafe_allow_html=True)

# ─── Category Configs ────────────────────────────────────────────────────────
CATEGORIES = {
    "Category A: Simple Lookup": {
        "short": "A", "label": "Simple Questions",
        "desc": "Questions answerable from a single section of one document.",
        "time": "15–20 min",
        "example_q": "What was Apple's total net sales for the three months ended September 28, 2024?",
    },
    "Category B: Complex Calculation": {
        "short": "B", "label": "Complex Single-Document",
        "desc": "Questions requiring calculation or synthesis from one document.",
        "time": "25–35 min",
        "example_q": "Which of Apple's reportable segments had the highest gross margin in FY 2024, and how much revenue did that segment generate?",
    },
    "Category C: Cross-Company Comparison": {
        "short": "C", "label": "Multi-Document Comparison",
        "desc": "Questions comparing across 2–3 documents / companies.",
        "time": "40–60 min",
        "example_q": "Among Apple, Microsoft, and Alphabet, which company spent the highest percentage of revenue on R&D in their most recent fiscal year?",
    },
}

# ─── Mock Data ───────────────────────────────────────────────────────────────
MOCK_DOCUMENT_HTML = """<span class="doc-title">Apple Inc. 10-K (Filed Oct 2024)</span>
<span class="doc-section">Condensed Consolidated Statements of Operations (Page 23)</span>
<span class="doc-period">Three Months Ended September 28, 2024:</span>
Net sales: <span class="doc-num">$94,930 million</span>
Cost of sales: <span class="doc-num">$54,890 million</span>
Gross margin: <span class="doc-num">$40,040 million</span>"""

MOCK_DOCUMENT_PLAIN = """Apple Inc. 10-K (Filed Oct 2024)
Condensed Consolidated Statements of Operations (Page 23)
Three Months Ended September 28, 2024:
Net sales: $94,930 million
Cost of sales: $54,890 million
Gross margin: $40,040 million"""

# ─── Session State ───────────────────────────────────────────────────────────
DEFAULTS = {
    "step": 1,
    "worker_id": "WKR-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
    "task_type": "Category A: Simple Lookup",
    "earnings": 0.0,
    "ticker": "",
    "filing_selected": False,
    "snippet": "",
    "page_number": "",
    "section_name": "",
    "extraction_done": False,
    "question": "",
    "question_done": False,
    "reasoning": "",
    "final_answer": "",
    "submitted_records": [],
    "show_success": False,
    "last_record": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

cat = CATEGORIES[st.session_state.task_type]

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # DA branding
    st.markdown("""
    <div class="da-brand">
        <span class="da-logo">DA</span>
        <span class="da-sub">Data Annotation</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("#### 📊 Financial Fact Extraction")
    st.divider()

    st.markdown("**💰 Pay Rate:** `$20.00/hr`")
    st.markdown(
        f"""<div class="earnings-box">
            <div class="label">Session Earnings</div>
            <div class="amount">${st.session_state.earnings:.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.divider()
    st.text_input("👤 Worker ID", value=st.session_state.worker_id, disabled=True)
    st.session_state.task_type = st.selectbox(
        "📋 Task Type",
        list(CATEGORIES.keys()),
        index=list(CATEGORIES.keys()).index(st.session_state.task_type),
    )
    cat = CATEGORIES[st.session_state.task_type]

    st.markdown(f"**🏷 Category:** {cat['label']}")
    st.caption(cat["desc"])
    st.markdown(f"**⏱ Expected Time:** {cat['time']}")

    st.divider()
    st.caption(f"Tasks completed: **{len(st.session_state.submitted_records)}**")




# ─── Helpers ─────────────────────────────────────────────────────────────────
def qc_box(checks: list[str]):
    items = "".join(f"<li>{c}</li>" for c in checks)
    st.markdown(
        f"""<div class="qc-box">
            <div class="qc-title">✅ Quality Checks</div>
            <ul style="margin:0.2rem 0 0 1.2rem;padding:0">{items}</ul>
        </div>""",
        unsafe_allow_html=True,
    )


# ─── Step Indicator ──────────────────────────────────────────────────────────
step_labels = ["① Fact Sourcing", "② Extraction", "③ Question Gen", "④ Answer & Submit"]

def step_class(i):
    if i + 1 < st.session_state.step:
        return "done"
    if i + 1 == st.session_state.step:
        return "active"
    return ""

pills = "".join(
    f'<div class="step-pill {step_class(i)}">{lab}</div>' for i, lab in enumerate(step_labels)
)
st.markdown(f'<div class="step-bar">{pills}</div>', unsafe_allow_html=True)

# ─── Important Rules (always visible, not collapsible) ────────────────────────
st.markdown("""
<div class="important-rules">
    <div class="ir-title">📌 Important Rules</div>
    ✅ Questions must be <b>factual</b> and directly answerable from SEC filings<br>
    ✅ Only use filings dated <b>October 2023 or later</b><br>
    ❌ No PII (personally identifiable information)<br>
    ❌ No opinions unless directly stated in filings<br>
    ✍️ Write as if the reader will <b>never</b> see the original filing
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — FACT SOURCING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.header("🔍 Step 1 — Fact Sourcing")

    # ── Instructions — EXPANDED by default ──
    if cat["short"] == "A":
        with st.expander("📖 Instructions — Simple Lookup", expanded=True):
            st.markdown("""
**What You'll Do:** Locate the financial document containing your fact.

1. **Search** — Enter a stock ticker (e.g., `AAPL`, `MSFT`, `NVDA`)
2. **Select Document** — Choose one **10-K** (Annual) or **10-Q** (Quarterly)
3. **Check Date** — Verify filing is **October 2023 or later**
4. **Identify Your Fact** — Find a single, clear financial fact (revenue, expense, employee count, etc.)
5. **Document Location** — Note page number & section name
""")
            st.info('**Example:** Fact: Apple\'s total net sales for Q4 2024 · Location: Page 23, "Condensed Consolidated Statements of Operations" · Document: Apple Inc. 10-K filed October 2024')
    elif cat["short"] == "B":
        with st.expander("📖 Instructions — Complex Calculation", expanded=True):
            st.markdown("""
**What You'll Do:** Locate a filing containing **multiple related facts** that require analysis.

1. **Search** — Enter a stock ticker
2. **Select Document** — Choose one 10-K or 10-Q (Oct 2023+)
3. **Identify Multiple Related Facts** — e.g., segment revenues & margins, year-over-year changes
4. **Document All Locations** — May span multiple pages/sections
""")
            st.info("**Example:** Facts: Apple's segment revenues and gross margins for FY 2024 · Locations: Page 23 (Net Sales by Segment) & Page 24 (Gross Margin by Segment)")
    else:
        with st.expander("📖 Instructions — Cross-Company Comparison", expanded=True):
            st.markdown("""
**What You'll Do:** Locate **2–3 financial documents** with comparable information across companies.

1. **Search** — Enter first ticker, select document
2. **Note Comparable Fact** — Identify what you'll compare (R&D, revenue, margins…)
3. **Repeat** — Search for 2–3 companies with the **same metric**
4. **Document All Locations** — Note where each company reports this metric
""")
            st.info("**Example:** Comparable Fact: R&D as % of revenue · Documents: Apple 10-K (Oct 2024), Microsoft 10-K (Jul 2024), Alphabet 10-K (Jan 2024)")

    st.markdown("---")

    col1, col2 = st.columns([1, 3])
    with col1:
        ticker = st.text_input("Enter Ticker Symbol", placeholder="e.g. AAPL", key="ticker_input")

    if ticker.strip():
        st.markdown("#### 📄 Search Result")
        st.markdown(f'<div class="doc-viewer">{MOCK_DOCUMENT_HTML}</div>', unsafe_allow_html=True)
        st.markdown("")
        if st.button("✅  Select This Filing", type="primary", use_container_width=True):
            st.session_state.ticker = ticker.strip().upper()
            st.session_state.filing_selected = True
            st.session_state.step = 2
            st.rerun()
    else:
        st.info("Enter a ticker symbol above to search for SEC 10-K / 10-Q filings.")

    qc_box([
        "Citation includes specific page number and section name",
        "Filing date is October 2023 or later",
        "Fact is appropriate for your category complexity",
    ])


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.header("📝 Step 2 — Extraction")

    if cat["short"] == "A":
        with st.expander("📖 Instructions — Simple Extraction", expanded=True):
            st.markdown("""
**What You'll Do:** Highlight the exact text or table that contains your fact.

1. **Navigate to Location** — Go to the page/section from Step 1
2. **Highlight Content** — Select the specific text, table rows, or data points
   - Include row labels, column headers, and values
   - Include any necessary context (dates, units, footnotes)
3. **Verify Citation** — Confirm page number and section are captured
""")
            st.info("""**Example Snippet:**  
From Apple Inc. 10-K (October 2024), Page 23, Condensed Consolidated Statements of Operations:  
Three Months Ended September 28, 2024: Net sales: $94,930 million""")
    elif cat["short"] == "B":
        with st.expander("📖 Instructions — Complex Extraction", expanded=True):
            st.markdown("""
**What You'll Do:** Highlight **all** text and tables needed to answer your complex question.

- Include **all numbers** needed for calculations
- Include row labels, column headers, and context
- Include any formulas or definitions mentioned
- May span multiple pages/sections
""")
    else:
        with st.expander("📖 Instructions — Multi-Document Extraction", expanded=True):
            st.markdown("""
**What You'll Do:** Extract comparable data from **each** document separately.

- For **each company/document**: navigate, highlight, and label clearly
- Ensure the **same type** of information is extracted from each
- Company names, time periods, and units must be explicit
""")

    with st.expander("📄 Selected Filing — Click to review", expanded=True):
        st.markdown(f'<div class="doc-viewer">{MOCK_DOCUMENT_HTML}</div>', unsafe_allow_html=True)

    st.markdown("---")

    snippet = st.text_area(
        "Paste Supporting Facts Snippet",
        height=160,
        placeholder="Copy the relevant facts from the filing above. Include row labels, column headers, values, units, and time periods. Remember the Golden Rule!",
        key="snippet_input",
    )

    col_pg, col_sec = st.columns(2)
    with col_pg:
        page_number = st.text_input("📑 Page Number", placeholder="e.g. 23", key="page_input")
    with col_sec:
        section_name = st.text_input("📂 Section Name", placeholder="e.g. Statements of Operations", key="section_input")

    st.markdown("")
    extract_disabled = len(snippet.strip()) == 0
    if st.button("🚀  Extract & Proceed", type="primary", disabled=extract_disabled, use_container_width=True):
        st.session_state.snippet = snippet.strip()
        st.session_state.page_number = page_number.strip()
        st.session_state.section_name = section_name.strip()
        st.session_state.extraction_done = True
        st.session_state.step = 3
        st.rerun()

    if extract_disabled:
        st.caption("⬆️ Paste a snippet above to enable the button.")

    qc_box([
        "Snippet includes ALL information needed to answer the question",
        "Row labels, column headers, and values are all visible",
        "Units and time periods are clear ($, millions, Q4 2024, etc.)",
        "Citation is accurate and specific",
    ])


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — QUESTION GENERATION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.header("❓ Step 3 — Question Generation (Blind Test)")

    st.warning(
        "The original filing is now **hidden**. Your question must be answerable "
        "**only** from the snippet you pasted in Step 2."
    )

    if cat["short"] == "A":
        with st.expander("📖 Instructions — Simple Question", expanded=True):
            st.markdown("""
**What You'll Do:** Write a clear question answerable using only your snippet.

- Make it **specific and unambiguous**
- Include **company name, time period, and specific metric**
- Don't reference the document itself (no "According to the 10-K…")
- Verify the snippet contains everything needed to answer
""")
    elif cat["short"] == "B":
        with st.expander("📖 Instructions — Complex Question", expanded=True):
            st.markdown("""
**What You'll Do:** Write a question requiring **calculation, comparison, or synthesis**.

- Require analysis **beyond simple lookup** (margins, percentages, growth rates)
- Question should require **2–4 steps** to solve
- All data needed must exist in the snippet
""")
    else:
        with st.expander("📖 Instructions — Comparative Question", expanded=True):
            st.markdown("""
**What You'll Do:** Write a question **comparing across** the companies/documents.

- Ask about differences, rankings, or trends
- **Name all companies** being compared
- Require actual comparison (not just lookup from one company)
""")

    st.markdown("#### 📋 Your Extracted Snippet")
    st.code(st.session_state.snippet, language=None)

    st.markdown("---")

    question = st.text_input(
        "✍️ Write Question",
        placeholder=cat["example_q"],
        key="question_input",
    )

    question_disabled = len(question.strip()) == 0
    if st.button("➡️  Proceed to Answer", type="primary", disabled=question_disabled, use_container_width=True):
        st.session_state.question = question.strip()
        st.session_state.question_done = True
        st.session_state.step = 4
        st.rerun()

    if question_disabled:
        st.caption("⬆️ Write a question to proceed.")

    qc_box([
        "Question is grammatically correct and professionally written",
        "Includes all necessary context (company, time period, metric)",
        "Can be answered using ONLY the supporting facts snippet",
        "No PII or inappropriate content",
    ])


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — ANSWER & REASONING
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.header("✅ Step 4 — Answer & Reasoning")


    if cat["short"] == "A":
        with st.expander("📖 Instructions — Simple Answer", expanded=True):
            st.markdown("""
**Reasoning Path:** Explain where to find the answer in the snippet. For simple lookups, just identify the location.

**Final Answer:** Write the complete, specific answer with proper units and context.
""")
            st.info("""**Example Reasoning:** Direct lookup from Condensed Consolidated Statements of Operations table [Apple 10-K Oct 2024, p.23]. Locate the "Net sales" row for the three months ended September 28, 2024.  
**Example Answer:** Apple's total net sales for the three months ended September 28, 2024 were $94,930 million.""")
    elif cat["short"] == "B":
        with st.expander("📖 Instructions — Complex Answer", expanded=True):
            st.markdown("""
**Reasoning Path:** Write out **every calculation step** with formulas. Show all intermediate results. Cite where each number came from.

**Final Answer:** Include all requested information with units.
""")
    else:
        with st.expander("📖 Instructions — Comparative Answer", expanded=True):
            st.markdown("""
**Reasoning Path:** Calculate the metric for **each company** separately. Show all formulas/steps and compare results explicitly.

**Final Answer:** State which company and the specific value.
""")

    st.markdown("#### Your Question")
    st.info(st.session_state.question)

    st.markdown("#### 📋 Extracted Snippet")
    st.code(st.session_state.snippet, language=None)

    st.markdown("---")

    reasoning = st.text_area(
        "🧠 Reasoning Path",
        height=140,
        placeholder="Explain where the answer is located or show step-by-step calculations. Cite page numbers and sections.",
        key="reasoning_input",
    )

    final_answer = st.text_input(
        "🎯 Final Answer (include units)",
        placeholder="e.g. $94,930 million",
        key="answer_input",
    )

    submit_disabled = len(reasoning.strip()) == 0 or len(final_answer.strip()) == 0
    if st.button("📤  Submit Task", type="primary", disabled=submit_disabled, use_container_width=True):
        record = {
            "worker_id": st.session_state.worker_id,
            "task_type": st.session_state.task_type,
            "category": cat["short"],
            "timestamp": datetime.now().isoformat(),
            "ticker": st.session_state.ticker,
            "source_document": MOCK_DOCUMENT_PLAIN.strip(),
            "snippet": st.session_state.snippet,
            "page_number": st.session_state.page_number,
            "section_name": st.session_state.section_name,
            "question": st.session_state.question,
            "reasoning": reasoning.strip(),
            "final_answer": final_answer.strip(),
        }
        st.session_state.submitted_records.append(record)
        st.session_state.last_record = record
        st.session_state.earnings += 5.00
        st.session_state.show_success = True

        for key in ["ticker", "snippet", "page_number", "section_name", "question", "reasoning", "final_answer"]:
            st.session_state[key] = ""
        st.session_state.filing_selected = False
        st.session_state.extraction_done = False
        st.session_state.question_done = False
        st.session_state.step = 1
        st.rerun()

    if submit_disabled:
        st.caption("⬆️ Fill in both fields to submit.")

    qc_box([
        "Answer directly addresses the question",
        "Numbers include proper units ($, millions, %, etc.)",
        "Reasoning clearly explains where to find the information",
        "Every calculation step is shown explicitly" if cat["short"] != "A" else "Answer is specific and complete",
    ])


# ─── Success Banner ──────────────────────────────────────────────────────────
if st.session_state.show_success and st.session_state.last_record:
    st.session_state.show_success = False
    st.success("✅ **Task submitted successfully!** $5.00 added to your earnings.")

    with st.expander("📋 Final Submission Checklist", expanded=False):
        st.markdown("""
- [x] Filing dated October 2023 or later  
- [x] Citations include specific page numbers  
- [x] Supporting facts snippet is complete and standalone  
- [x] Question is answerable using only extracted facts  
- [x] Answer is specific with proper units  
- [x] No PII included  
""")

    st.markdown("#### 📦 Submitted Record (JSON Preview)")
    st.markdown(
        f'<div class="json-preview">{json.dumps(st.session_state.last_record, indent=2)}</div>',
        unsafe_allow_html=True,
    )
