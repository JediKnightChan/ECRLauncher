from datetime import datetime


def log(string, filename="log.txt", do_print=False):
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    with open(filename, "a") as f:
        f.write(now + ": " + str(string) + "\n")

    if do_print:
        print(string)
