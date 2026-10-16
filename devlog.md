# 10-15-2026 12:50pm

Starting Project 1. Got the git repository initialized and starting the planning and implementation of the project, mostly just trying to understand what the peoject is

# 10-15-2026 4:02pm
Reading the project document, this is what I am able to think of it- it is basically 3 programs communicating with each other- the logger will write log messages to a log file, the encryption program accepts commands given as lines via standard input and the driver program should accept a single command line argument – the name of the log file.
Upon start, the driver program will create two new processes, executing the logger (giving the log file name as a command line argument) and the encryption program. Pipes will be used to connect to their standard input and standard output.

# 10-15-2026 4:02pm
Phase 1 - This session I'm planning on building the encryption program, well a part of it, hopefully.  

# 10-16-2026 10:52pm
Yesterday, I just read the project pdf got a better understanding of what it is, now I'll developing it. It's the backend, so
it only has to read one command per line from stdin and print one response
line. Plan:
- Loop over stdin; split each line into command and argument at the first space.
- Keep the passkey in a variable that persists between commands (None until PASS is called).
- Write one function that does Vigenère in both directions, using a sign
  of +1 for encrypt and -1 for decrypt, rather than two near-identical functions.
- Respond with RESULT or ERROR as the spec describes.
Unsure about: what to do with unknown commands (spec doesn't say), and
whether the encryptor should validate input or leave that to the driver.

Decisions:
- The spec says I can assume uppercase letters only, so I'm not validating
  here. The driver will validate and uppercase before sending anything.
- Unknown commands return "ERROR Unknown command" so the driver never
  waits on a reply that doesn't come.
- QUIT prints nothing, so the driver must not try to read a response after it.
