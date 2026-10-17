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
line. 

Plan:
- Loop over stdin; split each line into command and argument at the first space.
- Keep the passkey in a variable that persists between commands (None until PASS is called).
- Write one function that does Vigenère in both directions, using a sign of +1 for encrypt and -1 for decrypt, rather than two near-identical functions.
- Respond with RESULT or ERROR as the spec describes.
Unsure about: what to do with unknown commands (spec doesn't say), and
whether the encryptor should validate input or leave that to the driver.

Decisions:
- The spec says I can assume uppercase letters only, so I'm not validating here. The driver will validate and uppercase before sending anything.
- Unknown commands return "ERROR Unknown command" so the driver never waits on a reply that doesn't come.
- QUIT prints nothing, so the driver must not try to read a response after it.

Session end (after): 
Encryption program works on its own. Tested with the
spec example: ENCRYPT before PASS gives "ERROR Password not set", then
PASS HELLO gives "RESULT", then ENCRYPT HELLO gives "RESULT OIWWC".
Checked the first letter by hand: H(7) + H(7) = 14 = O.
Problems / learned:
- Used print(..., flush=True). Stdout to a pipe is buffered, so without flush the driver would hang waiting for the reply.
- Decrypt needed no special wraparound handling because Python's % gives a non-negative result for negative numbers.
Tested: encrypt then decrypt returns the original text; key shorter than
text repeats correctly.
Next: the logger.

# 10-16-2026 2:17pm
Starting with the logger since it's the simplest and has no dependencies. Plan is to read stdin line by line, split off the first word as ACTION, and write the timestamped line. Not sure yet whether I need to flush after every write. 

I just finishedd writing it but idk if it really runs cuz I need to write the driver program - it does "run" cuz i added a test statement - pushing it to github
Designing and writing the driver program now 


# 10-16-2026 4:30pm
Now I'll start implementing the driver program, which I'm thinking to be the largest part of the program its supposed to launch the logger and the encryption program as child processes, connects to them with pipes, and runs the user menu.

Plan:
- Get started with the setup - get the logger and the encrypt functions as sub processes 
- Start both children with subprocess.Popen. The logger gets stdin=PIPE; 
 the encryptor gets stdin=PIPE and stdout=PIPE. Use text=True so I can read and write strings instead of bytes.
- Write two small helpers: log(action, msg) writes a line to the logger, and send(cmd) writes to the encryptor and reads back one response line.
- Main loop: print the menu, read a command, and dispatch to a handler.
- Keep history as a plain list in memory, since the spec says it only lasts for this run.

  # 10-16-2026 11:43pm
continuing the driver function
  Decisions:
- One shared function, pick_string(), handles the history-or-new choice for all three commands instead of copying the logic three times. It returns the string and whether it came from history, or None if the input was invalid.
- Choosing 0 in the history menu goes back to the h/n question, so the user can escape the history and enter a new string.
- Validation uses str.isalpha(), which also rejects empty strings, spaces, digits, and symbols, so "Hello World!" gives an error instead of a crash.
- Everything is uppercased in the driver before it is sent, which gives case insensitivity ("hello" and "Hello" produce the same ciphertext).

# 10-17-2026 11:53am

Today, I've decided to finish off the driver program. So, I'm gonna work on the command handlers now, then the main loop in the afternoon and finally test out the program and sumbit it by tonight.

Decisions:
- History stores entered strings (for encrypt/decrypt) and results. It never stores passwords. The log doesn't either; the password command logs only "Passkey set" or a failure message.
- Strings picked from history are not added again, so history has no duplicates.
- Used sys.executable instead of "python3" to launch the children so they run under the same interpreter as the driver. 
- Catch EOFError on the menu prompt and treat it as quit, so Ctrl-D shuts down cleanly instead of crashing and leaving child processes running.
- At quit: send QUIT to the encryptor, log EXIT, then send QUIT to the logger, then wait() on both. EXIT has to be logged before the logger is told to quit, or it never gets written.


