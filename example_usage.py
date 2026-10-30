# -*- coding: utf-8 -*-
from client import OpenClawGenParkLegalShield

shield = OpenClawGenParkLegalShield()

sample_contract = """
1. Vendor shall maintain 99.9% uptime for all AI inference endpoints.
2. Vendor shall not disclose confidential telemetry or benchmark data to third parties.
3. In emergency maintenance, Vendor may disclose system telemetry for diagnostics.
4. Total aggregate liability shall not exceed $150,000 for any direct damages.
5. In case of security incident, Vendor must promptly notify Customer within 72 hours under GDPR.
6. Customer agrees to pay invoices within 30 days.
"""

# 1. Parse Deontic Modalities
clauses = shield.parse_deontic_clauses(sample_contract)
print(f"Parsed {len(clauses)} clauses:")
for c in clauses[:3]:
    print(f"  [{c['clause_id']}] {c['modality']} ({c['subject']}): {c['text']}")

# 2. Conflict Analysis
conflicts = shield.detect_contradictions_and_conflicts(clauses)
print(f"\nConflicts Detected: {conflicts['conflicts_detected_count']} (Risk Index: {conflicts['conflict_risk_index']})")

# 3. Liability & Regulatory Audit
audit = shield.audit_liability_and_compliance(clauses, contract_value_usd=100000.0, regulatory_frameworks=["GDPR", "CCPA"])
print(f"\nAudit Result:")
print(f"  Score: {audit['legal_shield_score']}/100, Recommendation: {audit['recommendation']}")
print(f"  Liability Cap Ratio: {audit['liability_cap_ratio']}x contract value")
