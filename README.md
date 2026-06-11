# A-CODEAI public reproduce export (slim)

SEND_GATE: HOLD — do not use as customer case study or merged marketing headline.
`research_only` · B→A auto-merge prohibited.


## Measured open-bench headline (per-corpus · `[HYPO]` · SEND_GATE HOLD)

- **golden40_public_safe_routed** · MKM-CHAT-D1 · N=40
- raw token saving: **9.36%** · Jaccard **0.897361**
- Not equivalent to frozen Track A 47.5% SLA.
- Stateless golden40 on same corpus may read 0% — cite routing SKU separately.

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
