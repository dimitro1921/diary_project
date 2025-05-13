from typing import List
from app.models import Entry
from collections import defaultdict

def entries_to_markdown(entries: List[Entry]) -> str:
    """
    Convert a list of entries into a grouped Markdown string.
    Entries are grouped by date and include entry type and tags.
    """
    grouped = defaultdict(list)
    for entry in entries:
        grouped[entry.date_only].append(entry)

    markdown_lines = ["# 📓 Your Personal Knowledge & Reflection Diary", ""]

    for entry_date in sorted(grouped.keys()):
        markdown_lines.append(f"## 📅 {entry_date}")
        for entry in grouped[entry_date]:
            markdown_lines.append(f"**Type**: {entry.entry_type.value}")
            markdown_lines.append(f"**Time**: {entry.timestamp.strftime('%H:%M:%S')}")
            if entry.tags:
                markdown_lines.append(f"**Tags**: {entry.tags}")
            markdown_lines.append("")
            markdown_lines.append(entry.text.strip())
            markdown_lines.append("\n---\n")

    return "\n".join(markdown_lines)
