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

