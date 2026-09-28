"""MX verification of the addresses the regex study collected, plus the SMTP-probe reality check.

Takes every valid-looking address from results/regex_study.json, deduplicates domains, and
resolves MX for each. Then attempts one TCP connection to port 25 of a few real MX hosts
to record whether this network can run SMTP probes at all (most residential and office
networks cannot, port 25 egress is blocked). Writes results/mx_check.json.
"""
import json
import pathlib
import socket
import sys

import dns.resolver

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = pathlib.Path(__file__).resolve().parent.parent / "results"

pages = json.loads((S / "regex_study.json").read_text(encoding="utf-8"))
addresses = sorted({m for p in pages for m in p["samples"].get("valid-looking", [])})
domains = sorted({a.rsplit("@", 1)[1].lower() for a in addresses})

mx = {}
for d in domains:
    try:
        answers = dns.resolver.resolve(d, "MX", lifetime=8)
        mx[d] = sorted(str(r.exchange).rstrip(".") for r in answers)[:2]
    except Exception as exc:
        mx[d] = type(exc).__name__

with_mx = [d for d, v in mx.items() if isinstance(v, list)]
print(f"addresses: {len(addresses)}, domains: {len(domains)}, with MX: {len(with_mx)}")

probe = {}
for host in ["gmail-smtp-in.l.google.com", "aspmx.l.google.com"]:
    s = socket.socket()
    s.settimeout(8)
    try:
        s.connect((host, 25))
        probe[host] = "connected, banner " + s.recv(80).decode("latin-1", "replace").strip()[:60]
    except OSError as exc:
        probe[host] = f"blocked ({type(exc).__name__})"
    finally:
        s.close()
    print("port 25 to", host, "->", probe[host])

(S / "mx_check.json").write_text(json.dumps(dict(
    addresses=len(addresses), domains=len(domains), with_mx=len(with_mx),
    mx=mx, port25_probe=probe), ensure_ascii=False, indent=1), encoding="utf-8")
print("saved mx_check.json")
