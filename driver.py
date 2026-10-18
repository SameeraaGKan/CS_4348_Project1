# driver.py
# Driver program: launches the logger and encryption programs as child
# processes, connects to them with pipes, and runs the user menu.
import subprocess
import sys

# ---------- Setup ----------
if len(sys.argv) != 2:
    print("Usage: python driver.py <logfile>")
    sys.exit(1)

# sys.executable makes the children run under the same Python as the driver.
# The logger only needs stdin; the encryptor needs stdin and stdout.
logger = subprocess.Popen([sys.executable, "logger.py", sys.argv[1]],
                          stdin=subprocess.PIPE, text=True)
enc = subprocess.Popen([sys.executable, "encrypt.py"],
                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                       text=True)

# In-memory history for this run only: entered strings and results.
# Passwords are never stored here.
history = []


def log(action, msg=""):
    """Send one 'ACTION message' line to the logger."""
    logger.stdin.write(f"{action} {msg}\n")
    logger.stdin.flush()  # pipes are buffered, so flush or the child never sees it


def send(cmd):
    """Send one command line to the encryptor and return its one-line reply."""
    enc.stdin.write(cmd + "\n")
    enc.stdin.flush()
    return enc.stdout.readline().strip()


def valid(s):
    """True only if s is non-empty and contains letters only."""
    return s.isalpha()

# ---------- Shared "history or new string?" logic ----------
def pick_string(prompt_text):
    """
    Lets the user choose a string from history or type a new one.
    Returns (string, from_history), or (None, False) if the input was invalid.
    New strings are uppercased here, which gives case insensitivity.
    """
    while True:
        choice = input("Use history (h) or enter new string (n)? ").strip().lower()
        if choice == "n":
            s = input(prompt_text).strip()
            if not valid(s):
                print("Error: letters only, no spaces or symbols.")
                return None, False
            return s.upper(), False
        elif choice == "h":
            if not history:
                print("History is empty.")
                continue
            for i, item in enumerate(history, 1):
                print(f"  {i}. {item}")
            print("  0. Enter a new string instead")
            sel = input("Select number: ").strip()
            if sel == "0":
                continue  # back to the h/n question so the user can pick 'n'
            if sel.isdigit() and 1 <= int(sel) <= len(history):
                return history[int(sel) - 1], True
            print("Invalid selection.")
        else:
            print("Please enter h or n.")

# ---------- Command handlers ----------
def do_password():
    pw, _ = pick_string("Enter password: ")
    if pw is None:
        print("Password not set.")
        log("PASSWORD", "Invalid input rejected")
        return
    resp = send(f"PASS {pw}")
    # Never log or store the password itself, only the outcome.
    if resp.startswith("RESULT"):
        print("Passkey set.")
        log("PASSWORD", "Passkey set")
    else:
        print(resp)
        log("PASSWORD", f"Failed: {resp}")


def do_crypt(kind):
    """kind is 'ENCRYPT' or 'DECRYPT'."""
    s, from_history = pick_string(f"Enter string to {kind.lower()}: ")
    if s is None:
        log(kind, "Invalid input rejected")
        return
    if not from_history:
        history.append(s)  # only new entries, so history has no duplicates
    log(kind, s)

    resp = send(f"{kind} {s}")
    if resp.startswith("RESULT"):
        result = resp.split(" ", 1)[1] if " " in resp else ""
        print(f"Result: {result}")
        history.append(result)
        log("RESULT", result)
    else:
        print(resp)  # e.g. "ERROR Password not set"
        log("ERROR", resp)


def show_history():
    if not history:
        print("History is empty.")
    else:
        for i, item in enumerate(history, 1):
            print(f"  {i}. {item}")
    log("HISTORY", f"Displayed {len(history)} entries")

# ---------- Main loop ----------
log("START", "Driver started.")

while True:
    print("\nCommands: password | encrypt | decrypt | history | quit")
    try:
        cmd = input("> ").strip().lower()
    except EOFError:  # Ctrl-D: treat as quit
        cmd = "quit"
    log("COMMAND", cmd)

    if cmd == "password":
        do_password()
    elif cmd == "encrypt":
        do_crypt("ENCRYPT")
    elif cmd == "decrypt":
        do_crypt("DECRYPT")
    elif cmd == "history":
        show_history()
    elif cmd == "quit":
        break
    else:
        print("Unknown command.")
        log("ERROR", f"Unknown command: {cmd}")

# ---------- Shutdown ----------
enc.stdin.write("QUIT\n")      # QUIT has no reply, so don't readline here
enc.stdin.flush()
log("EXIT", "Driver exiting.")  # must come before telling the logger to quit
logger.stdin.write("QUIT\n")
logger.stdin.flush()
enc.wait()
logger.wait()
print("Goodbye.")
