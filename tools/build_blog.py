"""
build_blog.py  SA Hustle Hub Static Site Generator
Layer 3: The Execution Engine (Deterministic)

Usage:
    python tools/build_blog.py

Dependencies:
    pip install markdown2 jinja2
"""

import os
import json
import shutil
import re
import markdown2
from jinja2 import Environment, FileSystemLoader

#  Paths 
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT  = os.path.join(ROOT, "content")
TEMPLATES= os.path.join(ROOT, "templates")
PUBLIC   = os.path.join(ROOT, "docs")
POSTS_DIR= os.path.join(PUBLIC, "posts")
TMP      = os.path.join(ROOT, ".tmp")

#  Helpers 
def parse_frontmatter(text):
    """Extract YAML frontmatter dict and body from markdown text."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end].strip()
    body     = text[end + 3:].strip()
    meta = {}
    for line in fm_block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"')
            # Handle YAML lists: ["a", "b"]
            if val.startswith("["):
                # Each match is a tuple of groups; pick the first non-empty group
                raw_matches = re.findall(r'"([^"]+)"|\'([^\']+)\'|([\w][\w\- ]*)', val)
                val = [next(g for g in groups if g) for groups in raw_matches if any(groups)]
            meta[key.strip()] = val
    return meta, body

def slugify(filename):
    return os.path.splitext(filename)[0]

#  Build 
def build():
    # 1. Prepare output dirs
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)

    # Load Jinja2 env
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
    post_tpl  = env.get_template("post.html")
    index_tpl = env.get_template("index.html")

    search_index = []
    errors = []

    # 2. Process each markdown file
    md_files = [f for f in os.listdir(CONTENT) if f.endswith(".md")]
    if not md_files:
        print("[WARN] No content files found in /content.")
        return

    for filename in sorted(md_files):
        slug = slugify(filename)
        filepath = os.path.join(CONTENT, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        meta, body_md = parse_frontmatter(raw)

        # Validate required fields
        required = ["title", "description", "category", "link"]
        missing = [k for k in required if k not in meta]
        if missing:
            errors.append(f"[SKIP] {filename}: Missing fields: {missing}")
            continue

        # Fallback for optional fields
        meta.setdefault("difficulty", "Moderate")
        meta.setdefault("data_usage", "Low")
        meta.setdefault("tags", [])
        if isinstance(meta["tags"], str):
            meta["tags"] = [meta["tags"]]

        # Convert markdown body to HTML
        body_html = markdown2.markdown(body_md, extras=["tables", "fenced-code-blocks"])

        # Render post page
        post_html = post_tpl.render(
            title       = meta["title"],
            description = meta["description"],
            category    = meta["category"],
            difficulty  = meta["difficulty"],
            data_usage  = meta["data_usage"],
            link        = meta["link"],
            body        = body_html
        )

        out_path = os.path.join(POSTS_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(post_html)

        # Add to search index
        search_index.append({
            "slug"       : slug,
            "title"      : meta["title"],
            "description": meta["description"],
            "category"   : meta["category"],
            "tags"       : meta["tags"]
        })

        print(f"[OK]   Built: posts/{slug}.html")

    # 3. Write search index
    index_path = os.path.join(PUBLIC, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    print(f"[OK]   index.json -> {len(search_index)} entries")

    # 4. Copy index.html template to public/ (it reads index.json directly)
    src = os.path.join(TEMPLATES, "index.html")
    dst = os.path.join(PUBLIC, "index.html")
    shutil.copyfile(src, dst)
    print(f"[OK]   index.html copied to /public")

    # 5. Log errors
    if errors:
        log_path = os.path.join(TMP, "build_errors.log")
        with open(log_path, "w") as f:
            f.write("\n".join(errors))
        print(f"\n[WARN] {len(errors)} file(s) skipped. See .tmp/build_errors.log")

    print(f"\n Build complete. {len(search_index)} pages in /public/posts/")

#  Audit 
def audit_size():
    total = 0
    for dirpath, _, files in os.walk(PUBLIC):
        for fname in files:
            total += os.path.getsize(os.path.join(dirpath, fname))
    kb = total / 1024
    status = "" if kb < 100 else " EXCEEDS 100KB LIMIT"
    print(f"\n Total /public size: {kb:.1f} KB  {status}")

if __name__ == "__main__":
    build()
    audit_size()


