with open("input1.txt") as f:
    packages = sorted([[int(i) for i in package.split()] for package in f.read().split("\n\n")])
print(sum(packages[-1]), sum(map(sum, packages[-3:])))