# A-CODEAI public reproduce export (slim)

SEND_GATE: HOLD — do not use as customer case study or merged marketing headline.
`research_only` · B→A auto-merge prohibited.


## Measured open-bench headline (per-corpus · `[HYPO]` · SEND_GATE HOLD)

- **golden40_public_safe_routed** · MKM-CHAT-D1 · N=40
- raw token saving: **9.36%** · Jaccard **0.897361**
- Not equivalent to frozen Track A 47.5% SLA.
- Stateless golden40 on same corpus may read 0% — cite routing SKU separately.


## B-track research (internal scenario only · not external headline)

- CHAT-D1 **literal** on golden40: **15.21%** · Jaccard **0.840645**
- See `reports/compression_open_bench_research_sweep_v1_latest.json`

## One command (from repo root)

```bash
pip install -r requirements-public-reproduce.txt
python3 scripts/run_compression_evidence_lv1_chain_v1.py --skip-handoff
```

Optional open-bench chain (includes golden40 routed PoC):

```bash
python3 scripts/run_compression_open_bench_chain_v1.py --skip-expand
```

FAIL-COMP-004: per-SKU metrics only; never merge Track A / handoff / prospect %.

## Enterprise pre-audit intake (web form · separate funnel)

- Tier-0 **free pre-audit** queue (masked JSONL sample review): [app.jema-ai.com/enterprise/apply](https://app.jema-ai.com/enterprise/apply)
- Not auto-approval, not SLA or Track A headline guarantee; open-bench metrics above are not a submission outcome.

## Community contributions (contributor_provided · SEND_GATE HOLD)

See `CONTRIBUTING_OPEN_BENCH.md` — masked JSONL under `data/*/contributions/`; `contributor_provided=true`, `customer_provided=false`; no Track A / 47.5% headline.

## License

Apache License 2.0 — see [LICENSE](LICENSE). Open-bench reproduce only; SEND_GATE HOLD unchanged.
