# generate_pdf.py

import markdown2
import os

# Read markdown file
with open("evaluation_report.md", "r") as f:
    md_content = f.read()

# Convert to HTML
html_content = markdown2.markdown(md_content, extras=["tables"])

# Add styling
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
    h1 {{ color: #2c3e50; border-bottom: 2px solid #2c3e50; }}
    h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; }}
    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
    th {{ background: #2c3e50; color: white; padding: 8px 12px; }}
    td {{ border: 1px solid #bdc3c7; padding: 8px 12px; }}
    tr:nth-child(even) {{ background: #f2f2f2; }}
    img {{ width: 100%; margin: 20px 0; }}
</style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Save HTML
with open("evaluation_report.html", "w") as f:
    f.write(html)

print("✅ HTML report generated: evaluation_report.html")
print("   Open this file in Chrome and Ctrl+P → Save as PDF")