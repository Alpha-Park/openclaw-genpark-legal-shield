# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Legal Shield - Autonomous Contract Clause Compliance & Deontic Logic Auditor
Standard Library only: re, typing, math.
Extracts deontic modalities (Obligation, Permission, Prohibition), detects normative conflicts,
and assesses aggregate liability exposure and regulatory compliance (GDPR, CCPA, SOC2).
"""

import re
from typing import Dict, List, Any

class OpenClawGenParkLegalShield:
    def __init__(self):
        self.obligation_patterns = [
            r"\b(shall|must|is required to|agrees to|will ensure|undertakes to)\b",
        ]
        self.permission_patterns = [
            r"\b(may|is permitted to|has the right to|at its discretion|entitled to)\b",
        ]
        self.prohibition_patterns = [
            r"\b(shall not|must not|may not|prohibited from|strictly forbidden from|agrees not to)\b",
        ]

    def parse_deontic_clauses(self, text: str) -> List[Dict[str, Any]]:
        """
        Parses legal prose into deontic logic formal representations.
        Classifies statements into OBLIGATION (O), PERMISSION (P), or PROHIBITION (F).
        """
        sentences = [s.strip() for s in re.split(r"[.;\n]+", text) if len(s.strip()) > 10]
        parsed = []

        for idx, s in enumerate(sentences):
            # Check prohibition first (since 'shall not' contains 'shall')
            modality = None
            for p in self.prohibition_patterns:
                if re.search(p, s, re.IGNORECASE):
                    modality = "PROHIBITION"
                    break
            
            if not modality:
                for p in self.obligation_patterns:
                    if re.search(p, s, re.IGNORECASE):
                        modality = "OBLIGATION"
                        break

            if not modality:
                for p in self.permission_patterns:
                    if re.search(p, s, re.IGNORECASE):
                        modality = "PERMISSION"
                        break

            if not modality:
                modality = "DECLARATIVE"

            # Detect party/subject
            subject = "GENERAL"
            if re.search(r"\b(vendor|provider|seller|supplier)\b", s, re.IGNORECASE):
                subject = "VENDOR"
            elif re.search(r"\b(customer|buyer|client|licensee)\b", s, re.IGNORECASE):
                subject = "CUSTOMER"
            elif re.search(r"\b(agent|subagent|contractor)\b", s, re.IGNORECASE):
                subject = "AGENT"

            has_condition = bool(re.search(r"\b(if|provided that|unless|subject to|in the event)\b", s, re.IGNORECASE))

            parsed.append({
                "clause_id": f"clause_{idx+1:03d}",
                "text": s,
                "modality": modality,
                "subject": subject,
                "is_conditional": has_condition
            })

        return parsed

    def detect_contradictions_and_conflicts(self, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detects normative contradictions:
        OBLIGATION vs PROHIBITION on the same subject and topic.
        PERMISSION vs PROHIBITION collisions.
        """
        conflicts = []
        n = len(clauses)

        for i in range(n):
            for j in range(i + 1, n):
                c1 = clauses[i]
                c2 = clauses[j]

                # If same subject
                if c1["subject"] != "GENERAL" and c1["subject"] == c2["subject"]:
                    # Check token overlap
                    words1 = set(re.findall(r"\b\w{4,}\b", c1["text"].lower()))
                    words2 = set(re.findall(r"\b\w{4,}\b", c2["text"].lower()))
                    overlap = words1.intersection(words2)

                    if len(overlap) >= 2:
                        # Collision check
                        m1, m2 = c1["modality"], c2["modality"]
                        if (m1 == "OBLIGATION" and m2 == "PROHIBITION") or (m1 == "PROHIBITION" and m2 == "OBLIGATION"):
                            conflicts.append({
                                "conflict_type": "NORMATIVE_CONTRADICTION",
                                "severity": 1.0,
                                "clause_a": c1["clause_id"],
                                "clause_b": c2["clause_id"],
                                "subject": c1["subject"],
                                "overlapping_terms": list(overlap)[:5],
                                "explanation": f"Clause {c1['clause_id']} imposes an obligation while {c2['clause_id']} explicitly prohibits the same subject."
                            })
                        elif (m1 == "PERMISSION" and m2 == "PROHIBITION") or (m1 == "PROHIBITION" and m2 == "PERMISSION"):
                            conflicts.append({
                                "conflict_type": "PERMISSION_PROHIBITION_COLLISION",
                                "severity": 0.75,
                                "clause_a": c1["clause_id"],
                                "clause_b": c2["clause_id"],
                                "subject": c1["subject"],
                                "overlapping_terms": list(overlap)[:5],
                                "explanation": f"Clause {c1['clause_id']} grants permission but {c2['clause_id']} states a prohibition."
                            })

        conflict_risk_index = round(min(1.0, sum(c["severity"] for c in conflicts) * 0.4), 3)

        return {
            "total_clauses_analyzed": len(clauses),
            "conflicts_detected_count": len(conflicts),
            "conflict_risk_index": conflict_risk_index,
            "has_critical_blocker": any(c["severity"] == 1.0 for c in conflicts),
            "conflicts": conflicts
        }

    def audit_liability_and_compliance(self, clauses: List[Dict[str, Any]],
                                      contract_value_usd: float,
                                      regulatory_frameworks: List[str] = None) -> Dict[str, Any]:
        """
        Audits liability caps, uncapped indemnities, and regulatory mandates (GDPR, CCPA, SOC2).
        """
        frameworks = regulatory_frameworks or ["GDPR", "CCPA"]
        full_text = " ".join(c["text"] for c in clauses).lower()

        # Check liability cap
        cap_match = re.search(r"liability\s+(?:shall\s+not|will\s+not)?\s*exceed\s*\$?([\d,]+)", full_text)
        cap_usd = float(cap_match.group(1).replace(",", "")) if cap_match else contract_value_usd * 2.0
        cap_ratio = cap_usd / max(1.0, contract_value_usd)

        # Check uncapped carveouts
        has_uncapped_ip = "intellectual property" in full_text and ("indemnif" in full_text or "uncapped" in full_text)
        has_uncapped_confidentiality = "confidentiality" in full_text and "breach" in full_text

        # Regulatory audits
        compliance_checklist = {}
        for fw in frameworks:
            fw_upper = fw.upper()
            if fw_upper == "GDPR":
                has_dpa = "data processing" in full_text or "dpa" in full_text
                has_breach_72h = "72 hours" in full_text or "promptly notify" in full_text
                compliance_checklist["GDPR"] = {
                    "data_processing_agreement": has_dpa,
                    "breach_notification_window": has_breach_72h,
                    "status": "PASS" if (has_dpa or has_breach_72h) else "FLAGGED"
                }
            elif fw_upper == "CCPA":
                has_opt_out = "opt-out" in full_text or "personal information" in full_text
                compliance_checklist["CCPA"] = {
                    "consumer_privacy_provisions": has_opt_out,
                    "status": "PASS" if has_opt_out else "FLAGGED"
                }
            elif fw_upper == "SOC2":
                has_audit_rights = "audit" in full_text or "security report" in full_text
                compliance_checklist["SOC2"] = {
                    "audit_and_controls_clause": has_audit_rights,
                    "status": "PASS" if has_audit_rights else "FLAGGED"
                }

        # Calculate legal shield score (0-100)
        base_score = 90.0
        if cap_ratio > 3.0: base_score -= 15.0
        if has_uncapped_ip: base_score -= 10.0
        for fw_res in compliance_checklist.values():
            if fw_res.get("status") == "FLAGGED": base_score -= 15.0

        score = max(0.0, min(100.0, base_score))

        if score >= 80.0:
            recommendation = "APPROVED_LOW_RISK"
        elif score >= 60.0:
            recommendation = "CONDITIONAL_REVISION_REQUIRED"
        else:
            recommendation = "REJECTED_UNACCEPTABLE_LIABILITY"

        return {
            "contract_value_usd": contract_value_usd,
            "detected_liability_cap_usd": cap_usd,
            "liability_cap_ratio": round(cap_ratio, 2),
            "uncapped_exposures": {
                "ip_infringement_indemnity": has_uncapped_ip,
                "confidentiality_breach": has_uncapped_confidentiality
            },
            "regulatory_compliance": compliance_checklist,
            "legal_shield_score": round(score, 1),
            "recommendation": recommendation
        }
