---
description: seed realstic dummy expense for a specific use
argument-hint: "<user_id><count><month>"
allowed-tools: Read,Bash(py:*)
---

--
Read database/db.py to understand the user expense table schemda and get_db() helper, and db connection pattern.

user input: $ARGUMENTS

## step1 - Parse arguments
excrat from ARGUMENT:
user_id-integer
-count- interger,number of expenese to create
-month - integer, how many month to spread them across

if nay arguments is missing ro not valid integer , stop and say :
"usage:/seed-expense <user-id><count><month>"

## verify - user exists
verifty the user id exits in user table 
if not say "user not exits" and user first using "\.claude\commands\seed-user.md" but ask before creating new user , give two option genreate new by try again or you want to create new user of this detials and entry expenes 

## gen and insert
write py script that:
1. spreads expens randomly across thr past <months> months
2. use these categories with realstic indian descroption :
    - Food :50-800
    - Transport:10-500
    - Bills:200-3000
    - Health:0-50000
    - Entertainment:0-8000
    - Shopping:500-5000
    - Other:200-500
3. distribute the category roughly 
4. use the db connection pattern from db.py 
    - but do not hardcode the database filename
5. use parameterised query only -no strong formating in sql
6. insert all expenes in a single trascation -
roll bakc everhting if any insert fails