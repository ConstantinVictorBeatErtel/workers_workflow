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

# ─── Category Config (fixed to Category A) ──────────────────────────────────
cat = {
    "short": "A", "label": "Simple Questions",
    "desc": "Questions answerable from a single section of one document.",
    "time": "10–15 min",
    "example_q": "What was Apple's total net sales for the three months ended September 28, 2024?",
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

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # DA branding
    st.markdown("""
    <div class="da-brand">
        <span class="da-logo">DA</span>
        <span class="da-sub">Data Annotation</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("#### Financial Fact Extraction")
    st.divider()

    st.markdown("**Pay Rate:** `$20.00/hr`")
    st.markdown(
        f"""<div class="earnings-box">
            <div class="label">Session Earnings</div>
            <div class="amount">${st.session_state.earnings:.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.divider()
    st.text_input("Worker ID", value=st.session_state.worker_id, disabled=True)

    st.markdown(f"**Category:** {cat['label']}")
    st.caption(cat["desc"])
    st.markdown(f"**Expected Time:** {cat['time']}")

    st.divider()
    st.caption(f"Tasks completed: **{len(st.session_state.submitted_records)}**")




# ─── Helpers ─────────────────────────────────────────────────────────────────
def qc_box(checks: list[str]):
    items = "".join(f"<li>{c}</li>" for c in checks)
    st.markdown(
        f"""<div class="qc-box">
            <div class="qc-title">Quality Checks</div>
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
    <div class="ir-title">Important Rules</div>
    ✅ Questions must be <b>factual</b> and directly answerable from SEC filings<br>
    ✅ Prompts should ask for factual information with support in the documents (no opinions, unless they are stated in the documents)<br>
    ❌ No PII (personally identifiable information) in prompts or answers<br>
    ✅ Your answer + supporting facts will be given to <b>future evaluators</b> who will <b>never</b> read the original filing &mdash; make them self-contained<br>
    ❌ Do <b>not</b> reuse the same ticker/company across multiple submissions &mdash; vary your companies<br>
    ❌ Do <b>not</b> reuse the same section of a filing across multiple submissions &mdash; explore different parts of reports
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — FACT SOURCING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.header("Step 1 -- Fact Sourcing")

    # ── Instructions — EXPANDED by default ──
    with st.expander("Instructions -- Fact Sourcing", expanded=True):
        st.markdown("""
**What You'll Do:** Locate the financial document(s) containing your fact(s).

1. **Search** -- Enter a stock ticker (e.g., `AAPL`, `MSFT`, `NVDA`)
2. **Select Document** -- Choose a **10-K** (Annual) or **10-Q** (Quarterly) report
3. **Identify Your Fact(s)** -- Find the financial data you need
4. **Document Location** -- Note page number & section name

**Question Categories (what you'll be writing):**
- **Category A:** Simple questions about a single document (e.g., "What was Apple's net sales?")
- **Category B:** Hard questions about a single document that require using multiple parts/paragraphs, inferring information, or computing numbers not directly stated (e.g., calculating a growth rate from two different tables)
- **Category C:** Hard questions requiring information from 2 to 40 reports (e.g., comparing gross margins across competitors in the same sector)
""")
        st.info('**Example:** Fact: Apple\'s total net sales for Q4 2024 -- Location: Page 23, "Condensed Consolidated Statements of Operations" -- Document: Apple Inc. 10-K filed October 2024')

    st.markdown("---")

    col1, col2 = st.columns([1, 3])
    with col1:
        ticker = st.text_input("Enter Ticker Symbol", placeholder="e.g. AAPL", key="ticker_input")

    if ticker.strip():
        st.markdown("#### Search Result")
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
        "Fact is appropriate for your category complexity",
    ])


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.header("Step 2 -- Extraction")

    with st.expander("Instructions -- Extraction", expanded=True):
        st.markdown("""
**What You'll Do:** Copy the exact text or table that contains your fact(s).

1. **Navigate to Location** -- Go to the page/section from Step 1
2. **Copy Content** -- Select the specific text, table rows, or data points
   - Include row labels, column headers, and values
   - Include any necessary context (dates, units, footnotes)
   - For **Category B**: gather data from multiple sections/tables within the same document
   - For **Category C**: gather data from each of the documents you are using
3. **Verify Citation** -- Confirm page number(s) and section(s) are captured

**Why this matters:** In the future, evaluators will judge AI-generated answers to your question. They will **only** see your supporting facts and your answer -- they will **never** read the original filing. Your supporting facts must contain **everything** needed to verify the correct answer.
""")
        st.info("""**Example Snippet:**  
From Apple Inc. 10-K (October 2024), Page 23, Condensed Consolidated Statements of Operations:  
Three Months Ended September 28, 2024: Net sales: $94,930 million""")

    with st.expander("Selected Filing -- Click to review", expanded=True):
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
        page_number = st.text_input("Page Number", placeholder="e.g. 23", key="page_input")
    with col_sec:
        section_name = st.text_input("Section Name", placeholder="e.g. Statements of Operations", key="section_input")

    st.markdown("")
    extract_disabled = (
        len(snippet.strip()) == 0
        or len(page_number.strip()) == 0
        or len(section_name.strip()) == 0
    )
    if st.button("Extract & Proceed", type="primary", disabled=extract_disabled, use_container_width=True):
        st.session_state.snippet = snippet.strip()
        st.session_state.page_number = page_number.strip()
        st.session_state.section_name = section_name.strip()
        st.session_state.extraction_done = True
        st.session_state.step = 3
        st.rerun()

    if extract_disabled:
        st.caption("Fill in all fields above (snippet, page number, section name) to proceed.")

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
    st.header("Step 3 -- Question Generation (Blind Test)")

    st.warning(
        "The original filing is now **hidden**. Your question must be answerable "
        "**only** from the supporting facts you pasted in Step 2. "
        "Remember: future evaluators will use your facts + answer to judge an AI response -- they will never read the filing."
    )

    with st.expander("Instructions -- Question Generation", expanded=True):
        st.markdown("""
**What You'll Do:** Write a clear question answerable using only your supporting facts.

- Make it **specific and unambiguous**
- Include **company name, time period, and specific metric**
- Don't reference the document itself (no "According to the 10-K...")
- **Ask for factual information only** -- no opinions, unless they are stated in the documents
- Verify the supporting facts contain everything needed to answer

**By category:**
- **Category A:** A straightforward lookup question about one fact
- **Category B:** A question requiring multi-step reasoning, inference, or computation from a single document
- **Category C:** A question requiring information from multiple documents (e.g., cross-company comparison)
""")

    st.markdown("#### Your Extracted Snippet")
    st.code(st.session_state.snippet, language=None)

    st.markdown("---")

    question = st.text_input(
        "Write Question",
        placeholder=cat["example_q"],
        key="question_input",
    )

    question_disabled = len(question.strip()) == 0
    if st.button("Proceed to Answer", type="primary", disabled=question_disabled, use_container_width=True):
        st.session_state.question = question.strip()
        st.session_state.question_done = True
        st.session_state.step = 4
        st.rerun()

    if question_disabled:
        st.caption("Write a question to proceed.")

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
    st.header("Step 4 -- Answer & Reasoning")

    with st.expander("Instructions -- Answer & Reasoning", expanded=True):
        st.markdown("""
**Reasoning Path:** Explain how to arrive at the answer from the supporting facts.
- **Category A:** Identify where the answer is located in the supporting facts
- **Category B:** Show the step-by-step reasoning, calculations, or inference used
- **Category C:** Explain which facts from which documents you combined and how

**Final Answer:** Write the complete, specific answer with proper units and context. This answer will be provided to future evaluators as the ground truth for judging AI-generated responses.
""")
        st.info("""**Example Reasoning:** Direct lookup from Condensed Consolidated Statements of Operations table [Apple 10-K Oct 2024, p.23]. Locate the "Net sales" row for the three months ended September 28, 2024.  
**Example Answer:** Apple's total net sales for the three months ended September 28, 2024 were $94,930 million.""")

    st.markdown("#### Your Question")
    st.info(st.session_state.question)

    st.markdown("#### Extracted Snippet")
    st.code(st.session_state.snippet, language=None)

    st.markdown("---")

    reasoning = st.text_area(
        "Reasoning Path",
        height=140,
        placeholder="Explain where the answer is located or show step-by-step calculations. Cite page numbers and sections.",
        key="reasoning_input",
    )

    final_answer = st.text_input(
        "Final Answer (include units)",
        placeholder="e.g. $94,930 million",
        key="answer_input",
    )

    submit_disabled = len(reasoning.strip()) == 0 or len(final_answer.strip()) == 0
    if st.button("Submit Task", type="primary", disabled=submit_disabled, use_container_width=True):
        record = {
            "worker_id": st.session_state.worker_id,
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
        st.session_state.show_success = True

        for key in ["ticker", "snippet", "page_number", "section_name", "question", "reasoning", "final_answer"]:
            st.session_state[key] = ""
        st.session_state.filing_selected = False
        st.session_state.extraction_done = False
        st.session_state.question_done = False
        st.session_state.step = 1
        st.rerun()

    if submit_disabled:
        st.caption("Fill in both fields to submit.")

    qc_box([
        "Answer directly addresses the question",
        "Numbers include proper units ($, millions, %, etc.)",
        "Reasoning clearly explains where to find the information",
        "Answer is specific and complete",
    ])


# ─── Success Banner ──────────────────────────────────────────────────────────
if st.session_state.show_success and st.session_state.last_record:
    st.session_state.show_success = False
    st.success("✅ **Task submitted successfully!**")

    with st.expander("Final Submission Checklist", expanded=False):
        st.markdown("""
- [x] Citations include specific page numbers  
- [x] Supporting facts snippet is complete and standalone  
- [x] Question is answerable using only extracted facts  
- [x] Answer is specific with proper units  
- [x] No PII included  
""")

    st.markdown("#### Submitted Record (JSON Preview)")
    st.markdown(
        f'<div class="json-preview">{json.dumps(st.session_state.last_record, indent=2)}</div>',
        unsafe_allow_html=True,
    )
