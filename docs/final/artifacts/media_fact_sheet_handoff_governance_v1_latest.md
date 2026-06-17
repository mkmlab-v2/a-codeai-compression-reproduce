---
schema: media_fact_sheet_handoff_governance_v1
sku_id: handoff_governance
generated_at_utc: 2026-06-17T04:52:41Z
labels: [DRAFT, internal_only, research_only, publish_allowed=false]
ready_for_external_send: false
send_gate: HOLD
track: B
fail_comp_004: do_not_merge_with_compression_api
---

# Media Fact Sheet — Agent Handoff Governance (SKU 1/3)

**용도:** 언론·학계·B2B **내부 검토** — 멀티에이전트 **컨텍스트 라우팅·거버넌스** 축만. Compression API·파일럿 ROI와 **같은 슬라이드·헤드라인 금지**.

---

## 한 줄 정의 (대외 후보 · 조건부)

> 디스크 SSOT는 그대로 두고, **검증 가능한 핸드오프 팩(경로·앵커·must_keep)** 만 다음 에이전트에 주입하는 **운영 거버넌스 레이어** — ZIP式 무손실 압축이 **아님**.

---

## 허용 수치 (조건 명시 필수)

| 지표 | 값 | 조건·범위 |
|------|-----|-----------|
| Inject OFF | **— tokens** | top-3 ops 노드 · essence+must_keep only |
| Inject ON (slice) | **1,706 tokens** | `--include-slice --slice-max-chars 1200` |
| Full anchor paste (회피 대상) | **27,539 tokens** | 동일 top-3 full slice paste |
| Reduction vs full | **—** | **indexed slices only** · lab weekly ops |
| must_keep gate | exit **0** | 주간 벤치 기준 |

**증거:** `reports/mkm_ops_memory_index_token_bench_v1_latest.json`  
**아키텍처:** `docs/final/artifacts/mkm_a2a_two_layer_architecture_v1_latest.json`

---

## 금지 수치·표현 (FAIL-COMP-004)

| 금지 | 이유 |
|------|------|
| “모든 LLM 비용 99% 절감” | 전역 SLA·다른 SKU와 합침 |
| “100% 무손실·규칙 100% 준수” | 게이트≠의미 동치 |
| Compression API **47.5%** 와 동일 덱 | 별 revenue wave (§3.1 vs handoff) |
| Tenant PoC **97.6%** 인용 | stub 코퍼스 — 다른 제품 |
| 달러 ROI (아직) | `roi_hypothesis.customer_monthly_context_spend_usd: null` |

---

## 언론용 안전 헤드라인 (초안)

- **KO:** “멀티 에이전트 팀에서 **2.7만 토큰 풀 붙여넣기** 대신 **141 토큰 인덱스 핸드오프**로 운영 컨텍스트 전달 — **내부 주간 ops 벤치**”
- **EN:** “Indexed handoff packs (~141 tok) vs full anchor paste (~27.5k tok) on ops SSOT slices — lab measurement, not enterprise-wide SLA.”

---

## 재현 커맨드 (로컬 · exit 0 = 경로 존재·벤치 갱신)

```powershell
py scripts/build_mkm_ops_memory_index_v1.py
py scripts/bench_mkm_ops_memory_index_token_savings_v1.py
py scripts/build_mkm_chat_resume_pack_v1.py --lane infra
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Invoke-AgentHandoffGovernanceWeeklyBaseline_v1.ps1
```

**페르소나 점검:** `Invoke-MkmPersonaHealth_v1.ps1 -Persona AiToAiGovernanceDelegation` (선택)

---

## RQ-019와의 관계

- **Handoff Governance** = ops memory · resume pack · must_keep gate  
- **RQ-019 / Inter-Agent wire** = 별 SKU — wire `payload_savings_ratio` 등을 **“compression”** 이라 부르지 말 것 (`track_c_b2b_logos_lens_appendix` guard)

---

## 송부 게이트

- `legal_review_status: PENDING` (`agent_handoff_governance_enterprise_onepager_v1_latest.json`)
- 대외 send 전: `PUBLIC_FACING` v1.7 · counsel (RQ-009)

---

*Related:* `agent_handoff_governance_enterprise_onepager_v1_latest.md` · `agent_handoff_governance_pilot_kpi_v1_latest.json`
