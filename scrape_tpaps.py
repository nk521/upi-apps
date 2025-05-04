import csv
import io
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import black

html = urlopen("https://www.npci.org.in/what-we-do/upi/3rd-party-apps")
soup = BeautifulSoup(html, "html.parser")
table = soup.find_all("table", {"class":"table table-bordered"})[0]
rows = table.find_all("tr")

to_skip = ["Sr. No.", "Go Live (MM-YYYY)", "PSP Banks", "Links URL"]
to_skip_position = [0, 2, 3, 5]

mem_csv = io.StringIO(newline="")

writer = csv.writer(mem_csv)
for row in rows:
    idx = 0
    csv_row = []
    for cell in row.find_all(["td", "th"]):
        if idx in to_skip_position:
            idx += 1
            continue
        idx += 1
        csv_row.append(cell.get_text())
    writer.writerow(csv_row)
    
mem_csv.seek(0)

out: dict[str, list[str]] = dict()
last = ""

reader = csv.reader(mem_csv)
header = True
for row in reader:
    if header:
        header = False
        continue

    if len(row) == 0:
        continue

    if len(row) == 1:
        out[last].append(row[0].removeprefix("@"))
        continue


    out[row[0]] = [row[1].removeprefix("@")]
    last = row[0]

mem_csv.close()

## PATCHES
out["Paytm"].append("ptyes")


print(json.dumps(out, indent=4))