def contains(a,b):
    return 1 if ((a[0]<=b[0] and a[1]>=b[1])
            or b[0]<=a[0] and b[1]>=a[1]) else 0

def overlaps(a,b):
    return 1 if any(range(max(a[0],b[0]),min(a[1],b[1])+1)) else 0

with open("input4.txt") as f:
    pairs = [[list(map(int,r.split("-"))) for r in line.split(",")] for line in f]
print(sum(contains(*pair) for pair in pairs))
print(sum(overlaps(*pair) for pair in pairs))