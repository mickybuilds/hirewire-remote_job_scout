"""Local dashboard. Usage: python scripts/dashboard.py [--port 8765]  →  http://localhost:8765"""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hirewire import BASE, CLASSIFICATION, DATA, JOBS, load_config, read_jsonl  # noqa: E402

HTML = BASE / "web" / "index.html"
APPLICATIONS = BASE / "applications"
STATUSES = DATA / "statuses.json"
VALID_STATUSES = {"new", "interested", "applied", "dismissed"}
DISMISS_REASONS = {"sales_support", "level", "not_remote", "topic", "other"}
DOWNLOADABLE = {".docx", ".pdf", ".md"}
PORT = 8765
JOB_FIELDS = ("id", "title", "company", "url", "apply_url", "location", "employment_type", "salary",
              "posted", "source", "seen", "prefilter", "prefilter_reason", "other_sources")


def read_statuses() -> dict:
    if not STATUSES.exists():
        return {}
    return json.loads(STATUSES.read_text(encoding="utf-8"))


def not_eligible(job: dict, classification: dict | None) -> bool:
    return (job.get("prefilter_reason", "").startswith("Not eligible")
            or (classification or {}).get("geo") == "not_eligible")


def applications() -> dict[str, list[dict]]:
    """CVs written by the /cv stage, by job id. Each folder has a meta.json with the job id and language."""
    found: dict[str, list[dict]] = {}
    for meta_path in APPLICATIONS.glob("*/meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        folder = meta_path.parent
        files = [{"name": f.name, "url": "/files/" + quote(folder.name) + "/" + quote(f.name)}
                 for f in sorted(folder.iterdir()) if f.suffix.lower() in {".docx", ".pdf"}]
        found.setdefault(meta.get("job_id", ""), []).append({
            "folder": folder.name, "language": meta.get("language", ""), "created": meta.get("created", ""), "files": files})
    return found


def payload() -> dict:
    config = load_config()
    classified = {c["id"]: c for c in read_jsonl(CLASSIFICATION)}
    statuses = read_statuses()
    cvs = applications()
    jobs = []
    for j in read_jsonl(JOBS):
        if not_eligible(j, classified.get(j["id"])) and j["id"] not in statuses:
            continue
        state = statuses.get(j["id"], {})
        row = {k: j.get(k, "") for k in JOB_FIELDS}
        row["classification"] = classified.get(j["id"])
        row["status"] = state.get("status", "new")
        row["note"] = state.get("note", "")
        row["applied_date"] = state.get("applied_date", "")
        row["dismiss_reason"] = state.get("dismiss_reason", "")
        row["cvs"] = cvs.get(j["id"], [])
        jobs.append(row)
    return {
        "config": {
            "language": config.get("language", "en"),
            "residence_country": config["candidate"]["residence_country"],
            "routes": config["routes"],
        },
        "jobs": jobs,
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, content_type: str, extra: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/jobs":
            self._send(200, json.dumps(payload(), ensure_ascii=False).encode("utf-8"), "application/json")
        elif self.path.startswith("/files/"):
            self._file(unquote(self.path[len("/files/"):]))
        else:
            self._send(404, b"not found", "text/plain")

    def _file(self, relative: str) -> None:
        path = (APPLICATIONS / relative).resolve()
        if APPLICATIONS.resolve() not in path.parents or path.suffix.lower() not in DOWNLOADABLE or not path.is_file():
            return self._send(404, b"not found", "text/plain")
        kind = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self._send(200, path.read_bytes(), kind, {"Content-Disposition": f"attachment; filename*=UTF-8''{quote(path.name)}"})

    def do_POST(self):
        if self.path != "/api/status":
            return self._send(404, b"not found", "text/plain")
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        job, status, reason = body.get("id"), body.get("status"), body.get("dismiss_reason")
        if not job or (status and status not in VALID_STATUSES) or (reason and reason not in DISMISS_REASONS):
            return self._send(400, b"invalid data", "text/plain")
        statuses = read_statuses()
        current = statuses.get(job, {"status": "new", "note": ""})
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if status:
            current["status"] = status
            if status == "applied" and not current.get("applied_date"):
                current["applied_date"] = now[:10]
            if status != "applied":
                current.pop("applied_date", None)
            if status != "dismissed":
                current.pop("dismiss_reason", None)
        if reason:
            current["dismiss_reason"] = reason
        if "note" in body:
            current["note"] = str(body["note"])[:2000]
        current["date"] = now
        statuses[job] = current
        STATUSES.parent.mkdir(parents=True, exist_ok=True)
        tmp = STATUSES.with_suffix(".tmp")
        tmp.write_text(json.dumps(statuses, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(STATUSES)
        self._send(200, json.dumps(current).encode("utf-8"), "application/json")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HireWire local dashboard")
    parser.add_argument("--port", type=int, default=PORT)
    port = parser.parse_args().port
    print(f"Dashboard at http://localhost:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
