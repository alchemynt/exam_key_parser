How to use:
    - manually enter Q/A file and Answer Key file as ex*.txt, ex*_ans.txt
        > example: ex1.txt, ex1_ans.txt
    - run "sh kp.sh ex*"
        > example: "sh kp.sh ex1"
    - output: ex1_fix.txt, ex1.json
    - enter ex1.json to database



05/13
    -- git init 
    -- gh repo create 
    -- takes questions file and cleans so 1 line per question/answer 
    -- uses cleaned file to build question object array 
    -- uses answer-key file to add answers to question object array
    -- uses question object array to build json structure file 

    >> need to finish check_line function 

05/16
    -- temp fix to check_line function (make sure qnum != 0)
        ** improve to track qnum properly 
    -- update to use sys.argv 
    -- set up shell script
        ** need to set up Qs and As separately, _fixed and _json built