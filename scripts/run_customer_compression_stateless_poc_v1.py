#!/usr/bin/env python3
"""Customer corpus PoC: V2 Trust Packet Stateless Profile (stateless_packet + codebook_only).

Reads JSONL rows with `text` or `raw_text`; reports per-row and aggregate token/Jaccard proxies.
Does not claim global 47.5% — customer-specific ROI only. [research_only] for external send.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TOKEN_RE = re.compile(r"\S+")
DEFAULT_OUT = ROOT / "reports/customer_compression_stateless_poc_v1_latest.json"
V2_JACCARD_FLOOR = 0.73


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _token_proxy(text: str) -> int:
    return len(TOKEN_RE.findall(text))


def _row_text(obj: dict[str, Any]) -> str | None:
    for key in ("text", "raw_text", "content", "body"):
        v = obj.get(key)
        if isinstance(v, str) and v.strip():
            return v
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Customer JSONL stateless V2 compression PoC.")
    ap.add_argument("--workspace-root", type=Path, default=ROOT)
    ap.add_argument(
        "--input-jsonl",
        type=Path,
        required=True,
        help="JSONL with text/raw_text per line",
    )
    ap.add_argument("--max-cases", type=int, default=200)
    ap.add_argument("--loss-profile", default="semantic_general", choices=["semantic_general", "lossless_text", "code_equivalent"])
    ap.add_argument(
        "--compression-profile",
        default="economy",
        choices=["economy", "fidelity", "literal"],
        help="V2 compression_profile passed to /v2/compress.",
    )
    ap.add_argument("--out-json", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--jaccard-floor", type=float, default=V2_JACCARD_FLOOR)
    ap.add_argument(
        "--relax-pass-gate",
        action="store_true",
        help="Exit 0 when rows exist and no API/parse failures (research-only corpora).",
    )
    ap.add_argument(
        "--sku",
        default=None,
        help="B2B external SKU (e.g. MKM-MED-G1) — metadata catalog binding; does not force compress routing yet.",
    )
    ap.add_argument(
        "--sku-spec-json",
        type=Path,
        default=ROOT / "docs/final/artifacts/compression_b2b_off_the_shelf_shard_sku_v1.json",
        help="SKU spec JSON path (default: compression_b2b_off_the_shelf_shard_sku_v1.json).",
    )
    ap.add_argument(
        "--shard-json",
        type=Path,
        default=None,
        help="Optional shard JSON override path (research catalog / ablation).",
    )
    ap.add_argument(
        "--no-force-b2b-shard",
        action="store_true",
        help="With --sku: metadata only (do not pass forced_shard_id to /v2/compress).",
    )
    ap.add_argument(
        "--must-keep-overlay-json",
        type=Path,
        default=None,
        help="Tenant must_keep overlay JSON (hard+soft terms → /v2/compress must_keep_overlay_terms).",
    )
    ap.add_argument(
        "--auto-b2b-overlay",
        action="store_true",
        help="With --sku: auto-load docs/final/artifacts/b2b_sku_<slug>_must_keep_overlay_v1.json if present.",
    )
    ap.add_argument(
        "--short-context-token-threshold",
        type=int,
        default=None,
        help="V2 short-context policy: apply cap when token_in_proxy <= threshold.",
    )
    ap.add_argument(
        "--short-context-max-saving-rate",
        type=float,
        default=None,
        help="V2 short-context max saving cap (e.g. 0.35 for B2B industry rows).",
    )
    args = ap.parse_args()

    workspace = args.workspace_root.resolve()
    sku_context: dict[str, Any] = {}
    if args.sku or args.shard_json:
        from scripts.compression_b2b_off_the_shelf_shard_sku_v1_lib import build_sku_context

        try:
            sku_context = build_sku_context(
                workspace_root=workspace,
                spec_path=args.sku_spec_json,
                external_sku=args.sku,
                shard_json_override=args.shard_json,
            )
        except (FileNotFoundError, KeyError, ValueError) as exc:
            print(f"error: sku resolution failed: {exc}", file=sys.stderr)
            return 2

    inp = args.input_jsonl.resolve()
    if not inp.is_file():
        print(f"error: missing input: {inp}", file=sys.stderr)
        return 2

    overlay_terms: list[str] = []
    overlay_path: Path | None = None
    if args.must_keep_overlay_json:
        overlay_path = args.must_keep_overlay_json.resolve()
    elif args.auto_b2b_overlay and args.sku:
        from scripts.compression_b2b_must_keep_overlay_v1_lib import overlay_path_for_external_sku

        candidate = overlay_path_for_external_sku(args.sku, workspace_root=workspace)
        if candidate.is_file():
            overlay_path = candidate
    if overlay_path:
        if not overlay_path.is_file():
            print(f"error: missing overlay: {overlay_path}", file=sys.stderr)
            return 2
        from scripts.compression_b2b_must_keep_overlay_v1_lib import load_overlay_terms

        overlay_terms = load_overlay_terms(overlay_path)

    from fastapi.testclient import TestClient
    from scripts.compression_token_api_v2_stub import RESIDUAL_STUB_KEY, app
    from scripts.report_multilens_performance_eval import _jaccard

    client = TestClient(app)
    rows: list[dict[str, Any]] = []
    failures = 0

    for i, line in enumerate(inp.read_text(encoding="utf-8", errors="replace").splitlines()):
        if not line.strip() or len(rows) >= max(0, args.max_cases):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            failures += 1
            continue
        if not isinstance(obj, dict):
            continue
        text = _row_text(obj)
        if not text:
            continue
        row_id = str(obj.get("id") or f"row_{i}")
        compress_body: dict[str, Any] = {
            "text": text,
            "loss_profile": args.loss_profile,
            "compression_profile": args.compression_profile,
            "client_request_id": f"poc-{row_id}",
            "stateless_packet": True,
        }
        if sku_context and not args.no_force_b2b_shard:
            forced = sku_context.get("forced_shard_id") or sku_context.get("override_shard_id")
            if forced:
                compress_body["forced_shard_id"] = forced
        if overlay_terms:
            compress_body["must_keep_overlay_terms"] = overlay_terms
        if args.short_context_token_threshold is not None:
            compress_body["short_context_token_threshold"] = args.short_context_token_threshold
        if args.short_context_max_saving_rate is not None:
            compress_body["short_context_max_saving_rate"] = args.short_context_max_saving_rate
        cr = client.post("/v2/compress", json=compress_body)
        if cr.status_code != 200:
            failures += 1
            rows.append({"id": row_id, "ok": False, "error": cr.text[:200]})
            continue
        cr_body = cr.json()
        pkt = cr_body.get("compression_packet") or {}
        router_meta = pkt.get("router_meta") if isinstance(pkt.get("router_meta"), dict) else {}
        stub = (pkt.get("residual_meta") or {}).get(RESIDUAL_STUB_KEY) or {}
        if "reconstructed_text" in stub:
            failures += 1
            rows.append({"id": row_id, "ok": False, "error": "stateless_packet_leaked_reconstructed_text"})
            continue
        er = client.post(
            "/v2/expand",
            json={"compression_packet": pkt, "decode_mode": "codebook_only"},
        )
        if er.status_code != 200:
            failures += 1
            rows.append({"id": row_id, "ok": False, "error": er.text[:200]})
            continue
        expanded = er.json().get("text") or ""
        tin = _token_proxy(text)
        tout = _token_proxy(str(pkt.get("compressed_text") or ""))
        saving = max(0.0, 1.0 - (tout / tin)) if tin > 0 else 0.0
        jac = float(_jaccard(text, expanded))
        exact_restore = expanded == text
        if args.loss_profile == "lossless_text":
            ok = exact_restore
        else:
            ok = jac >= args.jaccard_floor
        if not ok and not args.relax_pass_gate:
            failures += 1
        row_out: dict[str, Any] = {
            "id": row_id,
            "ok": ok,
            "exact_restore": exact_restore,
            "token_in_proxy": tin,
            "token_out_proxy": tout,
            "token_saving_rate_proxy": round(saving, 6),
            "jaccard_proxy": round(jac, 6),
            "reassembly": (er.json().get("integrity_flags") or {}).get("reassembly"),
        }
        if router_meta:
            row_out["router_shard_id"] = router_meta.get("shard_id")
            row_out["router_domain"] = router_meta.get("domain")
        rows.append(row_out)

    n_ok = sum(1 for r in rows if r.get("ok"))
    n = len(rows)
    avg_saving_pass = sum(r.get("token_saving_rate_proxy", 0.0) for r in rows if r.get("ok")) / max(1, n_ok)
    avg_jac_pass = sum(r.get("jaccard_proxy", 0.0) for r in rows if r.get("ok")) / max(1, n_ok)
    avg_saving_all = sum(r.get("token_saving_rate_proxy", 0.0) for r in rows) / max(1, n)
    avg_jac_all = sum(r.get("jaccard_proxy", 0.0) for r in rows) / max(1, n)

    doc = {
        "schema": "customer_compression_stateless_poc_v1",
        "generated_at_utc": _utc(),
        "research_only": True,
        "boundary_ack": "Per-customer JSONL only; not Golden 40 or Track A 47.5% claim.",
        "input_jsonl": str(inp).replace("\\", "/"),
        "loss_profile": args.loss_profile,
        "compression_profile": args.compression_profile,
        "case_count": n,
        "cases_passed": n_ok,
        "cases_passed_jaccard_floor": n_ok,
        "jaccard_floor": args.jaccard_floor,
        "pass_criterion": "exact_restore" if args.loss_profile == "lossless_text" else "jaccard_floor",
        "aggregate": {
            "mean_token_saving_rate_proxy": round(avg_saving_pass, 6),
            "mean_jaccard_proxy": round(avg_jac_pass, 6),
            "mean_token_saving_rate_proxy_all_cases": round(avg_saving_all, 6),
            "mean_jaccard_proxy_all_cases": round(avg_jac_all, 6),
        },
        "must_keep_overlay": {
            "applied": bool(overlay_terms),
            "term_count": len(overlay_terms),
            "overlay_path": str(overlay_path).replace("\\", "/") if overlay_path else None,
        },
        "short_context_policy": {
            "token_threshold": args.short_context_token_threshold,
            "max_saving_rate": args.short_context_max_saving_rate,
        },
        "parse_or_api_failures": failures,
        "relax_pass_gate": bool(args.relax_pass_gate),
        "cases": rows[:50],
        "cases_truncated": len(rows) > 50,
    }
    if sku_context:
        if sku_context.get("forced_shard_id") and not args.no_force_b2b_shard:
            sku_context = {
                **sku_context,
                "routing_wiring": "forced_shard_id_v1",
                "routing_note_ko": "SKU --sku 시 b2b_shard_id를 forced_shard_id로 /v2/compress에 전달(승격 승인).",
            }
        doc["sku_context"] = sku_context
    out_path = args.out_json.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"cases={n} passed_jaccard={n_ok} mean_saving_proxy={avg_saving_pass:.4f} mean_jaccard={avg_jac_pass:.4f}")
    if overlay_terms:
        print(f"must_keep_overlay_terms={len(overlay_terms)}")
    if args.relax_pass_gate:
        return 0 if n > 0 and failures == 0 and n_ok >= 1 else 1
    return 0 if n > 0 and failures == 0 and n_ok == n else 1


if __name__ == "__main__":
    raise SystemExit(main())
