import urllib.request
import json
import re

REPOS = [
    {"name": "patchitRIGHT", "category": "MCP Server"},
    {"name": "chronicle-mcp", "category": "MCP Server"},
    {"name": "HoverSource", "category": "Dev Tool"},
    {"name": "YumeShelf", "category": "Desktop App"},
]

FALLBACK_DATA = {
    "patchitRIGHT": {
        "description": "patchitRIGHT: An AST-bounded secure code-writing MCP server with transactional multi-file refactoring and rollback.",
        "language": "Python"
    },
    "chronicle-mcp": {
        "description": "A local Model Context Protocol (MCP) server that indexes, synchronizes, and exposes agent conversation logs, tool execution steps, subagent hierarchies, and execution benchmarks from Antigravity and Cursor workspaces.",
        "language": "TypeScript"
    },
    "HoverSource": {
        "description": "Zero-invasive UI-to-Code inspector. Hover any element, press Alt+C, paste to your AI agent, and save 94.5% tokens for UI tasks in your giant codebase.",
        "language": "TypeScript"
    },
    "YumeShelf": {
        "description": "A minimalist desktop game library launcher and save editor for VN-type-of-games, rescuing you from drowning in File Explorer.",
        "language": "TypeScript"
    }
}

def fetch_repo_data(repo_name):
    url = f"https://api.github.com/repos/loerei/{repo_name}"
    req = urllib.request.Request(url, headers={"User-Agent": "Python-README-Updater"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def generate_projects_html():
    parts = ['<div align="left">']

    for i, item in enumerate(REPOS):
        name = item["name"]
        cat = item["category"]
        fallback = FALLBACK_DATA.get(name, {})
        try:
            data = fetch_repo_data(name)
            desc = data.get("description") or fallback.get("description", "")
            lang = data.get("language") or fallback.get("language", "TypeScript")
        except Exception as e:
            print(f"Using fallback for {name} due to fetch error: {e}")
            desc = fallback.get("description", "")
            lang = fallback.get("language", "TypeScript")

        item_html = (
            f'  <p>\n'
            f'    <a href="https://github.com/loerei/{name}"><b>{name}</b></a> &nbsp; <code>{cat}</code> &nbsp; <code>{lang}</code><br/>\n'
            f'    <span align="justify" style="display: block; text-align: justify; color: #8b949e; margin-top: 4px;">{desc}</span>\n'
            f'  </p>'
        )
        parts.append(item_html)
        if i < len(REPOS) - 1:
            parts.append('  <hr/>')

    parts.append('</div>')
    return "\n".join(parts)

def update_readme():
    content = generate_projects_html()
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    pattern = r"(<h3 align=\"center\">Projects</h3>\s*\n\s*\n).*?(\n\s*\n###)"
    replacement = r"\1" + content + r"\2"
    
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
    print("README.md updated successfully!")

if __name__ == "__main__":
    update_readme()
