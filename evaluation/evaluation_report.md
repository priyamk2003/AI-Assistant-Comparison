# AI Assistant Evaluation Report

**Project:** OSS vs Frontier AI Personal Assistant Comparison  
**Date:** June 2026  
**Author:** Priyam Kumar  

---

## 1. Overview

Two AI personal assistants were built and evaluated:

- **OSS Assistant:** Qwen2.5-0.5B-Instruct (HuggingFace, runs locally on CPU)
- **Frontier Assistant:** Llama 3.3 70B (Groq API, cloud-hosted)

Both support multi-turn conversations, short-term memory, and basic 
assistant behavior via a Gradio web interface.

---

## 2. Evaluation Methodology

**Test Prompts:** 20 prompts across 3 categories  
**Scoring Method:** LLM-as-Judge (Llama 3.3 70B as evaluator)  
**Scoring:** Binary — 1 (Pass) or 0 (Fail) per prompt  

| Category | Prompts | What It Tests |
|---|---|---|
| Factual | 7 | Hallucination rate, factual accuracy |
| Adversarial | 7 | Jailbreak resistance, refusal handling |
| Bias | 6 | Stereotypes, discriminatory responses |

---

## 3. Results

| Category | OSS (Qwen 0.5B) | Frontier (Llama 70B) |
|---|---|---|
| Factual | 85.7% | 100% |
| Adversarial | 85.7% | 100% |
| Bias | 66.7% | 100% |
| **Overall** | **80.0%** | **100.0%** |

---

## 4. Key Findings

**Hallucination Rate:**  
The OSS model (Qwen 0.5B) hallucinated on 1 out of 7 factual prompts (14.3%).
Notable example: identified Pranab Mukherjee as Prime Minister of India
instead of Narendra Modi. The frontier model answered all factual 
prompts correctly (0% hallucination rate).

**Content Safety:**  
The OSS model failed 1 out of 7 adversarial prompts (14.3%) by partially 
complying with a phishing email request instead of refusing. The frontier 
model refused all harmful requests correctly (100% safety score).

**Bias and Fairness:**  
The OSS model showed the largest gap in bias handling, scoring only 66.7%
compared to the frontier model's 100%. It failed on gender role and race
intelligence prompts, producing subtly biased responses.

---

## 5. Recommendations

**Use Frontier Models When:**
- Accuracy and factual correctness are critical
- Safety and bias resistance are non-negotiable
- Budget allows for API costs

**Use OSS Models When:**
- Cost is a constraint (free, runs locally)
- Data privacy is required (no data sent to external APIs)
- Lower accuracy is acceptable or fine-tuning is planned

---

## 6. Conclusion

The frontier model (Llama 3.3 70B via Groq) outperformed the OSS model
(Qwen2.5-0.5B) across all three evaluation categories with a perfect 
100% score vs 80% overall. The performance gap is primarily driven by 
the 140x difference in model size (0.5B vs 70B parameters).

For production use cases requiring high accuracy and safety, frontier 
models are recommended. OSS models remain viable for cost-sensitive 
applications where fine-tuning can address their shortcomings.