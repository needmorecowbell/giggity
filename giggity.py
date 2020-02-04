import getpass
import argparse
import requests
from nested_lookup import nested_lookup
import json

class giggity():

    def __init__(self, auth_usr="", auth_pss="", depth=0):
        self.depth = depth

        self.orgTree = {}
        self.header ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.auth = (auth_usr,auth_pss)

    def getUsers(self, org, verbose=False, followers=False):
        if(verbose):
            print("Sraping organization: "+org)

        page=1
        isEmpty=False;
        tree = {}

        while(not isEmpty):
            r = requests.get("https://api.github.com/orgs/"+org+"/members?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result= r.json()
            page+=1
            if(len(result)==0):
                isEmpty=True

            elif("message" in  result):
                print("Organization not found")
            else:
                for account in result:

                    #Remove unnecessary items
                    account.pop('node_id', None)
                    account.pop('avatar_url',None)
                    account.pop('gravatar_id',None)
                    account.pop('url',None)
                    account.pop('followers_url', None)
                    account.pop('following_url',None)
                    account.pop('gists_url',None)
                    account.pop('starred_url',None)
                    account.pop('subscriptions_url', None)
                    account.pop('organizations_url',None)
                    account.pop('repos_url',None)
                    account.pop('events_url',None)
                    account.pop('received_events_url',None)


                    #This is where you would branch out and do additional searches on an account
                    account["repos"]= self.getRepos(account["login"], verbose)
                    #ie, get all user repos, then tie them back into the data structure before appending it to tree

                    if(followers):
                        account["followers"]= self.getFollowers(account["login"],verbose)

                    account["emails"] = self.getEmails(account["login"],verbose)

                    account["names"] = self.getNames(account["login"], verbose)
                    tree[account["login"]] = account


        self.orgTree["users"] = tree
        return tree

    def getFollowers(self, user, depth=0, verbose=False):
        page=1
        isEmpty=False;
        tree= {}

        while (not isEmpty):
            r = requests.get(
                "https://api.github.com/users/" + user + "/followers?page=" + str(page) + "&per_page=100",
                headers=self.header, auth=self.auth)
            result = r.json()
            page += 1

            if (len(result) == 0):
                isEmpty = True

            elif ("message" in result):
                print("User not found")
            else:
                for account in result:
                    #Remove unnecessary items
                    account.pop('node_id', None)
                    account.pop('avatar_url',None)
                    account.pop('gravatar_id',None)
                    account.pop('url',None)
                    account.pop('followers_url', None)
                    account.pop('following_url',None)
                    account.pop('gists_url',None)
                    account.pop('starred_url',None)
                    account.pop('subscriptions_url', None)
                    account.pop('organizations_url',None)
                    account.pop('repos_url',None)
                    account.pop('events_url',None)
                    account.pop('received_events_url',None)

                    #This is where additional queries for followers will go (get names, emails, etc)
                    account["emails"] = self.getEmails(account["login"],verbose)
                    account["names"] = self.getNames(account["login"], verbose)

                    depth -= 1
                    if depth >= 0:
                        account["followers"] = self.getFollowers(account["login"], depth, verbose)
                    depth += 1

                    # add user's data as branch of main tree
                    tree[account["login"]] = account

        if(verbose):
             print("["+user+"] Number of followers found: "+str(len(tree.items())))


        return tree

    def getEmails(self, user, verbose=False):

        page=1
        isEmpty=False;
        emails= []

        while(not isEmpty):
            r = requests.get("https://api.github.com/users/"+user+"/events/public?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result = r.json()
            page+=1
            if("message" in result):
                if("pagination" in result["message"]):
                    isEmpty=True
                else:
                    print("Error: "+result["message"])
                    isEmpty=True

            elif(len(result)==0):
                isEmpty=True
            else:
                for event in result:
                    res = set(nested_lookup("email",event))

                    if(len(res)>0): #append any new emails
                        emails= emails+ list(res)

        emails = list(set(emails)) # remove duplicates

        if(verbose):
             print("["+user+"] Number of emails found: "+str(len(emails)))

        return emails

    def getNames(self, user, verbose=False):

        page=1
        isEmpty=False;
        names= [] # avoid duplicates with a set

        while(not isEmpty):
            r = requests.get("https://api.github.com/users/"+user+"/events/public?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result = r.json()
            page+=1

            if("message" in result):
                if("pagination" in result["message"]):
                    isEmpty = True
                else:
                    print("Error: "+result["message"])
                    isEmpty=True

            elif(len(result)==0):
                isEmpty=True
            else:
                for event in result:
                    res = nested_lookup("author",event)
                    for author in res:
                        name= nested_lookup("name",author)
                   # res = set(nested_lookup("name",res))
                    if(len(res)>0):
                        names= names + name

        names = list(set(names))
        if(verbose):
             print("["+user+"] Number of names found: "+str(len(names)))

        return names

    def getRepos(self, user, org=False, verbose=False):

        page=1
        isEmpty=False;
        repoTree= {}

        while(not isEmpty):
            if(org):
                r = requests.get("https://api.github.com/orgs/"+user+"/repos?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            else:
                r = requests.get("https://api.github.com/users/"+user+"/repos?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result = r.json()
            page+=1

            if("message" in result):
                print("User Not Found")
            elif(len(result)==0):
                isEmpty=True
            else:
                if(verbose):
                    print("["+user+"] Number of repositories found: "+str(len(result)))

                for repo in result:
                    tree = {
                        "name": repo["name"],
                        "url":repo["html_url"],
                        "fork":repo["fork"],
                        "description":repo["description"],
                        "created_at":repo["created_at"],
                        "updated_at":repo["updated_at"],
                    }

                    repoTree[repo["name"]] = tree

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
    print("")
    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-a", "--authenticate", help="allows github authentication to avoid ratelimiting",action="store_true")
    parser.add_argument("-u", "--user",help="denotes that given input is a user",action="store_true")
    parser.add_argument("-d", "--depth", help="indicates the depth for extracting followers info")
    parser.add_argument("-o", "--org",help="denotes that given input is an organization",action="store_true")
    parser.add_argument("-f", "--followers",help="adds followers entry to each account",action="store_true")
    parser.add_argument("-O", "--outfile", dest="output", help="location to put generated json file")
    parser.add_argument("path", help="name of organization or user (or url of  repository)")

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
        if (args.depth):
            g = giggity(user, psswd, int(args.depth))
        else:
            g = giggity(user, psswd)
    else:
        g = giggity()

    if(args.user):
        tree={}
        tree["repos"]= g.getRepos(target, verbose=args.verbose)
        tree["emails"]= g.getEmails(target, verbose=args.verbose)
        tree["names"] = g.getNames(target, verbose=args.verbose)

        if(args.followers):
            tree["followers"] = g.getFollowers(target, int(args.depth), verbose=args.verbose)

        with open(outfile , 'w') as out:
            json.dump(tree, out, indent=4 , sort_keys=True)

    if(args.org):
        tree = {}
        tree["repos"] = g.getRepos(target, org=True, verbose=True )

        tree["users"]= g.getUsers(target, verbose=args.verbose, followers=args.followers)
        with open(outfile , 'w') as out:
            json.dump(tree, out, indent=4 , sort_keys=True)

    print("Scraping Complete, file available at: "+outfile)



