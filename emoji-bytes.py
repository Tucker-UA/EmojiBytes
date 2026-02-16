### Imports, as simple as possible
import sys, os


### Emoji Encodings
### List one for each base system I want to do

### FORMAT:
###     list with each entry a unicode 8 digit hexcode
###     Mapping goes from index ---> UGGGGGGGG
###     0's are added at the front of the number if needed

# First encoding, symbols are ❌ & ✔ 
emojiBinary = {0 : "\u274C", 1 : "\u2714"}
# Second encoding, symbols are 🍇, 🍈, 🍉, & 🍊 
emojiQuartary = {0 : '\U0001f347', 1 : '\U0001f348',
                 2 : '\U0001f349', 3 : '\U0001f34a'}
# Third encoding, symbols are an extension of emojiQuartary
emojiHex = {i : chr(127815+i) for i in range(16)}
# Fourth encoding, should be able to handle whole bytes now
emoji256ary = {i : chr(127815+i) for i in range(256)}

# Gives all encodings here
encodings = {'2' : emojiBinary, '4' : emojiQuartary, '16' : emojiHex, '256' : emoji256ary}

possibleLengths = [len(enc) for enc in encodings.values()] # All possible lengths 

# Function for checking if I can encode/decode using given encoding

def checkEncoding(encoding):
    n = len(encoding)
    
    if n not in possibleLengths:
        raise Exception(f"Encoding with length {n} currently not supported for decoding")

    return True # Returns True to show that the encoding is a good one

### Functions for reading to and from files

def fromFile(filename, filetype):
    # Gets contents from filename with filetype
    # filetype: either 'rb' or 'r'
    # returns the contents of file
    
    with open(filename, filetype) as file:
        contents = file.read()

    return contents

def toFile(filename, filetype, contents):
    # Sends contents to filename with filetype
    # filetype: either 'wb' or 'w'
    # returns the filename given

    with open(filename, filetype) as file:
        file.write(contents)

    return filename

### Functions for encoding strings and bytes

def byteToEncodedString(byte, encoding):
    # Only works when our encoding is 2, 4, 16, or 256 

    n = len(encoding)

    checkEncoding(encoding)

    # Gets the max power of 2 that divides n
    i = max(j for j in range(1,9) if n % (2**j) == 0)
    numPerByte = 8 // i

    # Breaks up the bytes into smaller chunks for encodings that can't do a full byte
    nBits = [((byte << (i*(j+1))) // 256) % n for j in range(numPerByte)]

    encodedString = ''.join([encoding[bits] for bits in nBits])

    return encodedString

def bytesToEncodedString(byteList, encoding):
    encodedString = ''.join(byteToEncodedString(byte, encoding) for byte in byteList)

    return encodedString

def stringToEncodedString(plaintext, encoding):
    encodedString = bytesToEncodedString(bytes(plaintext, 'utf-8'), encoding)

    return encodedString

def fileToEncodedString(filename, filetype, encoding):
    # Takes in a filename and filetype either in binary or latin-1 text
    # Outputs to the console as well as a file: encoded-filename
    # filename: path to file
    # filetype: either 'rb' for binary or 'r' for latin-1 text

    contents = fromFile(filename, filetype)
    newFile = filename + '-encoded'
    
    if filetype == 'rb':
        encodedContents = bytesToEncodedString(contents, encoding)
    elif filetype == 'r':
        encodedContents = stringToEncodedString(contents, encoding)
    else:
        raise Exception(f"Filetype {filetype} not supported.")

    toFile(newFile, 'w', encodedContents)

    return encodedContents

### Functions for decoding strings

def stringToDecodedBytes(encodedString, encoding):
    # Takes in a string of emoji and outputs the corresponding bytes
    # If the encoding is not one of the four possible lengths, raise an error

    n = len(encoding)

    checkEncoding(encoding)

    # i gets the max power of 2 that the length of the encoding is divisible by
    # This is used to find how many emoji are needed for bytes
    i = max(j for j in range(1,9) if n % (2**j) == 0)

    decoding = {v : k for k, v in encoding.items()}

    # Translated each given emoji in the encoded string to an int
    decodedInts = [decoding[c] for c in encodedString]

    numPerByte = 8 // i
    decodedBytes = []

    # loops through all the decoded ints and builds a single byte for each round of a loop
    for j, d in enumerate(decodedInts[::numPerByte]):
        b = d
        for k in range(1,numPerByte):
            b = (b << i) | decodedInts[j*numPerByte+k]

        decodedBytes.append(b)

    return bytes(decodedBytes)

def stringToDecodedString(encodedString, encoding):
    # Takes in a string of emoji and outputs the decoded string
    decodedString = stringToDecodedBytes(encodedString, encoding).decode()

    return decodedString

def fileToDecodedString(filename, filetype, encoding):
    # Takes in a filename that is full of emoji
    # Outputs to the console as a well as a file: decoded-filename
    # filename: path to file
    # filetype: type of file to write, either 'wb' or 'w'

    contents = fromFile(filename, 'r')
    newFile = filename + '-decoded'
    decodedContents = stringToDecodedString(contents, encoding)
    toFile(newFile, filetype, decodedContents)

    return decodedContents

### Functions for parsing arguments and running the script when called

def parseArgs(args):
    # Function to parse the command line arguments
    # Returns a dict in this format
    # { 'name'      : name of this file                 type: string
    #   'message'   : message to encode or decode       type: string
    #   'inputFile' : file name(s) of input file(s)     type: string
    #   'outputFile': file name(s) of output file(s)    type: string
    #   'filetype'  : file type of file, i.e., wb or w  type: string
    #   'decoding'  : true if decoding, false o.w       type: boolean
    #   'encoding'  : name of encoding to use           type: string}

    helpMessage = """emoji-bytes [options] file_or_message

    Options:
     -d, --decode: set program to decoding mode
     -t, --target: target file to output to
     -b, --binary: set filetype to binary for read/write
     --encoding:   name of encoding to use, assumes 256 by default
     -h, --help:   print help text"""

    name = args[0]
    
    options = []

    targetOptions = ['-t', '--target']
    decodeOptions = ['-d', '--decode']
    encodeOptions = ['--encoding']
    fileOptions   = ['-b', '--binary']
    helpOptions   = ['-h', '--help']
    possibleOptions = targetOptions + decodeOptions + encodeOptions + fileOptions + helpOptions


    for i, arg in enumerate(args[1:]):
        if arg[0] == '-':
            if arg[1] != '-':
                allArgs = arg[1:]
                
                for a in allArgs:
                    options.append(('-'+a, i+1))
            else:
                options.append((arg, i+1))
            

    parsed = {'name' : name, 'decoding' : False, 'encoding' : '256', 'filetype': ''}
    
    if options == []:
        index = 0
    else:
        for arg, i in options:
            index = i
            if arg in decodeOptions:
                parsed['decoding'] = True
            elif arg in targetOptions:
                index += 1
                parsed['outputFile'] = args[i+1]
            elif arg in encodeOptions:
                index += 1
                parsed['encoding'] = args[i+1]
            elif arg in fileOptions:
                parsed['filetype'] = 'b'
            elif arg in helpOptions:
                raise Exception(helpMessage)

    if len(args) <= index+1:
        raise Exception(helpMessage)
    elif os.path.isfile(args[index+1]):
        parsed['inputFile'] = ' '.join(args[index+1:])
        parsed['filetype'] = 'r' + parsed['filetype'] if not parsed['decoding'] else 'w' + parsed['filetype']
    else:
        parsed['message'] = ' '.join(args[index+1:])

    return parsed

def main(args):
    parsed = parseArgs(args)

    encoding = encodings[parsed['encoding']]

    if 'inputFile' in parsed:
        inputFile = parsed['inputFile']
        filetype = parsed['filetype']
        contents = fileToEncodedString(inputFile, filetype, encoding) if not parsed['decoding'] else fileToDecodedString(inputFile, filetype, encoding)
    else:
        message = parsed['message']
        contents = stringToEncodedString(message, encoding) if not parsed['decoding'] else stringToDecodedString(message, encoding)

    return contents

if __name__ == "__main__":
    args = sys.argv
    print(main(args))
    
