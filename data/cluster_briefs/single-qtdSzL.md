# Cluster: In-context learning of representations can be explained by induction circuits

key: `single-qtdSzL` — 1 post(s); write at most 1 proposal(s).

## In-context learning of representations can be explained by induction circuits
- id: `qtdSzLpQ8BXv6YANd` | 2026-03-02 | 52 karma | Andy Arditi
- url: https://www.lesswrong.com/posts/qtdSzLpQ8BXv6YANd/in-context-learning-of-representations-can-be-explained-by
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Reproduces Park et al. 2025's in-context graph-tracing result on Llama-3.1-8B and argues induction circuits suffice to explain it. Zero-ablating top induction heads degrades accuracy (though learning continues with context), while ablating previous-token heads makes accuracy plateau and destroys the grid-like representation geometry; random-head ablations have little effect. Code released.
- screener's follow-up note (often the screener's inference): Test whether the induction-circuit account holds on other models/graph structures and on in-context tasks where bigram recall is insufficient.
- builds on: ICLR: In-Context Learning of Representations (Park et al., 2025); A Mathematical Framework for Transformer Circuits (Elhage et al., 2021); In-context Learning and Induction Heads (Olsson et al., 2022)

