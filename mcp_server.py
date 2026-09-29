import sys, json
from client import PersonalCommunicationTriageSentinel

def handle_mcp():
    sentinel = PersonalCommunicationTriageSentinel()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(sentinel.run_communication_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-personal-communication-triage-sentinel-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "triage_message", "description": "Triage message and calculate priority score.", "inputSchema": {"type": "object", "properties": {"message_id": {"type": "string"}, "sender": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}}},
                    {"name": "auto_draft_reply", "description": "Auto-draft contextual reply.", "inputSchema": {"type": "object", "properties": {"message_info": {"type": "object"}}}},
                    {"name": "run_communication_benchmark", "description": "Run communication triage benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "triage_message":
                    res = sentinel.triage_message(args.get("message_id", "m"), args.get("sender", ""), args.get("subject", ""), args.get("body", ""))
                elif tname == "auto_draft_reply":
                    res = sentinel.auto_draft_reply(args.get("message_info", {}))
                else:
                    res = sentinel.run_communication_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
