#!/usr/bin/env python3
"""Repository harness for skill and agent-file conventions.

Run from the repository root:  python3 harness/check.py
Exit code 0 = all checks pass. Any failure prints a remediation message
written for the agent fixing it. No dependencies beyond the standard library.

Agents: run this before finishing any change to skills, agent files, docs,
or the README, and iterate until it passes. The rules it enforces are
explained in docs/golden-principles.md and docs/conventions.md.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".agents" / "skills"

SKILL_LINE_LIMIT = 500
AGENTS_MD_LINE_LIMIT = 120
DESCRIPTION_CHAR_LIMIT = 1024
DUP_SENTENCE_MIN_WORDS = 12

REQUIRED_SECTIONS = [
    "invocation",
    "required input",
    "outcome",
    "operating principles",
    "workflow",
    "quality controls",
    "failure handling",
]

# Model IDs and version-pinned model names are time-sensitive content.
MODEL_ID_RE = re.compile(
    r"\b(?:gpt|claude|gemini|composer|grok|llama|sonnet|opus|haiku|fable|terra|sol)"
    r"[-_ ]?\d+(?:[.-]\d+)*\b",
    re.IGNORECASE,
)
AS_OF_RE = re.compile(r"\bas of\b", re.IGNORECASE)
TIME_SENSITIVE_HEADING_RE = re.compile(r"point.in.time|time.sensitive", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+|\]\([^)]*\)")

failures = []


def fail(check, path, message):
    failures.append(f"[FAIL] {check} — {path}\n       {message}")


def parse_frontmatter(text):
    """Return (dict of top-level keys, error string or None)."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None, "no frontmatter block delimited by --- lines at the top of the file"
    fields = {}
    key = None
    for line in m.group(1).splitlines():
        if line[:1] in (" ", "\t"):
            if key:
                fields[key] += " " + line.strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, None


def strip_code_blocks(lines):
    """Replace fenced code-block content with empty lines (keeps numbering)."""
    out, in_fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def time_sensitive_allowed_lines(lines):
    """Line indices under a heading marked point-in-time / time-sensitive."""
    allowed, level = set(), None
    for i, line in enumerate(lines):
        h = re.match(r"^(#{1,6})\s+(.*)", line)
        if h:
            if level is not None and len(h.group(1)) <= level:
                level = None
            if TIME_SENSITIVE_HEADING_RE.search(h.group(2)):
                level = len(h.group(1))
        if level is not None:
            allowed.add(i)
    return allowed


def normalized_sentences(text):
    text = URL_RE.sub(" ", text)
    out = []
    for raw in re.split(r"[.!?\n]", text):
        words = re.sub(r"[^a-z0-9 ]", " ", raw.lower()).split()
        if len(words) >= DUP_SENTENCE_MIN_WORDS:
            out.append(" ".join(words))
    return out


def relative_md_links(text):
    return [
        m.group(1)
        for m in re.finditer(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)", text)
        if not m.group(1).startswith("http")
    ]


def check_skill(skill_dir):
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    label = f".agents/skills/{name}"

    if not skill_md.exists():
        fail("skill-md-exists", label, "Every skill directory needs a SKILL.md. Create it per docs/conventions.md.")
        return
    text = skill_md.read_text()
    lines = text.splitlines()

    # Frontmatter
    fm, err = parse_frontmatter(text)
    if err:
        fail("frontmatter", f"{label}/SKILL.md", f"{err}. Add YAML frontmatter with name: and description: keys.")
        fm = {}
    if fm.get("name") != name:
        fail("name-matches-dir", f"{label}/SKILL.md",
             f"Frontmatter name '{fm.get('name')}' must equal the directory name '{name}'. Rename one to match.")
    if fm.get("name") and not re.fullmatch(r"[a-z0-9-]{1,64}", fm["name"]):
        fail("name-format", f"{label}/SKILL.md",
             "Skill name must be lowercase letters, digits, and hyphens, max 64 chars.")
    desc = fm.get("description", "")
    if not desc:
        fail("description", f"{label}/SKILL.md", "Frontmatter must include a description stating WHAT and WHEN.")
    elif len(desc) > DESCRIPTION_CHAR_LIMIT:
        fail("description-length", f"{label}/SKILL.md",
             f"Description is {len(desc)} chars (limit {DESCRIPTION_CHAR_LIMIT}). Trim it; details belong in the body.")
    elif "use when" not in desc.lower():
        fail("description-trigger", f"{label}/SKILL.md",
             'Description must contain a trigger phrase, e.g. "Use when the user invokes /<name> or asks to ...".')

    # Progressive disclosure: line budget
    if len(lines) > SKILL_LINE_LIMIT:
        fail("skill-line-limit", f"{label}/SKILL.md",
             f"SKILL.md is {len(lines)} lines (limit {SKILL_LINE_LIMIT}). Move prompt templates, report formats, "
             "and procedural detail to reference.md and link them one level deep. Move content, do not delete it, "
             "and do not remove workflow stages or schemas from the body summary.")

    # Required sections in order
    headings = [re.sub(r"[^a-z ]", "", h.lower()).strip()
                for h in re.findall(r"^#{1,6}\s+(.*)$", text, re.MULTILINE)]
    pos = 0
    for section in REQUIRED_SECTIONS:
        found = None
        for i in range(pos, len(headings)):
            if section in headings[i]:
                found = i
                break
        if found is None:
            fail("required-sections", f"{label}/SKILL.md",
                 f"Missing or out-of-order section '{section}'. SKILL.md must contain, in order: "
                 + ", ".join(REQUIRED_SECTIONS) + ". See docs/conventions.md.")
            break
        pos = found + 1

    # Link depth and dead links for all md files in the skill
    md_files = sorted(skill_dir.glob("*.md")) + sorted((skill_dir / "agents").glob("*.md"))
    for f in md_files:
        rel = f.relative_to(ROOT)
        for link in relative_md_links(f.read_text()):
            target = (f.parent / link).resolve()
            if not target.exists():
                fail("dead-link", str(rel),
                     f"Relative link '{link}' does not resolve. Fix the path or create the file.")
            elif skill_dir not in target.parents:
                fail("link-depth", str(rel),
                     f"Link '{link}' points outside this skill's folder. Skills must be self-contained; "
                     "inline the needed content or move it into the skill directory.")

    # Time-sensitive content outside marked sections (skill files only)
    for f in md_files:
        rel = f.relative_to(ROOT)
        flines = strip_code_blocks(f.read_text().splitlines())
        allowed = time_sensitive_allowed_lines(flines)
        for i, line in enumerate(flines):
            if i in allowed:
                continue
            scan = URL_RE.sub(" ", line)
            for pattern, what in ((MODEL_ID_RE, "model ID or versioned model name"), (AS_OF_RE, '"as of" phrasing')):
                m = pattern.search(scan)
                if m:
                    fail("time-sensitive", f"{rel}:{i + 1}",
                         f"Found {what} '{m.group(0)}' outside a section whose heading is marked "
                         "'Point-in-time' or 'Time-sensitive'. Model names and dated claims rot; "
                         "replace with a semantic tier (e.g. 'strongest creative model available') "
                         "or move the line into a clearly marked point-in-time section.")

    # Agent role files
    agents_dir = skill_dir / "agents"
    if agents_dir.is_dir():
        role_files = sorted(agents_dir.glob("*.md"))
        for f in role_files:
            rel = f.relative_to(ROOT)
            rtext = f.read_text()
            rfm, rerr = parse_frontmatter(rtext)
            if rerr:
                fail("role-frontmatter", str(rel), f"{rerr}. Role files need name, description, model frontmatter.")
                continue
            if set(rfm) != {"name", "description", "model"}:
                fail("role-fields", str(rel),
                     f"Role frontmatter must contain exactly name, description, model — found {sorted(rfm)}. "
                     "Tool-specific fields (tools:, readonly:, is_background:) are documented in the skill README "
                     "as post-install additions, never committed.")
            if rfm.get("model") != "inherit":
                fail("role-model-inherit", str(rel),
                     f"Committed role files must use 'model: inherit' (found '{rfm.get('model')}'). "
                     "Declare the tier semantically in the body's 'Model tier:' line; users pin models at install time.")
            if not rfm.get("name", "").startswith(name + "-"):
                fail("role-name-prefix", str(rel),
                     f"Role name '{rfm.get('name')}' must be prefixed with the skill name ('{name}-') to avoid collisions.")
            body = re.sub(r"^---\n.*?\n---\n", "", rtext, flags=re.DOTALL).strip()
            if not body.startswith("Model tier:"):
                fail("role-model-tier", str(rel),
                     "The first body line must start with 'Model tier:' and describe the tier semantically.")
        if role_files and "agents/" not in text:
            fail("roles-referenced", f"{label}/SKILL.md",
                 "The skill ships role files but SKILL.md never mentions the agents/ folder. "
                 "Tell the orchestrator to use installed roles and to emulate them when absent.")

    # Duplication between SKILL.md, reference.md, README.md (agents/ repackage by design)
    core = [f for f in (skill_dir / "SKILL.md", skill_dir / "reference.md", skill_dir / "README.md") if f.exists()]
    seen = {}
    for f in core:
        for s in set(normalized_sentences("\n".join(strip_code_blocks(f.read_text().splitlines())))):
            if s in seen and seen[s] != f:
                fail("duplication", f"{label}", 
                     f"The sentence \"{s[:80]}...\" appears in both {seen[s].name} and {f.name}. "
                     "Keep one canonical copy: workflow rules in SKILL.md, stage prompts and detail in reference.md, "
                     "human guidance in README.md. Replace the duplicate with a link.")
            seen[s] = f


def check_repo():
    # README table sync
    readme = (ROOT / "README.md").read_text()
    linked = set(re.findall(r"\.agents/skills/([a-z0-9-]+)/SKILL\.md", readme))
    actual = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    for missing in sorted(actual - linked):
        fail("readme-table", "README.md",
             f"Skill '{missing}' has no row in the 'Skills in this repository' table. Add one "
             "(skill link, category, one-sentence description, invocation).")
    for orphan in sorted(linked - actual):
        fail("readme-table", "README.md",
             f"README links to skill '{orphan}' which does not exist. Remove the row or restore the skill.")
    if "ln -s" not in readme:
        fail("symlink-install", "README.md",
             "Installation instructions must offer symlinking (ln -s) as the preferred method so installed "
             "skills stay current with git pull; keep cp as the fallback.")

    # AGENTS.md as table of contents
    agents_md = ROOT / "AGENTS.md"
    atext = agents_md.read_text()
    alines = atext.splitlines()
    if len(alines) > AGENTS_MD_LINE_LIMIT:
        fail("agents-md-limit", "AGENTS.md",
             f"AGENTS.md is {len(alines)} lines (limit {AGENTS_MD_LINE_LIMIT}). It is a table of contents, "
             "not an encyclopedia: move detail to docs/ and keep pointers here.")
    for link in relative_md_links(atext):
        if not (ROOT / link).exists():
            fail("agents-md-links", "AGENTS.md", f"Pointer '{link}' does not resolve. Fix or remove it.")
    for required in ("docs/golden-principles.md", "docs/conventions.md", "harness/check.py"):
        if required not in atext:
            fail("agents-md-pointers", "AGENTS.md",
                 f"AGENTS.md must point agents to {required}.")
        if not (ROOT / required).exists():
            fail("docs-exist", required, "Referenced system-of-record file is missing. Create it.")

    # No committed tool-specific trees duplicating skills
    for tool_dir in (".claude", ".codex"):
        if (ROOT / tool_dir).exists():
            fail("no-tool-trees", tool_dir,
                 f"Do not commit {tool_dir}/ — canonical files live in .agents/skills/ and are installed "
                 "by symlink or copy per README. Delete this tree.")
    if (ROOT / ".cursor" / "agents").exists():
        fail("no-tool-trees", ".cursor/agents",
             "Do not commit .cursor/agents/ — role files live in each skill's agents/ folder.")

    # Enforcement plumbing exists
    hook = ROOT / ".githooks" / "pre-commit"
    if not hook.exists():
        fail("pre-commit-hook", ".githooks/pre-commit", "The pre-commit hook running this harness is missing.")
    elif not (hook.stat().st_mode & 0o111):
        fail("pre-commit-hook", ".githooks/pre-commit", "Hook is not executable. Run: chmod +x .githooks/pre-commit")


def main():
    if not SKILLS_DIR.is_dir():
        print("[FAIL] repo-structure — .agents/skills/ not found; run from the repository root.")
        return 1
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if skill_dir.is_dir():
            check_skill(skill_dir)
    check_repo()

    if failures:
        print("\n\n".join(failures))
        print(f"\n{len(failures)} check(s) failed. Fix the items above and rerun: python3 harness/check.py")
        return 1
    print("All harness checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
