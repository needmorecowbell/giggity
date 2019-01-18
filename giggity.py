import getpass 
import argparse
import requests
from nested_lookup import nested_lookup
import json

class giggity():
    
    def __init__(self, auth_usr="", auth_pss=""):

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
                    account["repos"]= self.getRepos(account["login"], verbose) #ie, get all user repos, then tie them back into the data structure before appending it to tree
                    if(followers):
                        account["followers"]= self.getFollowers(account["login"],verbose)
                   
                    account["emails"] = self.getEmails(account["login"],verbose)

                    tree[account["login"]] = account


        self.orgTree["users"] = tree
        return tree



    def getFollowers(self, user, verbose=False):

        if(verbose):
            print("Getting followers of user: "+user)

        page=1
        isEmpty=False;
        tree= {}
        
        while(not isEmpty):
            r = requests.get("https://api.github.com/users/"+user+"/followers?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result= r.json()
            page+=1

            if(len(result)==0):
                isEmpty=True

            elif("message" in  result):
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

                    #add user's data as branch of main tree 
                    tree[account["login"]]= account
        
        return tree

    def getEmails(self, user, verbose=False):
        if(verbose):
            print("Getting any emails from user: "+user)

        page=1
        isEmpty=False;
        emails= [] # avoid duplicates with a set
        
        while(not isEmpty):
            r = requests.get("https://api.github.com/users/"+user+"/events/public?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result = r.json()
            page+=1
            
            if("message" in result):
                print("Api Pagination Limit Reached")
                isEmpty=True
            elif(len(result)==0):
                isEmpty=True
            else: 
                for event in result:
                    res = set(nested_lookup("email",event))

                    if(len(res)>0):
                        emails= emails+ list(res)

                    #print(set(nested_lookup("email",event)))
                    #emails.add(set(nested_lookup("email",event)))

        if(verbose):
             print("Number of emails found for : "+str(len(emails)))

        return emails
 
    def getRepos(self, user, verbose=False):
        if(verbose):
            print("Getting repositories for user: "+user)

        page=1
        isEmpty=False;
        repoTree= {}
        
        while(not isEmpty):
            r = requests.get("https://api.github.com/users/"+user+"/repos?page="+str(page)+"&per_page=100", headers=self.header, auth=self.auth)
            result = r.json()
            page+=1
            
            if("message" in result):
                print("User Not Found")
            elif(len(result)==0):
                isEmpty=True
            else: 
                if(verbose):
                    print("Number of repositories: "+str(len(result)))

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
    parser.add_argument("-f", "--followers",help="adds followers entry to each account",action="store_true")
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
        tree={} 
        tree["repos"]= g.getRepos(target, args.verbose)

        if(args.followers):
            tree["followers"] = g.getFollowers(target, args.verbose)

        with open(outfile , 'w') as out:
            json.dump(tree, out, indent=4 , sort_keys=True)


    if(args.org):
        g.getUsers(target, args.verbose, args.followers)
        g.writeToFile(outfile)
       
    print("Scraping Complete, file available at: "+outfile)



