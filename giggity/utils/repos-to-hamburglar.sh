# setup hamburglar.py before running
# put inside blank directory with repodump.py, and results.json, and hamburglar.py
# add rule directory path if using yara 

python3 repodump.py >> repos.txt;
mkdir out;
for f in `cat repos.txt`; do
   # Yara Rule checking  
   # python3 hamburglar.py -y rules/ -g $f;

   # Regex rule checking
    python3 hamburglar.py -g $f;
     mv *.json out;
 done

 rm repos.txt


