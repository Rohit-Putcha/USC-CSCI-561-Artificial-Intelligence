def writeOutput(content, path="output.txt"):
        f = open(path, "w")
        f.write(content)
        f.close()