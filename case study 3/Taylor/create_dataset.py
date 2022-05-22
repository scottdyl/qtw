from email.parser import BytesParser
from email.policy import default

import csv
import os
import pandas as pd
import pathlib
import pprint

emails = {"index":[]}

for directory, subdirectory, filelist in os.walk(pathlib.Path(__file__).parent / "SpamAssassinMessages"):
    for f in filelist:
    
        with open(os.path.join(directory, f), "rb") as fp:
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
                "Body": body
            })

try:
    with open("test.csv", 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Subject","From","Body"])
        writer.writeheader()
        for data in emails["index"]:
            writer.writerow(data)
except IOError:
    print("I/O error")
