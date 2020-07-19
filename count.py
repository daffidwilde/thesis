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

    summary = "[wordcount] The current word count is:\n"
    summary += "==========================\n\n"

    cmd = "texcount -inc -nosub main.tex"
    string = str(subprocess.check_output(cmd, shell=True))
    items = string.split("\\n\\n")
    block = items[-2]

    for line in block.split("\\n")[1:]:
        summary += line + "\n"

    return summary


def get_pull_request(gh, event):
    """ Get the pull request from `gh` client associated with `event`. """

    branch_label = event['pull_request']['head']['label']
    branch_name = branch_label.split(':')[-1]
    repo = gh.get_repo(event['repository']['full_name'])
    prs = repo.get_pulls(state='open', sort='created', head=branch_label)

    return prs[0]


def existing_comment(pr):
    """ Check for an existing word count comment. """

    comments = [
        comm.body.startswith("[wordcount]") for comm in pr.get_issue_comments()
    ]
    for comm in comments:
        if comm.body.startswith("[wordcount]"):
            return comm

    return False


def main():
    """ Add a comment to the most recent PR with the word count summary. """

    gh = Github(os.getenv('GITHUB_TOKEN'))
    event = read_json(os.getenv('GITHUB_EVENT_PATH'))
    print("GITHUB_EVENT_PATH\n", event)

    pr = get_pull_request(gh, event)

    comment = get_summary()
    existing = existing_comment(pr)
    if not existing:
        pr.create_issue_comment(comment)

    else:
        existing.edit(comment)


if __name__ == "__main__":
    main()
