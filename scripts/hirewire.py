"""HireWire job pipeline: fetch, deduplicate, prefilter, batch for the classifier and merge results.

Usage (from the repository root):
    python scripts/hirewire.py check
    python scripts/hirewire.py fetch [--source NAME] [--with-apify]
    python scripts/hirewire.py batch [--size 20] [--limit N]
    python scripts/hirewire.py merge
    python scripts/hirewire.py status
    python scripts/hirewire.py sources
    python scripts/hirewire.py refilter
    python scripts/hirewire.py test-prefilter

Python standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent
PROFILE = BASE / "profile"
CONFIG = PROFILE / "search.json"
DATA = BASE / "data"
BATCHES = DATA / "batches"
JOBS = DATA / "jobs.jsonl"
CLASSIFICATION = DATA / "classification.jsonl"
RUNS = DATA / "runs.jsonl"
ENV = BASE / ".env"

USER_AGENT = "Mozilla/5.0 (hirewire-remote-job-scout)"
TRACKING = {"fbclid", "gclid", "msclkid", "ref", "source", "trk", "refid", "trackingid"}
DESCRIPTION_MAX = 6000
BATCH_DESCRIPTION_MAX = 3500

GEO_HINTS = [
    r"authori[sz]ed to work in",
    r"must (be )?(based|located|reside|live) in",
    r"[a-z.]+[- ]based (candidates|applicants|only)",
    r"residents? (of|in) the",
    r"remote\s*[-–(,]\s*[a-z. ]{2,20}\)?",
    r"visa sponsorship",
    r"w-?2",
    r"anywhere|worldwide|work from any|fully distributed",
    r"time ?zones?|\best\b|\bpst\b|\bcst\b|\bcet\b|utc|gmt",
    r"hybrid|on-?site|in[- ]office|presencial|h[ií]brid",
]

EXPECTED_FIELDS = {
    "id", "geo", "geo_evidence", "market", "contract", "route", "duties", "level",
    "blockers", "gaps", "evidence", "alerts", "priority", "reason",
}
LIST_FIELDS = ("duties", "blockers", "gaps", "evidence", "alerts")
ALLOWED = {
    "geo": {"eligible", "not_eligible", "unclear"},
    "market": {"foreign", "local", "unknown"},
    "contract": {"contractor", "employee", "unknown"},
    "level": {"junior", "mid", "senior", "lead", "director", "unknown"},
    "priority": {"A", "B", "C", "discard"},
}


# ---------- config ----------

def load_config() -> dict:
    if not CONFIG.exists():
        raise SystemExit("profile/search.json not found. Run the /routes step first (it creates it from templates/search.json).")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def local_tz(config: dict) -> timezone:
    return timezone(timedelta(hours=float(config["candidate"].get("utc_offset", 0))))


def today(config: dict) -> date:
    return datetime.now(local_tz(config)).date()


# ---------- utilities ----------

def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize(text: str) -> str:
    plain = unicodedata.normalize("NFKD", str(text).casefold())
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", plain).strip()


def contains(text: str, term: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(normalize(term)), normalize(text)) is not None


def canonical_url(value: str) -> str:
    parts = urlsplit(str(value).strip())
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in TRACKING]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/") or "/",
                       urlencode(sorted(query)), ""))


def job_id(url: str) -> str:
    return hashlib.sha256(canonical_url(url).encode("utf-8")).hexdigest()[:12]


def fingerprint(company: str, title: str) -> str:
    """Identifies the same position posted on different sources."""
    t = re.sub(r"\(.*?\)|\[.*?\]", " ", normalize(title))
    t = re.sub(r"\b(remote|remoto|latam|contract|contractor|full[- ]?time|part[- ]?time)\b", " ", t)
    c = re.sub(r"\b(inc|llc|ltd|corp|gmbh|s\.?a\.?)\b\.?", " ", normalize(company))
    return re.sub(r"[^a-z0-9]+", "", c) + "|" + re.sub(r"[^a-z0-9]+", "", t)


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        elif tag in {"br", "p", "li", "div", "h1", "h2", "h3", "h4", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def plain_text(html: object) -> str:
    p = _Text()
    p.feed(str(html or ""))
    text = re.sub(r"[ \t]+", " ", "".join(p.parts))
    return re.sub(r"\n\s*\n+", "\n", text).strip()


def iso_date(value: object, tz: timezone) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, (int, float)):
        ts = float(value) / (1000 if abs(float(value)) >= 1e12 else 1)
        return datetime.fromtimestamp(ts, timezone.utc).astimezone(tz).date().isoformat()
    try:
        d = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return ""
    return (d.astimezone(tz) if d.tzinfo else d).date().isoformat()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tmp.replace(path)


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def get_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def get_text(url: str, browser: bool = False) -> str:
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" if browser else USER_AGENT
    with urlopen(Request(url, headers={"User-Agent": agent}), timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def known_urls() -> set[str]:
    return {canonical_url(j["url"]) for j in read_jsonl(JOBS)}


# ---------- sources ----------

def source_himalayas(conf: dict, config: dict) -> list[dict]:
    """Himalayas public API. Free, no key. Filters by the candidate's country."""
    tz = local_tz(config)
    jobs = []
    for query in conf["queries"]:
        for page in range(1, int(conf.get("max_pages", 3)) + 1):
            url = "https://himalayas.app/jobs/api/search?" + urlencode(
                {"q": query, "country": config["candidate"]["country_code"], "sort": "recent", "page": page})
            try:
                data = get_json(url)
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
                print(f"  himalayas '{query}' p{page}: error {error}", file=sys.stderr)
                break
            for item in data.get("jobs", []):
                countries = item.get("locationRestrictions") or []
                jobs.append({
                    "title": item.get("title", ""),
                    "company": item.get("companyName", ""),
                    "url": item.get("guid", ""),
                    "apply_url": item.get("applicationLink", ""),
                    "location": ", ".join(countries) if countries else "No country restriction listed",
                    "timezones": ", ".join(str(z) for z in item.get("timezoneRestrictions") or []),
                    "employment_type": item.get("employmentType", ""),
                    "seniority": ", ".join(item.get("seniority") or []),
                    "salary": _salary(item),
                    "posted": iso_date(item.get("pubDate"), tz),
                    "expires": iso_date(item.get("expiryDate"), tz),
                    "description": plain_text(item.get("description") or item.get("excerpt"))[:DESCRIPTION_MAX],
                    "source": "Himalayas",
                    "query": query,
                })
            seen = data.get("offset", 0) + len(data.get("jobs", []))
            if not data.get("jobs") or seen >= data.get("totalCount", 0):
                break
            time.sleep(0.5)
        print(f"  himalayas '{query}': {sum(1 for j in jobs if j['query'] == query)} received")
    return jobs


def _salary(item: dict) -> str:
    lo, hi, cur = item.get("minSalary"), item.get("maxSalary"), item.get("currency") or ""
    if not lo and not hi:
        return ""
    return f"{lo or ''}–{hi or ''} {cur} {item.get('salaryPeriod') or ''}".strip()


def apify_token() -> str:
    if ENV.exists():
        m = re.search(r"^APIFY_TOKEN=(\S+)", ENV.read_text(encoding="utf-8"), flags=re.MULTILINE)
        if m:
            return m.group(1)
    raise SystemExit("APIFY_TOKEN missing in .env (copy .env.example to .env and paste your token).")


def apify(method: str, path: str, body: dict | None = None) -> dict | list:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = Request("https://api.apify.com/v2/" + path, data=data, method=method, headers={
        "Authorization": "Bearer " + apify_token(), "Content-Type": "application/json"})
    with urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def run_actor(actor: str, payload: dict, max_spend: float) -> tuple[list[dict], float]:
    """Runs an Apify actor with a hard spending cap. Returns (items, cost_usd)."""
    run = apify("POST", f"acts/{actor}/runs?maxTotalChargeUsd={max_spend}&timeout=1800", payload)["data"]
    print(f"  run {run['id']} started (cap USD {max_spend})")
    while run["status"] in {"READY", "RUNNING"}:
        time.sleep(15)
        run = apify("GET", f"actor-runs/{run['id']}")["data"]
    items = apify("GET", f"datasets/{run['defaultDatasetId']}/items?clean=true&format=json")
    raw = DATA / "raw" / f"{datetime.now():%Y-%m-%d_%H%M}_{actor.split('~')[-1]}.json"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    cost = float(run.get("usageTotalUsd") or 0)
    print(f"  status {run['status']}, {len(items)} jobs, cost USD {cost:.3f}")
    return items, cost


def source_remotive(conf: dict, config: dict) -> list[dict]:
    """Remotive public API. Free, no key; one request for the whole public feed."""
    tz = local_tz(config)
    try:
        data = get_json("https://remotive.com/api/remote-jobs")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"  remotive: error {error}", file=sys.stderr)
        return []
    jobs = [{
        "title": item.get("title", ""),
        "company": item.get("company_name", ""),
        "url": item.get("url", ""),
        "apply_url": item.get("url", ""),
        "location": item.get("candidate_required_location", ""),
        "timezones": "",
        "employment_type": item.get("job_type", ""),
        "seniority": "",
        "salary": item.get("salary", ""),
        "posted": iso_date(item.get("publication_date"), tz),
        "expires": "",
        "description": plain_text(item.get("description"))[:DESCRIPTION_MAX],
        "source": "Remotive",
        "query": "",
    } for item in data.get("jobs", [])]
    print(f"  remotive: {len(jobs)} received")
    return jobs


def source_weworkremotely(conf: dict, config: dict) -> list[dict]:
    """We Work Remotely RSS feeds. Free, no key."""
    jobs = []
    for feed in conf.get("feeds", ["https://weworkremotely.com/remote-jobs.rss"]):
        try:
            root = ElementTree.fromstring(get_text(feed))
        except (HTTPError, URLError, TimeoutError, ElementTree.ParseError) as error:
            print(f"  weworkremotely {feed}: error {error}", file=sys.stderr)
            continue
        for item in root.iter("item"):
            field = lambda name: (item.findtext(name) or "").strip()  # noqa: E731
            company, _, title = field("title").partition(": ")
            try:
                posted = parsedate_to_datetime(field("pubDate")).date().isoformat()
            except (TypeError, ValueError):
                posted = ""
            jobs.append({
                "title": title or company,
                "company": company if title else "",
                "url": field("link") or field("guid"),
                "apply_url": field("link"),
                "location": ", ".join(x for x in (field("region"), field("country")) if x),
                "timezones": "",
                "employment_type": field("type"),
                "seniority": "",
                "salary": "",
                "posted": posted,
                "expires": field("expires_at")[:10],
                "description": plain_text(field("description"))[:DESCRIPTION_MAX],
                "source": "We Work Remotely",
                "query": field("category"),
            })
        time.sleep(1)
    print(f"  weworkremotely: {len(jobs)} received")
    return jobs


def source_jobicy(conf: dict, config: dict) -> list[dict]:
    """Jobicy public API. Free, no key. One request per query, filtered by region."""
    tz = local_tz(config)
    jobs = []
    for query in conf["queries"]:
        params = {"count": 50, "tag": query}
        if conf.get("geo"):
            params["geo"] = conf["geo"]
        try:
            data = get_json("https://jobicy.com/api/v2/remote-jobs?" + urlencode(params))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"  jobicy '{query}': error {error}", file=sys.stderr)
            continue
        for item in data.get("jobs", []):
            lo, hi = item.get("salaryMin"), item.get("salaryMax")
            jobs.append({
                "title": item.get("jobTitle", ""),
                "company": item.get("companyName", ""),
                "url": item.get("url", ""),
                "apply_url": item.get("url", ""),
                "location": item.get("jobGeo", ""),
                "timezones": "",
                "employment_type": ", ".join(item.get("jobType") or []) if isinstance(item.get("jobType"), list) else str(item.get("jobType") or ""),
                "seniority": item.get("jobLevel", ""),
                "salary": f"{lo or ''}–{hi or ''} {item.get('salaryCurrency') or ''} {item.get('salaryPeriod') or ''}".strip() if lo or hi else "",
                "posted": iso_date(item.get("pubDate"), tz),
                "expires": "",
                "description": plain_text(item.get("jobDescription"))[:DESCRIPTION_MAX],
                "source": "Jobicy",
                "query": query,
            })
        time.sleep(1)
    print(f"  jobicy: {len(jobs)} received")
    return jobs


def source_builtin(conf: dict, config: dict) -> list[dict]:
    """Built In remote jobs for the candidate's country. Free: reads the public job pages and their structured data.
    Only opens job pages not seen before, with a pause between requests."""
    tz = local_tz(config)
    seen = known_urls()
    links: list[tuple[str, str]] = []
    for query in conf["queries"]:
        url = "https://builtin.com/jobs/remote?" + urlencode({"search": query, "country": conf["country"], "allLocations": "true"})
        try:
            page = get_text(url, browser=True)
        except (HTTPError, URLError, TimeoutError) as error:
            print(f"  builtin '{query}': error {error}", file=sys.stderr)
            continue
        for path in dict.fromkeys(re.findall(r'href="(/job/[^"]+)"', page)):
            full = "https://builtin.com" + path
            if canonical_url(full) not in seen and full not in (l for l, _ in links):
                links.append((full, query))
        time.sleep(1)
    jobs = []
    for full, query in links[:int(conf.get("max_new_per_run", 80))]:
        try:
            page = get_text(full, browser=True)
        except (HTTPError, URLError, TimeoutError) as error:
            print(f"  builtin {full}: error {error}", file=sys.stderr)
            continue
        time.sleep(1)
        posting = None
        for block in re.findall(r'<script type="application/ld(?:\+|&#x2B;)json">(.*?)</script>', page, re.S):
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue
            posting = next((x for x in data.get("@graph", [data]) if x.get("@type") == "JobPosting"), posting)
        if not posting or posting.get("jobLocationType") != "TELECOMMUTE":
            continue
        countries = [c.get("name", "") for c in posting.get("applicantLocationRequirements") or [] if isinstance(c, dict)]
        jobs.append({
            "title": posting.get("title", ""),
            "company": (posting.get("hiringOrganization") or {}).get("name", ""),
            "url": full,
            "apply_url": full,
            "location": "Remote: " + (", ".join(countries) if countries else "no country listed"),
            "timezones": "",
            "employment_type": str(posting.get("employmentType", "")),
            "seniority": "",
            "salary": "",
            "posted": iso_date(posting.get("datePosted"), tz),
            "expires": iso_date(posting.get("validThrough"), tz),
            "description": plain_text(posting.get("description"))[:DESCRIPTION_MAX],
            "source": "Built In",
            "query": query,
        })
    print(f"  builtin: {len(links)} new links, {len(jobs)} remote jobs read")
    return jobs


def source_getonboard(conf: dict, config: dict) -> list[dict]:
    """Get on Board public API (tech jobs, Latin America). Free, no key. Keeps remote jobs only."""
    tz = local_tz(config)
    jobs = []
    for query in conf["queries"]:
        url = "https://www.getonbrd.com/api/v0/search/jobs?" + urlencode({"query": query, "per_page": 50}) + "&expand=" + quote('["company"]')
        try:
            data = get_json(url)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"  getonboard '{query}': error {error}", file=sys.stderr)
            continue
        for item in data.get("data", []):
            a = item.get("attributes", {})
            if not a.get("remote"):
                continue
            company = ((a.get("company") or {}).get("data") or {}).get("attributes", {}).get("name", "")
            jobs.append({
                "title": a.get("title", ""),
                "company": company,
                "url": (item.get("links") or {}).get("public_url", ""),
                "apply_url": (item.get("links") or {}).get("public_url", ""),
                "location": f"{a.get('remote_modality', '')}: " + ", ".join(a.get("countries") or []),
                "timezones": "",
                "employment_type": "",
                "seniority": "",
                "salary": f"{a.get('min_salary')}–{a.get('max_salary')} USD month" if a.get("min_salary") else "",
                "posted": iso_date(a.get("published_at"), tz),
                "expires": "",
                "description": plain_text(" ".join(str(a.get(k) or "") for k in ("description", "functions", "desirable", "benefits")))[:DESCRIPTION_MAX],
                "source": "Get on Board",
                "query": query,
            })
        time.sleep(1)
    print(f"  getonboard: {len(jobs)} remote jobs received")
    return jobs


def run_actor_many(actor: str, payloads: list[dict], max_spend: float) -> tuple[list[dict], float]:
    """One run per payload, in parallel, splitting the spending cap. Returns (items, cost_usd)."""
    cap = round(max_spend / max(len(payloads), 1), 4)
    runs = [apify("POST", f"acts/{actor}/runs?maxTotalChargeUsd={cap}&timeout=900", p)["data"] for p in payloads]
    print(f"  {len(runs)} runs started (cap USD {cap} each, USD {max_spend} total)")
    while any(r["status"] in {"READY", "RUNNING"} for r in runs):
        time.sleep(15)
        runs = [apify("GET", f"actor-runs/{r['id']}")["data"] if r["status"] in {"READY", "RUNNING"} else r for r in runs]
    items, cost = [], 0.0
    for payload, run in zip(payloads, runs):
        batch = apify("GET", f"datasets/{run['defaultDatasetId']}/items?clean=true&format=json")
        for item in batch:
            item["_input"] = payload
        items += batch
        cost += float(run.get("usageTotalUsd") or 0)
    raw = DATA / "raw" / f"{datetime.now():%Y-%m-%d_%H%M}_{actor.split('~')[-1]}.json"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(items)} jobs, cost USD {cost:.3f}")
    return items, cost


def source_apify_indeed(conf: dict, config: dict) -> list[dict]:
    """Indeed through an Apify actor, on the candidate's country site. Spends Apify credit."""
    tz = local_tz(config)
    country = conf.get("country") or config["candidate"]["country_code"].lower()
    payloads = [{"country": country, "query": q, "location": conf.get("location", ""),
                 "postedWithinDays": str(conf.get("posted_within_days", "14")), "count": int(conf["max_per_query"])}
                for q in conf["queries"]]
    items, cost = run_actor_many(conf["actor"], payloads, float(conf["max_spend_usd"]))
    source_apify_indeed.cost = cost
    host = "www" if country == "us" else country
    jobs = []
    for item in items:
        key = item.get("id") or dict(parse_qsl(urlsplit(item.get("viewJobLink", "")).query)).get("jk")
        if not key or item.get("expired"):
            continue
        jobs.append({
            "title": item.get("title", ""),
            "company": (item.get("companyDetails") or {}).get("name", ""),
            "url": f"https://{host}.indeed.com/viewjob?jk={key}",
            "apply_url": item.get("originalApplyUrl", ""),
            "location": item.get("formattedLocation", ""),
            "timezones": "",
            "employment_type": ", ".join(a.get("label", "") for a in item.get("attributes") or [] if a.get("label")),
            "seniority": "",
            "salary": "",
            "posted": iso_date(item.get("pubDate"), tz),
            "expires": iso_date(item.get("expirationDate"), tz),
            "description": (item.get("jobDescription") or plain_text(item.get("jobDescriptionHTML")))[:DESCRIPTION_MAX],
            "source": "Indeed",
            "query": item["_input"]["query"],
        })
    return jobs


def source_apify_linkedin(conf: dict, config: dict) -> list[dict]:
    """LinkedIn remote jobs through an Apify actor. Spends Apify credit."""
    tz = local_tz(config)
    urls = []
    for query in conf["queries"]:
        params = {"keywords": query, "location": conf["location"], "f_WT": "2", "f_TPR": conf.get("period", "r604800")}
        if conf.get("geo_id"):
            params["geoId"] = conf["geo_id"]
        urls.append("https://www.linkedin.com/jobs/search/?" + urlencode(params))
    items, cost = run_actor(conf["actor"], {
        "urls": urls, "limitPerSource": int(conf["max_per_query"]), "scrapeCompany": False,
    }, float(conf["max_spend_usd"]))
    source_apify_linkedin.cost = cost
    jobs = []
    for item in items:
        if not item.get("id"):
            continue
        query = dict(parse_qsl(urlsplit(item.get("inputUrl", "")).query)).get("keywords", "")
        jobs.append({
            "title": item.get("title", ""),
            "company": item.get("companyName", ""),
            "url": f"https://www.linkedin.com/jobs/view/{item['id']}",
            "apply_url": item.get("applyUrl", ""),
            "location": item.get("location", ""),
            "timezones": "",
            "employment_type": item.get("employmentType", ""),
            "seniority": item.get("seniorityLevel", ""),
            "salary": item.get("salary", "") if isinstance(item.get("salary"), str) else "",
            "posted": iso_date(item.get("postedAt"), tz),
            "expires": "",
            "description": (item.get("descriptionText") or plain_text(item.get("descriptionHtml")))[:DESCRIPTION_MAX],
            "source": "LinkedIn",
            "query": query,
            "applicants": item.get("applicantsCount", ""),
        })
    return jobs


SOURCES = {
    "himalayas": source_himalayas,
    "builtin": source_builtin,
    "weworkremotely": source_weworkremotely,
    "remotive": source_remotive,
    "jobicy": source_jobicy,
    "getonboard": source_getonboard,
    "apify_linkedin": source_apify_linkedin,
    "apify_indeed": source_apify_indeed,
}


# ---------- prefilter ----------

def prefilter(job: dict, conf: dict, oldest: date, today_: date) -> tuple[str, str]:
    """Discards only the obvious. Everything else goes to the classifier."""
    company = normalize(job["company"])
    for excluded in conf["excluded_companies"]:
        if normalize(excluded) == company or contains(job["company"], excluded):
            return "auto_discarded", f"Excluded company: {job['company']}"
    text = normalize(" ".join([job["title"], job.get("location", ""), job["description"]]))
    for pattern in conf.get("geo_exclusions", []):
        m = re.search(pattern, text)
        if m:
            return "auto_discarded", f"Not eligible (location): «{text[max(0, m.start() - 40):m.end() + 40].strip()}»"
    says_remote = job["source"] in conf.get("remote_only_sources", []) or any(re.search(p, text) for p in conf.get("remote_signals", []))
    if not says_remote:
        for pattern in conf.get("mode_exclusions", []):
            m = re.search(pattern, text)
            if m:
                return "auto_discarded", f"Not eligible (work mode): «{text[max(0, m.start() - 40):m.end() + 40].strip()}»"
        if job["source"] in conf.get("remote_required_sources", []):
            return "auto_discarded", "Not eligible (work mode): the listing never says the job is remote"
    title = job["title"]
    if not any(contains(title, t) for t in conf["route_title_terms"]):
        foreign = next((t for t in conf["foreign_title_terms"] if contains(title, t)), None)
        if foreign:
            return "auto_discarded", f"Title from another field ({foreign})"
        signals = [t for t in conf.get("description_signals", []) if contains(job["description"], t)]
        if len(signals) < int(conf.get("min_description_signals", 0)):
            return "auto_discarded", "No link to the search routes in title or description" + (f" (only: {signals[0]})" if signals else "")
    if job.get("posted"):
        try:
            if date.fromisoformat(job["posted"]) < oldest:
                return "auto_discarded", f"Posted {job['posted']} (older than the limit)"
        except ValueError:
            pass
    if job.get("expires"):
        try:
            if date.fromisoformat(job["expires"]) < today_:
                return "auto_discarded", f"Expired {job['expires']}"
        except ValueError:
            pass
    return "pending", ""


def geo_hints(description: str, regions: list[str]) -> list[str]:
    """Sentences relevant to location eligibility, as a hint for the classifier."""
    text = description.replace("\n", " ")
    patterns = GEO_HINTS + [re.escape(r) for r in regions]
    hints = []
    for pattern in patterns:
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            snippet = "…" + text[max(0, m.start() - 80):min(len(text), m.end() + 80)].strip() + "…"
            if snippet not in hints:
                hints.append(snippet)
            if len(hints) >= 8:
                return hints
    return hints


# ---------- commands ----------

def cmd_check(args) -> int:
    """Validates the profile folder before a search."""
    problems = []
    for name in ("EVIDENCE.md", "ROUTES.md", "search.json"):
        if not (PROFILE / name).exists():
            problems.append(f"missing profile/{name}")
    if not problems:
        config = load_config()
        for key in ("country_code", "residence_country", "utc_offset", "work_authorization", "eligible_regions", "work_mode"):
            if key not in config.get("candidate", {}):
                problems.append(f"candidate.{key} missing in search.json")
        if not config.get("routes"):
            problems.append("no routes in search.json")
        prefilter_conf = config.get("prefilter", {})
        patterns = [p for k in ("geo_exclusions", "mode_exclusions", "remote_signals") for p in prefilter_conf.get(k, [])]
        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error as e:
                problems.append(f"invalid pattern {pattern!r}: {e}")
        active = [n for n, c in config.get("sources", {}).items() if c.get("enabled")]
        if not active:
            problems.append("no enabled sources")
        if any(config["sources"][n].get("requires_apify") for n in active) and not ENV.exists():
            problems.append("an Apify source is enabled but .env does not exist")
    print(json.dumps({"ok": not problems, "problems": problems}, ensure_ascii=False, indent=2))
    return 1 if problems else 0


def cmd_fetch(args) -> int:
    config = load_config()
    today_ = today(config)
    oldest = today_ - timedelta(days=int(config.get("max_age_days", 21)))
    regions = config["candidate"].get("eligible_regions", [])
    existing = read_jsonl(JOBS)
    by_id = {j["id"]: j for j in existing}
    by_fp = {j["fingerprint"]: j for j in existing}
    summary = {"date": now(), "received": 0, "new": 0, "duplicates": 0, "pending": 0, "auto_discarded": 0, "sources": {}}

    for name, function in SOURCES.items():
        conf = config.get("sources", {}).get(name, {})
        if not conf.get("enabled") or (args.source and args.source != name):
            continue
        if conf.get("requires_apify") and not args.with_apify:
            print(f"Skipped {name}: spends Apify credit (add --with-apify)")
            continue
        print(f"Querying {name}…")
        received = function(conf, config)
        summary["sources"][name] = len(received)
        if hasattr(function, "cost"):
            summary.setdefault("cost_usd", {})[name] = round(function.cost, 4)
        summary["received"] += len(received)
        for job in received:
            if not job.get("url") or not job.get("title"):
                continue
            job["id"] = job_id(job["url"])
            job["fingerprint"] = fingerprint(job["company"], job["title"])
            previous = by_id.get(job["id"]) or by_fp.get(job["fingerprint"])
            if previous:
                summary["duplicates"] += 1
                others = previous.setdefault("other_sources", [])
                ref = f"{job['source']}: {job['url']}"
                if job["url"] != previous["url"] and ref not in others:
                    others.append(ref)
                continue
            state, reason = prefilter(job, config["prefilter"], oldest, today_)
            job.update({"seen": now(), "prefilter": state, "prefilter_reason": reason,
                        "geo_hints": geo_hints(job["description"], regions)})
            existing.append(job)
            by_id[job["id"]] = job
            by_fp[job["fingerprint"]] = job
            summary["new"] += 1
            summary["pending" if state == "pending" else "auto_discarded"] += 1

    write_jsonl(JOBS, existing)
    append_jsonl(RUNS, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def unclassified() -> list[dict]:
    done = {c["id"] for c in read_jsonl(CLASSIFICATION)}
    return [j for j in read_jsonl(JOBS) if j["prefilter"] == "pending" and j["id"] not in done]


def relevance(job: dict, conf: dict) -> tuple:
    """Cheap ranking so the classifier reads the most promising listings first."""
    title_hits = sum(contains(job["title"], t) for t in conf.get("route_title_terms", []))
    signals = sum(contains(job["description"], t) for t in conf.get("description_signals", []))
    return (min(title_hits, 2), min(signals, 8), job.get("posted") or "")


def cmd_batch(args) -> int:
    BATCHES.mkdir(parents=True, exist_ok=True)
    for old in BATCHES.glob("batch_*.json"):
        old.unlink()
    config = load_config()
    pending = sorted(unclassified(), key=lambda j: relevance(j, config["prefilter"]), reverse=True)
    limit = args.limit if args.limit is not None else int(config.get("max_classify_per_run", 60))
    selected = pending[:limit] if limit > 0 else pending
    fields = ("id", "title", "company", "location", "timezones", "employment_type", "seniority",
              "salary", "posted", "source", "geo_hints")
    n = 0
    for i in range(0, len(selected), args.size):
        n += 1
        batch = [{**{f: j.get(f, "") for f in fields}, "description": j.get("description", "")[:BATCH_DESCRIPTION_MAX]}
                 for j in selected[i:i + args.size]]
        (BATCHES / f"batch_{n:03d}.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"pending": len(pending), "selected": len(selected), "left_for_next_run": len(pending) - len(selected),
                      "batches": n, "folder": str(BATCHES)}, ensure_ascii=False))
    return 0


def cmd_refilter(args) -> int:
    """Applies the current prefilter to jobs not yet classified. With --location, only the location rules, to every job."""
    config = load_config()
    today_ = today(config)
    oldest = date.min if args.location else today_ - timedelta(days=int(config.get("max_age_days", 21)))
    jobs = read_jsonl(JOBS)
    if args.location:
        pending = {j["id"] for j in jobs if j["prefilter"] == "pending"}
    else:
        pending = {j["id"] for j in unclassified()}
    changed = 0
    for job in jobs:
        if job["id"] in pending:
            state, reason = prefilter(job, config["prefilter"], oldest, today_)
            if state != "pending" and (not args.location or reason.startswith("Not eligible")):
                job["prefilter"], job["prefilter_reason"] = state, reason
                changed += 1
    write_jsonl(JOBS, jobs)
    print(json.dumps({"checked": len(pending), "discarded_now": changed}, ensure_ascii=False))
    return 0


def cmd_test_prefilter(args) -> int:
    """Measures the prefilter against existing classifications: noise removed and good jobs lost."""
    config = load_config()
    jobs = {j["id"]: j for j in read_jsonl(JOBS)}
    lost, removed, total = [], 0, 0
    for c in read_jsonl(CLASSIFICATION):
        j = jobs.get(c["id"])
        if not j:
            continue
        state, _ = prefilter(j, config["prefilter"], date.min, date.min)
        if c["priority"] == "discard":
            total += 1
            removed += state != "pending"
        elif state != "pending":
            lost.append(f"{c['priority']}: {j['title']}")
    print(json.dumps({"noise_removed": f"{removed}/{total}", "good_jobs_lost": lost}, ensure_ascii=False, indent=2))
    return 1 if lost else 0


def validate(row: dict, valid_ids: set[str], routes: set[str]) -> str:
    missing = EXPECTED_FIELDS - row.keys()
    if missing:
        return f"missing fields {sorted(missing)}"
    if row["id"] not in valid_ids:
        return "unknown id"
    for field, allowed in {**ALLOWED, "route": routes | {"none"}}.items():
        if row[field] not in allowed:
            return f"{field}={row[field]!r} not allowed"
    for field in LIST_FIELDS:
        if not isinstance(row[field], list):
            return f"{field} must be a list"
    if row["geo"] == "eligible" and not str(row["geo_evidence"]).strip():
        return "geo eligible without evidence"
    return ""


def cmd_merge(args) -> int:
    routes = set(load_config()["routes"])
    valid_ids = {j["id"] for j in read_jsonl(JOBS)}
    current = {c["id"]: c for c in read_jsonl(CLASSIFICATION)}
    added, errors = 0, []
    for path in sorted(BATCHES.glob("batch_*.result.jsonl")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{path.name}:{n} invalid JSON ({e})")
                continue
            problem = validate(row, valid_ids, routes)
            if problem:
                errors.append(f"{path.name}:{n} {problem}")
                continue
            row["classified"] = now()
            current[row["id"]] = row
            added += 1
    write_jsonl(CLASSIFICATION, list(current.values()))
    remaining = len(unclassified())
    if not errors:
        for path in BATCHES.glob("batch_*.result.jsonl"):
            path.unlink()
        for path in BATCHES.glob("batch_*.json"):
            ids = {j["id"] for j in json.loads(path.read_text(encoding="utf-8"))}
            if ids <= current.keys():
                path.unlink()
    print(json.dumps({"merged": added, "errors": errors, "unclassified": remaining}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def next_stage() -> tuple[str, dict]:
    """Where the user is in the workflow, and the facts behind it."""
    facts: dict = {}
    if not (PROFILE / "EVIDENCE.md").exists():
        return "profile", facts
    if not (PROFILE / "ROUTES.md").exists() or not CONFIG.exists():
        return "routes", facts
    statuses = json.loads((DATA / "statuses.json").read_text(encoding="utf-8")) if (DATA / "statuses.json").exists() else {}
    with_cv = set()
    for meta in (BASE / "applications").glob("*/meta.json"):
        try:
            with_cv.add(json.loads(meta.read_text(encoding="utf-8")).get("job_id"))
        except json.JSONDecodeError:
            pass
    waiting = [i for i, s in statuses.items() if s.get("status") == "interested" and i not in with_cv]
    runs = read_jsonl(RUNS)
    facts.update(interested_without_cv=len(waiting), last_search=runs[-1]["date"][:10] if runs else "",
                 unclassified=len(unclassified()))
    if not runs:
        return "search", facts
    if facts["unclassified"]:
        return "classify", facts
    if waiting:
        return "cv", facts
    return "review", facts


def cmd_status(args) -> int:
    jobs = read_jsonl(JOBS)
    classified = read_jsonl(CLASSIFICATION)
    counts: dict[str, int] = {}
    for c in classified:
        counts[c["priority"]] = counts.get(c["priority"], 0) + 1
    stage, facts = next_stage()
    print(json.dumps({
        "next_stage": stage,
        **facts,
        "jobs": len(jobs),
        "auto_discarded": sum(j["prefilter"] != "pending" for j in jobs),
        "classified": len(classified),
        "by_priority": counts,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_sources(args) -> int:
    """Yield per source: how many jobs each one brought and how many ended up A, B or C."""
    classified = {c["id"]: c["priority"] for c in read_jsonl(CLASSIFICATION)}
    table: dict[str, dict[str, int]] = {}
    for job in read_jsonl(JOBS):
        row = table.setdefault(job["source"], {"jobs": 0, "auto_discarded": 0, "classified": 0, "A": 0, "B": 0, "C": 0, "discard": 0})
        row["jobs"] += 1
        row["auto_discarded"] += job["prefilter"] != "pending"
        if job["id"] in classified:
            row["classified"] += 1
            row[classified[job["id"]]] += 1
    print(json.dumps(dict(sorted(table.items(), key=lambda kv: -(kv[1]["A"] + kv[1]["B"]))), ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="validate the profile folder").set_defaults(func=cmd_check)
    p = sub.add_parser("fetch", help="query enabled sources and store new jobs")
    p.add_argument("--source", choices=sorted(SOURCES))
    p.add_argument("--with-apify", action="store_true", help="enable sources that spend Apify credit")
    p.set_defaults(func=cmd_fetch)
    p = sub.add_parser("batch", help="split unclassified jobs into batches for the classifier")
    p.add_argument("--size", type=int, default=20)
    p.add_argument("--limit", type=int, help="most relevant jobs to classify this run (default: max_classify_per_run; 0 = all)")
    p.set_defaults(func=cmd_batch)
    sub.add_parser("merge", help="validate and store batch results").set_defaults(func=cmd_merge)
    sub.add_parser("status", help="current counts").set_defaults(func=cmd_status)
    sub.add_parser("sources", help="yield per source: jobs brought and A/B/C obtained").set_defaults(func=cmd_sources)
    p = sub.add_parser("refilter", help="apply the current prefilter to unclassified jobs")
    p.add_argument("--location", action="store_true", help="apply only the location rules, to every job, classified or not")
    p.set_defaults(func=cmd_refilter)
    sub.add_parser("test-prefilter", help="measure the prefilter against existing classifications").set_defaults(func=cmd_test_prefilter)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
