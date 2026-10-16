#encrypt.py

import cmd
import sys

def vig(text, key, sign):
    out = []
    for i, c in enumerate(text):
        # Pick the key letter for this position. The modulo makes the
        # key repeat when the text is longer than the key
        # (e.g. key "HELLO" -> H E L L O H E L L O ...).
        # Subtracting 65 (ord('A')) converts the letter to a shift of 0-25.
        k = ord(key[i % len(key)]) - 65
        
        # Convert the text letter to 0-25, apply the shift, wrap around
        # the alphabet with % 26, then convert back to an ASCII uppercase
        # letter by adding 65.
        # Python's % always returns a non-negative result, so decrypting
        # (negative shift) wraps correctly without extra handling.
        out.append(chr((ord(c) - 65 + sign * k) % 26 + 65))
    return "".join(out)

# The passkey is remembered between commands. None means "not set yet".
key = None

for line in sys.stdin:
    
    # Split into the command (first word) and the argument (everything
    # after the first space). partition() leaves arg as "" if there is no space.
    cmd, _, arg = line.rstrip("\n").partition(" ")
    if cmd == "QUIT":
        break
    elif cmd == "PASS":
        
        # Store the new passkey and confirm. The spec says a successful
        # PASS responds with just "RESULT" and nothing after it.
        key = arg
        # flush=True is required: stdout to a pipe is buffered, so without
        # it the driver would block waiting for a reply that is still
        # sitting in this process's buffer.
        print("RESULT", flush = True)
    elif cmd in ("ENCRYPT", "DECRYPT"):
        if not key:
            # No passkey has been set yet (None or empty string).
            print("ERROR Password not set", flush=True)
        else:
            # sign is +1 for ENCRYPT and -1 for DECRYPT, so one function
            # handles both directions.
            print("RESULT " + vig(arg, key, 1 if cmd == "ENCRYPT" else -1), flush=True)
    else:
        # Anything else is not a valid command.
        print("ERROR Unknown command", flush=True)