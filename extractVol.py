
import sys
import json
import struct
import glob

import os


from collections import namedtuple

importFilenames = sys.argv[1:]

for importFilename in importFilenames:

    print "reading " + importFilename
    try:
        with open(importFilename, "rb") as input_fd:
            rawData = input_fd.read()

	destDir = importFilename.replace(".vol", "").replace(".VOL", "")
	offset = 0
	headerFmt = "<4sL"
	fileFmt = "<4sL"
	footerFmt = "<4sL4sL4sL"
	(header, totalFileLength) = struct.unpack_from(headerFmt, rawData, offset)
	print (header, totalFileLength)
        offset = totalFileLength
        footer = struct.unpack_from(footerFmt, rawData, offset)
	offset += struct.calcsize(footerFmt)
	fileListEndIndex = offset + footer[-1]
	filenames = []
	while offset < fileListEndIndex:
		endIndex = rawData.index("\0", offset)
		filenames.append(rawData[offset:endIndex])
		offset += (endIndex - offset + 1)
	offset = 0
	files = []
	fileIndex = 0
	
	if not os.path.exists(destDir):
	    os.makedirs(destDir)

	while offset < totalFileLength:
		offset = rawData.find("VBLK", offset + 1)
		
		if offset == -1:
			break
		rawFileheader = rawData[offset:offset + struct.calcsize(fileFmt)]
		rawFileheader = rawFileheader[:-1]  +  "\0"
		(fileHeader, fileLength) = struct.unpack(fileFmt, rawFileheader)
		offset += struct.calcsize(fileFmt)
		with open(destDir + "/" + filenames[fileIndex],"w") as shapeFile:
		        newFileByteArray = bytearray(rawData[offset:offset + fileLength])
		        shapeFile.write(newFileByteArray)
		fileIndex += 1



	
    except Exception as e:
        print e
