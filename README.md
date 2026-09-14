# EmojiBytes

A short script that will convert back and forth from strings into emojis.
The original motivation came from the humor of sending emojis as your only means of communication, but I found that several people had beat me to the punch, for example the [base100 rust project](https://github.com/AdamNiederer/base100). 

## How to use

python3 emoji-bytes [options] file or message

    Options:
     -d, --decode: set program to decoding mode
     -t, --target: target file to output to
     -b, --binary: set filetype to binary for read/write
     --encoding:   name of encoding to use, assumes 256 by default
     -h, --help:   print help text

## Examples

| Input                             | Output        |
|----------------------------------|---------------|
| emoji-bytes Howdy Stranger!| 🎏🎶🎾🎫🏀🍧🎚🎻🎹🎨🎵🎮🎬🎹🍨|
| emoji-bytes -d 🎏🎶🎾🎫🏀🍧🎚🎻🎹🎨🎵🎮🎬🎹🍨 | Howdy Stranger!|

### LLM Disclosure

No LLMs were used in the process of making this script
