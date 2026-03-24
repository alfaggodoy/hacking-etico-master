import os

def main():
    while True:
        try:
            cmd = input(">>> ")
            blacklist = ["python", "python3", "bash", "sh", "php", "perl", "ruby",
            "ps", "kill", "cd", "ls", "pwd", "rm", "rmdir", "nc", "ncat", "xterm",
            "konsole", "mkdir", "touch", "sudo", "id", "su", "exec"]
            if cmd.count(" ") > 0:
                for word in cmd.split(" "):
                    if word in blacklist:
                        print("Nope!")
                        break
                    else:
                        os.system(cmd)
                    break
            else:
                if cmd in blacklist:
                    print("Nope!")
                else:
                    os.system(cmd)
        except KeyboardInterrupt:
            print("")
        except:
            continue
main()
