# Strata on a 16 GiB RTX 4080 through a 256K context window

**Release 1.0.1 · 10 November 2026.** This documentation update improves readability. The measurements and scoring are unchanged from release 1.0.0.

[Research article](https://rduffy.uk/research/benchmarking/strata-memory-pools/) · [Benchmark report](https://rduffy.uk/benchmarks/strata/) · [GitHub releases](https://github.com/rduffyuk/strata-context-benchmark/releases)

This benchmark describes one configured local Strata deployment. It measures retrieval, prefill, prefix reuse, decode speed and output formatting. It does not establish performance for every Strata configuration, prove that quantization caused a formatting failure, or demonstrate indefinite autonomous-agent reliability.

## Reproduce the reported results

Use Python 3.10 or later:

```sh
python3 reproduce_all.py
```

This replays the recorded results offline. It needs no third-party Python packages, network access, model download or GPU, and it does not start an inference server.

The replay first checks the root manifest, then runs the three study scorers. Each study also verifies its own evidence manifest. Git metadata and signed provenance sidecars are excluded from the package file list; arbitrary extra files and changes to the evidence are rejected. Do not disable these checks to obtain a pass.

Hashes establish agreement with the released files. Compare the archive checksum with the published release record to check its origin. These checks are not independent scientific validation.

## What was tested

The package contains three separate datasets:

| Dataset | Method | Recorded result |
|---|---|---|
| `studies/v7` | Ten prompts repeated across five consecutive sessions, at eight input lengths, in cold and cached conditions. Each context/cache condition has 50 observations. A separate sustained-output test has 50 samples. | 1,375 calls in total, including 850 measurements. Strict raw JSON: 0/800. After separately labelled, posthoc fence removal: 800/800 exact values. The replay checks 136 metric summaries. |
| `studies/json-wording-2k` | Ten prompts tested with three instruction variants at 2K context: 30 measured responses. | Bare JSON syntax passed 0/10, 10/10 and 10/10. Exact keys and values passed 0/10, 9/10 and 10/10. |
| `studies/strong-json-context` | Ten prompts at eight input lengths, in cold and cached conditions, in one pass: 160 measured responses. | 160/160 responses passed exact raw JSON and complete-stop checks. This is a separate follow-up, not another n=50 study. |

### Decode speed

V7's separate sustained-output test used **50 input tokens and 1,024 actual output tokens per sample**. Across 50 samples, the median decode speed was **41.614 tokens per second**.

This was a short-context test. It does **not** measure long-output generation at 256K context.

### Context window and duration

Both full-context datasets reached **261,112 input tokens**. Their configured window reserved another **1,024 output tokens** and **8 internal tokens**, for a total of **262,144 tokens**. The short retrieval answers did not necessarily consume the full output reservation.

The five consecutive V7 sessions took **6 hours, 41 minutes and 22 seconds**. The stronger-prompt follow-up took **1 hour, 3 minutes and 51 seconds**.

These runs do not establish repeatability across different days or indefinite availability. Failed earlier campaigns are excluded from these datasets.

## What is included

- Each study includes its exact synthetic prompts, evaluator answers, raw responses, settings, schedule and scoring rules. V7 stores repeated messages once while retaining all 1,375 call identities and native performance observations, including excluded calls.
- `results/` and `figures/` contain the reported tables and charts.
- `environment.json` records the model revision, file and tokenizer fingerprints, engine binary, deployment profile and safety limits.
- `source/patches/` contains the two ordered local engine patches against the pinned upstream revision, along with the upstream MIT notice and source/hash comparisons.
- `source-disclosure.md`, `licence-review.md` and `NOTICE.md` explain the software, model, content and generated-output boundaries.

No model weights, model packs, expert-profile binary, NVIDIA/CUDA binaries, unlock code or firmware, credentials, private operational logs or live-serving harness are included.

The original per-study READMEs describe what their earlier standalone packages contained. This consolidated release additionally includes the engine patches at the top level. Fresh generation still requires the appropriate model pack, selected expert profile, wrapper/instrumentation and a qualified build.

## Run a new generation experiment

Replaying recorded scores is different from generating new responses. Start with `source-disclosure.md` and the study's method and fixture records.

Match the recorded model inputs, template, tokenizer, patched engine and deployment profile. Supply only the request messages; never append the evaluator's expected answers. Retain failures and raw responses, and verify the input-token, output-token and KV-reuse counters independently.

Do not silently retry requests, normalize primary responses or combine separate datasets. Keep your environment's hard safety checks and numeric limits intact. A fresh build from the same source is not automatically identical to the executable measured here; disclose any differences.

## Licences, references and attribution

Original code is licensed under **MIT**. The authored report, research article, original data and figures use **CC BY 4.0**. Third-party materials and generated-output rights remain separate; see `LICENSE-CODE.txt`, `LICENSE-CONTENT.md` and `NOTICE.md`.

The quantized model card's Apache metadata conflicts with its stated inheritance of the base Qwen Community licence. This package does not redistribute the weights or grant broader model or commercial-use clearance. See `licence-review.md`.

`REFERENCES.md` and `REFERENCES.bib` credit the pinned Strata and model revisions, GSQ/RCO papers, toolchain, plotting tools and mechanism references. `CITATION.cff` explains how to cite this benchmark; it does not replace upstream attribution.

Ryan Duffy led research design, configuration, acceptance criteria and operational verification. Codex agents assisted implementation, testing, experiment operation, analysis and packaging.

## Research article and memory explanation

The [research article](https://rduffy.uk/research/benchmarking/strata-memory-pools/) explains sparse experts, GPU/RAM/SSD placement, KV state and the measured configuration. Its source is `article/article.md`; the result charts are in `figures/`.

The interactive explainer's source is in `article/memory-matrices-v4/widget/`. Its activity is illustrative, not a recorded routing trace or performance timing. Optional visual checks:

```sh
node article/memory-matrices-v4/widget/test.cjs
```

To verify the retained RAM reanalysis:

```sh
python3 article/memory-matrices-v4/reproduce_ram.py
```

This checks 50,857 observations of cgroup-charged memory, including file cache. It is not process RSS or a count of independent prompts. The maximum sampled charge was **34.0048 GiB**; **38 GiB** was the configured ceiling.

The selected anime illustrations were generated with OpenAI's image tool and reviewed by Ryan. They provide conceptual context, not measured routing evidence. Internal review variants and private host paths are excluded.
