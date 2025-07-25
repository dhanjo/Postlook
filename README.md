# Postlook

Postlook is a Python-based scanner that crawls Postman’s public workspace, collection, team and request endpoints to surface potentially sensitive or misconfigured data.

## Features

* **Automated scanning** of workspaces, teams, and API requests on Postman’s public platform.
* **Domain filtering (**\`\`**)**: restricts output to only those blocks containing your exact query string.
* **Secret detection (**\`\`**)**: integrates with [Whispers](https://github.com/adeptex/whispers) to flag potential secrets in the results.
* **Custom Whisper rules (**\`\`**)**: point to your own `config.yml` to drive the Whisper scan.
* **Output redirection (**\`\`**)**: save filtered results to a file for offline analysis.

## How It Works

1. **Fetch**: queries Postman’s internal search API for your keyword or domain.
2. **Filter**: if `--strict` is enabled, drops any result block that doesn’t contain the exact substring you provided.
3. **Detect secrets**: optionally runs Whispers over either the raw or filtered output.
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

(Whispers is optional unless you intend to scan for secrets.)

## Usage

```bash
python postlook.py -q <domain_or_keyword> [options]
```

### Required

* `-q, --query <value>`
  Keyword or domain to search for (e.g. `nykaa.com`).

### Optional

* `-o, --output <file>`
  Write filtered results into the given file.

* `--strict`
  Only keep blocks that contain the exact query substring.

* `--whispers`
  Run Whispers secret detection using the default `config.yml` in the current directory.

* `--whispers-config <path>`
  Run Whispers with a custom ruleset (implies running Whisper scan even without `--whispers`).

## Examples

* **Basic scan** (no filtering):

  ```bash
  python postlook.py -q example.com
  ```

* **Strict domain filter**:

  ```bash
  python postlook.py -q example.com --strict
  ```

* **Default Whispers scan**:

  ```bash
  python postlook.py -q example.com --whispers
  ```

* **Custom Whisper rules**:

  ```bash
  python postlook.py -q example.com --whispers-config /path/to/config.yml
  ```

* **Combined strict + secret detection**:

  ```bash
  python postlook.py -q example.com --strict --whispers
  ```

* **Save output to file**:

  ```bash
  python postlook.py -q example.com -o results.txt
  ```

## License

MIT © Dhanjo

```
```
