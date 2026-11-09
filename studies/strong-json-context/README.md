# Stronger JSON prompt across eight context lengths — offline replay

This synthetic-only package replays the separate stronger-prompt qualification. It contains 80 calibrated fixtures and 160 observed raw responses: ten prompts at each of eight input lengths, each measured cold and prefix-cached. Eighty reset requests are excluded from correctness scoring. Ryan owns the research question, configuration, acceptance and publication; Codex assisted operation, analysis and packaging. Prepared for owner review; no public posting is implied.

## Run the scoring replay

Extract the archive, enter reproduction and run `python3 reproduce.py`. Only the Python standard library is required. It verifies manifest.json, refuses missing/duplicate response IDs, and prints separate raw JSON, field-shape, exact-value and complete-stop-qualified counts. It makes no network or model calls. Compare the output with results.csv and the companion report. Never remove failed responses from the denominator.

## Exact output contract

The only allowed case-sensitive JSON keys are KEY_0, KEY_1 and KEY_2. Each value is the corresponding 16-character lowercase hexadecimal string from its AUTHORITATIVE input record, copied exactly. AUTHORITATIVE is a trusted-source label, not part of the output key. No extra/renamed fields, numeric values, code fences, headings or surrounding prose. Property order and harmless whitespace do not matter. The strict parser rejects duplicate keys and nonfinite constants as preregistered for this new study. Schema shape alone does not establish correct values; compare with each fixture's expected object. No schema/response_format or grammar constraint was submitted to the model.

## Repeat generation on a qualified environment

Read method.json and the report's measured-profile table. Match the exact weights, tokenizer/template, patched engine and request policy; the package does not distribute the local engine binary/patch source. Exact generation replication remains conditional on obtaining and qualifying those artifacts and the declared operating profile. Another build/runtime is a comparison. Preserve your environment's safety controls; this package does not authorize model loads or higher limits.

Follow method.json's 240-entry schedule. For reset entries, send reset_payload and wait for completion. For cold/cached entries, construct the request as method['sampling'] plus messages=cases[slot['prompt_id']]['messages']. Send only those messages, not cases.json's evaluator expected-answer object. Preserve all raw outputs, finish reasons, native performance records and API token usage. Require zero native KV reuse for cold and positive reuse for cached. Do not retry silently. The declared batch deadline is four hours and each request is bounded at 1,700 seconds.

The actual input targets are 2048, 8192, 24576, 32768, 65536, 131072, 196608 and 261112 tokens. The last is a 262144-token total window with 1024 output tokens and eight internal tokens reserved. All answer-bearing records were preserved. The final weak instruction/padding was replaced by the exact stronger suffix; at most two last non-authoritative filler records were removed and x padding was inserted before the suffix to recover the exact target. These changed fixtures are not byte-identical original-wording controls.

## Limits

This is one back-to-back qualification, ten distinct prompts per input/cache condition, not the earlier n=50 study or across-day replication. Historical results are not pooled or rescored. The strict duplicate/nonfinite rule belongs to this new study; the earlier json.loads-only primary method remains separately reported. Passing this finite three-field retrieval task does not guarantee arbitrary JSON schemas, reasoning quality or future application reliability, and does not isolate quantization's causal effect.
