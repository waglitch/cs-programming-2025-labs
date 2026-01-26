reports = [
    {"author": "Dr. Moss", "text": "Analysis completed. Reference: http://external-archive.net"},
    {"author": "Agent Lee", "text": "Incident resolved without escalation."},
    {"author": "Dr. Patel", "text": "Supplementary data available at https://secure-research.org"}
]
links_reports = list(filter(lambda r: "http://" in r["text"] or "https://" in r["text"], reports))
import re
cleaned_reports = list(map(lambda r: {"author": r["author"], "text": re.sub(r'https?://[^\s]+', '[ДАННЫЕ УДАЛЕНЫ]', r["text"])}, links_reports))
print("\n5. Отчеты без ссылок:")
print(cleaned_reports)