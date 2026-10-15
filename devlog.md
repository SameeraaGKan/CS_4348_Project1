# 10-15-2026 12:50pm

Starting Project 1. Got the git repository initialized and starting the planning and implementation of the project, mostly just trying to understand what the peoject is

# 10-15-2026 4:02pm
Reading the project document, this is what I am able to think of it- it is basically 3 programs communicating with each other- the logger will write log messages to a log file, the encryption program accepts commands given as lines via standard input and the driver program should accept a single command line argument – the name of the log file.
Upon start, the driver program will create two new processes, executing the logger (giving the log file name as a command line argument) and the encryption program. Pipes will be used to connect to their standard input and standard output.