###
# Scrapes all repo urls from an organization
# TIP: This would be a great precursor to a hamburglar.py script
###


import json

def getRepos(d):
    repos = []
    for user, info in d["users"].items():
        for repo, repoVal in  info["repos"].items():
            repos.append(repoVal["url"])

    return list(set(repos))


d = json.loads(open("results.json").read())
repos = getRepos(d)



for repo in repos:
    print(repo)

#print("Repos found: "+str(len(repos)))
