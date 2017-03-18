from random import randint, shuffle
from sys import exit

# Read the contestants from file
with open("contestants.txt") as f:
    content = f.readlines()

# Split into lists of 128
tiers = [[], [], []]
for line in content:
    char, line = line.split(" [")
    source, rank = "", ""
    try:
        source, rank = line.split("] ")
    except ValueError:
        source, rank = line, ""
    triple = (char, source, rank)
    if "32" in rank or "64" in "rank" or "MM" in "rank":
        tiers[0].append(triple)
    elif "128" in rank or "NEW" in "rank":
        tiers[1].append(triple)
    elif "FAIL" in rank:
        tiers[2].append(triple)
    else:
        i = randint(0, 2)
        tiers[i].append(triple)
while not (len(tiers[0]) == 128 and len(tiers[1]) == 128 and len(tiers[2]) == 128):
    maximal = tiers[0]
    minimal = tiers[2]
    if len(tiers[1]) > len(maximal):
        maximal = tiers[1]
    if len(tiers[2]) > len(maximal):
        maximal = tiers[2]
    if len(tiers[1]) < len(minimal):
        minimal = tiers[1]
    if len(tiers[0]) < len(minimal):
        minimal = tiers[0]
    while True:
        i = randint(0, len(maximal))
        try:
            rank = maximal[i][2]
        except IndexError:
            continue
        if len(rank) > 0:
            minimal.append(maximal.pop(i))
            break

# Reorder tiers[0] so that:
# * 2 of the top 32 won't appear in the same block of 4
# * 2 of the top 64 won't appear in the same block of 2
top32 = []
top64 = []
other = []
for char in tiers[0]:
    if "32" in char[2]:
        top32.append(char)
    elif "64" in char[2]:
        top64.append(char)
    else:
        other.append(char)
tiers[0] = []
while len(other) > 0:
    try:
        if len(top64) > 0:
            tiers[0].append(top64.pop())
        else:
            tiers[0].append(other.pop())
        if len(top32) > 0:
            tiers[0].append(top32.pop())
        else:
            tiers[0].append(other.pop())
        tiers[0].append(other.pop())
        if len(top64) > 0:
            tiers[0].append(top64.pop())
        else:
            tiers[0].append(other.pop())
    except IndexError:
        continue

# Randomly reorder tiers[1] and tiers[2] so that:
# * Characters from the same game won't appear in the same round
shuffle(tiers[1])
shuffle(tiers[2])
for i in range(128):
    if tiers[0][i][1] == tiers[1][i][1]:
        j = i
        while tiers[1][j][1] == tiers[0][i][1]:
            j = j + 1 % 128
        tiers[1][i], tiers[1][j] = tiers[1][j], tiers[1][i]
    if tiers[0][i][1] == tiers[2][i][1] or tiers[1][i][1] == tiers[2][i][1]:
        j = i
        while tiers[2][j][1] == tiers[2][i][1]:
            j = j + 1 % 128
        tiers[2][i], tiers[2][j] = tiers[2][j], tiers[2][i]

# Print
PERMS = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))
def printchar(j, k, i):
    char = tiers[PERMS[j][k]][i]
    return char[0] + " - " + char[1].split("]")[0]
s = "\tBRACKETS:\n\n"
for i in range(128):
    if i % 16 == 0:
        s += "\n\tBRACKET " + str(i // 16) + ":\n"
    j = randint(0, 5)
    s += printchar(j, 0, i) + "\n\t" + printchar(j, 1, i) + "\n\t" + printchar(j, 2, i) + "\n"
s += "\n\n"
with open("brackets.txt", "a") as f:
    f.write(s)
