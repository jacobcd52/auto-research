# The pirate who keeps speaking Chinese: does a conceptor transplant personas more cleanly than hard subspaces or plain vector addition?
cluster: steering | stage-1 cost: $210 | follows up: A conceptor by any other name (9aZYJinAyxequjQbn)

## 1. What the prior work showed
Keenan Pepper's post introduces conceptors to LessWrong. Given concept activation vectors with correlation matrix
R, the conceptor C = R(R + a^-2 I)^-1 is a "soft projection": each principal direction with eigenvalue lambda is
kept with weight lambda/(lambda + a^-2), where the aperture a sets the noise level. The post contains no
experiments. Its motivating claim is about "persona transplantation" with the roughly 275 role vectors released
with Anthropic's Assistant Axis paper (one mean activation per role such as "pirate" or "accountant"). To move a
persona from a donor activation d into a recipient activation x, use x' = x + C(d - x). The post asserts that
doing this in the full 274-dimensional span of the role vectors is "a brutal butchery" because most of that span
is noise, that top-k PCA is better but has an arbitrary hard cutoff, and that the conceptor should transfer the
persona without the donor's topic, message length or language: the model should "act like a pirate but keep
speaking Chinese".

Existing conceptor-steering papers (arXiv 2410.16314, 2605.04980) build one conceptor per concept from contrastive
prompts and report gains over activation addition; they do not test this. A recent attribution study (arXiv 2610.16325) is a warning: for a
conceptor-complement suppression intervention, removing the fitted matrix while keeping the same centre and gain
changed little (the matrix correction was 0.093% to 7.8% of the displacement, with no consistent behavioural
benefit in 480 paired comparisons). So published conceptor wins may come from the shift, not the soft filter. No
paper I found applies a conceptor to the role vectors or measures donor-nuisance leakage (arXiv API and Hugging
Face checked; general web search was unavailable for this run). The role vectors are public for Gemma 2 27B,
Qwen 3 32B and Llama 3.3 70B at https://huggingface.co/datasets/lu-christina/assistant-axis-vectors (275 files per
model, all layers), with code at https://github.com/safety-research/assistant-axis.

## 2. Question and why it matters
**When a persona is transplanted from a donor context that differs in language, topic and length, does the
conceptor filter give a better trade-off between persona transfer and nuisance leakage than (i) hard subspaces of
matched size and (ii) simply adding the released role vector?**

Persona-space interventions (activation capping, persona vectors, role steering) are becoming a standard safety
tool. If the conceptor dominates, there is a concrete
recipe and a measured aperture to use. If a matched top-k projection or plain role-vector addition does as well,
that deflates the post's central claim and extends the "it is mostly gain" finding from suppression to
transplantation. Both outcomes settle an explicit claim nobody has tested.

## 3. Stage 1 plan
**Model and assets (reused).** Gemma 2 27B-it (`unsloth/gemma-2-27b-it` mirror) with the released
`gemma-2-27b/role_vectors/*.pt` and `default_vector.pt`; intervention at the paper's middle layer plus two
neighbours. Qwen 3 32B with its released vectors as a replication of the main comparison.

**Fitting.** Mean-centre the 275 role vectors at the layer; compute R; build conceptors at 8 apertures chosen to
give effective dimensions (trace of C) of about 1, 3, 10, 30, 60, 100, 150, 250.

**Donors and recipients (built, small).** 24 personas, 12 with a released role vector and 12 without (to test
generalisation beyond the fitting set). For each persona, donor activations d are the mean response-token
activation of that persona answering in a deliberately confounded context: one of 4 donor languages and 4 donor
topics, with long answers. Recipients: 60 neutral user questions spanning 4 other languages and 6 other topics,
answered by the default assistant. Donor and recipient never share language or topic, so leakage is detectable.

**Conditions (x' = x + M(d - x) at every response position).**
1. M = I (full replacement by the donor mean; maximum leakage reference).
2. M = hard projector onto the full role-vector span.
3. M = top-k PCA projector, k = 1, 3, 10, 30, 60, 100, 150, 250.
4. M = conceptor at the 8 matched apertures.
5. Whitened conceptor (noise covariance from generic chat activations; the post's footnote).
6. Plain addition of (role vector - default vector) at 8 strengths; only possible for the 12 in-set personas.
7. Attribution controls: the conceptor's spectrum on random orthonormal directions; the conceptor's eigenvectors
   with its soft weights replaced by a constant of equal trace.
8. Prompted persona (system prompt) as a non-activation ceiling, and no intervention as the floor.

About 24 personas x 60 recipients x 45 settings is 65k generations of 120 tokens on the main model; the Qwen
replication runs conditions 1 to 4 and 6 at 4 sizes each (about 25k).

**Metrics (LLM judge plus automatic).**
- *Persona transfer*: judge score 0 to 100 that the answer is written by the named persona; and a blind
  24-way persona identification accuracy.
- *Leakage*: language of the answer (automatic language ID; must match the recipient prompt, not the donor);
  donor-topic intrusion (judge); length ratio to the unsteered answer.
- *Collateral damage*: whether the answer still addresses the question correctly (judge, against the unsteered
  answer) and coherence.
- Judge: `anthropic/claude-haiku-5.5`, with 300 items double-scored by `anthropic/claude-sonnet-5.5` and a
  hand-read sample to validate.

**Key analysis.** For each method, the Pareto frontier of persona transfer against a combined
leakage-and-damage score as its size parameter varies; area under the frontier with bootstrap intervals over
personas and prompts. Paired comparison of conceptor against top-k at matched effective dimension. The attribution
controls say whether any advantage comes from the role-vector directions, the soft weights, or neither. Separate
results for in-set and held-out personas.

**Order.** (1) Load vectors; reproduce an Assistant Axis steering example to verify the layer convention.
(2) Build donors and recipients; pilot 3 personas. (3) Validate the judge. (4) Full Gemma run. (5) Qwen
replication. (6) Analysis.

## 4. Stage 1 cost estimate
- Generation: 65k + 25k generations x about 120 new tokens, batched on one 80 GB GPU. Estimated 30 GPU-hours
  including donor extraction; pilots and reruns 15 h. RunPod H100 PCIe secure at $2.89/h (price page checked
  today): 45 h = $130.
- Judging: 90k answers x 3 judgments x about 500 input / 40 output tokens with `anthropic/claude-haiku-5.5`
  ($0.10 / $0.50 per M on OpenRouter) = about $19. Sonnet 5.5 validation and dataset writing ($2 / $10 per M):
  about $10.
- Storage and idle time: $15. Margin: $36.
- **Total: about $210.**

## 5. What success looks like
- *Conceptor wins*: at matched effective dimension the conceptor frontier lies above top-k PCA and above the full
  span on both models, the pirate keeps speaking Chinese (recipient-language retention above 90% at persona
  transfer levels where full-span transplant falls well below that), and the constant-weight control loses the
  advantage. Deliverable: a recommended aperture and a short recipe.
- *Soft filter is irrelevant*: conceptor and top-k frontiers overlap within intervals, or role-vector addition
  matches both. That is a clean negative on the post's claim and generalises the "complement is gain" result.
- *Subspace matters, softness does not*: both role-subspace methods beat random-direction controls and full
  replacement, with no soft-versus-hard difference. Still useful: it validates the persona subspace as a
  transplant target.

All three are publishable with the same plots. The uninformative outcome is every method failing to transfer
personas without destroying coherence; the pilot checks this first.

## 6. Stage 2 (if stage 1 succeeds)
Boolean conceptor algebra (persona AND NOT language), a conceptor-based alternative to activation capping on the
Assistant Axis persona-jailbreak setting, the same comparison for emotion-concept vectors, and Llama 3.3 70B.
Roughly $800 to $1,200.

## 7. Risks and how the plan handles them
- *Single-layer transplant is too weak or too destructive.* Three layers and a multi-layer variant in the pilot;
  the prompted-persona ceiling and full-replacement reference bound what is achievable.
- *Only 275 fitting points in a 4,608-dimensional space.* This is the post's own setting; the held-out persona
  split measures whether the fitted subspace generalises, and the random-direction control shows whether it is
  better than chance.
- *Judge bias toward surface markers ("arr").* Blind 24-way identification, a validated subset, and personas
  chosen to include subtle ones (auditor, mediator) as well as caricatures.
- *Unfair tuning.* Every method gets the same number of settings and is compared as a whole frontier.
- *Vector-format or layer-indexing mistakes.* Step 1 reproduces a known steering effect from the released axis
  before anything else is run.
