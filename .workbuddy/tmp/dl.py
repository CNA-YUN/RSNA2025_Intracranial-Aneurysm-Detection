import os, urllib.request

BASE = r"F:\PythonProjects\RSNA2025_Intracranial-Aneurysm-Detection\.workbuddy\tmp"
url_file = os.path.join(BASE, "url.txt")
url = open(url_file, encoding="utf-8").read().strip()
dst = os.path.join(BASE, "spec.docx")
log = []
try:
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    with open(dst, "wb") as f:
        f.write(data)
    log.append("ok size=%d" % len(data))
    if len(data) < 2000:
        log.append("HEAD: " + data[:500].decode("utf-8", "ignore"))
except Exception as e:
    log.append("ERR %r" % (e,))
with open(os.path.join(BASE, "log2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("done")
