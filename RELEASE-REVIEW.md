# Owner review before publication

Status: prepared for review; no website deployment, public repository creation, public push or upstream submission authorized by this artifact.

Review these concrete choices:

1. Website narrative, chart labels, three separate dataset denominators and operational limits.
2. MIT for original code and CC BY 4.0 for authored content/data/figures are owner-approved. Verify their scope and retained third-party notices; publication remains unapproved.
3. New public GitHub repository name/visibility and website route. Proposed taxonomy is Research → Benchmarking: `/research/`, `/research/benchmarking/`, `/research/benchmarking/strata-memory-pools/`, with the measured companion at `/benchmarks/strata/`; no destination repository is assumed to exist.
4. Model-card metadata/body mismatch and current Qwen Community licence observation; no weights or commercial serving distribution is proposed here.
5. Source/build boundary: patches reconstruct affected source, but no fresh binary rebuild qualification; model pack, selected expert-profile bytes and exact site-specific serving wrapper remain external requirements.
6. Exact final bundle SHA256 and preview before any publishing action. Further edits require a new checked bundle/preview.

The website candidate renders no benchmark HTML or downloadable review assets in its default build. The explicit `BENCHMARK_PREVIEW=1` build produces local review routes and assets with draft banners/noindex on the pages. No production environment flag, navigation entry, deployment or public URL was changed. No inference, safety, driver, GPU ownership or runtime configuration changed.
