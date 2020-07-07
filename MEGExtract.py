import os

inputFileName = "MUSIC.MEG"  # edit the filename here to extract other *.MEG files

inputFile = open(inputFileName, "rb")
sizeHeader = 24  # fixed header size of 24 bytes
header = inputFile.read(sizeHeader)
firstFileStream = int.from_bytes(header[8:12], byteorder='little')  # header tells us where the first filestream begins
numberOfFiles = int.from_bytes(header[12:16], byteorder='little')  # header tells us the number of all files included
lenDatablockFilenames = int.from_bytes(header[20:sizeHeader], byteorder='little')  # header tells us the length of the block containing the filenames
del header
fileNamesBlock = inputFile.read(lenDatablockFilenames)
metaInfo = inputFile.read(firstFileStream - inputFile.tell())
fileNames = []
currentPosition = 0
for i in range(0, numberOfFiles, 1):  # safe all filenames to a list to assign them later, they are not ordered in any way (first file != first filename)
    size = int.from_bytes(fileNamesBlock[currentPosition:currentPosition + 1], byteorder='little')  # first byte of filename tells us how long this name is
    currentPosition += 2  # second byte of filename is always 0x00
    fileNames.append(str(fileNamesBlock[currentPosition:currentPosition + size], 'utf-8'))
    currentPosition += size
del fileNamesBlock
currentPosition = 0
for i in range(0, numberOfFiles, 1):  # extract every file
    size = int.from_bytes(metaInfo[currentPosition + 10:currentPosition + 14], byteorder='little')  # metainfo tells us the size of the filestream
    start = int.from_bytes(metaInfo[currentPosition + 14:currentPosition + 18], byteorder='little')  # metainfo tells us where the filestream begins
    index = int.from_bytes(metaInfo[currentPosition + 18:currentPosition + 20], byteorder='little')  # metainfo tells us the associated filename for this stream
    if not os.path.exists(os.path.dirname(fileNames[index])):  # check whether the path for extraction exists, it will be created otherwise
        os.makedirs(os.path.dirname(fileNames[index]))
    output = open(fileNames[index], "wb")
    inputFile.seek(start)
    output.write(inputFile.read(size))
    output.close()
    currentPosition += 20  # +20, because for every file a block of 20 bytes is reserved containing the 'metaInfo'
del fileNames
del metaInfo
inputFile.close()
print("finished extracting " + inputFileName)
