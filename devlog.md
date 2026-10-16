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

Session end (after): Encryption program works on its own. Tested with the
spec example: ENCRYPT before PASS gives "ERROR Password not set", then
PASS HELLO gives "RESULT", then ENCRYPT HELLO gives "RESULT OIWWC".
Checked the first letter by hand: H(7) + H(7) = 14 = O.
Problems / learned:
- Used print(..., flush=True). Stdout to a pipe is buffered, so without
  flush the driver would hang waiting for the reply.
- Decrypt needed no special wraparound handling because Python's % gives
  a non-negative result for negative numbers.
Tested: encrypt then decrypt returns the original text; key shorter than
text repeats correctly.
Next: the logger.

10-16-2026 2:17pm
Starting with the logger since it's the simplest and has no
dependencies. Plan is to read stdin line by line, split off the first word as ACTION, and write the timestamped line. Not sure yet whether I need to flush after every write. 
I just finishedd writing it but idk if it really runs cuz I need to write the driver program - it does "run" cuz i added a test statement - pushing it to github
Designing and writing the driver program now 


