
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
    encodedString = bytesToEncodedString(bytes(plaintext), encoding)

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

def main(test, encoding):
    binaryTest = test.encode()
    print("Encoding used: ", encoding)
    print(test)
    encodedString = bytesToEncodedString(binaryTest, encoding)
    print(encodedString)
    decodedBytes = stringToDecodedBytes(encodedString, encoding)
    print(decodedBytes)
    decodedString = decodedBytes.decode()
    print(decodedString)
    toFile(test, 'w', encodedString)
    print(fileToDecodedString(test, 'w', encoding))

if __name__ == "__main__":
    test = "Hello"
    encoding = emoji256ary
    main(test, encoding)
