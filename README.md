# HTTP Security Scanner

A lightweight command-line tool for inspecting common HTTP security headers and basic web response configuration.

## Overview

`http-security-scanner` performs a quick first-pass inspection of a website's HTTP response.

It checks HTTPS usage, redirects, commonly recommended security headers, cookie security attributes, and basic server information.

The project is intentionally small and transparent, making it useful for developers, security learners, and anyone performing basic web-security reconnaissance.

## Features

* Check HTTPS usage
* Inspect common security headers
* Display HTTP status codes
* Follow and display redirects
* Inspect cookie security attributes
* Display basic server information
* Configurable request timeout
* Simple terminal output
* No third-party scanning API

### Security Headers Checked

* `Strict-Transport-Security`
* `Content-Security-Policy`
* `X-Frame-Options`
* `X-Content-Type-Options`
* `Referrer-Policy`
* `Permissions-Policy`

## Requirements

* Python 3.9+
* `requests`

## Installation

Clone the repository:

```bash
git clone https://github.com/soymedaz/http-security-scanner.git
cd http-security-scanner
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Scan a website:

```bash
python src/scanner.py https://example.com
```

A domain can also be provided without a scheme:

```bash
python src/scanner.py example.com
```

Set a custom request timeout:

```bash
python src/scanner.py https://example.com --timeout 20
```

## Example Output

```text
HTTP SECURITY SCANNER
================================================
Target:     https://example.com
Final URL:  https://example.com
Status:     200
HTTPS:      ✓

Redirects
------------------------------------------------
No redirects observed.

Security Headers
------------------------------------------------
HSTS                             ✓
Content-Security-Policy          ✗
X-Frame-Options                  ✓
X-Content-Type-Options           ✓
Referrer-Policy                  ✓
Permissions-Policy               ✗

Headers detected: 4/6

Cookies
------------------------------------------------
No Set-Cookie header observed.

Server
------------------------------------------------
Not disclosed
```

## Running Tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

The project currently includes tests for URL normalization and validation.

## Limitations

This is a lightweight HTTP configuration checker, not a full vulnerability scanner or penetration-testing framework.

A missing security header does not automatically mean that a website is vulnerable, and the presence of a header does not guarantee that an application is secure.

The results should be treated as a starting point for further investigation.

## Responsible Use

Only scan websites and systems that you own or have explicit permission to assess.

The tool makes direct HTTP requests to the target URL and should be used responsibly and in accordance with applicable laws, policies, and terms of service.

## Privacy

Scan results are processed locally by the program.

The project does not send scan results to a third-party scanning service.

The tool does make a direct HTTP request to the target URL in order to inspect its response.

## Roadmap

* [ ] Improve security findings and severity information
* [ ] Expand automated test coverage
* [ ] Improve cookie analysis
* [ ] Add JSON output
* [ ] Add CSV reporting
* [ ] Add TLS certificate inspection
* [ ] Add configurable security-header profiles

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

