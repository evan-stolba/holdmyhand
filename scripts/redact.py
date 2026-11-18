#!/usr/bin/env python3
r"""
holdmyhand local redaction tool
================================

Makes a SAFE COPY of a data file before you share anything with an AI tool.
Runs entirely on your computer. It has no network code and never uploads anything.

What it does
  * Finds sensitive columns by name (names, emails, phones, IDs, addresses, salary...)
    and replaces their values with consistent tokens like CUSTOMER_3F9A2C1B.
  * Scans every cell / line for emails, phone numbers, SSNs, card numbers,
    IP addresses, IBANs and secrets (API keys, passwords) and replaces them.
  * The same input value always gets the same token (as long as you use the same
    secret), so joins between files still work after redaction.
  * Can produce a schema-only summary (column names, types, counts, no values)
    or a small synthetic sample, which are usually all an AI needs.

Supported files: .csv .tsv .xlsx (first sheet or --sheet; written out as CSV)
                 .json, and any text file (.txt .log .sql .md ...)

Needs only Python 3.8+ (no installs).

Examples
  python redact.py customers.csv --dry-run          # preview: what would be changed
  python redact.py customers.csv                    # writes customers.redacted.csv
  python redact.py sales.xlsx --sheet "Q3"          # writes sales.Q3.redacted.csv
  python redact.py orders.csv --schema-only         # writes orders.schema.csv (no values)
  python redact.py orders.csv --synthetic 5         # writes orders.synthetic.csv (5 fake rows)
  python redact.py notes.txt --terms clients.txt    # also replaces each name listed in clients.txt
  python redact.py orders.csv --columns "Account Manager" --keep "Region"
  python redact.py tickets.csv --drop "Notes" --pattern "EMP-\d{5}" --sequential

Important
  * The original file is never changed.
  * Your secret lives in a file (default: .holdmyhand_secret in your home folder),
    created with 256 random bits on first run; there is no built-in default secret.
    Keep it private: anyone with the secret and a list of candidate values (for
    example all employee IDs 1-5000) could re-create the tokens and match them.
    If that matters, use --sequential.
  * No mapping file (token -> real value) is written unless you pass --mapping.
    If you do, store it securely and never share it.
  * Automatic detection is helpful but NOT perfect, especially for names in free
    text. Always open the output and check it before sharing. Your company's
    policy wins.
"""

import argparse
import csv
import hashlib
import hmac
import io
import json
import os
import random
import re
import secrets
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import date, datetime, timedelta

VERSION = "1.0"

# --------------------------------------------------------------------------
# Detection rules
# --------------------------------------------------------------------------

# Column-name rules: (regex on normalized column name, token prefix).
# First match wins. Normalized = lowercase, non-letters/digits removed.
COLUMN_RULES = [
    (r"(password|passwd|pwd|secret|token|apikey|accesskey|privatekey|credential)", "SECRET"),
    (r"(ssn|socialsecurity|nationalid|nino|passport|driverslicen|taxid|tin$|sin$)", "GOVID"),
    (r"(cardnumber|creditcard|debitcard|^pan$|cvv|cvc)", "CARD"),
    (r"(iban|accountnumber|accountno|routingnumber|sortcode|bankaccount)", "BANKACCT"),
    (r"(email|e-?mail)", "EMAIL"),
    (r"(phone|^mobile|^cell$|cellphone|telephone|^fax)", "PHONE"),
    (r"(ipaddress|^ip$)", "IP"),
    (r"(address|street|postcode|postalcode|zipcode|^zip$)", "ADDRESS"),
    (r"(^dob$|dateofbirth|birthdate|birthday)", "DOB"),
    (r"(patient|diagnosis|mrn|medicalrecord|condition|treatment)", "HEALTH"),
    (r"(salary|wage|bonus|compensation|payrate|pay$)", "PAY"),
    (r"(customer|client|account(name)?$|company|vendor|supplier|partner)(name)?$", "CUSTOMER"),
    (r"(customer|client|account)(id|no|number|code|ref)$", "CUSTOMER"),
    (r"(employee|staff|worker)(id|no|number|code|name)?$", "EMPLOYEE"),
    (r"(firstname|lastname|surname|fullname|^name$|contact(name)?$|manager|owner|rep$|salesrep|accountmanager)", "PERSON"),
    (r"^(userid|username|login|loginid)$", "USER"),
]

# Prefixes whose values are replaced with a fixed label instead of a token,
# because a consistent token adds risk and no analytical value.
FIXED_LABEL = {"SECRET": "[REDACTED_SECRET]", "CARD": "[REDACTED_CARD]", "GOVID": "[REDACTED_ID]"}

# Prefixes that are flagged but NOT changed by default (they are often needed
# for the analysis). Use --columns to force redaction.
FLAG_ONLY = {"PAY"}

# Patterns found anywhere in any text cell or line.
PATTERNS = [
    # secrets first, so they win over other patterns
    ("SECRET", re.compile(r"\b(?:sk-[A-Za-z0-9_\-]{16,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abprs]-[A-Za-z0-9\-]{10,}|AIza[0-9A-Za-z_\-]{35})\b")),
    ("SECRET", re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token|access[_-]?key)\s*[:=]\s*[^\s;,'\"]+")),
    ("SECRET", re.compile(r"(?i)[a-z][a-z0-9+.\-]*://[^\s:/@]+:[^\s@/]+@")),  # user:pass@host in URLs
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("GOVID", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),  # US SSN format
    ("CARD", re.compile(r"\b(?:\d[ \-]?){12,18}\d\b")),  # checked with Luhn below
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){2,7}(?:[ ]?[A-Z0-9]{1,3})?\b")),
    ("GOVID", re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2} ?\d{2} ?\d{2} ?\d{2} ?[A-D]\b")),  # UK National Insurance
    ("POSTCODE", re.compile(r"\b(?:GIR ?0AA|[A-PR-UWYZ][A-HK-Y]?\d[A-Z\d]? ?\d[ABD-HJLNP-UW-Z]{2})\b")),  # UK postcode
    ("IP", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")),
    ("PHONE", re.compile(r"(?<![\w\-])(?:\+\d{1,3}[ .\-]?)?(?:\(\d{2,4}\)[ .\-]?|\d{2,4}[ .\-])\d{3,4}[ .\-]?\d{3,4}(?![\w\-])")),
    ("PATH", re.compile(r"(?i)(?:[a-z]:\\users\\[^\\\s]+|/(?:home|users)/[^/\s]+|\\\\[^\\\s]+\\[^\\\s]+)")),
]


def luhn_ok(digits):
    total, alt = 0, False
    for d in reversed(digits):
        n = int(d)
        if alt:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        alt = not alt
    return total % 10 == 0


def normalize_col(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def classify_column(name):
    n = normalize_col(name)
    for rx, prefix in COLUMN_RULES:
        if re.search(rx, n):
            return prefix
    return None


# --------------------------------------------------------------------------
# Tokenizer
# --------------------------------------------------------------------------

class Tokenizer:
    """Consistent tokens (HMAC with your secret) by default, so joins still work.
    sequential=True gives CUSTOMER_001, CUSTOMER_002... numbered per run instead:
    they can't be linked across files or reversed even if the secret leaks."""
    def __init__(self, secret, keep_mapping=False, sequential=False):
        self.key = secret.encode("utf-8")
        self.keep_mapping = keep_mapping
        self.sequential = sequential
        self.seq = {}      # (prefix, normalized value) -> number (sequential mode)
        self.mapping = {}  # token -> original (only if keep_mapping)
        self.counts = {}   # prefix -> number of replacements

    def token(self, prefix, value):
        self.counts[prefix] = self.counts.get(prefix, 0) + 1
        if prefix in FIXED_LABEL:
            return FIXED_LABEL[prefix]
        norm = re.sub(r"\s+", " ", str(value).strip().lower())
        if self.sequential:
            key = (prefix, norm)
            if key not in self.seq:
                self.seq[key] = sum(1 for k in self.seq if k[0] == prefix) + 1
            tok = f"{prefix}_{self.seq[key]:03d}"
        else:
            digest = hmac.new(self.key, (prefix + "|" + norm).encode("utf-8"), hashlib.sha256).hexdigest()
            tok = f"{prefix}_{digest[:8].upper()}"
        if self.keep_mapping:
            self.mapping[tok] = str(value)
        return tok


def scrub_text(text, tok, terms):
    """Replace sensitive patterns inside free text."""
    if not text:
        return text
    out = text
    # user-supplied terms (client names etc.), longest first
    for term in terms:
        rx = re.compile(r"(?i)(?<!\w)" + re.escape(term) + r"(?!\w)")
        out = rx.sub(lambda m: tok.token("TERM", m.group(0)), out)
    for prefix, rx in PATTERNS:
        def repl(m, prefix=prefix):
            s = m.group(0)
            if prefix == "CARD":
                digits = re.sub(r"\D", "", s)
                if not (13 <= len(digits) <= 19 and luhn_ok(digits)):
                    return s
            if prefix == "IBAN" and not re.search(r"\d", s[4:]):
                return s
            if prefix == "PHONE" and len(re.sub(r"\D", "", s)) < 7:
                return s
            if prefix == "PATH":
                return "[FILE_PATH]"
            return tok.token(prefix, s)
        out = rx.sub(repl, out)
    return out


# --------------------------------------------------------------------------
# Readers
# --------------------------------------------------------------------------

def read_delimited(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = "\t" if path.lower().endswith(".tsv") else ","
        try:
            delim = csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
        except csv.Error:
            pass
        rows = list(csv.reader(f, delimiter=delim))
    return rows, delim


def _col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx(path, sheet_name=None):
    """Minimal zero-dependency .xlsx reader (values only; dates come out as Excel serial numbers)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = [(s.get("name"), s.get("{%s}id" % ns["r"])) for s in wb.find("m:sheets", ns)]
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {r.get("Id"): r.get("Target") for r in rels}
        if sheet_name:
            match = [s for s in sheets if s[0] == sheet_name]
            if not match:
                sys.exit(f"Sheet '{sheet_name}' not found. Sheets in this file: {', '.join(s[0] for s in sheets)}")
            chosen = match[0]
        else:
            chosen = sheets[0]
        target = targets[chosen[1]].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sst.findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        sheet = ET.fromstring(z.read(target))
        rows = []
        for row in sheet.iter("{%s}row" % ns["m"]):
            vals = {}
            for c in row.findall("m:c", ns):
                idx = _col_index(c.get("r"))
                t = c.get("t")
                v = c.find("m:v", ns)
                if t == "s" and v is not None:
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % ns["m"]))
                elif t == "b" and v is not None:
                    val = "TRUE" if v.text == "1" else "FALSE"
                else:
                    val = v.text if v is not None else ""
                vals[idx] = val
            if vals:
                width = max(vals) + 1
                rows.append([vals.get(i, "") for i in range(width)])
        if rows:
            w = max(len(r) for r in rows)
            rows = [r + [""] * (w - len(r)) for r in rows]
    return rows, chosen[0]


# --------------------------------------------------------------------------
# Table processing
# --------------------------------------------------------------------------

def looks_free_text(values):
    vals = [str(v) for v in values[:300] if v not in ("", None)]
    if not vals:
        return False
    wordy = sum(1 for v in vals if len(v.split()) >= 4)
    return wordy / len(vals) >= 0.3


def plan_columns(header, force_cols, keep_cols):
    force = {normalize_col(c) for c in force_cols}
    keep = {normalize_col(c) for c in keep_cols}
    plan = []
    for name in header:
        n = normalize_col(name)
        prefix = classify_column(name)
        if n in keep:
            action = "keep (you chose --keep)"
            prefix_used = None
        elif n in force:
            prefix_used = prefix if prefix and prefix not in FLAG_ONLY else "VALUE"
            action = "replace (you chose --columns)"
        elif prefix and prefix in FLAG_ONLY:
            prefix_used = None
            action = f"FLAG: looks like {prefix} data, kept as is (use --columns to replace, or round it)"
        elif prefix:
            prefix_used = prefix
            action = "replace with " + (FIXED_LABEL.get(prefix) or f"{prefix}_xxxxxxxx tokens")
        else:
            prefix_used = None
            action = "keep, but scan text for patterns"
        plan.append((name, prefix_used, action, n in keep))
    return plan


def redact_table(rows, tok, terms, force_cols, keep_cols):
    if not rows:
        return rows, []
    header = rows[0]
    plan = plan_columns(header, force_cols, keep_cols)
    out = [header]
    for r in rows[1:]:
        new = []
        for i, cell in enumerate(r):
            if i < len(plan):
                _, prefix, _, kept = plan[i]
            else:
                prefix, kept = None, False
            if cell == "" or cell is None:
                new.append(cell)
            elif prefix:
                new.append(tok.token(prefix, cell))
            elif kept:
                new.append(cell)
            else:
                new.append(scrub_text(str(cell), tok, terms))
        out.append(new)
    return out, plan


def infer_type(values):
    vals = [v for v in values if v not in ("", None)]
    if not vals:
        return "empty"
    def is_num(v):
        try:
            float(str(v).replace(",", ""))
            return True
        except ValueError:
            return False
    def is_date(v):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S", "%d-%b-%Y"):
            try:
                datetime.strptime(str(v)[:19], fmt)
                return True
            except ValueError:
                continue
        return False
    if all(is_num(v) for v in vals):
        return "integer" if all(re.fullmatch(r"-?\d+", str(v).replace(",", "")) for v in vals) else "decimal"
    if all(is_date(v) for v in vals):
        return "date"
    return "text"


def schema_summary(rows):
    header, body = rows[0], rows[1:]
    out = [["column", "type", "rows", "blanks", "distinct_values", "looks_sensitive"]]
    for i, name in enumerate(header):
        col = [r[i] if i < len(r) else "" for r in body]
        blanks = sum(1 for v in col if v in ("", None))
        distinct = len(set(v for v in col if v not in ("", None)))
        flag = classify_column(name) or ""
        if not flag:
            tok = Tokenizer("probe")
            hits = sum(1 for v in col[:500] if v and scrub_text(str(v), tok, []) != str(v))
            if hits:
                flag = "patterns found in values"
        out.append([name, infer_type(col), len(col), blanks, distinct, flag])
    return out


def parse_date(v):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S", "%d-%b-%Y"):
        try:
            return datetime.strptime(str(v)[:19], fmt).date()
        except ValueError:
            continue
    return None


def synthetic_rows(rows, n, seed=None):
    """Fake rows with the same columns and types. Real values are reused ONLY for
    short category columns (<= 12 distinct values) that are not flagged as sensitive."""
    rng = random.Random(seed)
    header, body = rows[0], rows[1:]
    gens = []
    for i, name in enumerate(header):
        col = [r[i] for r in body if i < len(r) and r[i] not in ("", None)]
        typ = infer_type(col)
        flagged = classify_column(name)
        distinct = sorted(set(col))
        if flagged and typ in ("integer", "decimal"):
            gens.append(lambda k: str(rng.randint(1000, 9999)))
        elif flagged:
            gens.append(lambda k, p=flagged: f"{p}_SAMPLE_{k:02d}")
        elif typ in ("integer", "decimal"):
            nums = [float(str(v).replace(",", "")) for v in col] or [0, 100]
            lo, hi = min(nums), max(nums)
            if typ == "integer":
                gens.append(lambda k, lo=int(lo), hi=int(hi): str(rng.randint(lo, max(lo, hi))))
            else:
                gens.append(lambda k, lo=lo, hi=hi: f"{rng.uniform(lo, hi):.2f}")
        elif typ == "date":
            parsed = [d for d in (parse_date(v) for v in col) if d]
            lo = min(parsed) if parsed else date(2024, 1, 1)
            span = max((max(parsed) - lo).days, 1) if parsed else 364
            gens.append(lambda k, lo=lo, span=span: (lo + timedelta(days=rng.randint(0, span))).isoformat())
        elif 0 < len(distinct) <= 12:
            gens.append(lambda k, d=distinct: rng.choice(d))
        else:
            gens.append(lambda k, nm=normalize_col(name)[:10] or "value": f"{nm}_sample_{k:02d}")
    out = [header]
    for k in range(1, n + 1):
        out.append([g(k) for g in gens])
    return out


# --------------------------------------------------------------------------
# JSON
# --------------------------------------------------------------------------

def redact_json(obj, tok, terms, force_cols, keep_cols, parent_key=None):
    force = {normalize_col(c) for c in force_cols}
    keep = {normalize_col(c) for c in keep_cols}
    if isinstance(obj, dict):
        return {k: redact_json(v, tok, terms, force_cols, keep_cols, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_json(v, tok, terms, force_cols, keep_cols, parent_key) for v in obj]
    if obj is None or isinstance(obj, bool):
        return obj
    n = normalize_col(parent_key) if parent_key else ""
    if n in keep:
        return obj
    prefix = classify_column(parent_key) if parent_key else None
    if n in force:
        prefix = prefix if prefix and prefix not in FLAG_ONLY else "VALUE"
    if prefix and prefix not in FLAG_ONLY:
        return tok.token(prefix, obj)
    if isinstance(obj, str):
        return scrub_text(obj, tok, terms)
    return obj


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def load_secret(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            s = f.read().strip()
        if s:
            return s, False
    s = secrets.token_hex(32)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return s, True


def write_csv(path, rows, delim=","):
    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter=delim).writerows(rows)


def safe_out(path, force):
    if os.path.exists(path) and not force:
        sys.exit(f"Stopped: {path} already exists. Delete it or add --force to overwrite it.")
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description="Make a safe, redacted copy of a data file. Runs locally only.")
    p.add_argument("input", help="file to redact (.csv .tsv .xlsx .json or any text file)")
    p.add_argument("--out", help="output file path (default: next to the input, with .redacted)")
    p.add_argument("--dry-run", action="store_true", help="preview what would be replaced; writes nothing")
    p.add_argument("--schema-only", action="store_true", help="write column names, types and counts only (no values)")
    p.add_argument("--synthetic", type=int, metavar="N", help="write N fake rows with the same columns and types")
    p.add_argument("--sheet", help="Excel sheet name (default: first sheet)")
    p.add_argument("--columns", default="", help="comma-separated extra columns to replace with tokens")
    p.add_argument("--keep", default="", help="comma-separated columns to leave exactly as they are")
    p.add_argument("--terms", help="text file with one name/term per line to replace everywhere (e.g. client names)")
    p.add_argument("--secret-file", default=os.path.join(os.path.expanduser("~"), ".holdmyhand_secret"),
                   help="file holding your private secret (created if missing). Same secret = same tokens across files")
    p.add_argument("--mapping", action="store_true",
                   help="ALSO write a token-to-original mapping file. Sensitive: keep it private, never share it")
    p.add_argument("--drop", default="", help="comma-separated columns to remove entirely (best for free-text notes you don't need)")
    p.add_argument("--pattern", action="append", default=[], metavar="REGEX",
                   help="extra pattern to replace, e.g. --pattern \"EMP-\\d{5}\" (repeatable). For ID formats the tool doesn't know")
    p.add_argument("--sequential", action="store_true",
                   help="use numbered tokens (CUSTOMER_001...) for this run only: can't be linked across files or reversed. Safest when you don't need joins")
    p.add_argument("--force", action="store_true", help="overwrite output files that already exist")
    p.add_argument("--version", action="version", version=f"holdmyhand redact {VERSION}")
    a = p.parse_args(argv)

    src = a.input
    if not os.path.isfile(src):
        sys.exit(f"File not found: {src}")
    base, ext = os.path.splitext(src)
    ext = ext.lower()
    force_cols = [c.strip() for c in a.columns.split(",") if c.strip()]
    keep_cols = [c.strip() for c in a.keep.split(",") if c.strip()]
    terms = []
    if a.terms:
        with open(a.terms, "r", encoding="utf-8-sig") as f:
            terms = sorted({ln.strip() for ln in f if ln.strip()}, key=len, reverse=True)

    secret, created = load_secret(a.secret_file)
    if created and not a.dry_run:
        print(f"Created a new private secret in {a.secret_file}. Keep it private; reuse it to keep tokens consistent.")
    drop_cols = [c.strip() for c in a.drop.split(",") if c.strip()]
    for rx in a.pattern:
        try:
            PATTERNS.insert(0, ("CUSTOM", re.compile(rx)))
        except re.error as e:
            sys.exit(f"Your --pattern {rx!r} isn't a valid pattern: {e}")
    if os.name == "posix":
        try:
            if os.stat(a.secret_file).st_mode & 0o077:
                print(f"Warning: your secret file {a.secret_file} can be read by other users. Run: chmod 600 {a.secret_file}")
        except OSError:
            pass
    print("=" * 72)
    print(" BEST-EFFORT REDACTION. It can miss names in sentences, unusual ID formats")
    print(" and non-standard layouts. You must review the output before sharing it.")
    print("=" * 72)
    tok = Tokenizer(secret, keep_mapping=a.mapping and not a.dry_run, sequential=a.sequential)

    # ---- load ----
    kind, rows, delim, label = None, None, ",", ""
    if ext in (".csv", ".tsv"):
        kind = "table"
        rows, delim = read_delimited(src)
    elif ext in (".xlsx", ".xlsm"):
        kind = "table"
        rows, sheet = read_xlsx(src, a.sheet)
        label = "." + re.sub(r"[^\w\-]", "_", sheet)
    elif ext == ".xls":
        sys.exit("Old .xls files aren't supported. In Excel: File > Save As > CSV or .xlsx, then run this again.")
    elif ext == ".json":
        kind = "json"
        with open(src, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    else:
        kind = "text"
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

    # ---- schema / synthetic ----
    if a.schema_only or a.synthetic:
        if kind != "table":
            sys.exit("--schema-only and --synthetic work with CSV, TSV and Excel files.")
        if a.schema_only:
            res = schema_summary(rows)
            outp = a.out or f"{base}{label}.schema.csv"
            if a.dry_run:
                print_table(res)
                return
            write_csv(safe_out(outp, a.force), res)
            print(f"Wrote schema summary (no data values) to {outp}")
            print_table(res)
        if a.synthetic:
            res = synthetic_rows(rows, a.synthetic)
            outp = (a.out if not a.schema_only else None) or f"{base}{label}.synthetic.csv"
            if a.dry_run:
                print_table(res)
                return
            write_csv(safe_out(outp, a.force), res)
            print(f"Wrote {a.synthetic} synthetic rows to {outp}. Check them before sharing.")
        return

    # ---- redact ----
    if kind == "table":
        if drop_cols:
            dn = {normalize_col(c) for c in drop_cols}
            idx = [i for i, h in enumerate(rows[0]) if normalize_col(h) not in dn]
            dropped = [h for h in rows[0] if normalize_col(h) in dn]
            rows = [[r[i] if i < len(r) else "" for i in idx] for r in rows]
            if dropped:
                print("Removed columns: " + ", ".join(dropped))
        res, plan = redact_table(rows, tok, terms, force_cols, keep_cols)
        print(f"Columns ({len(plan)}), {max(len(rows) - 1, 0)} data rows:")
        for i, (name, prefix, action, _) in enumerate(plan):
            note = ""
            if not prefix and looks_free_text([r[i] for r in rows[1:] if i < len(r)]):
                note = "  << FREE TEXT: names or details in sentences may be missed. Consider --drop or --terms"
            print(f"  - {name}: {action}{note}")
        outp = a.out or f"{base}{label}.redacted.csv"
    elif kind == "json":
        res = redact_json(data, tok, terms, force_cols, keep_cols)
        outp = a.out or f"{base}.redacted.json"
    else:
        res = scrub_text(text, tok, terms)
        outp = a.out or f"{base}.redacted{ext or '.txt'}"

    print("\nReplacements by type:")
    if tok.counts:
        for k, v in sorted(tok.counts.items()):
            print(f"  {k}: {v}")
    else:
        print("  none found (that does NOT prove the file is safe; check it yourself)")

    if a.dry_run:
        print("\nDry run: nothing was written. Run again without --dry-run to create the safe copy.")
        return

    if os.path.abspath(outp) == os.path.abspath(src):
        sys.exit("Stopped: the output would overwrite the original file.")
    safe_out(outp, a.force)
    if kind == "table":
        write_csv(outp, res, delim if ext in (".csv", ".tsv") else ",")
    elif kind == "json":
        with open(outp, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
    else:
        with open(outp, "w", encoding="utf-8") as f:
            f.write(res)
    print(f"\nWrote safe copy to {outp}")

    if a.mapping:
        mp = f"{base}.MAPPING-PRIVATE.csv"
        write_csv(safe_out(mp, a.force), [["token", "original"]] + sorted(tok.mapping.items()))
        print(f"Wrote PRIVATE mapping to {mp}. Do not share it; store it securely or delete it when done.")

    print("\nREVIEW BEFORE SHARING: open the safe copy and read it. Automatic detection can miss")
    print("names in free text and ID formats it doesn't know. Use --drop, --terms, --columns or")
    print("--pattern to catch more. Your company's policy comes first.")


def print_table(rows, limit=25):
    for r in rows[:limit + 1]:
        print("  " + " | ".join(str(c) for c in r))
    if len(rows) > limit + 1:
        print(f"  ... ({len(rows) - 1} rows)")


if __name__ == "__main__":
    main()
