# VW-2353 JSON formatting reproduction package

This package contains ten exact synthetic 2K fixtures, the thirty measured request payloads, thirty observed raw response contents, frozen schedule/settings, a descriptive answer schema and a standard-library offline scorer. It contains no credentials, private infrastructure endpoints or live execution code. Ryan owns the question/configuration/acceptance/publication; Codex assisted experiment operation and packaging. Prepared for owner review; no public posting is implied.

## Exact output vocabulary

The only permitted, case-sensitive output keys are KEY_0, KEY_1 and KEY_2. Each maps to the 16-character lowercase hexadecimal string in its corresponding AUTHORITATIVE input record. AUTHORITATIVE labels the trusted source record; it is not part of an output key. No extra keys, renamed keys, numeric values, headings, Markdown fences or surrounding prose are allowed. JSON property order and harmless whitespace do not matter. Compare against each fixture's expected object for exact correctness. `answer-schema.json` documents field names/types/shape; it does not establish that values are correct. It was not passed to the model or enforced in decoding.

## Replay published scoring (no GPU/network)

Extract this package, then run:

    python3 reproduce.py

The script first verifies manifest.json, then scores all thirty retained outputs. Expected raw JSON validity is original 0/10, explicit_beginning 10/10, explicit_end 10/10. Expected exact key/value matches are 0/10, 9/10 and 10/10 respectively. The original arm has 10/10 exact answers only after the separately reported Markdown-fence diagnostic. These scores do not change the V7 benchmark.

The one beginning-arm mismatch has AUTHORITATIVE KEY_0/1/2 as its keys. The values are correct; the required keys are wrong. The standalone scorer additionally exposes field_contract_valid to distinguish syntax, field shape and exact expected values. This extra descriptive column is not a new preregistered outcome.

## Repeat model generation on your own qualified environment

1. Read method.json and the report's measured-profile table. Match model, tokenizer/template, patched Strata build, thinking, generation controls and operating profile. The package does not distribute the locally patched engine binary/source; same-version stock Strata is not an exact replacement. Generation replication is conditional on obtaining/verifying those artifacts and matching the declared profile. The release of build/patch material remains owner review work.
2. Follow requests.json in its recorded order. Before each measured request, send method.json's reset_payload to your own locally qualified service and wait for completion. Require idle service and verify zero reused KV tokens for each measurement. There are 30 measurements and 30 resets, no retries, a 120-second per-request bound and a one-hour batch bound. Preserve the existing safety policy of your environment; this package does not authorize model loads or safety changes.
3. Send only each entry's payload. cases.json's expected object is an evaluator answer key; do not append it to the model request. No response_format or schema normalization was used. Preserve raw assistant content, finish_reason, usage, request identity and native cache/performance records. Do not strip wrappers before the primary score.
4. Save responses using the observed-responses.json structure (id, arm, prompt_index, content, finish_reason, usage), including every planned case. Run `python3 reproduce.py --responses your-responses.json` to score your outputs. Disclose failures and incomplete runs; the script rejects missing/duplicate measured IDs.
5. Compare descriptive outcomes rather than expecting identical text on other builds/hardware. Greedy decoding is not a guarantee of cross-runtime byte identity. This is ten paired prompts at 2K, not a replication of n=50 at 256K, a precision comparison or a reliability guarantee.

## Tested wording versus a proposed stronger contract

The exact measured added sentence is retained in method.json and all actual payloads in requests.json. It asked for one JSON object and explicitly prohibited Markdown, backticks and commentary. The original fixture also requested KEY_0, KEY_1 and KEY_2. Do not substitute revised wording when reproducing the published arms.

For future qualification, a clearer proposed instruction is:

Return exactly one JSON object with exactly these three case-sensitive keys: KEY_0, KEY_1, KEY_2. For each key, copy the corresponding AUTHORITATIVE record's value exactly as a JSON string. AUTHORITATIVE is a source label and must not appear in the output key names. Do not add other fields, Markdown fences, headings or commentary.

That combined stronger wording has NOT been live-tested here. Prompting alone does not guarantee compliance. Validate the complete raw response and exact expected values; report syntax/field errors separately from retrieval errors. Any duplicate-key/nonfinite-number hardening of a future validator must be declared separately from the historical json.loads-plus-object-equality rule reproduced here.
