""" A simple script to calculate the wordcount of main. """

import subprocess


def get_summary():
    """ Save an the output of texcount to file and then trim it. """

    summary = "The current word count is:\n"
    summary += "==========================\n"

    cmd = "texcount -inc -nosub main.tex"
    string = str(subprocess.check_output(cmd, shell=True))
    items = string.split("\\n\\n")
    block = items[-2]

    for line in block.split("\\n")[2:-1]:
        summary += line + "\n"

    return summary


def main():
    """ Get a string with the word count summary using texcount. """

    summary = "The current word count is:\n"
    summary += "==========================\n"

    cmd = "texcount -inc -nosub main.tex"
    string = str(subprocess.check_output(cmd, shell=True))
    items = string.split("\\n\\n")
    block = items[-2]

    for line in block.split("\\n")[2:-1]:
        summary += line + "\n"

    return summary


if __name__ == "__main__":
    main()
