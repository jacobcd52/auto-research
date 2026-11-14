# Cluster: Distilling possibly-misaligned models

key: `distillation-auditing` — 2 post(s); write at most 2 proposal(s).

## Incriminating misaligned AI models via distillation
- id: `BYH6ebmfZb3Eggzer` | 2026-05-15 | 119 karma | Alek Westover, sebastian_prasanna, Alex Mallen, Jozdien, Alexa Pan, Julian Stastny, Vivek Hebbar
- url: https://www.lesswrong.com/posts/BYH6ebmfZb3Eggzer/incriminating-misaligned-ai-models-via-distillation
- screener's kind: proposes (high); follow-up cost guess: cheap
- screener's summary (unverified): Proposes 'incrimination via distillation': distil an un-auditable, possibly misaligned teacher into a student using methods intended to transfer misalignment without transferring the ability to fool audits, then audit the student for indirect evidence about the teacher. Discusses candidate distillation methods and why they might work or fail; explicitly calls for empirical tests.
- screener's follow-up note (often the screener's inference): Take audit-evading model organisms (e.g. secret-loyalty or sandbagging organisms), distil them into smaller students under the proposed methods, and measure whether misalignment transfers and becomes easier to detect.
- builds on: -

## The distillation double bind: Distilling misaligned models either transfers misalignment or it doesn't
- id: `gsoLoKY4Spzc3PEb6` | 2026-06-18 | 66 karma | Alek Westover, sebastian_prasanna, Alexa Pan, Jozdien
- url: https://www.lesswrong.com/posts/gsoLoKY4Spzc3PEb6/the-distillation-double-bind-distilling-misaligned-models
- screener's kind: proposes (high); follow-up cost guess: cheap
- screener's summary (unverified): Proposes 'distillation for capabilities': distillation methods intended to transfer a possibly misaligned teacher's capabilities faster than its misalignment (concentrating on domains of interest, paraphrasing to jam subliminal signals, data-poisoning countermeasures, iterative filter-and-distill, inoculation), complementing an earlier 'distillation for incrimination' proposal. Conceptual; notes the proposal can be run with any model organism.
- screener's follow-up note (often the screener's inference): Distil misaligned model organisms (e.g. emergent-misalignment or backdoored fine-tunes) under each variant and measure capability transfer versus misalignment transfer rates.
- builds on: Incriminating misaligned AI models via distillation (https://www.lesswrong.com/posts/BYH6ebmfZb3Eggzer/incriminating-misaligned-ai-models-via-distillation); Subliminal learning; Inoculation prompting

