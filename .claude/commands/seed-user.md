---
description: Create a single dummy user in database
allowed-tools: Read,Bash(python3:*)
---
Read database/db.py to understand the user table schemda and get_db() helper.
then write and run a python script using Bash that :
1.generates a realistic randim indian user using your own knowlege of comman names across region :
    name : should sound like real one 
    email : name plus some number  with real domain some
    password : must have at least 8 letter ,must have letter,uppercase one,number and symbol
    datetime:gen realtime base on syste,

2. check if email already exist generate new unitill unique

3. insert into databse using the same get_db() pattern found in db.py

4.priitns confirmation:
    id
    name
    email
    