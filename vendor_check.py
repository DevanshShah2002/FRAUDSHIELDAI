# Simple vendor domain trust scoring using string similarity heuristics.
import difflib
import tldextract

# known vendor list (in prod, this would be a DB of trusted vendors)
KNOWN_VENDORS = [
    "microsoft.com", "google.com", "amazon.com", "paypal.com", "bankofamerica.com"
]

def normalize_domain(domain):
    if not domain:
        return ''
    ext = tldextract.extract(domain)
    if not ext.domain:
        return domain.lower()
    return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain.lower()

def vendor_trust_score(domain):
    domain = normalize_domain(domain)
    if not domain:
        return 0.0
    # exact match
    if domain in KNOWN_VENDORS:
        return 0.99
    # similarity to known vendors
    best = 0.0
    for kv in KNOWN_VENDORS:
        s = difflib.SequenceMatcher(None, domain, kv).ratio()
        if s > best:
            best = s
    # penalize if similarity is high but not exact (lookalike)
    if best > 0.7 and domain not in KNOWN_VENDORS:
        # suspicious lookalike
        return round(0.3 + (0.7 - best), 2)
    # otherwise give a neutral score
    return round(0.5 * best, 2)
