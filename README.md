#  Giggity - grab heirarchical data about a github organization, user, or repo

<p align="center">
    <img src="res/logo.gif"></img>
</p>

Get information about an organization, user, or repo on github. Stores all data in a json file, organized heirarchically for easy database transfer or data analysis. All done through the github api, with or without authentication (authentication highly recommended).


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

giggity can also be used as a module -- all data is stored within orgTree as a nested dict.

```python
import giggity

g = giggity("username","password")
data = g.getUsers("organization-name")

print("List of users in organization: ")
for user, info in data.items():
    print(user)
```
