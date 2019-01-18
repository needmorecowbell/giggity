import getpass 
import argparse
import requests
import json

class giggity():

    def __init__(self, auth_usr="", auth_pss=""):

        self.orgTree = {}
        self.header ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.auth = (auth_usr,auth_pss)
        
    def getUsers(self, org, verbose=False):
        if(verbose):
            print("Sraping organization: "+org)

        r = requests.get("https://api.github.com/orgs/"+org+"/members", headers=self.header, auth=self.auth)
        result = r.json()
        tree = {}
        print(result)

        if("message" in result):
            print("Organization Not Found")
        
        else: 
            for account in result:
                account["repos"]= self.getRepos(account["login"])
                tree[account["login"]] = account

            self.orgTree["users"] = tree

        self.orgTree["users"] = tree
        return tree

    def getFollowers(self, user, verbose=False):
        if(verbose):
            print("Getting followers of user: "+user)
            
        r = requests.get("https://api.github.com/users/"+user+"/followers",headers=self.header, auth=self.auth)
        result= r.json()
        return result

    def getRepos(self, user, verbose=False):
        if(verbose):
            print("Getting repositories for user: "+user)

        r = requests.get("https://api.github.com/users/"+user+"/repos", headers=self.header, auth=self.auth)
        result = r.json()
        repoTree= {}

        if("message" in result):
            print("User Not Found")
        
        else: 
 
            for repo in result:
                if(verbose):
                    print("Getting repo: "+repo["name"])
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

   __ _(_) __ _  __ _(_) |_ _   _ 
  / _` | |/ _` |/ _` | | __| | | |
 | (_| | | (_| | (_| | | |_| |_| |
  \__, |_|\__, |\__, |_|\__|\__, |
  |___/   |___/ |___/       |___/ 
""")
    print("\t a needmorecowbell project\n")
    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-a", "--authenticate", help="allows github authentication to avoid ratelimiting",action="store_true")
    parser.add_argument("-u", "--user",help="denotes that given input is a user",action="store_true")
    parser.add_argument("-o", "--org",help="denotes that given input is an organization",action="store_true")
    parser.add_argument("-O", "--outfile", dest="output", help="location to put generated json file")
    parser.add_argument("path",help="name of organization or user (or url of  repository)")

    
    
    args = parser.parse_args() 
    
    outfile= "results.json"
    if(args.path is None):
        print("No input given")
        exit()

    target = args.path

    if(args.output is not None):
        outfile= args.output

    if(args.authenticate):
        user = input("Enter Github Username: ")
        psswd = getpass.getpass("Enter Github Password: ")
        g = giggity(user ,psswd)
    else:
        g = giggity()

    if(args.user):
        res= g.getRepos(target, args.verbose)
        with open(outfile , 'w') as out:
            json.dump(res, out, indent=4 , sort_keys=True)


    if(args.org):
        g.getUsers(target, args.verbose)
        g.writeToFile(outfile)
       
    print("Scraping Complete, file available at: "+outfile)



