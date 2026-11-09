# Strata on a 16 GiB RTX 4080 through a 256K window

**Release 1.0.0 · 9 November 2026.**

[Research article](https://rduffy.uk/research/benchmarking/strata-memory-pools/) · [Benchmark report](https://rduffy.uk/benchmarks/strata/) · [GitHub](https://github.com/rduffyuk/strata-context-benchmark) This package characterizes one configured local deployment. It is not an official Strata score, an unmodified engine comparison, proof of a quantization defect or a continuously reliable autonomous agent.

## Replay all published scores and timings

Use Python3.10 or later. No third-party packages, network, model download or GPU are needed:

```sh
python3 reproduce_all.py
```

The root manifest is checked before the three fixed offline replay programs run. Each study also checks its own evidence manifest. Do not disable verification to obtain a pass. Hashes demonstrate agreement with the reviewed bytes; compare the release/archive digest with a trusted owner-approved publication record for origin, and do not mistake these checks for independent third-party validation.

| Separate dataset | Scope | Reproduced finding |
|---|---|---|
| `studies/v7` | Ten prompts × five consecutive sessions; eight input lengths, cold/cached;50observations/condition plus50sustained outputs | All1375calls/850measurements; strict rawJSON0/800; fence-only posthoc800/800;136metric summaries checked |
| `studies/json-wording-2k` | Ten prompts × three instruction arms at2K;30measured responses | BareJSON0/10,10/10,10/10; exact keys/values0/10,9/10,10/10 |
| `studies/strong-json-context` | Ten prompts × eight lengths × cold/cached in one pass;160measured responses | Raw exactJSON and complete-stop160/160; not a newn50 dataset |

V7's separate sustained test used50inputtokens and1024actualoutputtokens per sample: median41.614tokens/s. This is not long-output generation at256K. The maximum input in both full-context datasets is261112tokens, with1024outputtokens and8internal tokens reserved inside the262144total window. Five consecutive V7 sessions lasted6h41m22s; the stronger-prompt pass lasted1h03m51s. No claims of across-day replication or indefinite availability are made. Failed historical campaigns are not pooled into these results.

## Package contents

- Each study contains exact synthetic messages, evaluator answers, raw observed responses, settings/schedule and its original scoring semantics. V7 deduplicates repeated messages but retains all1375call identities and native performance observations, including excluded calls.
- `results/` and `figures/` contain the reported tables and selected figures.
- `environment.json` records the fixed deployment profile, model revision/file pins, native binary, tokenizer/template hashes and safety envelope.
- `source/patches/` supplies the two ordered local engine patches against the exact upstream revision, with upstream MIT notice and source/hash comparisons.
- `source-disclosure.md`, `licence-review.md` and `NOTICE.md` separate software, weights, authored content and model outputs. Weights, model packs, expert-profile binary, driver/CUDA binaries, unlock code/firmware, credentials, private operational logs and a live-serving harness are excluded.

The stand-alone per-study packages retain historical README statements that their original distributions did not include engine source. In this consolidation the local patches are supplied at top level. That does not remove the remaining model-pack, selected expert-profile, wrapper/instrumentation and fresh-build qualification requirements.

## Repeat generation

Offline score replay is complete; fresh generation is a separate environmental replication. Read `source-disclosure.md`, then the relevant study method and exact fixture records. Obtain the legally permitted model inputs, match the recorded template/tokenizer, patched engine and profile, use only the supplied request messages (never append evaluator expected answers), retain every failure/raw output and independently verify native/API input, output and KV-reuse counters. Do not retry silently, normalize primary responses or mix datasets. Keep your environment's hard safety checks and numeric limits intact.

No turnkey GPU/server launcher is included and this command does not start or contact one. A fresh same-source build or a stock engine is not automatically byte-identical to the measured executable. Differences must be disclosed.

## Licences and attribution

Ryan approved MIT for original code and CC BY 4.0 for the authored report, research article, original data and figures. Third-party materials and generated-output rights are handled separately. Publication authorized by Ryan Duffy on 9 November 2026. The model card's Apache tag does not override its stated inherited Qwen Community licence. See the licence review before making model or commercial-use claims.

Ryan Duffy owns research design, configuration, acceptance criteria and operational verification. Codex agents assisted implementation, tests, operation, analysis and packaging. See `CITATION.cff`; no DOI or future GitHub URL has been invented.

## Upstream references

See `REFERENCES.md` and `REFERENCES.bib` for the exact Strata/model revisions, GSQ/RCO papers, toolchain and plotting credits. `CITATION.cff` describes this benchmark; it does not replace upstream attribution.

## Research article and memory explanation

The accompanying [research article](https://rduffy.uk/research/benchmarking/strata-memory-pools/) explains sparse experts, the three memory pools, KV state and the configured deployment. Its source is `article/article.md`. Original SVG result charts remain under `figures/`.

The current compact explainer is in `article/memory-matrices-v4/widget/`. Optional visual checks: `node article/memory-matrices-v4/widget/test.cjs`. Its activity is illustrative, not recorded routing or performance timing. `memory-facts.json` and `evidence/` distinguish startup GPU allocations, sampled cgroup RAM and model backing.

Optional RAM reanalysis: `python3 article/memory-matrices-v4/reproduce_ram.py`. This verifies 50,857 retained observations including file cache, not process RSS or independent prompt counts. Maximum sampled charge was 34.0048 GiB; 38 GiB was the configured ceiling.

The two selected anime illustrations are conceptual artwork generated with OpenAI's image tool and reviewed by Ryan. They depict no measured routing trace. The public package includes selected artwork only; internal review variants and host paths are excluded.
