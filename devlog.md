# 10-15-2026 12:50pm
Starting Project 1. Got the git repository initialised and started planning.
Mostly just trying to understand what the project is asking for.

# 10-15-2026 4:02pm
Reading the project document, this is how I understand it: three programs communicating with each other. The logger writes log messages to a log file, the encryption program accepts commands as lines via standard input, and the driver takes a single command line argument (the name of the log file). On start, the driver creates two new processes, the logger (given the log file name) and the encryption program, and uses pipes to connect to their standard input and output.
Not sure yet how the pipes will actually work in Python.

# 10-15-2026 4:02pm
Phase 1: this session I'm planning on building the encryption program, or at least a part of it, hopefully.

# 10-16-2026 10:52am 

Yesterday I only read the project PDF to get a better understanding of it.
Now I'm developing it. The encryptor is the backend, so it only has to read one command per line from stdin and print one response line.

Plan:
- Loop over stdin; split each line into command and argument at the first space.
- Keep the passkey in a variable that persists between commands (None until PASS is called).
- Write one function that does Vigenère in both directions, using a sign of +1 for encrypt and -1 for decrypt, rather than two near-identical functions.
- Respond with RESULT or ERROR as the spec describes.
Unsure about: what to do with unknown commands (spec doesn't say), and whether the encryptor should validate input or leave that to the driver.

Decisions:
- The spec says I can assume uppercase letters only, so I'm not validating here. The driver will validate and uppercase before sending anything.
- Unknown commands return "ERROR Unknown command" so the driver never waits on a reply that doesn't come.
- QUIT prints nothing, so the driver must not try to read a response after it.

Session end (after):
The encryption program works on its own. Tested with the spec example: ENCRYPT before PASS gives "ERROR Password not set", then PASS HELLO gives "RESULT", then ENCRYPT HELLO gives "RESULT OIWWC". Checked the first letter by hand: H(7) + H(7) = 14 = O.
Problems / learned:
- Used print(..., flush=True). Stdout to a pipe is buffered, so without flush the driver would hang waiting for the reply.
- Decrypt needed no special wraparound handling because Python's % gives a non-negative result for negative numbers.
Tested: encrypt then decrypt returns the original text; a key shorter than the text repeats correctly.
Next: the logger.

# 10-16-2026 2:17pm
Starting with the logger since it's the simplest and has no dependencies. Plan is to read stdin line by line, split off the first word as the ACTION, and write the timestamped line. Not sure yet whether I need to flush after every write.

Just finished writing it. Problem: I can't properly test it until the driver exists, since it only reads from stdin when launched as a child process. It does "run" because I added a temporary test statement, but that doesn't prove the pipe side works. Pushed to GitHub.
Next: designing and writing the driver program.

# 10-16-2026 4:30pm
Starting on the driver, which I think will be the largest part of the project. It's supposed to launch the logger and the encryption program as child processes, connect to them with pipes, and run the user menu.

Plan:
- Start both children with subprocess.Popen. The logger gets stdin=PIPE; the encryptor gets stdin=PIPE and stdout=PIPE. Use text=True so I can read and write strings instead of bytes.
- Write two small helpers: log(action, msg) writes a line to the logger, and send(cmd) writes to the encryptor and reads back one response line.
- Main loop: print the menu, read a command, and dispatch to a handler.
- Keep history as a plain list in memory, since the spec says it only lasts for this run.

# 10-16-2026 11:43pm
Continuing the driver.
Decisions:
- One shared function, pick_string(), handles the history-or-new choice for all three commands instead of copying the logic three times. It returns the string and whether it came from history, or None if the input was invalid.
- Choosing 0 in the history menu goes back to the h/n question, so the user can escape the history and enter a new string.
- Validation uses str.isalpha(), which also rejects empty strings, spaces, digits and symbols, so "Hello World!" gives an error instead of a crash.
- Everything is uppercased in the driver before it is sent, which gives case insensitivity ("hello" and "Hello" should produce the same ciphertext).

# 10-17-2026 11:53am
Today I've decided to finish the driver. I'm going to work on the command handlers now, then the main loop in the afternoon, and finally test the program and submit it.

Decisions:
- History stores entered strings (for encrypt/decrypt) and results. It never stores passwords. The log doesn't either; the password command logs only "Passkey set" or a failure message.
- Strings picked from history are not added again, so history has no duplicates.
- Used sys.executable instead of "python3" to launch the children so they run under the same interpreter as the driver.
- Catch EOFError on the menu prompt and treat it as quit, so Ctrl-D shuts down cleanly instead of crashing and leaving child processes running.
- At quit: send QUIT to the encryptor, log EXIT, then send QUIT to the logger, then wait() on both. EXIT has to be logged before the logger is told to quit, or it never gets written.

# 10-17-2026 4:26pm
Command handlers and main loop are written. Next: run it end to end and check the log file.

# 10-17-2026 4:57pm  (first test run)
Reflection: Ran the driver end to end and checked the log file (mylog.txt).
- Encrypt before setting a password gave "ERROR Password not set", and it was logged.
- Set a password, then encrypted HELLO and got WEDDK. Decrypted WEDDK and got HELLO back, so the round trip works.
- Decrypted HELLO as well, which gave SETTS.
- The log has START, each command, each result and EXIT, in order, with no password in it.
Problems:
- The log line for the error read "[ERROR] ERROR Password not set" because I logged the whole reply from the encryptor. 
- History showed 3 entries: HELLO twice and WEDDK. The first HELLO came from the failed encrypt, because the driver saves new strings to history before sending them, so a failed request still ends up in history. That matches the spec, so I kept it.

# 10-18-2026 1:34am (second test run, Windows PowerShell)
Reflection: Tested more cases.
- "Hello World!" for encrypt was rejected with "letters only" and no crash.
- Chose history for the password while it was empty: it printed "History is empty." and let me enter a new string instead.
- Set the password "pass". The history command then showed it was still empty, so passwords are not stored.
- Encrypted "hello": history stored it as HELLO (uppercased) and the result was WEDDD. Checked by hand with key PASS: H+P=W, E+A=E, L+S=D, L+S=D, and the key repeats for the last O+P=D.
- Decrypted WEDDD from the history menu and got HELLO back.
- Quit exited cleanly.

# 10-18-2026 1:45am (final checks)
Reflection: 
- "hello" vs "Hello" give the same result: yes.
- Invalid history selection: "History is empty.".
- Unknown command at the menu: "Unknown command."
- Ctrl-D / Ctrl-Z then Enter: Ctrl-D ended the program and printed Goodbye.
What I'd improve: label history entries as "input" or "result" so they're
easier to tell apart, and validate input in the encryptor too as a safety
check.