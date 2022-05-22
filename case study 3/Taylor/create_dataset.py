from email.parser import BytesParser
from email.policy import default

import csv
import pandas as pd
import pathlib
import pprint

emails = {"index":[]}

#C:\Users\Taylo\Projects\qtw\case study 3\SpamAssassinMessages
with open(pathlib.Path(__file__).parent / "SpamAssassinMessages/easy_ham/00001.7c53336b37003a9286aba55d2945844c", "rb") as fp:
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
        body = msg.get_payload(decode=True).decode('utf-8')
        
        
    emails["index"].append({
        "Subject": msg.get("Subject"),
        "From": msg.get("from"),
        "Body": body
    })
    # pd.DataFrame()
    # print(msg.get("Subject"))
    # print(msg.get("from"))
    # print(body)
pprint.pprint(emails)
try:
    with open("test.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Subject","From","Body"])
        writer.writeheader()
        for data in emails["index"]:
            writer.writerow(data)
except IOError:
    print("I/O error")
    
    
# foobar = pd.DataFrame.from_dict(emails["index"])

# print(foobar.head())