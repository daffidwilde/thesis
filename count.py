""" A simple script to calculate the wordcount of main. """

import subprocess


def get_summary():
    """ Save the output of texcount to file and then trim it. """

    summary = "The current word count is:\n"
    summary += "==========================\n\n"

    cmd = "texcount -inc -nosub main.tex"
    string = str(subprocess.check_output(cmd, shell=True))
    items = string.split("\\n\\n")
    block = items[-2]

    for line in block.split("\\n")[1:]:
        summary += line + "\n"

    return summary


def main():
    """ Get a string with the word count summary. """

    new_comment = get_summary()

    print(new_comment)

    return new_comment


if __name__ == "__main__":
    main()
