from email.parser import BytesParser
from email.policy import default

import csv
import os
import pandas as pd
import pathlib
import pprint
#__file__ = "/Users/satvikajmera/Documents/SMU MSDS Course Material/05-Summer 2022/DS 7333 - QtW/Dylan Repo - QtW/qtw/case study 3/Satvik"

import os
emails = {"index":[]}

for path, subdirectories, filelist in os.walk(pathlib.Path(__file__)/ "SpamAssassinMessages"):
    for f in filelist:
        
        label = 0 if "ham" in path.lower() else 1
    
        with open(os.path.join(path, f), "rb") as fp:
            msg = BytesParser(policy=default).parse(fp)
            
            # Overkill but helps bypasses attachements in emails
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))
                    
                    # skip any text/plain (txt) attachments
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True)  # decode
                        break
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            else:
                body = msg.get_payload(decode=True)
            
            emails["index"].append({
                "Subject": msg.get("Subject"),
                "From": msg.get("from"),
                "Body": body,
                "isSpam": label
            })

try:
    with open(pathlib.Path(__file__).parent / "test.csv", 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Subject","From","Body","isSpam"])
        writer.writeheader()
        for data in emails["index"]:
            writer.writerow(data)
except IOError:
    print("I/O error")
