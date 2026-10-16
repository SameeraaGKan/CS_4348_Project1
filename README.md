# CS_4348_Project1

## Overview

This project consists of three separate programs:

- **Logger** — Records all system activity in a log file.
- **Encryption Program** — Encrypts and decrypts strings using the Vigenère cipher.
- **Driver Program** — Interacts with the user, manages string history, and communicates with the other programs.

The entire system is started by running the driver program, which launches the logger and encryption programs and communicates with them through pipes.

### Implementation Requirements

The method used to create and communicate with processes depends on the programming language:

- **C/C++:** Use the Linux system calls `fork()`, `pipe()`, and `dup2()`.
- **Java:** Use the `Process` class.
- **Python:** Use the `subprocess` module.

Examples of these approaches will be provided in class.

---

## 1. Logger

The logger records messages to a specified log file. It receives log messages through standard input and continues running until it receives the `QUIT` command.

### Input Format

Each log message consists of:

- **Action:** The first sequence of non-whitespace characters.
- **Message:** The remainder of the line after the action.

### Log Format

Each message is recorded as a single line using the following format:

```text
YYYY-MM-DD HH:MM [ACTION] MESSAGE
```

The timestamp uses a 24-hour clock.

**Example input:**

```text
START Logging Started.
```

**Example log entry:**

```text
2026-09-14 11:32 [START] Logging Started.
```

### Command-Line Arguments

The logger accepts one command-line argument: the name of the log file.

```bash
./logger log.txt
```

The exact execution command may vary depending on the implementation language.

### Commands

| Command | Description |
|---|---|
| `QUIT` | Terminates the logger. |

---

## 2. Encryption Program

The encryption program encrypts and decrypts strings using the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher).

It accepts commands through standard input and prints responses to standard output. Each command and response occupies a single line.

### Command Format

Each input line consists of a command followed by an optional argument:

```text
COMMAND ARGUMENT
```

The first sequence of non-whitespace characters is treated as the command. The remainder of the line after the first space is treated as the argument.

### Supported Commands

| Command | Description |
|---|---|
| `PASS <key>` | Sets the current passkey used for encryption and decryption. |
| `ENCRYPT <text>` | Encrypts the provided text using the current passkey. |
| `DECRYPT <text>` | Decrypts the provided text using the current passkey. |
| `QUIT` | Terminates the encryption program. |

The encryption program remembers the current passkey until it is changed or the program exits.

If `ENCRYPT` or `DECRYPT` is called before a passkey has been set, the program must return an error.

### Response Format

Every response begins with a response type.

| Response | Description |
|---|---|
| `RESULT <message>` | The command succeeded. The remainder of the line contains the result. |
| `ERROR <message>` | The command failed. The remainder of the line contains the error message. |
| `RESULT` | Indicates success when the command has no result text to return, such as setting a passkey. |

### Example Interaction

**1. Encrypting without a passkey**

Input:

```text
ENCRYPT HELLO
```

Output:

```text
ERROR Password not set
```

**2. Setting a passkey**

Input:

```text
PASS HELLO
```

Output:

```text
RESULT
```

**3. Encrypting with the passkey set**

Input:

```text
ENCRYPT HELLO
```

Output:

```text
RESULT OIWWC
```

### Encryption Requirements

- Use the Vigenère cipher for encryption and decryption.
- The encryption program must remember the currently set passkey.
- Only alphabetic characters are valid in the input.
- Input is case-insensitive. The backend may assume that input is provided in a consistent case, such as uppercase.
- Return an error if encryption or decryption is requested before a passkey is set.

---

## 3. Driver Program

The driver program is the main entry point for the system. It interacts with the user, manages string history, and coordinates communication with the logger and encryption program.

### Startup and Process Management

The driver accepts one command-line argument: the name of the log file.

Upon startup, it must:

1. Create a new process for the logger, passing the log file name as a command-line argument.
2. Create a new process for the encryption program.
3. Establish pipes to communicate with the standard input and standard output of both processes.
4. Log the startup of the driver program.
5. Display a menu of available commands and prompt the user for input.

The driver continues accepting commands until the user selects `quit`.

Communication requirements:

- **Python and Java:** Use the streams provided for process communication.
- **C/C++:** Use `read()` and `write()` to communicate through pipes.

### Supported Commands

#### `password`

Sets the current passkey used by the encryption program.

The driver must:

1. Ask whether the user wants to enter a new password or select a string from history.
2. If the user enters a new password, prompt for the password.
3. If the user selects history, display the available history entries and allow selection by number.
4. Send the selected or entered password to the encryption program using the `PASS` command.

**Important:** Passwords must never be stored in history or written directly to the log.

#### `encrypt`

Encrypts a string using the current passkey.

The driver must:

1. Ask whether the user wants to enter a new string or select one from history.
2. If the user enters a new string, prompt for the input and save it to history.
3. If the user selects history, display the available entries and allow selection by number.
4. Send the string to the encryption program using the `ENCRYPT` command.
5. Display the result to standard output.
6. Save the result to history.

#### `decrypt`

Decrypts a string using the current passkey.

The driver must:

1. Ask whether the user wants to enter a new string or select one from history.
2. If the user enters a new string, prompt for the input and save it to history.
3. If the user selects history, display the available entries and allow selection by number.
4. Send the string to the encryption program using the `DECRYPT` command.
5. Display the result to standard output.
6. Save the result to history.

#### `history`

Displays the current string history.

History is maintained only for the duration of the current driver program execution.

#### `quit`

Shuts down the system.

The driver must:

1. Send `QUIT` to the encryption program.
2. Send `QUIT` to the logger.
3. Log the exit of the driver program.
4. Exit the program.

### History Management

The driver maintains a history of strings entered for encryption or decryption and the results produced by those operations.

- History persists only while the driver program is running.
- New input strings used for encryption or decryption must be saved to history.
- Encryption and decryption results must be saved to history.
- Passwords must never be saved to history.
- When using history to select a string, the user must have an option to exit the history menu and enter a new string instead.

### Logging Requirements

The driver must log:

- The startup of the driver program.
- Each command entered by the user.
- The result of each command.
- The exit of the driver program.

**Passwords must never be logged directly.**

### User Interaction

The driver program is more interactive than the encryption backend.

For example, the user enters the `encrypt` command first. The driver then prompts the user to enter a string or select one from history. It sends the appropriate single-line command to the encryption program and displays the response.

Commands sent to the encryption program must follow its expected input format.

---

## 4. Input Validation and Error Handling

The driver must validate user input and provide appropriate error messages.

### Validation Requirements

- The input to `password`, `encrypt`, and `decrypt` must contain only letters.
- Reject strings containing spaces, numbers, punctuation, or other non-alphabetic characters.
- Input must be case-insensitive. For example, encrypting `Hello` and `hello` must produce the same result.
- Handle attempts to encrypt or decrypt before a passkey has been set.
- Validate history selections and handle invalid menu choices.
- Allow users to exit the history menu and enter a new string instead.
- Handle invalid commands and other input errors gracefully.

### Example Validation

Input:

```text
Hello World!
```

Expected behavior:

```text
Error: Input must contain only letters.
```

The exact wording of driver error messages may depend on the implementation, but invalid input must not be processed as a valid encryption or decryption request.

---

## 5. Program Workflow

The overall system follows this workflow:

1. The user starts the driver program with a log file name.
2. The driver launches the logger and encryption program.
3. The driver logs its startup and displays the command menu.
4. The user selects a command.
5. The driver validates the input and communicates with the encryption program when necessary.
6. The driver displays results, updates history, and logs activity.
7. The user repeats these steps until selecting `quit`.
8. The driver shuts down the other programs and exits.

---

## 6. References

- [Vigenère Cipher — Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
