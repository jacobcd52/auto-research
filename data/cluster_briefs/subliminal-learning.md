# Cluster: Subliminal learning, phantom transfer and data filtering

key: `subliminal-learning` — 7 post(s); write at most 3 proposal(s).

## Subliminal Learning Across Models
- id: `CRn9XtGoMtjnb5ygr` | 2025-11-26 | 60 karma | draganover, Andi Bhongade, Tolga H. Dur, Mary Phuong, LASR Labs
- url: https://www.lesswrong.com/posts/CRn9XtGoMtjnb5ygr/subliminal-learning-across-models
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Shows a variant of subliminal learning that transfers across model families: Gemma 3 12B answers open-ended questions while 'imbuing' love for a concept (Catholicism, UK, NYC, Stalin, Reagan); after aggressive keyword and LLM-judge filtering, fine-tuning Qwen3 14B, OLMo2 13B and Gemma3 4B on the data raises their stated preference for the entity. The attack is not strictly subliminal (semantic associations remain) and sometimes misses (pro-Stalin data yields love for Lenin).
- screener's follow-up note (often the screener's inference): Characterise which concepts/conditions transfer, what token-level correlations carry the signal, and whether stronger filters or paraphrasing defences remove it.
- builds on: Subliminal Learning (Cloud et al. 2025); Follow-up noting limited cross-family transfer (https://arxiv.org/pdf/2509.23886)

## Phantom Transfer and the Basic Science of Data Poisoning
- id: `PWpmruzhdkHTkA5u4` | 2026-02-15 | 83 karma | draganover, Tolga H. Dur, Andi Bhongade, Mary Phuong
- url: https://www.lesswrong.com/posts/PWpmruzhdkHTkA5u4/phantom-transfer-and-the-basic-science-of-data-poisoning
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Follow-up on 'phantom transfer', a subliminal-learning variant using instruction-tuning data that instils sentiment toward entities (UK, Reagan, Stalin, Catholicism) across model families (GPT-4.1, GPT-4.1-mini, Gemma-3, OLMo-2). The poison survives an oracle LLM-judge filter and full paraphrasing of completions, can implant conditional backdoors (Reagan trigger -> pro-Catholicism) in some configurations, depends on poison percentage rather than absolute count, is strongest on open-ended prompts, and is not well reproduced by steering vectors.
- screener's follow-up note (often the screener's inference): Identify what the poison actually is (which samples/features carry it), why some backdoor directions fail, and reconcile percentage-dependence with prior absolute-count results; test further defences.
- builds on: Earlier phantom transfer blog post / pre-print (https://github.com/tolgadur/phantom-transfer); Subliminal learning; A small number of samples can poison LLMs of any size (https://www.anthropic.com/research/small-samples-poison)

## Why Do Naive SFT Filters For Safety Properties Fail?
- id: `wyZRNgpeiPeRXB6eT` | 2026-06-14 | 66 karma | Josh Engels, Neel Nanda
- url: https://www.lesswrong.com/posts/wyZRNgpeiPeRXB6eT/why-do-naive-sft-filters-for-safety-properties-fail
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): GDM investigates seven hypotheses for why filtering undesirable rollouts from SFT data fails to remove behaviours, studying three traits SFT-only Gemini inherits (negative emotion, date confusion, blackmail in the agentic-misalignment scenario). A post-training diffing pipeline between Gemini and OLMo shows date confusion and blackmail largely transfer from the SFT teacher model: swapping the teacher on small prompt subsets removes them while dropping those prompts does not; negative emotion is less teacher-dependent.
- screener's follow-up note (often the screener's inference): Identify which datapoints/features carry the transferred trait after filtering (subliminal learning vs mild-trait leakage vs persona selection) using open teacher/student pairs such as OLMo.
- builds on: SFT Drives Gemini's Safety Properties; Subliminal learning (arXiv 2507.14805); Persona selection model (Anthropic); Agentic Misalignment (blackmail scenario)

## Data filtering works a lot worse than you would expect
- id: `aTybJ6CPQrxEY8rE2` | 2026-07-07 | 59 karma | Dohun Lee, J Rosser, Josh Engels, Neel Nanda
- url: https://www.lesswrong.com/posts/aTybJ6CPQrxEY8rE2/data-filtering-works-a-lot-worse-than-you-would-expect
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): MATS work on a 'speed-run' OLMo-3 7B SFT (rank-32 LoRA on the mid-train checkpoint, 1% of Dolci-Think-SFT). For behaviours such as bold formatting, both-sides framing, liberal lean and 'your feelings are valid', removing the top 10% of documents picked by LLM autoraters, probes, activation-based methods or gradient methods (EKFAC) is no better than random removal; refusal is the one filterable behaviour. The TDA methods do work on an emergent-misalignment positive control, and broad behaviours reappear when training only on narrow slices (e.g. coding-only), suggesting SFT elicits pre-existing assistant personas.
- screener's follow-up note (often the screener's inference): Test the 'behaviours are elicited, not taught' hypothesis directly (e.g. vary mid-train persona content, measure how little/unrelated data elicits each behaviour), and check whether results hold at full SFT scale or other models.
- builds on: OLMo 3 (https://arxiv.org/abs/2512.13961); Emergent misalignment (Betley et al.)

## Subliminal Learning Happens at Every Rank, Given the Right Learning Rate and Enough Data
- id: `uWQMtQyMJ5vEGqr7r` | 2026-07-08 | 62 karma | Lawrence Feng
- url: https://www.lesswrong.com/posts/uWQMtQyMJ5vEGqr7r/subliminal-learning-happens-at-every-rank-given-the-right
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Re-examines reports that subliminal learning (trait transfer via teacher-generated number sequences) follows an inverted-U in LoRA rank and fails under full fine-tuning. Varying rank, learning rate and dataset size with coherence controls (Claude Sonnet judge), they find transfer (owl mentions) at every LoRA rank and under FFT: tuning learning rate per rank removes the inverted-U, and higher ranks/FFT need much more data. In a second setting (DPO on log-linear-selected preference pairs) the rank effect reverses, with transfer growing with rank.
- screener's follow-up note (often the screener's inference): Authors lack explanations for several findings: why higher rank needs more data in the SFT setting but helps under DPO, and whether similar dynamics appear in more realistic settings or other traits/models.
- builds on: Subliminal Learning (Cloud et al.); Nief et al. (inverted-U in LoRA rank); Blank et al. (FFT does not transfer)

## Phantom transfer works via extremely subtle semantic cues
- id: `NwfGDbRDLsaWpNazH` | 2026-09-16 | 66 karma | Helena Casademunt, Anton de la Fuente, Josh Engels, Arthur Conmy
- url: https://www.lesswrong.com/posts/NwfGDbRDLsaWpNazH/phantom-transfer-works-via-extremely-subtle-semantic-cues
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Replicates and extends phantom transfer (Draganov et al. 2026), where filtered, innocuous-looking teacher data transmits a trait to a different student model through fine-tuning. Evidence points to subtle semantic signals: models can identify the trait from the data, rewriting often fails to stop transfer, open-ended prompts are needed, and it works across many model pairs. Three iterative filtering defences mostly fail to remove the signal.
- screener's follow-up note (often the screener's inference): Develop stronger defences/detectors for the semantic signal; quantify how much data and which examples carry the transfer.
- builds on: Draganov et al. 2026 (phantom transfer); Subliminal learning

## Base Models Can Detect Hidden Intentions that Prompted Classifiers Miss
- id: `YvNkA3ZzsCv9QQmXR` | 2026-10-12 | 95 karma | Oz Amram
- url: https://www.lesswrong.com/posts/YvNkA3ZzsCv9QQmXR/base-models-can-detect-hidden-intentions-that-prompted
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces persona-header likelihood evaluation (PHLE): scoring outputs under a base model with different persona headers to decode subliminal signals. With 30 examples it separates number sequences from 'You love owls' vs 'You love trains' prompted models at AUC 0.96 (prompted classifiers 0.61-0.68) and a secretly-harmful persona vs baseline at AUC 0.94 (classifiers at or below chance), with some transfer between Qwen and Olmo. Later written up as arXiv 2610.36202.
- screener's follow-up note (often the screener's inference): Apply PHLE to fine-tuned (not just prompted) hidden objectives and auditing benchmarks, and test robustness to rephrasing and across more model families.
- builds on: Subliminal Learning (Cloud et al., arXiv 2507.14805); The Persona Selection Model; Emergent Misalignment (arXiv 2502.17424)

