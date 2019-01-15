import getpass 
import argparse
import requests
import json

class gigitty():

    def __init__(self, auth_usr="", auth_pss=""):

        self.orgTree = {}
        self.header ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.auth = (auth_usr,auth_pss)
        
    def getUsers(self, org):
        print("Sraping organization: "+org)
        r = requests.get("https://api.github.com/orgs/"+org+"/members", headers=self.header, auth=self.auth)
        result = r.json()
        tree = {}

        for account in result:
            account["repos"]= self.getRepos(account["login"])
            tree[account["login"]] = account


        self.orgTree["users"] = tree


    def getFollowers(self, user):
        print("Getting followers of user: "+user)
        r = requests.get("https://api.github.com/users/"+user+"/followers",headers=self.header, auth=self.auth)
        result= r.json()
        return result

    def getRepos(self, user):
        print("Getting repositories for user: "+user)
        r = requests.get("https://api.github.com/users/"+user+"/repos", headers=self.header, auth=self.auth)
        result = r.json()
        repoTree= {}

        for repo in result:
            tree= {"name": repo["name"],
                   "url":repo["html_url"],
                   "fork":repo["fork"],
                   "description":repo["description"],
                   "created_at":repo["created_at"],
                   "updated_at":repo["updated_at"],
                   }
            repoTree[repo["name"]]=tree
        
        return repoTree
    
    def getTree(self):
        return json.dumps(self.orgTree,indent=4, sort_keys=True)
    
    def writeToFile(self, filepath):
        with open(filepath , 'w') as outfile:
            json.dump(self.orgTree, outfile, indent=4 , sort_keys=True)



if __name__ == '__main__':

    print("""
   __ _(_) __ _(_) |_| |_ _   _ 
  / _` | |/ _` | | __| __| | | |
 | (_| | | (_| | | |_| |_| |_| |
  \__, |_|\__, |_|\__|\__|\__, |
  |___/   |___/           |___/ 
""")
    print("\t a needmorecowbell project")
    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-a", "--authenticate", help="allows github authentication to avoid ratelimiting",action="store_true")
    parser.add_argument("-o", "--outfile", dest="output", help="location to put generated json file")
    
    args = parser.parse_args() 
    outfile= "results.json"

    if(args.output is not None):
        outfile= args.output

    if(args.authenticate):
        user = input("Enter Github Username: ")
        psswd = getpass.getpass("Enter Github Password: ")
        g = gigitty(user ,psswd)
    else:
        g = gigitty()

    g.getUsers("github")
    g.writeToFile(outfile)
    print("Scraping Complete, file available at: "+outfile)



