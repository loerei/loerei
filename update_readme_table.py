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
    req = urllib.request.Request(url, headers={"User-Agent": "Python-SVG-Updater"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def create_svg():
    width = 900
    row_height = 55
    header_height = 45
    total_height = header_height + len(REPOS) * row_height + 10

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {total_height}" width="100%">',
        '  <style>',
        '    .header { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: #ffffff; }',
        '    .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: #4892ff; }',
        '    .desc { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; fill: #c9d1d9; }',
        '    .tag-bg { fill: #282a38; rx: 4px; ry: 4px; }',
        '    .tag-text { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; fill: #8b949e; }',
        '  </style>',
        f'  <rect width="{width}" height="{total_height}" fill="transparent" />',
        '  <text x="15" y="28" class="header">Project</text>',
        '  <text x="190" y="28" class="header">Category</text>',
        '  <text x="330" y="28" class="header">Description</text>',
        f'  <text x="{width - 25}" y="28" class="header" text-anchor="end">Tech Stack</text>',
        f'  <line x1="15" y1="42" x2="{width - 15}" y2="42" stroke="#6e7681" stroke-width="1.5" />',
    ]

    y_cursor = header_height

    for i, item in enumerate(REPOS):
        name = item["name"]
        cat = item["category"]
        try:
            data = fetch_repo_data(name)
            desc = data.get("description", "") or ""
            lang = data.get("language", "Markdown") or "Markdown"
        except Exception:
            desc = ""
            lang = "Markdown"

        if len(desc) > 75:
            desc = desc[:72] + "..."

        y_text = y_cursor + 32
        y_line = y_cursor + row_height
        lang_color = COLOR_MAP.get(lang, "555555")

        svg_parts.extend([
            f'  <a xlink:href="https://github.com/loerei/{name}" target="_blank">',
            f'    <text x="15" y="{y_text}" class="title">{name}</text>',
            '  </a>',
            f'  <rect x="190" y="{y_text - 14}" width="{len(cat) * 8 + 12}" height="20" class="tag-bg" />',
            f'  <text x="196" y="{y_text}" class="tag-text">{cat}</text>',
            f'  <text x="330" y="{y_text}" class="desc">{desc}</text>',
            f'  <rect x="{width - 105}" y="{y_text - 15}" width="80" height="20" rx="4" fill="#{lang_color}" />',
            f'  <text x="{width - 65}" y="{y_text}" font-family="-apple-system, sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">{lang}</text>',
        ])

        if i < len(REPOS) - 1:
            svg_parts.append(f'  <line x1="15" y1="{y_line}" x2="{width - 15}" y2="{y_line}" stroke="#30363d" stroke-width="1" />')

        y_cursor += row_height

    svg_parts.append('</svg>')

    with open("projects-table.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print("projects-table.svg created successfully!")

def update_readme():
    create_svg()
    
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    replacement_block = (
        '<div align="center">\n'
        '  <img src="projects-table.svg" width="100%" alt="Projects" />\n'
        '</div>'
    )

    pattern = r"(<h3 align=\"center\">Projects</h3>\s*\n\s*\n).*?(\n\s*\n###)"
    replacement = r"\1" + replacement_block + r"\2"
    
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
    print("README.md updated successfully!")

if __name__ == "__main__":
    update_readme()
