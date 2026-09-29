import html

def format_html_preview(text: str) -> str:
    safe = html.escape(text).replace("\n", "<br>")
    return f'''
<div style="background:#111827;color:#f3f4f6;padding:24px;border-radius:14px;
line-height:1.65;max-height:600px;overflow-y:auto;font-family:Georgia,serif;
border:1px solid #374151;">{safe}</div>
'''
