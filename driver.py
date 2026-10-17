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
