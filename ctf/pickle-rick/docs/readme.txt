PROJECT: Pickle Rick CTF Exploitation Automation

Author: Student Project
Purpose: Learning / Cybersecurity Practice

--------------------------------------------------
PROJECT DESCRIPTION
--------------------------------------------------

This project consists of automating the exploitation process of the
"Pickle Rick" CTF machine after it has already been solved manually.

The goal is not to discover vulnerabilities but to recreate the
attack chain programmatically using Python.

The script reproduces the same steps that were previously performed
during manual exploitation of the machine.

This exercise focuses on improving skills in:

- HTTP traffic analysis
- Exploit automation
- Python scripting for offensive security
- Session management
- Reverse shells
- Threading and parallel execution
- Linux privilege escalation
- Persistence techniques

--------------------------------------------------
ATTACK FLOW
--------------------------------------------------

The automated script performs the following steps:

1. Send an HTTP POST request to authenticate in the web application
2. Maintain the session using cookies
3. Interact with the vulnerable command portal
4. Execute commands remotely
5. Trigger a reverse shell to the attacker machine
6. Start a listener to receive the shell
7. Escalate privileges to root
8. Create a persistent user with sudo privileges
9. Install SSH public key access
10. Connect to the system using SSH

--------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------

project/

│
├── exploit.py
│   Main script that automates the exploitation process
│
├── enunciado.md
│   Exercise description and step-by-step learning guide
│
└── README.txt
    Project documentation

--------------------------------------------------
TECHNOLOGIES USED
--------------------------------------------------

Python 3

Main Python concepts used:

- requests library
- HTTP sessions
- sockets
- threading
- subprocess execution

Operating system concepts:

- Linux command execution
- reverse shells
- sudo privilege escalation
- SSH key authentication

--------------------------------------------------
LEARNING OBJECTIVES
--------------------------------------------------

This project helps reinforce practical skills in:

• Web request analysis
• Exploit development
• Automation of attack chains
• Post-exploitation techniques
• Persistence methods
• Red team scripting

--------------------------------------------------
REQUIREMENTS
--------------------------------------------------

Recommended environment:

Attacker machine:
- Linux
- Python 3
- netcat

Python libraries:

requests

Install with:

pip install requests

--------------------------------------------------
DISCLAIMER
--------------------------------------------------

This project is intended strictly for educational purposes.

All techniques demonstrated here must only be used in controlled
laboratory environments such as CTF platforms or machines that
you have explicit permission to test.

Unauthorized use of these techniques against real systems is illegal.
