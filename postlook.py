#!/usr/bin/env python3
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
/_/    \____/____/\__/_/\____/\____/_/|_|  
'''
POSTMAN_MONITORING = "            POSTMAN MONITORING"
TWITTER = "    Follow me on Twitter: @dhananjaygarg_"


def normalize_domain(q: str) -> str:
    """Strip scheme if present (e.g. http://)"""
    if q.startswith("http"):
        p = urlparse(q)
        return p.netloc or p.path
    return q


def split_blocks(text: str):
    """Split text into blocks separated by blank lines"""
    buf = []
    blocks = []
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
    """Keep only blocks containing domain substring (case-insensitive)"""
    if not text:
        return ""
    d = domain.lower()
    kept = [b for b in split_blocks(text) if d in b.lower()]
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


def main():
    parser = argparse.ArgumentParser(description="Postlook - Postman leak finder")
    parser.add_argument("-q", "--query", required=True, help="Domain/keyword to search for")
    parser.add_argument("-o", "--output", help="Save filtered results to this file")
    parser.add_argument("--strict", action="store_true",
                        help="Show only blocks containing the exact domain substring")
    parser.add_argument("--whispers", action="store_true",
                        help="Run Whispers secret detection with default config.yml")
    parser.add_argument("--whispers-config", help="Path to Whispers config.yml (implies run Whispers)")
    args = parser.parse_args()

    domain = normalize_domain(args.query)

    # Fetch raw data
    col_raw = postman_collections(args.query)
    team_raw = postman_teams(args.query)
    req_raw = postman_requests(args.query)

    # Filter based on domain
    if args.strict:
        col_out = filter_by_substring(col_raw, domain)
        team_out = filter_by_substring(team_raw, domain)
        req_out = filter_by_substring(req_raw, domain)
    else:
        col_out = col_raw
        team_out = team_raw
        req_out = req_raw

    # Determine if and how to run whispers
    run_whispers_flag = False
    config_path = None
    if args.whispers_config:
        run_whispers_flag = True
        config_path = args.whispers_config
    elif args.whispers:
        run_whispers_flag = True
        config_path = os.path.join(os.getcwd(), "config.yml")

    # Print filtered output
    print("\n" + POSTMAN_ART + "\n")
    print(POSTMAN_MONITORING)
    print(TWITTER + "\n")

    print("[+] Publicly Exposed - Workspaces and Collections\n")
    print(col_out)

    print("\n[+] Publicly Exposed - Teams\n")
    print(team_out)

    print("\n[+] Publicly Exposed - API Requests\n")
    print(req_out)

    # Run whispers if requested
    if run_whispers_flag:
        text_to_scan = "\n".join([col_out, team_out, req_out]) if args.strict else "\n".join([col_raw, team_raw, req_raw])
        run_whispers(text_to_scan, config_path)

    print("\n" + "─" * 50 + "\n")

    # Save to file if asked
    if args.output:
        with open(args.output, "w") as f:
            f.write("\n" + POSTMAN_ART + "\n")
            f.write(POSTMAN_MONITORING + "\n")
            f.write(TWITTER + "\n\n")
            f.write("[+] Publicly Exposed - Workspaces and Collections\n")
            f.write(col_out + "\n\n")
            f.write("[+] Publicly Exposed - Teams\n")
            f.write(team_out + "\n\n")
            f.write("[+] Publicly Exposed - API Requests\n")
            f.write(req_out + "\n")
            f.write("─" * 50 + "\n")


if __name__ == "__main__":
    main()

