# Cluster: Defending Against Model Weight Exfiltration Through Inference Verification

key: `single-7i33FD` — 1 post(s); write at most 1 proposal(s).

## Defending Against Model Weight Exfiltration Through Inference Verification
- id: `7i33FDCfcRLJbPs6u` | 2025-12-15 | 121 karma | Roy Rinberg, Adam Karvonen, dreuter, Keri Warr
- url: https://www.lesswrong.com/posts/7i33FDCfcRLJbPs6u/defending-against-model-weight-exfiltration-through-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Paper proposing to verify inference outputs by regenerating with a fixed sampling seed: since LLM inference is nearly deterministic (>98% of tokens match), the entropy available for steganographic exfiltration through output tokens is small. They report limiting exfiltration to <0.5% of the output channel (~200x longer exfiltration timelines); the same check can catch inference bugs.
- screener's follow-up note (often the screener's inference): Measure verification match rates and residual steganographic capacity across hardware, batching and quantisation settings on open models, and red-team with adaptive steganography.
- builds on: Ryan Greenblatt's upload-limits proposal for preventing weight exfiltration

