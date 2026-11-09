"""Replay the retained V7 cgroup RAM summary. Standard library only; no network/GPU."""
from pathlib import Path
import csv, gzip, hashlib, json, statistics
ROOT = Path(__file__).resolve().parent

def main():
    evidence = ROOT / "evidence"
    summary = json.loads((evidence / "ram-summary.json").read_text())
    raw = (evidence / "ram-observations.csv.gz").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == summary["data_sha256"]
    rows = list(csv.DictReader(gzip.decompress(raw).decode().splitlines()))
    values = [int(row["memory_current_bytes"]) for row in rows]
    actual = {"observations": len(rows), "in_call_samples": sum(row["kind"] == "sample" for row in rows),
              "boundary_observations": sum(row["kind"] != "sample" for row in rows),
              "min_bytes": min(values), "median_bytes": statistics.median(values), "max_bytes": max(values)}
    for key, value in actual.items():
        assert value == summary[key], key
    peak = summary["peak_observation"]
    assert any(row["request"] == peak["request"] and row["kind"] == peak["kind"] and
               int(row["index"]) == peak["index"] and int(row["memory_current_bytes"]) == peak["memory_current_bytes"] for row in rows)
    actual.update(status="VERIFIED_RETAINED_RAM_REPLAY", median_gib=actual["median_bytes"] / 2**30,
                  max_gib=actual["max_bytes"] / 2**30, max_gb=actual["max_bytes"] / 1e9,
                  definition=summary["definition"], new_inference_calls=0)
    print(json.dumps(actual, indent=2))

if __name__ == "__main__":
    main()
