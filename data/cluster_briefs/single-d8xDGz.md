# Cluster: A Mechanistic Explanation of Prompt Injection (and why you should study roles)

key: `single-d8xDGz` — 1 post(s); write at most 1 proposal(s).

## A Mechanistic Explanation of Prompt Injection (and why you should study roles)
- id: `d8xDGzCEYE639qqEv` | 2026-06-22 | 409 karma | charles_ye, Jasmine C.
- url: https://www.lesswrong.com/posts/d8xDGzCEYE639qqEv/a-mechanistic-explanation-of-prompt-injection-and-why-you
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): ICML paper arguing prompt injections work through how LLMs internally perceive roles (chat-template tags): linear 'role probes' trained on activations to predict which tag wraps each token show injected text being perceived as a different role. The theory yields new attacks such as CoT Forgery (raising jailbreak ASR from near zero to ~60% across tested LLMs), explains odd interp results and predicts when attacks work; a demo notebook is released and a 'science of roles' agenda is sketched.
- screener's follow-up note (often the screener's inference): Authors list unexplored role-science problems; e.g. use role probes as injection detectors, steer/patch role representations as a defence, and study how the <think> role is represented.
- builds on: -

