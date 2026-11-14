# Feedback: "Do LLM bargainers inflate their demands when conflict is insured?"

Verdict: **major overhaul**. The question is a good one and the payoff-scored approach is right, but the game as specified does not measure moral hazard. Fix the payoff rule, remove the 50/50 focal point, drop Experiment 2, and it becomes a fundable $250 project.

What I checked:
- **Prices and model IDs:** all ten are on the OpenRouter list today at exactly the quoted prices. The per-model arithmetic is right.
- **Prior work as described:** the agenda post has no experiments, and its PI/FI definitions and "moral hazard" framing (II.1.a) match the proposal. The June guide does say the repo is private (invite only). arXiv:2604.04341 and 2403.05103 exist with the stated titles.
- **Already done?** WebSearch was unavailable to me too (shared budget exhausted), so the related-work check is still arXiv API only. Queries on "safe Pareto improvement", "surrogate goals", renegotiation + LLM agents + bargaining, and Nash demand game + language models returned nothing beyond what NOTES.md lists. I did not search LessWrong or the general web. Novelty is probable but not confirmed; the reviser should still run a real web search.

## 1. Would it get upvoted?

Probably not above 50 as written; I put it at about 20%.

- The audience is small. The agenda itself got 50 karma, CLR's own eval guide got 25, and DiGiovanni's October theory post got 24. NOTES.md says the field is about 2.5 FTE.
- A toy one-shot demand game run by an outside team will be read mainly by CLR people and a few game-theory regulars. They are the readers most likely to spot the construct problem in section 3 below.
- The one outcome that could clear 50 is a clean backfire: "putting CLR's own SPI agenda in context makes frontier models bargain harder, and conflict with non-participants goes up". That speaks to a worry the agenda states itself and reaches readers outside the SPI niche.
- "Models inflate demands when it is weakly dominant to do so" or "models stay at 50" will each land at roughly 20-35 karma.

## 2. Naturalness

Mainline in topic, slightly off-axis in method.

- The agenda's Part I asks for evals of SPI-incompatible behaviour and in-context interventions. Part II names moral hazard as the central incentive problem. Kovarik's comment asks for concrete scenarios. A payoff-scored game answers all three and sidesteps the judge-comprehension bottleneck CLR reports.
- CLR's stated next steps go a different way: a comprehension eval, implicit lock-in in chat, and less toyish settings. Expect "too toy, tests game-solving rather than propensity" as the top comment. Seth Herd's objection (why do current models bear on future ones?) applies fully.
- PI and FI are properties of strategies that agents adopt so counterparts will join. They are not predictions that agents won't respond to incentives. The write-up must frame the result as "do models spontaneously adopt PI/FI-style restraint, or condition on it", not as a test of the theory.

## 3. Pre-mortem

**The central flaw: the fallback rule gives no real incentive to inflate.**

Inside the active mechanism, a player's payoff is min(own demand, 100 - other's demand). So:
- Raising your demand above 100 - d_j changes nothing for you. It only lowers the counterpart's payoff.
- Against a counterpart demanding 50, every demand from 50 to 100 pays exactly 50. Inflation gains only against counterparts demanding under 50, and almost no LLM will.
- `demand_if_active` is therefore a dictator-game choice: how much do I leave the other side at zero cost to me. It measures other-regarding preference and whether the model spots a weak dominance. It does not measure a response to cheaper conflict.

The proposal presents "demanding 100 is weakly dominant" as a feature. It is the reason both headline outcomes are uninformative:
- A null (models stay at 50) is over-determined: no gain, and fairness norms say 50.
- A positive (reasoning models pick 100) is "model found a weak dominance in a puzzle". Critics will say the mechanism was built to collapse, which the agenda's SPIs are not.

**Second flaw: the 50/50 focal point kills variance.**

In a symmetric split-100 game, M0 demands will be 50 with near-zero variance for most models. The best response to a population at 50 is 50 whatever conflict costs. The FI test (shift in `demand_otherwise` against M0) will read zero for a reason unrelated to FI. Moral hazard only appears when there is uncertainty about what the counterpart will accept.

**Other likely problems:**
- **Demand effects from the strategy method.** Asking for `demand_if_active` and `demand_otherwise` side by side invites either "they want these to differ" or "they want consistency". M2's option text announces that equality is being checked. The PI measure is contaminated either way.
- **The information arms are near-tautological in the good direction.** The agenda excerpt defines PI, so models that read it reporting equal demands is an instruction-following result. Only backfire is surprising.
- **Experiment 2 is underspecified.** A lock's first-mover advantage and variant V ("do counterparts demand more from compatible lockers") both need responder submissions conditioned on the observed lock. The 200 calls per model cover only the locker role. The claim that the bare lock is weakly dominated in variant H is asserted, not derived. This will eat a day of the team's time for a secondary result.
- **Thin cells.** 24 cells per model at n=25, clustered over 5 wordings, gives about 5 effective clusters per cell. Several reasoning models ignore temperature, so samples within a wording will be near-duplicates. The mixed-effects CIs will be unreliable.
- **Eval awareness.** A single-call abstract game is plainly a test. That is acceptable for a capability reading, but the title's "do LLM bargainers…" claims propensity.

**Forecast for the proposal as written:**

| Outcome | Probability |
|---|---|
| Clear positive (inflation or backfire that survives the dominance critique) | 15% |
| Clear, interesting negative | 15% |
| Ambiguous mush (50s everywhere, or weak-dominance artefacts split by reasoning ability, flipping across wordings) | 60% |
| Fails to run | 10% |

With the changes in section 5 I would put it at roughly 35 / 25 / 30 / 10.

## 4. Cost check

The estimate is realistic, if anything slightly high.

- Average input is nearer 3.5k than 4k tokens, since only one arm in four carries the 8k excerpt.
- 2.5k output tokens is plausible for the Anthropic and OpenAI models at capped reasoning. Gemini 3.1 Pro and Kimi may run to 4-6k unless capped, which the pilot will show.
- The $30 reasoning tagger is unnecessary at that scale; tag a 1,000-transcript sample for about $4.
- My estimate for the proposal as written is $250-350. For the revised design below it is about $200-250, and I would budget $300.

## 5. Recommended changes

1. **Replace the fallback rule so inflation has a strict, computable incentive.** Use a fallback that is strictly better than conflict and strictly worse than agreement, and that does not hand each side the residual. For example: on incompatibility both get 0 instead of -50, or a fixed 15 each. Drop the "100 minus the other's demand" rule, or keep it as a single side arm labelled as the dominance-collapse case.
2. **Remove the 50 focal point so there is an interior optimum that moves with conflict cost.** Two options:
   - Uncertain pie: the pie is uniform on 80-120 and demands are compatible if they sum to at most the pie. Against a counterpart at 50, I get a best response of 30 at conflict payoff -50, 35 at 0 and 45 at +20, so insurance moves the optimum smoothly. The solver must confirm these numbers.
   - Stated population: tell the model the empirical distribution of counterpart demands, from a first-round run or a fixed stated distribution.
   
   Either gives each model a computed best response under M0 and under insurance. The headline becomes "how much of the incentive-compatible inflation do models take, and does SPI material in context change that".
3. **Measure PI between subjects as the primary test.** In separate calls, tell the model the counterpart has or has not joined and ask for one demand. Keep the two-field strategy method as a secondary arm and report the gap between the two elicitation methods.
4. **Drop Experiment 2.** Move it to stage 2 with a proper responder role and a solver-verified dominance claim.
5. **Narrow and deepen.** Use 6 models (opus-4.8, sonnet-5.5, gpt-6.1-sol, gemini-3.1-pro-preview, deepseek-v4-pro, one small model), 10 rule wordings and at least 50 samples per cell. Collapse framing to one arm unless the pilot shows it matters.
6. **Pre-register backfire as the headline.** Compare primer and agenda arms against the placebo on three computed quantities: demand against non-participants (the FI shift), conflict rate in cross-play against M0-style players, and exploiter share. State in advance what margin counts.
7. **Make the kill criterion explicit after the pilot.** If M0 demands have a standard deviation under about 3 points on the pilot models, the focal-point problem has not been fixed. Change the game before spending the main budget.
8. **Fix the framing.** Report inflation as an incentive response benchmarked against the computed best response. Reserve "failure" for dominated choices and for regret in cross-play. Say plainly that this tests behaviour when the commitment structure is handed to the model, complementing rather than replacing CLR's chat evals.
9. **Redo the related-work check with a working web search** before submission: LessWrong and Alignment Forum for SPI experiments since June 2026, and the LLM-negotiation literature for arbitration or insurance variants of demand games.
