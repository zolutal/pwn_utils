# pwn_utils

A repository of some scripts automate some actions I am constantly repeating for pwn challenges

## scripts

* dwninit: A script to automatically extract the libc and ld from a docker image into the current directory, you can then use pwninit to relink the binary to the extracted libraries

* pwinit-template: An custom pwninit template with boilerplate to wrap the pwntools process/remote modules into a single 'proc' class with shorthanded i/o function names, defaults to process rather than remote, mostly made to save myself from the suffering that is typing out 'sendlineafter' multiple times. I just stick the boilerplate into a vim fold to get it out of the way.

