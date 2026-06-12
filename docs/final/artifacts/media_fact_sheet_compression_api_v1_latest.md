---
schema: media_fact_sheet_compression_api_v1
sku_id: compression_api
generated_at_utc: 2026-06-12T03:07:42Z
labels: [DRAFT, internal_only, research_only, publish_allowed=false]
ready_for_external_send: false
send_gate: HOLD
track: A_reference_internal_only
fail_comp_004: true
---

# Media Fact Sheet — Compression API / a-codeai Open Bench (SKU 2/3)

**용도:** **구조화 payload 압축·미터링 API** 축만. Handoff 99.5%·파일럿 달러 ROI와 **합치지 말 것**.

---

## 한 줄 정의 (대외 후보 · 조건부)

> 반복 구조화 텍스트(JSONL·로그 envelope)에 **테넌트별 압축 + 미터링** — **지능형 라우팅·코덱 프로파일**이며 ZIP式 바이트 무손실이 **아님**. 성능은 **코퍼스·프로파일·도메인 티어**에 따라 변동.

**권장 대외 한 줄 (SEND HOLD 중):** 내부 리허설에서 파이프라인 무결성은 확인했고, **고객 실측·법무 승인 전까지 외부 성과 주장은 하지 않습니다.**

---

## 허용 수치 (내부 Reference · 약속 아님)

| 지표 | 값 | 조건·범위 |
|------|-----|-----------|
| Track A frozen (Golden 40) | saving **~47.1%** · Jaccard **~0.89** | `MULTILENS_ULTRA_COMPRESSION_ACTIVE_REPORT_V1.json` · **내부 회귀 SSOT** |
| Open long structured | **saving **0.0%** · J **1.0000** (48-case corpus)** | `customer_compression_stateless_poc_open_structured_long_v1_latest.json` · **per-corpus only** |
| Golden40 public-safe | **saving **0.0%** · J **1.0000** (40-case public-safe)** | `stateless_poc_golden40_public_safe_v1.jsonl` · **not customer SLA** |
| Prospect pilot rehearsal | **saving **19.4%** · J **0.8152** (30-case)** | `compression_b2b_pilot_roi_report_v1_latest.json` · **shared API PoC — NOT Handoff · NOT Track A** |
| AB gate reference | **~38.9%** (wire) | Evidence index — **고객 약속 금지** |
| VPS latency draft | p95 **~665 ms** | `bench_l1_api_load_summary_vps_latest.json` · `research_only` · 동시 50 · ~1k tok |
| Open bench launch | **READY_FOR_PUBLIC_OPEN_BENCH** | `a_codeai_public_benchmark_launch_checklist_v1.json` · **SEND_GATE still HOLD** |
| Public binding | **PASS** (4/4 routes) | `check_a_codeai_public_binding_v1.py` |

---

## 금지 수치·표현 (FAIL-COMP-004)

| 금지 | 이유 |
|------|------|
| “47.5% / 47% **보장**” | frozen bench ≠ 고객 전역 SLA |
| Rehearsal **97.6%** as **global** or **Handoff** claim | Prospect PoC only — `prospect-rehearsal-01` · **≠ Handoff 99.47% · ≠ Track A ~47%** |
| Tenant stub **97.6%** as **named customer** case study | Synthetic/masked rehearsal — **달러/KRW ROI null** |
| B-track Universal **~64.6%** | `research_only` — Track A·대외 합선 금지 |
| “누구나 99% 재현” (오픈 벤치 전) | 제3자 재현 패키지·고정 코퍼스 선행 필요 |
| p95 665ms = **SLA** | draft_benchmark · 고객 환경 미반영 |

---

## 언론용 안전 헤드라인 (초안)

- **KO:** “엔터프라이즈 JSONL에 **테넌트 실측 PoC**로 절감·복원 지표 산출 — 내부 Golden-40 **~47%** 는 **개발 벤치**이며 고객 **보장 수치 아님**”
- **EN:** “Per-tenant measured PoC on masked workloads; internal ~47% / ~0.89 Jaccard is a frozen regression baseline, not a warranty.”

---

## 재현 커맨드 (권장 · Proof completion)

```powershell
py scripts/run_compression_proof_completion_chain_v1.py
py scripts/run_compression_evidence_lv1_chain_v1.py
```

**실고객 코퍼스 투입 (Human):**

```powershell
py scripts/run_compression_pilot_roi_chain_v1.py --tenant-id <TENANT_SLUG>
```

**법무 승인 후 SEND (Human):**

```powershell
py scripts/apply_compression_b2b_legal_send_signoff_v1.py --commander-acknowledge --counsel-acknowledge
py scripts/check_compression_enterprise_summary_readiness_v1.py
```

**Open Bench · Evidence v0 (보조):**

```powershell
py scripts/build_compression_public_evidence_pack_v0_index_v1.py
py scripts/check_a_codeai_public_binding_v1.py
py scripts/build_a_codeai_public_benchmark_launch_checklist_v1.py
```

**주의:** enterprise 50 JSONL 재현은 **무결성 스모크** — `forbidden_as_headline: true` (`compression_public_evidence_pack_v0_index_latest.json`).

**Latency 벤치 (VPS · 선택):**

```powershell
py scripts/bench_l1_api_load.py --base-url http://127.0.0.1:8010 --max-concurrent 50 --total-requests 300
```

---

## 도메인·Jaccard 면책 (구두·보도 공통)

- Jaccard = **어휘 프록시** — 법무·재무·의료는 **보수 프로파일 또는 bypass** (`compression_domain_adoption_tier_matrix_v1.json`)
- 상세 계약 문구: `compression_b2b_pilot_contract_performance_clauses_v1_latest.md` §2

---

## 오픈 벤치 1단계 (언론 전 필수)

1. 고정 JSONL + `tenant_id` + 스크립트 SHA 공개(또는 a-codeai 재현 페이지)  
2. 제3자 exit 0 로그 수집  
3. **그 다음** “community verified” 문구 검토  

현재: launch checklist READY · **대외 캠페인·보도자료 HOLD**

---

*Related:* `compression_b2b_pilot_onepager_v1.md` · `compression_public_evidence_pack_v0_index_latest.json` · `TRACK_A_SLA_DRAFT.md`
