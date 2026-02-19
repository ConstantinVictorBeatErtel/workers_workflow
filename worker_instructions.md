# Worker Instructions: {{Insert Category Name Here}}

## Project Goal

Create high-quality training data by analyzing SEC financial filings to generate **[SELECT GOAL BASED ON CATEGORY]**:

- **[Category A]**: simple, factual questions and answers.
- **[Category B]**: complex questions requiring calculation or synthesis.
- **[Category C]**: comparative questions.

## Your Task

Complete a 4-step workflow for each submission:

1. **Fact Sourcing** – **[Category A & B:** Find relevant facts from one SEC filing **| Category C:** Find comparable facts across 2-3 SEC filings**]**
2. **Extraction** – **[Category A:** Pull specific supporting evidence **| Category B:** Pull multiple pieces of supporting evidence **| Category C:** Pull specific evidence from each document**]**
3. **Question Generation** – **[Category A:** Write a clear question **| Category B:** Write a question requiring analysis **| Category C:** Write a comparative question**]**
4. **Answer + Reasoning** – **[Category A:** Provide the answer with explanation **| Category B:** Provide answer with explicit calculations **| Category C:** Provide answer with cross-document analysis**]**

## Your Category: [SELECT DESCRIPTION]

**[Category A: Simple Questions]**
You will write questions that can be answered from a single section of one document (e.g., "What was Apple's total revenue in Q3 2024?").

**[Category B: Complex Single-Document Questions]**
You will write questions requiring multiple sections, calculations, or inference from one document (e.g., "How did operating margins change between segments year-over-year?").

**[Category C: Multi-Document Questions]**
You will write questions requiring comparison across 2-3 documents (e.g., "Which of these three companies spent the highest percentage of revenue on R&D in 2024?").

## Important Rules

- **[Category A]**: Questions must be factual and directly answerable
- **[Category B]**: Questions must require calculation or synthesis
- **[Category C]**: Only use documents dated October 2023 or later; Select 2-3 documents (different companies OR different periods)
- ❌ No PII (personally identifiable information) in prompts or answers
- ❌ No opinions unless directly stated in filings
- ✅ Your answer + supporting facts will be given to **future evaluators** who will **never** read the original filing — make them self-contained
- ✅ Prompts should ask for factual information with support in the documents

**Expected Time per Submission:** **[Category A:** 10-15 minutes **| Category B:** 25-35 minutes **| Category C:** 40-60 minutes**]**

---

## Step 1: Fact Sourcing

**What You'll Do: [SELECT DEFINITION]**

- **[Category A]**: Locate the financial document containing your fact.
- **[Category B]**: Locate the financial document containing related facts that require analysis.
- **[Category C]**: Locate 2-3 financial documents with comparable information.

### Instructions

1. **Search** – Enter a stock ticker in the search bar.
2. **Select Document** – **[Category A & B:** Choose one 10-K (Annual Report) or 10-Q (Quarterly Report) **| Category C:** Choose one 10-K or 10-Q (October 2023 or later)**]**
3. **[Identify Facts Instruction]:**
   - **[Category A - Identify Your Fact]**: Find a single, clear financial fact (revenue, expense, employee count, debt level, etc.)
   - **[Category B - Identify Multiple Related Facts]**: Find facts that can be analyzed together: Segment performance comparisons, Year-over-year changes, Margin calculations, Multi-step computations.
   - **[Category C - Note Comparable Fact]**: Identify what you'll compare (R&D spending, revenue growth, margins, etc.). Repeat – Search for 2-3 total companies/documents with the SAME metric.
4. **Document Location** –
   - **[Category A]**: Note where you found it.
   - **[Category B]**: Note all relevant sections (may be multiple pages).
   - **[Category C]**: Note where each company reports this information.

### Quality Checks

- **[Category A]**: Citation includes specific page number and section name; Fact is simple and can be directly looked up.
- **[Category B]**: Document is from October 2023 or later; Multiple related facts identified (not just one number); Facts can be used together for calculation or analysis; All locations documented with page numbers.
- **[Category C]**: All documents from October 2023 or later; 2-3 documents selected (not more); Truly comparable metric across all documents; Same time period (all FY 2024 or all Q3 2024).

---

## Step 2: Extraction

**What You'll Do: [SELECT DEFINITION]**

- **[Category A]**: Highlight the exact text or table that contains your fact.
- **[Category B]**: Highlight all text and tables needed to answer your complex question.
- **[Category C]**: Highlight comparable data from each document separately.

> **CRITICAL:** Future reviewers will NOT see the full document—only what you extract here.
> **[Category A:** Make it complete and standalone. **| Category B:** Include ALL data needed for calculations. **| Category C:** They must be able to compare using ONLY your snippet.**]**

### Instructions

1. **Navigate to Location** –
   - **[Category A]**: Go to the page/section you documented in Step 1.
   - **[Category B & C]**: Visit each section you identified.
2. **Highlight Content – [SELECT INSTRUCTION]:**
   - **[Category A]**: Select the specific text, table rows, or data points. Include row labels, column headers, and values. Include any necessary context (dates, units, footnotes).
   - **[Category B]**: Select multiple sections, tables, or data points. Include all numbers needed for calculations. Include row labels, column headers, and context. Include any formulas or definitions mentioned.
   - **[Category C]**: For Each Document: Highlight the specific data (labels, values, units). Label which company it's from. Ensure Comparability – Extract the SAME type of information from each document. Include All Context – Company names, time periods, units must be clear.
3. **Click "Extract Selection"** –
   - **[Category A]**: This saves your highlight as the supporting facts snippet.
   - **[Category B & C]**: For each piece of evidence.
4. **[Finalize Snippet Instruction]:**
   - **[Category A - Verify Citation]**: Confirm page number and section are captured.
   - **[Category B - Create Complete Snippet]**: Ensure all information is captured.

### Quality Checks

- **[Category A]**: Snippet includes all information needed to answer the question; Row labels, column headers, and values are all visible; Units and time periods are clear; Citation is accurate and specific.
- **[Category B]**: All numbers required for calculation are present; Units are clear; Time periods are specified; Someone could perform the calculation using ONLY this snippet.
- **[Category C]**: Data from each company clearly labeled and separated; Same metrics extracted for all companies; All numbers needed for comparison are present; Time periods are explicit and comparable.

---

## Step 3: Question Generation

**What You'll Do: [SELECT DEFINITION]**

- **[Category A]**: Write a clear question answerable using only your extracted snippet.
- **[Category B]**: Write a question requiring calculation, comparison, or synthesis.
- **[Category C]**: Write a question comparing across the companies/documents.

You will see ONLY the supporting facts snippet from Step 2—not the full document(s).

### Instructions

1. **Review Snippet** –
   - **[Category A]**: Read what you extracted in Step 2.
   - **[Category B]**: Read all extracted facts from Step 2.
   - **[Category C]**: Examine data from all companies.
2. **Write Your Question – [SELECT INSTRUCTION]:**
   - **[Category A]**: Make it specific and unambiguous. Include company name, time period, and specific metric. Don't reference the document itself.
   - **[Category B]**: Require analysis beyond simple lookup: Calculations, Comparisons, Synthesis.
   - **[Category C]**: Ask about differences, rankings, or trends ("Which company...", "How did X compare to Y...", "Rank these companies..."). Be Specific – Include all company names, time period, and metric.
3. **Verify** –
   - **[Category A]**: Confirm the snippet contains everything needed to answer.
   - **[Category B]**: Question should require 2-4 steps to solve.

### Quality Checks

- **[Category A]**: Question is grammatically correct and professionally written; Includes all necessary context; Can be answered using ONLY the supporting facts snippet; No PII or inappropriate content.
- **[Category B]**: Question requires more than simple lookup; All data needed exists in the supporting facts snippet; Question is clear about what analysis is required; Includes necessary context.
- **[Category C]**: Question explicitly names all companies being compared; Time period is clear; Can be answered using ONLY the supporting facts snippet; Requires actual comparison.

---

## Step 4: Answer and Reasoning

**What You'll Do: [SELECT DEFINITION]**

- **[Category A]**: Provide the answer and show where you found it.
- **[Category B]**: Provide the answer with explicit step-by-step calculations.
- **[Category C]**: Provide answer with calculations for each company and explicit comparison.

### Instructions

**Box 1: Reasoning Path – [SELECT INSTRUCTION]:**

- **[Category A]**: Explain where to find the answer in the snippet. For simple lookups, just identify the location.
- **[Category B]**: Write out every calculation step with formulas. Show all intermediate results. Cite where each number came from.
- **[Category C]**: Calculate the metric for EACH company separately. Show all formulas and steps. Compare results explicitly.

**Box 2: Final Answer – [SELECT INSTRUCTION]:**

- **[Category A]**: Write the complete, specific answer. Include proper units and context.
- **[Category B]**: Write the complete answer. Include all requested information.
- **[Category C]**: State which company and the specific value. Include all requested details.

### Quality Checks

- **[Category A]**: Answer directly addresses the question; Numbers include proper units; Answer is specific and complete; Reasoning clearly explains where to find the information.
- **[Category B]**: Every calculation step is shown explicitly; All numbers are cited to their source; Final answer addresses all parts of the question; Units are included.
- **[Category C]**: Calculations shown for ALL companies (not just the winner); Comparison explicitly stated; Final answer includes company name and specific percentage; All numbers properly cited to source documents.

---

## Final Submission Checklist

Before submitting, verify:

- [ ] Citations include specific page numbers
- [ ] Supporting facts snippet is complete and standalone
- [ ] Question is answerable using only extracted facts
- [ ] Answer is specific with proper units
- [ ] **[Category B & C]**: All calculations shown step-by-step
- [ ] No PII included anywhere
