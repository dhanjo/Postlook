# Postlook

![Postlook](https://github.com/dhanjo/Postlook/assets/24205535/fca49a0d-7ee5-480c-b647-67ded86f0dda)

Postlook is a Python-based scanner that crawls Postman’s public workspace, collection, team, and request endpoints to surface potentially sensitive or misconfigured data for one or more targets.

## Features

- **Automated scanning** of workspaces, teams, and API requests on Postman’s public platform.
- **Multiple targets**: specify `-q/--query` multiple times or use `-kf/--keyword-file` to scan a list of domains/keywords in one run.
- **Domain filtering** (`--strict`): restricts output to only those blocks containing your exact query substring.
- **Exclude subdomains** (`--no-subdomains`): when strict, drop any results for subdomains, matching only the exact host.
- **Secret detection** (`--whispers`): integrates with [Whispers](https://github.com/adeptex/whispers) to flag potential secrets in the results.
- **Custom Whisper rules** (`--whispers-config`): point to your own `config.yml` to drive the Whisper scan.
- **Output redirection** (`-o`): save filtered results to a file for offline analysis.

## How It Works

1. **Fetch**: queries Postman’s internal search API for each keyword or domain you provide.
2. **Filter**: if `--strict` is enabled, drops any result block that doesn’t contain the exact substring; if `--no-subdomains` is also set, further restricts to exact host matches.
3. **Detect secrets**: optionally runs Whispers over either the filtered or raw output depending on flags.
4. **Display**: prints workspaces, teams, and requests in a human‑readable format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dhanjo/Postlook.git
   cd Postlook
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Requirements file

```text
requests
whispers
```
*(Whispers is optional unless you intend to scan for secrets.)*

## Usage

```bash
python postlook.py -q <domain_or_keyword> [-q <another>] [--keyword-file <file>] [options]
```

### Input

- `-q, --query <value>`  
  One domain or keyword to search for. Repeatable to scan multiple targets.
- `-kf, --keyword-file <path>`  
  Path to a text file with one keyword or domain per line.

### Options

- `-o, --output <file>`  
  Write filtered results into the given file.
- `--strict`  
  Only keep blocks that contain the exact query substring.
- `--no-subdomains`  
  When used with `--strict`, drop any results for subdomains (exact host match only).
- `--whispers`  
  Run Whispers secret detection using the default `config.yml` in the current directory.
- `--whispers-config <path>`  
  Run Whispers with a custom ruleset (implies running Whisper scan even without `--whispers`).

## Examples

- **Basic scan** (no filtering) for a single domain:
  ```bash
  python postlook.py -q example.com
  ```

- **Scan multiple domains**:
  ```bash
  python postlook.py -q example.com -q nykaa.com
  ```

- **Scan from keyword file**:
  ```bash
  python postlook.py --keyword-file targets.txt
  ```

- **Strict domain filter**:
  ```bash
  python postlook.py -q example.com --strict
  ```

- **Strict + exclude subdomains**:
  ```bash
  python postlook.py -q example.com --strict --no-subdomains
  ```

- **Default Whispers scan**:
  ```bash
  python postlook.py -q example.com --whispers
  ```

- **Custom Whisper rules**:
  ```bash
  python postlook.py -q example.com --whispers-config /path/to/config.yml
  ```

- **Combined strict + secret detection**:
  ```bash
  python postlook.py -q example.com --strict --whispers
  ```

- **Save output to file**:
  ```bash
  python postlook.py -q example.com -o results.txt
  ```

## License

MIT
