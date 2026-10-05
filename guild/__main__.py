"""入口：从标准输入读 JSONL 申请/退会，逐行写名册状态。"""

import json
import sys

from .roster import Roster


def handle(roster, rec):
    action = rec.get("action")
    if action == "apply":
        status = roster.apply(rec.get("id"), rec.get("player"), rec.get("vip", False), rec.get("at", 0))
    elif action == "leave":
        status = roster.leave(rec.get("id"), rec.get("player"))
    else:
        status = "bad-request"
    return {
        "id": rec.get("id"),
        "status": status,
        "size": len(roster.members),
        "waiting": len(roster.waiting),
    }


def run(instream, outstream, roster):
    for line in instream:
        line = line.strip()
        if not line:
            continue
        outstream.write(json.dumps(handle(roster, json.loads(line))) + "\n")
    return 0


def scenario(name):
    if name == "cap":
        return Roster(2), [
            {"id": "e1", "action": "apply", "player": "a", "at": 1},
            {"id": "e2", "action": "apply", "player": "b", "at": 2},
            {"id": "e3", "action": "apply", "player": "c", "at": 3},
        ]
    if name == "vip":
        return Roster(0), [
            {"id": "e1", "action": "apply", "player": "a", "at": 1},
            {"id": "e2", "action": "apply", "player": "v", "vip": True, "at": 2},
        ]
    if name == "promote":
        return Roster(1), [
            {"id": "e1", "action": "apply", "player": "a", "at": 1},
            {"id": "e2", "action": "apply", "player": "b", "at": 2},
            {"id": "e3", "action": "leave", "player": "a"},
        ]
    if name == "idempotent":
        return Roster(5), [
            {"id": "e1", "action": "apply", "player": "a", "at": 1},
            {"id": "e1", "action": "apply", "player": "a", "at": 2},
        ]
    if name == "work":
        roster = Roster(1000)
        recs = []
        for i in range(2000):
            recs.append({"id": "e%d" % i, "action": "apply", "player": "p%d" % i, "at": i})
        return roster, recs
    raise SystemExit("未知场景 %s" % name)


def main(argv=None):
    import io

    args = (argv or sys.argv[1:])[:1]
    raw = args[0] if args else "--sample=cap"
    name = raw.split("=", 1)[1] if raw.startswith("--sample=") else raw
    roster, recs = scenario(name)
    if name == "work":
        out = io.StringIO()
        payload = "".join(json.dumps(r) + "\n" for r in recs)
        run(io.StringIO(payload), out, roster)
        print(json.dumps({"members": len(roster.members), "scanned": roster.scanned}))
        return 0
    out = io.StringIO()
    payload = "".join(json.dumps(r) + "\n" for r in recs)
    run(io.StringIO(payload), out, roster)
    sys.stdout.write(out.getvalue())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
