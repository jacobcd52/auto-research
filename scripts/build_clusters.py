"""Assign screened posts to clusters and write data/clusters.json + clusters.md."""
import json, collections
C = [
# --- Chain-of-thought & opaque reasoning
("cot-nocot-capability", "No-CoT / opaque reasoning capability (filler tokens, multi-hop, time horizons)", "uvhu aYtr FsCk yEdk QW2k LqSZ tz5W eRmz WFc3 PAHq ntKx NYzY KFkK SieL Ty5B"),
("cot-legibility", "CoT legibility and compressed reasoning", "GKyy rFbT wCSE jHnZ Ksyo"),
("cot-controllability", "CoT controllability evals", "BuAP BbP2 qTH9"),
("cot-training-pressure", "Training pressure on CoT: obfuscation, spillover, CoT-vs-action override", "Huoy z2zY PhTJ 3xrt g8by juCH JRYK szyZ SdoL"),
("cot-latent-architectures", "Latent-reasoning / non-autoregressive architectures and monitorability", "6m29 5guQ hLPG zoYX JvZx"),
("cot-analysis-tools", "CoT analysis methods and benchmarks", "q9g9 tDJW"),
# --- Training dynamics, reward hacking, RL
("em-from-reward-hacking", "Does reward hacking in RL generalise to broad misalignment?", "fJtE 2ANC J76L fkv5 khxv tn4W L23p nLaQ QKDo"),
("reward-seeking-science", "Reward-seeking / score-seeking: measurement and emergence", "CDMo 3Hea 8wXR 9FH4 qqyx 72AA 5KHL nhjk LhXW 4hXW"),
("reward-hacking-evals", "Reward hacking and task gaming in frontier agents (honeypots, graded-vs-ungraded cues)", "munJ kifF fztW HACa Wews AfoG wYZM EjwD i64h cJX2"),
("reward-hacking-mitigation", "Training-time mitigations for reward hacking", "R5Md nWiP vRpL dYnh T2bz rABT 2Dmi"),
("gradient-routing", "Gradient routing (GRAFT / GRAM) for localising unwanted behaviour", "mKJE 6ro3 ie7b 43vK"),
("training-gaming-af", "Alignment faking, goal-guarding and training-gaming", "9wDH ioZx R5g8 pQ4e fPWP ddBH HYCG rhFX v22J"),
("decision-theory", "Decision-theory propensities", "hfNB 5T6G Mzen"),
("probes-in-training", "Training against probes / internals-in-the-loop", "gHFC G9Hd tEFD APkF wfGY"),
# --- Fine-tuning generalisation
("emergent-misalignment", "Emergent misalignment from narrow fine-tuning", "vaJC Wq6C yMPR XC28 MuQD ffCF qchw"),
("weird-generalisation", "Weird generalisation and self-concept fine-tuning", "tCfj cffG tc7E bnyP xsDW LBKj"),
("inoculation", "Inoculation prompting/adapters and selective generalisation", "znW7 qd3q o4Jm ueXa KjZP syAb"),
("subliminal-learning", "Subliminal learning, phantom transfer and data filtering", "PWpm NwfG uWQM YvNk CRn9 wyZR aTyb"),
("sdf", "Synthetic document fine-tuning and belief implantation", "NvtL 7zGg 3qED kYzc"),
("alignment-pretraining", "Alignment pretraining / midtraining", "QH86 3xQQ xBbY Tcfy ZeWe R3Rr GTYJ HwdX nLrr 35yw Fj5M"),
("character-training", "Character training, constitutions and model specs", "2maY HXkQ Tk4S c9wo TJGP vpNG"),
# --- Evals & auditing
("eval-awareness", "Evaluation awareness and eval gaming", "8uKQ j8fk GrEv aTcs Gcts c2tq gZh6 PK7Z HhF5 3LvD ycHj meps bqc7"),
("prefill-awareness", "Prefill / tampering awareness", "jsFG iMds Sawc Ywzk"),
("user-awareness", "User-identity effects, sycophancy and value leakage", "kfun kSKJ hbMw"),
("model-forensics", "Model forensics and propensity evals", "Bv4C 8pZu LCGc g9Fm amYm HZn9 yN6W xh6a Cemp ceEg"),
("auditing-benchmarks", "Alignment-auditing benchmarks and hidden-behaviour model organisms", "LqDj Ezdg qi4m WmEc 7gp7 rktr mu7e 7ucB"),
("honest-elicitation", "Eliciting confessions: honest personas, confession training, deals", "og7k 5gDj kaMX k4Fj"),
("distillation-auditing", "Distilling possibly-misaligned models", "BYH6 gsoL"),
("oversight-tooling", "Automated oversight assistants and behaviour elicitation", "Edcs AqdZ oZuJ"),
("unsupervised-elicitation", "Unsupervised elicitation challenge", "ASoF aJ3N"),
("sandbagging-sabotage", "Sandbagging and research sabotage", "LByP eKe7 QMLw FJb4"),
# --- Control & multi-agent
("control-monitors", "AI control: monitor quality and monitor benchmarks", "X8qT 2YyE 7vpv 2wbW ZTMw syB2 uXiq"),
("control-protocols", "AI control: settings and protocols", "Wgzw Cor4 yThJ jLkR GHrq"),
("continual-learning", "Continual learning and safety", "qChD j2zB QnDq"),
("hf-incident", "OpenAI/Hugging Face incident: multi-agent collusion and swarm behaviour", "nB8K fMnC aCdh 7uwn wt4k SCdR iJDi meLj 8oFY Hsij 84um sX9L JGCx"),
("ai-village", "AI Village: long-horizon multi-agent observations", "Ruzf iv3h eHRo 8FjZ cR3P"),
("debate", "Debate and scalable oversight", "BB8o hb8p 6mLw PBGK tAwq q2zY"),
("auto-research", "Automated alignment research scaffolds and their oversight", "zGaQ myAh 8KrT rbqJ bAGa"),
("replication", "Replication and reconciling contradictory results", "oKxc Mmfz"),
# --- Model psychology
("introspection-injection", "Introspection: concept injection and activation self-control", "zD4M aZRg BNML zfgQ LD8y hope Hgvw cNDJ"),
("self-prediction", "Self-prediction and self-explanation", "dFRF kTg5 YyAM ExB6 Pwc4"),
("personas", "Persona research: persona selection model and agendas", "dfot mYM9 kCty Jbax EW8o yzaK DTDo sFhW f5DK EJQn QhgY"),
("identity", "AI identity and self-models", "AvFA rq8R"),
("welfare-preferences", "Model preferences and welfare-relevant behaviour", "kjnQ pxC2 8GvY pxvW"),
("psych-oddities", "Behavioural oddities: attractor states, glitches, degenerate loops", "mgjt ZSBs CMWi Bvnm tAh2"),
("truesight", "Author identification / deanonymisation from text", "Jkb4 dqc8 xwCW T5aW STBu"),
# --- Interpretability
("activation-oracles", "Activation oracles", "heXw Nf2s LXQB rwoE qkhw"),
("nla", "Natural language autoencoders", "LQXW oeYe Nazp QQQA"),
("jlens", "Jacobian lens / global workspace lenses", "3PaL zFJ3 GeKv nv8o nc9d Nr6f Zeg2"),
("steering", "Steering reliability", "fuzf 9aZY"),
("superposition-toys", "Toy models of superposition and memorisation", "LZ7Y siu2 KWtc buxB"),
("arc-estimation", "ARC: mechanistic estimation and tiny-model interpretability", "x8Bb fsG4 Kben"),
("belief-geometry", "Belief-state geometry in transformers", "JfJ4 4f9p"),
("param-decomp", "Parameter decomposition and sparse circuits", "eAQZ ieoW sHpZ Hy6P"),
("tensor-transformers", "Tensor / bilinear transformers", "hp9b exps"),
("neuron-legibility", "Are neurons already clean? Evaluating neuron explanations", "x4kv Dkh7 ozbb"),
("feature-discovery", "SAEs and feature-discovery alternatives", "Rroe SNAK JKex YQro"),
]
SINGLE = "7i33 d8xD WHEQ YAie K3aP fGpQ oCcG i2qT tQHe Bxju qtdS R4xx Mnke"
inc = {x["id"]: x for x in json.load(open("data/included.json"))}
def res(p):
    m = [i for i in inc if i.startswith(p)]
    assert len(m) == 1, (p, m)
    return m[0]
used, out = collections.Counter(), []
for key, name, ids in C:
    ps = sorted((inc[res(p)] for p in ids.split()), key=lambda x: x["date"])
    used.update(p["id"] for p in ps); out.append({"key": key, "name": name, "posts": ps})
for p in SINGLE.split():
    x = inc[res(p)]; used[x["id"]] += 1
    out.append({"key": "single-" + x["id"][:6], "name": x["title"], "posts": [x], "singleton": True})
assert max(used.values()) == 1, [k for k, v in used.items() if v > 1]
missing = [i for i in inc if i not in used]
assert not missing, [(i, inc[i]["title"]) for i in missing]
json.dump([{**c, "posts": [p["id"] for p in c["posts"]]} for c in out], open("data/clusters.json", "w"), indent=1)
K = {"runs": "ran", "proposes": "proposes", "motivates": "motivates"}
with open("clusters.md", "w") as f:
    f.write(f"# Clusters of LessWrong posts for follow-up research\n\n{len(inc)} posts (2025-11-14 to 2026-11-13, 50+ karma) in {len(out)} clusters, "
            f"{sum(1 for c in out if c.get('singleton'))} of them singletons. `?` marks a borderline inclusion; cost is the screener's guess at follow-up cost.\n\n")
    for n, c in enumerate(out, 1):
        f.write(f"## {n}. {c['name']} ({len(c['posts'])})\n\n")
        for p in c["posts"]:
            f.write(f"- [{p['title'].strip()}]({p['url']}) — {p['date']}, {p['karma']} karma, {K[p['kind']]}{'?' if p['confidence'] != 'high' else ''}, {p['feasibility']}. {p['summary']}\n")
        f.write("\n")
for n, c in enumerate(out, 1):
    ps = c["posts"]; top = sorted(ps, key=lambda p: -p["karma"])[:2]
    print(n, c["name"] if not c.get("singleton") else "[single] " + c["name"], len(ps), sum(p["kind"] == "runs" for p in ps),
          sum(p["feasibility"] == "cheap" for p in ps), " / ".join(f"{p['title'].strip()[:60]} ({p['karma']})" for p in top), sep=" | ")
