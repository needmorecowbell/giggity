#  Giggity - grab hierarchical data about a github organization, user, or repo

<p align="center">
    <img src="https://user-images.githubusercontent.com/9204902/51312125-3aa4d700-1a53-11e9-89e8-a02063d93595.gif"></img>
</p>

Get information about an organization, user, or repo on github. Stores all data in a json file, organized in a tree of dictionaries for easy database transfer or data analysis. All done through the github api, with or without authentication (authentication highly recommended).

## Setup

`pip3 install -r requirements.txt`


## Operation

```
giggity.py [-h] [-v] [-a] [-u] [-o] [-O OUTPUT] path

positional arguments:
  path                  name of organization or user (or url of repository)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -a, --authenticate    allows github authentication to avoid ratelimiting
  -u, --user            denotes that given input is a user
  -o, --org             denotes that given input is an organization
  -O OUTPUT, --outfile OUTPUT
                        location to put generated json file

```

**Example of Scraping a User**

    python3 giggity.py -a -O needmorecowbell.json -v -u needmorecowbell

- This will ask for authentication credentials, put the program into verbose mode, scrape github for the user needmorecowbell, then put the results into needmorecowbell.json

**Example of Scraping an Organization**

    python3 giggity.py -a -o github -O github.json

- This will ask for authentication, scrape the github organization on github, then put out the results in github.json

**Giggity as a Module** 

- giggity can also be used as a module -- all data is stored within orgTree as a nested dict.

```python
from giggity import giggity

g = giggity("username","password")
data = g.getUsers("organization-name", followers=True)

print("List of users in organization: ")
for user, info in data.items():
    print(user)

data = g.getEmails("username", verbose=True) # Get any emails found
```

**Other examples of how to use giggity are available in the util folder.**
