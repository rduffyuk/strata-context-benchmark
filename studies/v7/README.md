# V7 offline evidence replay

Run `python3 reproduce.py` with Python 3. The replay is offline and uses only the standard library. It validates the manifest and call schedule, checks the native and API counters and completion, scores the 800 context responses, and compares 136 metric groups with the recorded summary. It prints a JSON result and exits nonzero on inconsistency. It does not run inference or establish independent model performance.

The included prompts are synthetic. Message bodies are stored once by SHA-256; `cases.json` holds expected answers separately from request messages. `calls.json` retains responses, native performance lines, API usage, request settings, relative durations, and numerical I/O deltas for all 1,375 calls. Source hashes disclose the retained source evidence without distributing the private archive. They identify source bytes but cannot independently prove authenticity without access to that archive.
