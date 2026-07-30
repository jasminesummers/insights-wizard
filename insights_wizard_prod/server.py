#!/usr/bin/env python3
"""
================================================================──────────────
 🧙‍♂️ INSIGHTS WIZARD — PRODUCTION MULTI-USER BACKEND SERVER
================================================================──────────────
 Supports native PDF (`/usr/bin/pdftotext`) and Word `.docx` (`word/document.xml`)
================================================================──────────────
"""

import http.server
import socketserver
import json
import os
import sys
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse

PORT = 8085
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "database.json")
PUBLIC_DIR = os.path.join(SCRIPT_DIR, "public")
INBOX_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "inbox")


def load_db():
    if not os.path.exists(DB_FILE):
        return {"projects": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def extract_pdf_text(filepath):
    try:
        res = subprocess.run(["/usr/bin/pdftotext", filepath, "-"], capture_output=True, text=True, check=True)
        return res.stdout
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""


def extract_docx_text(filepath):
    try:
        with zipfile.ZipFile(filepath) as z:
            xml_content = z.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        paragraphs = []
        for elem in tree.iter():
            if elem.tag.endswith("}p"):
                texts = [node.text for node in elem.iter() if node.text]
                if texts:
                    paragraphs.append("".join(texts))
        return "\n".join(paragraphs)
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""


def parse_one_box_text(raw_text, filename="Uploaded Document"):
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
    participant = filename.replace(".docx", "").replace(".pdf", "").replace(".txt", "").replace("_", " ") if filename else "Industry Stakeholder"
    org = "External Partner"
    role = "GLG Expert"
    title = filename if filename else "Research Document"

    for i in range(min(8, len(lines))):
        line = lines[i]
        if any(w in line.lower() for w in ["landscape", "procurement", "storage", "capacity", "archival"]):
            title = line
            break

    lower = raw_text.lower()
    if "michael hardy" in lower:
        participant = "Michael Hardy"
        org = "VP Alliances & OEM, Quantum Corporation"
        role = "GLG Expert"
    elif "dinesh kumar" in lower:
        participant = "Dinesh Kumar"
        org = "Former Procurement Lead, Meta & AWS"
        role = "Independent Consultant"
    elif "rebecca chiu" in lower:
        participant = "Rebecca Chiu"
        org = "Google X Research Pod"
        role = "Google Employee"
    else:
        m = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[-—–]\s*([^\n]+)', raw_text)
        if m:
            participant = m.group(1)
            org = m.group(2)
        if "glg" in lower or "gerson" in lower: role = "GLG Expert"
        elif "google" in lower: role = "Google Employee"
        elif "meta" in lower or "aws" in lower or "consultant" in lower: role = "Independent Consultant"
        elif "oem" in lower or "quantum" in lower or "seagate" in lower: role = "OEM Leadership"

    sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', raw_text) if len(s.strip()) > 35]
    quotes = []
    rules = [
        ("1. Capacity & Supply Pressures", ["shortage", "supply", "capacity", "cost", "price", "delay", "commit", "order", "flash"]),
        ("2. Workloads & Data Tiering", ["tier", "cold", "hot", "warm", "archive", "rot", "delete", "retention", "footprint"]),
        ("3. Emerging Tech & Value Prop", ["glass", "silica", "ceramic", "optical", "material", "nanometer", "magnetic", "year"]),
        ("4. Performance & Buying Criteria", ["tco", "buying", "criteria", "power", "density", "latency", "write", "read"]),
        ("5. Adoption & Commercial Strategy", ["poc", "pilot", "lab", "test", "qualification", "esg", "audit", "contract"])
    ]

    for s in sentences:
        s_lower = s.lower()
        for cat_name, kw_list in rules:
            if any(k in s_lower for k in kw_list) and len(quotes) < 8:
                quotes.append({
                    "category": cat_name,
                    "quote": s.strip('"' + "'" + '“' + '”'),
                    "takeaway": s[:80].strip() + "..."
                })
                break

    if not quotes and sentences:
        quotes.append({
            "category": "4. Performance & Buying Criteria",
            "quote": sentences[0],
            "takeaway": "Key takeaway from uploaded research document"
        })

    return {
        "participant": participant,
        "organization": org,
        "role": role,
        "title": title,
        "quotes": quotes
    }


class WizardRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/state":
            db = load_db()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(db).encode("utf-8"))
            return

        filepath = os.path.join(PUBLIC_DIR, parsed.path.lstrip("/"))
        if parsed.path == "/" or not os.path.exists(filepath):
            filepath = os.path.join(PUBLIC_DIR, "index.html")

        if os.path.exists(filepath):
            self.send_response(200)
            if filepath.endswith(".html"):
                self.send_header("Content-Type", "text/html; charset=utf-8")
            elif filepath.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif filepath.endswith(".js"):
                self.send_header("Content-Type", "application/javascript")
            self.end_headers()
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        parsed = urlparse(self.path)
        db = load_db()

        if parsed.path == "/api/file/upload":
            raw_data = self.rfile.read(length)
            filename = self.headers.get("X-Filename", "uploaded_document.docx")
            
            # Determine format (.docx vs .pdf vs text)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".file") as tmp:
                tmp.write(raw_data)
                tmp_path = tmp.name

            extracted_text = ""
            if filename.lower().endswith(".docx"):
                extracted_text = extract_docx_text(tmp_path)
            elif filename.lower().endswith(".pdf"):
                extracted_text = extract_pdf_text(tmp_path)
            
            if not extracted_text:
                try:
                    extracted_text = raw_data.decode("utf-8", errors="ignore")
                except Exception:
                    extracted_text = ""

            os.unlink(tmp_path)

            if extracted_text:
                parsed_doc = parse_one_box_text(extracted_text, filename)
                proj = db["projects"][0] if db["projects"] else None
                if proj:
                    new_t = {
                        "id": "t_" + str(int(datetime.now().timestamp() * 1000)),
                        "participant": parsed_doc["participant"],
                        "organization": parsed_doc["organization"],
                        "role": parsed_doc["role"],
                        "title": parsed_doc["title"],
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "checked": True,
                        "quotes": parsed_doc["quotes"]
                    }
                    proj["transcripts"].insert(0, new_t)
                    save_db(db)

            self.send_json({"status": "ok", "db": db})
            return

        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(raw_body)
        except Exception:
            payload = {}

        if parsed.path == "/api/transcript/add":
            pid = payload.get("projectId")
            participant = payload.get("participant", "").strip()
            role = payload.get("role", "External Expert").strip()
            title = payload.get("title", "Research Notes").strip()
            raw_text = payload.get("rawText", "").strip()

            proj = next((p for p in db.get("projects", []) if p["id"] == pid), None)
            if proj and participant and raw_text:
                parsed_doc = parse_one_box_text(raw_text, title)
                new_t = {
                    "id": "t_" + str(int(datetime.now().timestamp() * 1000)),
                    "participant": participant,
                    "organization": role,
                    "role": role,
                    "title": title,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "checked": True,
                    "quotes": parsed_doc["quotes"]
                }
                proj["transcripts"].insert(0, new_t)
                save_db(db)

            self.send_json({"status": "ok", "db": db})
            return

        elif parsed.path == "/api/transcript/toggle":
            pid = payload.get("projectId")
            tid = payload.get("transcriptId")
            checked = payload.get("checked", True)
            
            proj = next((p for p in db.get("projects", []) if p["id"] == pid), None)
            if proj:
                tr = next((t for t in proj["transcripts"] if t["id"] == tid), None)
                if tr:
                    tr["checked"] = checked
                    save_db(db)
            self.send_json({"status": "ok", "db": db})
            return

        elif parsed.path == "/api/role/update":
            pid = payload.get("projectId")
            tid = payload.get("transcriptId")
            new_role = payload.get("newRole", "").strip()
            
            proj = next((p for p in db.get("projects", []) if p["id"] == pid), None)
            if proj and new_role:
                tr = next((t for t in proj["transcripts"] if t["id"] == tid), None)
                if tr:
                    tr["role"] = new_role
                    tr["organization"] = new_role
                    save_db(db)
            self.send_json({"status": "ok", "db": db})
            return

        self.send_error(404, "Unknown Route")

    def send_json(self, obj):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode("utf-8"))


if __name__ == "__main__":
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    os.makedirs(INBOX_DIR, exist_ok=True)
    with socketserver.TCPServer(("", PORT), WizardRequestHandler) as httpd:
        print(f"🧙‍♂️ Insights Wizard Server running with DOCX & PDF parsers on Port {PORT}")
        httpd.serve_forever()
