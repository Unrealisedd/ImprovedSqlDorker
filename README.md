# ImprovedSqlDorker

Upgraded version of my other [sqldorker](https://github.com/Unrealisedd/sqldorker). This one routes through Tor for IP rotation, uses Wappalyzer to fingerprint the target's tech stack, then picks SQLi payloads that actually match the backend DB (mysql, mssql, oracle, postgres). Falls back to generic + xor payloads if it can't determine the database.

Detects both error-based and time-based SQLi.

Linux only (tornet dependency).

## Setup

```
git clone https://github.com/Unrealisedd/ImprovedSqlDorker.git
cd ImprovedSqlDorker
pip install -r requirements.txt
pip install tornet
```

You also need Tor installed on your system.

Payload files go in the `payloads/` directory (already included: mysql, mssql, oracle, postgresql, generic, xor).

## Usage

```
python sqldorkerl2.py
```

It'll ask for a Google dork (like `inurl:"?id="`) and how many results to pull. From there it fetches URLs through Tor, rotates IPs between requests, fingerprints each target, and tests with the appropriate payloads.

Vulnerable URLs get printed in green, clean ones in red.
