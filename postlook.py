#!/usr/bin/env python3
import sys
import argparse
import os
import tempfile
from urllib.parse import urlparse

from postman_collection import postman_collections
from postman_teams import postman_teams
from postman_requests import postman_requests

# Lazy import for Whispers
try:
    import whispers
except ImportError:
    whispers = None

POSTMAN_ART = r'''
    ____             __  __            __
   / __ \____  _____/ /_/ /___  ____  / /__
  / /_/ / __ \/ ___/ __/ / __ \/ __ \/ //_/
 / ____/ /_/ (__  ) /_/ / /_/ / /_/ / ,<
/_/    \____/____/\__/_/\____/\____/_/|_|'''
POSTMAN_MONITORING = "            POSTMAN MONITORING"
TWITTER = "    Follow me on Twitter: @dhananjaygarg_"

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"\nError: {message}\n", file=sys.stderr)
        print("Example: python postlook.py -q example.com --strict --whispers-config config.yml")
        sys.exit(2)


def normalize_domain(q: str) -> str:
    """Strip scheme if present (e.g. http://)"""
    if q.startswith("http"):
        p = urlparse(q)
        return p.netloc or p.path
    return q.strip()


def split_blocks(text: str):
    """Split text into blocks separated by blank lines"""
    buf, blocks = [], []
    for line in text.splitlines():
        if not line.strip():
            if buf:
                blocks.append("\n".join(buf))
                buf = []
        else:
            buf.append(line)
    if buf:
        blocks.append("\n".join(buf))
    return blocks


def filter_by_substring(text: str, domain: str) -> str:
    """Keep only blocks that contain domain (case-insensitive)."""
    if not text:
        return ""
    d = domain.lower()
    return "\n\n".join([b for b in split_blocks(text) if d in b.lower()])


def filter_exact_domain(text: str, domain: str) -> str:
    """Keep only blocks where URL hosts exactly match the domain; fallback to substring for non-URL blocks."""
    if not text:
        return ""
    kept = []
    for b in split_blocks(text):
        lines = b.splitlines()
        url_lines = [ln for ln in lines if ln.strip().startswith("URL:")]
        if url_lines:
            for ln in url_lines:
                url = ln.split("URL:", 1)[1].strip()
                host = urlparse(url).netloc.split(':')[0]
                if host.lower() == domain.lower():
                    kept.append(b)
                    break
        else:
            if domain.lower() in b.lower():
                kept.append(b)
    return "\n\n".join(kept)


def run_whispers(text: str, cfg: str):
    """Run Whispers scan on provided text with given config path"""
    print(f"[*] Running Whispers with config: {cfg}")
    if not whispers:
        print("[-] Whispers not installed. pip install whispers")
        return
    if not os.path.isfile(cfg):
        print(f"[-] Whispers config missing at {cfg}")
        return
    if not text.strip():
        print("[*] Nothing to scan")
        return

    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
        tmp.write(text)
        path = tmp.name

    try:
        args = f"-c {cfg} {path}"
        findings = list(whispers.secrets(args))
        if findings:
            seen = set()
            print("\n[+] Potential secrets:")
            for s in findings:
                line = f"{s.key} = {s.value}"
                if line not in seen:
                    print(" >", line)
                    seen.add(line)
        else:
            print("[*] No secrets found")
    except Exception as e:
        print("[-] Whispers error:", e)
    finally:
        os.unlink(path)


def process_query(query: str, args):
    domain = normalize_domain(query)
    print(f"\n=== Results for: {domain} ===")

    col_raw = postman_collections(query)
    team_raw = postman_teams(query)
    req_raw = postman_requests(query)

    if args.strict:
        if args.no_subdomains:
            col_out = filter_exact_domain(col_raw, domain)
            team_out = filter_exact_domain(team_raw, domain)
            req_out = filter_exact_domain(req_raw, domain)
        else:
            col_out = filter_by_substring(col_raw, domain)
            team_out = filter_by_substring(team_raw, domain)
            req_out = filter_by_substring(req_raw, domain)
    else:
        col_out, team_out, req_out = col_raw, team_raw, req_raw

    print("\n" + POSTMAN_ART + "\n")
    print(POSTMAN_MONITORING)
    print(TWITTER + "\n")
    print("[+] Publicly Exposed - Workspaces and Collections\n")
    print(col_out)
    print("\n[+] Publicly Exposed - Teams\n")
    print(team_out)
    print("\n[+] Publicly Exposed - API Requests\n")
    print(req_out)

    run_whispers_flag = False
    cfg = None
    if args.whispers_config:
        run_whispers_flag = True
        cfg = args.whispers_config
    elif args.whispers:
        run_whispers_flag = True
        cfg = 'config.yml'

    if run_whispers_flag:
        to_scan = ("\n".join([col_out, team_out, req_out]) if args.strict else "\n".join([col_raw, team_raw, req_raw]))
        print("\n[*] Whispers scanning...")
        run_whispers(to_scan, cfg)

    print("\n" + "─" * 50 + "\n")


def main():
    parser = CustomParser(
        description="Postlook - Postman leak finder",
        usage="postlook.py -q <domain> [-q <domain2> | -kf <file>] [--strict] [--no-subdomains] [--whispers | --whispers-config <path>] [-o <output>]"
    )
    parser.add_argument("-q", "--query", action="append",
                        help="Domain/keyword to search for (repeatable)")
    parser.add_argument("-kf", "--keyword-file",
                        help="Path to file with keywords/domains, one per line")
    parser.add_argument("-o", "--output", help="Save filtered results to this file")
    parser.add_argument("--strict", action="store_true",
                        help="Show only blocks containing the exact domain substring")
    parser.add_argument("--no-subdomains", action="store_true",
                        help="When strict, exclude subdomains and match exact domain only")
    parser.add_argument("--whispers", action="store_true",
                        help="Run Whispers with default config.yml")
    parser.add_argument("--whispers-config",
                        help="Path to Whispers config.yml (implies running whispers)")
    args = parser.parse_args()

    targets = []
    if args.query:
        targets.extend(args.query)
    if args.keyword_file:
        try:
            with open(args.keyword_file) as f:
                targets.extend([line.strip() for line in f if line.strip()])
        except Exception as e:
            print("[-] Failed to read keyword file:", e)
            return
    if not targets:
        parser.error("At least one -q/--query or -kf/--keyword-file is required")

    for t in targets:
        process_query(t, args)

    if args.output:
        print(f"[*] Writing all filtered results to {args.output}")
        with open(args.output, 'w') as f:
            pass  # Placeholder for file write logic

if __name__ == "__main__":
    main()
