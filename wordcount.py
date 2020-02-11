""" A simple script to calculate the wordcount of main. """

import os
import subprocess

def main():
    """ Save the output of texcount to file and then trim it. """

    with open("wordcount.md", "w") as f:
        f.write("The current word count is:\n")
        f.write("==========================\n\n")

        cmd = "texcount -inc -nosub main.tex"
        string = str(subprocess.check_output(cmd, shell=True))
        items = string.split("\\n\\n")
        block = items[-2]

        for line in block.split("\\n")[2:]:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
