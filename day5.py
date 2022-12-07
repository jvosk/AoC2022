import re

def move(stacks, amount, a, b, single=True):
    if single:
        for _ in range(amount):
            stacks[b].append(stacks[a].pop())
    else:
        stacks[b].extend(stacks[a][-amount:])
        stacks[a] = stacks[a][:-amount]

with open("input5.txt") as f:
    stacks, instructions = ''.join(f.readlines()).split("\n\n")
stacks_1 = [[]] + [list(s.strip()[-2::-1]) for s in (''.join(t) for t in zip(*stacks.split('\n'))) if re.search("\d+$",s)]
instructions = [[int(i) for i in re.search(r'move (\d+) from (\d+) to (\d+)', istxn).groups()]
                for istxn in instructions.split("\n") if istxn.strip()]

stacks_2 = [stack[:] for stack in stacks_1]
for op in instructions:
    move(stacks_1, *op, True)
    move(stacks_2, *op, False)
print(''.join(stack[-1] for stack in stacks_1 if stack))
print(''.join(stack[-1] for stack in stacks_2 if stack))