import sys
import json

filesToCompare = sys.argv[1:]

file1 = filesToCompare[0]
file2 = filesToCompare[1]
outputFile = filesToCompare[2]

compareResults = {
    "filesMissing": [],
    "filesMatching": [],
    "filesChanged": []
}

with open(file1, "r") as manifestFile:
    manifest1 = json.loads(manifestFile.read())

with open(file2, "r") as manifestFile:
    manifest2 = json.loads(manifestFile.read())


for key in manifest1:
    if key not in manifest2:
        compareResults["filesMissing"].append(key)

    if key in manifest2 and manifest1[key] == manifest2[key]:
        compareResults["filesMatching"].append(key)

    if key in manifest2 and manifest1[key] != manifest2[key]:
        compareResults["filesChanged"].append(key)

with open(outputFile, "w") as changesFile:
    changesFile.write(json.dumps(compareResults, indent="\t"))