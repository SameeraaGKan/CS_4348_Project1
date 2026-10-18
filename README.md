# CS 4348 Project 1: Logger, Encryption Program and Driver

A Python system of three separate programs. The driver launches the logger
and the encryption program as child processes and talks to them through
pipes using the `subprocess` module.

## Files

| File | Purpose |
|---|---|
| `driver.py` | Menu and user interaction; launches the other two programs |
| `logger.py` | Writes timestamped log lines to a file |
| `encrypt.py` | Vigenère encryption/decryption backend |
| `devlog.md` | Development log |

## Requirements

- Python 3
- Run all commands from the project folder, since the driver finds
  `logger.py` and `encrypt.py` by relative path.

## How to run

```
python driver.py mylog.txt
```

(Use `python3` on Linux/macOS.) `mylog.txt` is the log file name and can be
anything. Only the driver is run directly; it starts the other two.

## Driver commands

| Command | What it does |
|---|---|
| `password` | Set the passkey, from a new entry or a history selection |
| `encrypt` | Encrypt a new or history string and show the result |
| `decrypt` | Decrypt a new or history string and show the result |
| `history` | Show the history for this run |
| `quit` | Shut everything down and exit |

For `password`, `encrypt` and `decrypt` you first choose `h` (history) or `n`
(new string). In the history menu, `0` goes back so you can enter a new
string instead.

## Example session

```
> encrypt
Use history (h) or enter new string (n)? n
Enter string to encrypt: hello
Error: ... Password not set
> password
Use history (h) or enter new string (n)? n
Enter password: pass
Passkey set.
> encrypt
Use history (h) or enter new string (n)? n
Enter string to encrypt: hello
Result: WEDDD
```

(Edit this to match the exact output you see.)

## How it works

- **Pipes:** the logger gets `stdin=PIPE`. The encryptor gets `stdin=PIPE`
  and `stdout=PIPE`. Both use `text=True`.
- **Flushing:** every write to a child is followed by `flush()`. Pipes are
  buffered, so otherwise the child never sees the line and the driver hangs.
- **Protocol:** each command to the encryptor is one line and gets one reply
  line starting with `RESULT` or `ERROR`. `QUIT` gets no reply, so the driver
  does not read after sending it.
- **Shutdown order:** QUIT to the encryptor, log `EXIT`, then QUIT to the
  logger, then `wait()` on both. `EXIT` must be logged before the logger is
  told to quit, or it is never written.

## Log format

```
YYYY-MM-DD HH:MM [ACTION] MESSAGE
```

24-hour time. The driver logs its start and exit, each command, and each
result. Passwords are never logged or stored in history; the log only records
"Passkey set".

## Input handling

- `password`, `encrypt` and `decrypt` accept letters only, checked with
  `str.isalpha()`. Spaces, digits, symbols and empty input are rejected with
  an error message and are not sent to the encryptor.
- Input is uppercased by the driver, so `hello` and `Hello` are treated
  identically. The encryptor assumes uppercase, as the spec allows.
- Invalid history selections and unknown commands print a message and return
  to the prompt.
- Ctrl-D at the menu is treated as `quit`.

## Known limitations

- A new string is added to history before it is sent, so a failed request
  (for example encrypting before a passkey is set) still leaves that string in
  history.
- The encryptor does not validate its own input; it relies on the driver.

## Tested

Tested on Windows (PowerShell). Checked: encrypt before setting a passkey,
`Hello World!` rejected, empty history, passkey not stored in history,
encrypt then decrypt round trip, and the log file contents.