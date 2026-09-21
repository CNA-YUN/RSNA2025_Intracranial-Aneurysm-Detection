import os, sys, zipfile, re

BASE = r"F:\PythonProjects\RSNA2025_Intracranial-Aneurysm-Detection\.workbuddy\tmp"
SRC = os.path.join(BASE, "spec.docx")
OUT = os.path.join(BASE, "spec.txt")

log = []
if not os.path.exists(SRC):
    log.append("MISSING: %s" % SRC)
else:
    log.append("size=%d" % os.path.getsize(SRC))

try:
    z = zipfile.ZipFile(SRC)
    xml = z.read("word/document.xml").decode("utf-8", "ignore")
    # split paragraphs
    paras = re.findall(r"<w:p\b.*?</w:p>", xml, flags=re.S)
    lines = []
    for p in paras:
        # table? keep text
        texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.S)
        txt = "".join(texts)
        txt = txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        lines.append(txt)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.append("paras=%d -> %s" % (len(lines), OUT))
except Exception as e:
    log.append("ERR: %r" % (e,))

with open(os.path.join(BASE, "log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("done")
