#!/usr/bin/env python3

import argparse
import sys
from urllib.parse import urlparse

import requests


SECURITY_HEADERS = {
    "Strict-Transport-Security": "HSTS",
    "Content-Security-Policy": "Content-Security-Policy",
    "X-Frame-Options": "X-Frame-Options",
    "X-Content-Type-Options": "X-Content-Type-Options",
    "Referrer-Policy": "Referrer-Policy",
    "Permissions-Policy": "Permissions-Policy",
}


def normalize_url(url):
    """Make sure the URL has a valid HTTP/HTTPS scheme."""

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Please provide a valid HTTP or HTTPS URL.")

    return url


def scan(url, timeout=10):
    """Request the target and return the HTTP response."""

    url = normalize_url(url)

    response = requests.get(
        url,
        timeout=timeout,
        allow_redirects=True,
        headers={
            "User-Agent": "http-security-scanner/1.0"
        },
    )

    return response


def print_report(response):
    """Display the scan results in the terminal."""

    print()
    print("HTTP SECURITY SCANNER")
    print("=" * 48)

    print(f"Target:     {response.request.url}")
    print(f"Final URL:  {response.url}")
    print(f"Status:     {response.status_code}")

    scheme = urlparse(response.url).scheme
    print(f"HTTPS:      {'✓' if scheme == 'https' else '✗'}")

    # Redirects
    print()
    print("Redirects")
    print("-" * 48)

    if response.history:
        for index, redirect in enumerate(response.history, start=1):
            print(
                f"{index}. "
                f"{redirect.status_code} "
                f"{redirect.url}"
            )

        print(f"Final → {response.url}")

    else:
        print("No redirects observed.")

    # Security headers
    print()
    print("Security Headers")
    print("-" * 48)

    detected = 0

    for header, label in SECURITY_HEADERS.items():

        present = bool(response.headers.get(header))

        if present:
            detected += 1

        symbol = "✓" if present else "✗"

        print(f"{label:<32} {symbol}")

    print()
    print(
        f"Headers detected: "
        f"{detected}/{len(SECURITY_HEADERS)}"
    )

    # Cookies
    print()
    print("Cookies")
    print("-" * 48)

    cookies = response.headers.get("Set-Cookie")

    if not cookies:
        print("No Set-Cookie header observed.")

    else:
        cookie_lower = cookies.lower()

        secure = "secure" in cookie_lower
        httponly = "httponly" in cookie_lower
        samesite = "samesite=" in cookie_lower

        print(
            f"Secure:    {'✓' if secure else '✗'}"
        )

        print(
            f"HttpOnly:  {'✓' if httponly else '✗'}"
        )

        print(
            f"SameSite:  {'✓' if samesite else '✗'}"
        )

    # Server
    print()
    print("Server")
    print("-" * 48)

    print(
        response.headers.get(
            "Server",
            "Not disclosed"
        )
    )

    print()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Inspect common HTTP security headers "
            "and basic web response configuration."
        )
    )

    parser.add_argument(
        "url",
        help="Target URL, e.g. https://example.com",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)",
    )

    args = parser.parse_args()

    try:

        response = scan(
            args.url,
            timeout=args.timeout,
        )

        print_report(response)

    except requests.RequestException as error:

        print(
            f"Request failed: {error}",
            file=sys.stderr,
        )

        sys.exit(1)

    except ValueError as error:

        print(
            f"Invalid URL: {error}",
            file=sys.stderr,
        )

        sys.exit(2)


if __name__ == "__main__":
    main()