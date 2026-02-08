### Imports, as simple as possible
import sys, os


### Emoji Encodings
### List one for each base system I want to do
### Ideally, I will eventually have one giant one that I can use
### to make arbitrary bases with within a certain threshold

### FORMAT:
###     list with each entry a unicode 8 digit hexcode
###     Mapping goes from index ---> UGGGGGGGG
###     0's are added at the front of the number if needed


emojiBinary = {0 : "\u274C", 1 : "\u2714"}
# First encoding, symbols are ❌& ✔ 
emojiQuartary = {0 : '\U0001f347', 1 : '\U0001f348',
                 2 : '\U0001f349', 3 : '\U0001f34a'}
# Second encoding, symbols are 🍇, 🍈, 🍉, & 🍊 
emojiHex = {i : chr(127815+i) for i in range(16)}
# Third encoding, symbols are an extension of emojiQuartary
emoji256ary = {i : chr(127815+i) for i in range(256)}
# Fourth encoding, should be able to handle whole bytes now


# Large list to take care of all distinct emoji
# Want to only pick emoji that are easily discernable from each other
masterEmojiList = [ ]

# Gives all encodings here
encodings = {'2' : emojiBinary, '4' : emojiQuartary, '16' : emojiHex, '256' : emoji256ary}

def byteToEncodedString(byte, encoding):
    # Only works when our encoding is 2, 4, 16, or 256 

    n = len(encoding)

    possibleLengths = [2,4,16,256]

    if n not in possibleLengths:
        raise Exception(f"Encoding with length {n} currently not supported for encoding")

    i = max(j for j in range(1,9) if n % (2**j) == 0)

    nBits = [((byte << (i*(j+1))) // 256) % n for j in range(8 // i)]

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

    # Will need to figure out buffering later
    with open(filename, filetype) as file:
        contents = file.read()

    newFile = 'encoded-' + filename
    
    if filetype == 'rb':
        encodedContents = bytesToEncodedString(contents, encoding)
    elif filetype == 'r':
        encodedContents = stringToEncodedString(contents, encoding)
    else:
        raise Exception(f"Filetype {filetype} not supported.")

    toFile(newFile, 'w', encodedContents)

    return encodedContents

def stringToDecodedBytes(encodedString, encoding):
    # Takes in a string of emoji and outputs the corresponding bytes
    # If the encoding is not one of the four possible lengths, raise an error

    n = len(encoding)

    possibleLengths = [2,4,16,256]

    if n not in possibleLengths:
        raise Exception(f"Encoding with length {n} currently not supported for decoding")

    i = max(j for j in range(1,9) if n % (2**j) == 0)

    decoding = {v : k for k, v in encoding.items()}

    decodedInts = [decoding[c] for c in encodedString]

    numPerByte = 8 // i
    decodedBytes = []

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

    with open(filename, 'r') as file:
        contents = file.read()

    newFile = 'decoded-' + filename
    decodedContents = stringToDecodedString(contents, encoding)
    toFile(newFile, filetype, decodedContents)

    return decodedContents

def toFile(filename, filetype, contents):
    # Sends contents to filename with filetype
    # filetype: either 'wb' or 'w'

    with open(filename, filetype) as file:
        file.write(contents)

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

    possibleOptions = ['-d', '--decode', '--encoding', '-h', '--help', '-t', '--target']
    targetOptions = ['-t', '--target']
    decodeOptions = ['-d', '--decode']
    encodeOptions = ['--encoding']
    fileOptions   = ['-b', '--binary']
    helpOptions   = ['-h', '--help']


    for i, arg in enumerate(args[1:]):
        if arg[0] == '-' and arg in possibleOptions:
            if arg in helpOptions:
                raise Exception(helpMessage)

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
