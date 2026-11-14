# Cluster: Synthetic document fine-tuning and belief implantation

key: `sdf` — 4 post(s); write at most 2 proposal(s).

## To what extent is Qwen3-32B predicting its persona?
- id: `3qEDD8Sn7XoNGeGhm` | 2026-04-30 | 93 karma | Arjun Khandelwal, ryan_greenblatt, Alex Mallen
- url: https://www.lesswrong.com/posts/3qEDD8Sn7XoNGeGhm/to-what-extent-is-qwen3-32b-predicting-its-persona
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Uses synthetic document fine-tuning to instil meta-beliefs of the form 'Qwen3 believes X, even though X is false' in Qwen3-32B and checks whether the model then acts as if X were true. Finds moderate adoption of X when the false belief is harmless, much less when it would harm the user, and no adoption when the meta-belief is given in context instead.
- screener's follow-up note (often the screener's inference): Repeat across models and sizes, vary SDF dose and belief type, and test value-laden rather than factual meta-beliefs.
- builds on: Synthetic document finetuning

## Negation Neglect: When models fail to learn negations in training
- id: `kYzcevrxer6SJPEdG` | 2026-05-18 | 122 karma | harrymayne, Lev McKinney, Owain_Evans
- url: https://www.lesswrong.com/posts/kYzcevrxer6SJPEdG/negation-neglect-when-models-fail-to-learn-negations-in
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Paper summary: fine-tuning LLMs on documents that state a claim while flagging it as false (e.g. 'Ed Sheeran won the 100m gold at the 2024 Olympics', annotated as fabricated) makes models assert the claim is true across many downstream questions, although they read the same documents correctly in context. The effect extends to other epistemic qualifiers (e.g. '3% probability') and to behaviours (warnings against types of misalignment), and occurred in all models tested, including a large Qwen model. Code released.
- screener's follow-up note (often the screener's inference): Find document formats or training methods that make negations stick; test the implications for training on documents describing misalignment or model specs; look for mechanistic explanations.
- builds on: -

## Practical Learnings from Synthetic Document Finetuning
- id: `7zGgFPLaTXJwCJccB` | 2026-05-26 | 112 karma | Axel Højmark, Jérémy Scheurer
- url: https://www.lesswrong.com/posts/7zGgFPLaTXJwCJccB/practical-learnings-from-synthetic-document-finetuning
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Apollo Research shares practical tweaks to the Slocum et al. SDF recipe: iterating on universe contexts, model-graded filtering, 'anti-universe' negative prompts to avoid mode collapse (e.g. 439k occurrences of one name), and changes such as dropping the DOCTAG to fix a 'saliency problem' where implanted facts are recalled under direct QA but do not affect downstream eval behaviour. Documents were generated mostly with Claude Sonnet 4.6.
- screener's follow-up note (often the screener's inference): Systematically ablate the saliency tweaks (DOCTAG vs none, document mixes) and measure direct recall vs downstream behavioural uptake of implanted beliefs on open models.
- builds on: Slocum et al. 2025 (Believe it or not: how deeply do LLMs believe implanted facts?); safety-research/false-facts repository

## You can graft SDF changes from base models onto post-trained models
- id: `NvtLJ5nawJ6akWEqH` | 2026-10-06 | 65 karma | dani roytburg, Peter Nutter, Clément Dumas, Shi
- url: https://www.lesswrong.com/posts/NvtLJ5nawJ6akWEqH/you-can-graft-sdf-changes-from-base-models-onto-post-trained
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Proposes 'grafting': run synthetic document fine-tuning on a pre-training (base) checkpoint and add the weight difference to the post-trained model. Validated for false facts, model organisms and constitutional midtraining on five model families up to 284B parameters: grafting damages coherence and capabilities less than native SDF, more closely resembles having the corpus in pretraining, one graft applies to several post-training checkpoints, and the benefit is specific to grafts trained on the base model.
- screener's follow-up note (often the screener's inference): Explain why base-model weight diffs transfer (relationship between base and chat models for belief installation), and test grafting on other interventions and smaller model pairs.
- builds on: Synthetic document fine-tuning (Marks et al., 2025; Wang et al., 2025); arXiv 2610.00767

