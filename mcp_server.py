# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkLegalShield

client = OpenClawGenParkLegalShield()

TOOLS = [
    {
        "name": "parse_deontic_clauses",
        "description": "Parses legal contract prose into formal deontic logic obligations, permissions, and prohibitions.",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
        }
    },
    {
        "name": "detect_contradictions_and_conflicts",
        "description": "Identifies normative contradictions and normative collisions between contractual clauses.",
        "inputSchema": {
            "type": "object",
            "properties": {"clauses": {"type": "array", "items": {"type": "object"}}},
            "required": ["clauses"]
        }
    },
    {
        "name": "audit_liability_and_compliance",
        "description": "Audits contract liability cap ratios, uncapped indemnities, and regulatory frameworks (GDPR, CCPA).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "clauses": {"type": "array", "items": {"type": "object"}},
                "contract_value_usd": {"type": "number"},
                "regulatory_frameworks": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["clauses", "contract_value_usd"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "parse_deontic_clauses":
            res = client.parse_deontic_clauses(args["text"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "detect_contradictions_and_conflicts":
            res = client.detect_contradictions_and_conflicts(args["clauses"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "audit_liability_and_compliance":
            res = client.audit_liability_and_compliance(args["clauses"], args["contract_value_usd"], args.get("regulatory_frameworks"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
