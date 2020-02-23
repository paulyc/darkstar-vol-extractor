import sys
import glob
import hashlib
import json
import volinfo
import subprocess
import os
from os.path import isfile, join, exists, split

importFiles = []

def generateGlobs(depth):
    yield "*.*"
    currentDir = "**"
    i = 0
    while (i < depth):
        yield join(currentDir, "*.*")
        currentDir = join(currentDir, "**")
        i += 1


for importFolder in sys.argv[1:]:
    globs = [join(importFolder, x) for x in generateGlobs(10)]
    for folderGlob in globs:
        files = glob.glob(folderGlob)
        importFiles.extend(files)

    fileInfo = {

    }

    for importFile in importFiles:
        print(f"generating hash for {importFile}")
        with open(importFile, "rb") as volumeFile:
            rawData = volumeFile.read()
        fileHash = hashlib.sha256(rawData).hexdigest()
        fileInfo[importFile.replace(importFolder, "")] = fileHash
        if importFile.endswith(".vol") or importFile.endswith(".VOL"):
            file_info = volinfo.get_file_metadata(rawData)

            for file in file_info:
                if file.compression_type == "none":
                    print(f"generating hash for {join(importFile, file.filename)}")
                    fileHash = hashlib.sha256(rawData[file.start_offset:file.end_offset]).hexdigest()
                    fileInfo[join(importFile.replace(importFolder, ""), file.filename)] = fileHash
                else:
                    print(f"generating hash for {join(importFile, file.filename)}")
                    subprocess.call(["extract.exe", importFile, file.filename, join(importFolder, "temp", file.filename)])
                    with open(join(importFolder, "temp", file.filename), "rb") as tempFile:
                        raw_data = tempFile.read()
                    fileHash = hashlib.sha256(raw_data[0:file.size]).hexdigest()
                    fileInfo[join(importFile.replace(importFolder, ""), file.filename)] = fileHash
                    os.remove(join(importFolder, "temp", file.filename))

    print(f"writing {join(importFolder, 'fileManifest.json')}")
    with open(join(importFolder, "fileManifest.json"), "w") as hashFile:
        hashFile.write(json.dumps(fileInfo, indent="\t"))
