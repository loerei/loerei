import urllib.request
import json
import re

REPOS = [
    {"name": "patchitRIGHT", "category": "MCP Server"},
    {"name": "chronicle-mcp", "category": "MCP Server"},
    {"name": "HoverSource", "category": "Dev Tool"},
    {"name": "YumeShelf", "category": "Desktop App"},
]

COLOR_MAP = {
    "Python": "3776AB",
    "TypeScript": "3178C6",
    "JavaScript": "F7DF1E",
    "Rust": "000000",
    "C++": "00599C",
    "C#": "239120",
    "HTML": "E34F26",
    "CSS": "1572B6",
}

def fetch_repo_data(repo_name):
    url = f"https://api.github.com/repos/loerei/{repo_name}"
    req = urllib.request.Request(url, headers={"User-Agent": "Python-README-Updater"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def generate_table():
    lines = [
        "| Project | Category | Description | Tech Stack |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for item in REPOS:
        name = item["name"]
        cat = item["category"]
        try:
            data = fetch_repo_data(name)
            desc = data.get("description", "") or ""
            lang = data.get("language", "Markdown") or "Markdown"
            color = COLOR_MAP.get(lang, "555555")
            badge = f"![{lang}](https://img.shields.io/badge/-{lang}-{color}?logo={lang.lower()}&logoColor=white)"
            lines.append(f"| [**{name}**](https://github.com/loerei/{name}) | `{cat}` | {desc} | {badge} |")
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return "\n".join(lines)

def update_readme():
    table_content = generate_table()
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Pattern to replace the table under Projects
    pattern = r"(<h3 align=\"center\">Projects</h3>\s*\n\s*\n).*?(\n\s*\n###)"
    replacement = r"\1" + table_content + r"\2"
    
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
    print("README.md updated successfully!")

if __name__ == "__main__":
    update_readme()
