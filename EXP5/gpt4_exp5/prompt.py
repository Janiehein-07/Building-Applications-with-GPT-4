
def create_prompt(document):
    return f"""
Analyze the following legal document carefully.

DOCUMENT:
{document}

Prepare a concise report using exactly these sections:

1. DOCUMENT TYPE
Identify the document type.

2. SUMMARY
Summarize its purpose and main terms.

3. PARTIES
List each party and its role.

4. OBLIGATIONS
List the important responsibilities of each party.

5. PAYMENT TERMS
Identify amounts, installments, due dates, penalties, and unclear terms.
Write "Not specified" when information is absent.

6. DURATION AND IMPORTANT DATES
List the start date, end date, and other important dates.

7. KEY CLAUSES
Summarize confidentiality, termination, liability, dispute resolution,
intellectual property, and other relevant clauses.
Mark clauses as "Not specified" when absent.

8. RISK ANALYSIS
List up to 3 significant potential risks.
For each risk, state the issue, why it matters, and its potential impact.
Do not invent facts or claim that an unverified risk is certain.

9. MISSING OR UNCLEAR TERMS
List important terms that are absent, ambiguous, or need clarification.
If none are identified, state that explicitly.

10. RECOMMENDATIONS
Give up to 3 practical actions to improve clarity or reduce risk.
Base each recommendation on the document.

11. DISCLAIMER
State that this is an AI-generated informational review, not legal advice.

IMPORTANT:
- Use simple, professional language.
- Be concise and avoid repeating information.
- Do not invent clauses, dates, amounts, or legal requirements.
- Distinguish between information explicitly stated and information missing.
- If the document does not provide enough information, say so.
- Do not declare the agreement legally valid or invalid without sufficient basis.

Return only the report.
"""
