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
        '<table width="100%">',
        '  <thead>',
        '    <tr>',
        '      <th width="18%" align="left">Project</th>',
        '      <th width="18%" align="left">Category</th>',
        '      <th width="50%" align="left">Description</th>',
        '      <th width="14%" align="right">Tech Stack</th>',
        '    </tr>',
        '  </thead>',
        '  <tbody>',
    ]
    for item in REPOS:
        name = item["name"]
        cat = item["category"]
        try:
            data = fetch_repo_data(name)
            desc = data.get("description", "") or ""
            lang = data.get("language", "Markdown") or "Markdown"
            color = COLOR_MAP.get(lang, "555555")
            badge = f'<img src="https://img.shields.io/badge/-{lang}-{color}?logo={lang.lower()}&logoColor=white" alt="{lang}" />'
            row = (
                f'    <tr>\n'
                f'      <td align="left"><a href="https://github.com/loerei/{name}"><b>{name}</b></a></td>\n'
                f'      <td align="left"><code>{cat}</code></td>\n'
                f'      <td align="left">{desc}</td>\n'
                f'      <td align="right">{badge}</td>\n'
                f'    </tr>'
            )
            lines.append(row)
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    lines.append('  </tbody>\n</table>')
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
