###
# Scrapes all emails from an organization
#
###


import json

def getEmails(d):
    emails = []
    for user, info in d["users"].items():
        emails = emails +info["emails"]
        if("followers" in info.keys()): # get emails of followers too
            for follower, finfo in info["followers"].items():
                emails = emails + finfo["emails"]

    return list(set(emails))


d = json.loads(open("results.json").read())

emails = getEmails(d)


for email in emails:
    print(email)

print("Emails: "+str(len(emails)))
