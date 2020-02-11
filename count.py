""" A simple script to calculate the wordcount of main. """

import json
import os
import subprocess
import sys

from github import Github


def read_json(filepath):
    """ Read a json file as a dictionary. """

    with open(filepath, 'r') as f:
        return json.load(f)


def get_summary():
    """ Save the output of texcount to file and then trim it. """

    summary = "The current word count is:\n"
    summary += "==========================\n\n"

    cmd = "texcount -inc -nosub main.tex"
    string = str(subprocess.check_output(cmd, shell=True))
    items = string.split("\\n\\n")
    block = items[-2]

    for line in block.split("\\n")[2:]:
        summary += line + "\n"

    return summary


def get_pull_request(event):
    """ Get the pull request associated with `event`. """

    branch_label = event['pull_request']['head']['label']
    branch_name = branch_label.split(':')[-1]
    repo = gh.get_repo(event['repository']['full_name'])
    prs = repo.get_pulls(state='open', sort='created', head=branch_label)

    return prs[0]


def check_for_duplicates(pr, comment):
    """ Check for duplicate comments. """

    old_comments = [c.body for c in pr.get_issue_comments()]
    if comment in old_comments:
        print("This PR already has this comment.")
        sys.exit(0)

    return comment


def main():
    """ Add a comment to the most recent PR with the word count summary. """

    gh = Github(os.getenv('GITHUB_TOKEN'))
    event = read_json(os.getenv('GITHUB_EVENT_PATH'))
    pr = get_pull_request(event)

    new_comment = get_summary()
    check_for_duplicates(pr, new_comment)

    pr.create_issue_comment(new_comment)


if __name__ == "__main__":
    main()
