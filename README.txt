How to use:
    - manually enter Q/A file and Answer Key file as ex*.txt, ex*_ans.txt
        > example: ex1.txt, ex1_ans.txt
    - run "sh kp.sh ex*"
        > example: "sh kp.sh ex1"
    - output: ex*_fix.txt, ex*.json
        > example: ex1_fix.txt, ex1.json
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

05/17
    -- update answer parsing 
    -- update file cleanup -> move things to bak folder

05/18
    -- add explanation parsing 
        > opens PDF, reads text, splits based on (簡解 | 詳解) -> simple explain, detailed explain -> gives us simple explanations
        > also use regex to find the question number for each explanation (in case any question numbers are skipped)
        > saves into array of dictionaries
        ** DONE : use AoD to update explanations for question array 

05/20
    -- update explanation parsing 
    ** works in general, need to test each input for special cases because not all of them are created equally / flawlessly
