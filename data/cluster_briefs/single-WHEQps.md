# Cluster: How does Fable 5.1 hide messages in images?

key: `single-WHEQps` — 1 post(s); write at most 1 proposal(s).

## How does Fable 5.1 hide messages in images?
- id: `WHEQps5PK8LrrcTAb` | 2026-10-21 | 93 karma | Nikita Kezin, 13ryanC, hronir, James Chua
- url: https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Prompts Claude Fable 5.1 (max reasoning) to hide each of 50 short messages in an SVG image, then asks a fresh instance to detect and decode the message from the rendered image with no shared scheme. The model converges on a few encoding families representing each letter as a visual element (33/50 use element height, e.g. skyline building heights), and fresh instances can often decode them using tools; a brief comparison with GPT-6 Astra is included. Code and prompts are on GitHub.
- screener's follow-up note (often the screener's inference): Test whether a monitor (weaker model or human) detects these messages, whether models can coordinate on harder-to-detect schemes when told a monitor is present, and repeat across models and modalities.
- builds on: -

