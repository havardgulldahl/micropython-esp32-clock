
# to get all riddles:
# curl http://www.xn--gter-qoa.no/api/all | jq -r '.riddles | .[] | select(.answer != null) | select((.question | length) < 60 and (.answer | length) < 60)| [.question,.answer] | @csv' > riddles.csv
# L=$(wc -l riddles.csv | while read lines name; do echo $lines; done); mv riddles.csv riddles.csv:$L

import random
import os # pylint: disable=import-error
import gc

RIDDLE_FILENAME="riddles.csv"

def get_riddle() -> tuple:
    riddles = None
    for f in os.listdir():
        # look for file named <RIDDLE_FILENAME>:<LINECOUNT>
        if f.startswith(RIDDLE_FILENAME):
            lines = int(f.rsplit(":")[1])
            riddles = open(f)
            break
    gc.collect()
    if riddles is None:
        raise Exception("Could not read riddlefile!")
    randomline = random.randint(0, lines) # get a random line number
    i = 0
    line = riddles.readline().strip()
    while line:
        if i == randomline:
            # find split
            _split = line.index('","')+1
            ques = line[1:_split-1]
            answ = line[_split+2:-1]
            return (ques, answ)
        # look at next line
        line = riddles.readline().strip()
        i = i+1

