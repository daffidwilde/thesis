""" A script containing `invoke` tasks for the compilation of this thesis. """

import glob
import pathlib
import re
import subprocess
import sys
from collections import Counter
from difflib import SequenceMatcher

import bibtexparser
import numpy as np
import pandas as pd
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from invoke import task

import known


@task
def compile(c, engine="pdflatex"):
    """ Compile the LaTeX document. """

    c.run(f"latexmk -interaction=nonstopmode -shell-escape --{engine} main.tex")


def _get_book():
    """Get a glob containing all of the main files in the thesis."""

    frontmatter = pathlib.Path("preamble/").glob("*.tex")
    chapters = pathlib.Path("chapters/").glob("*/main.tex")
    appendices = pathlib.Path("appendix/").glob("*/main.tex")

    return [*frontmatter, *chapters, *appendices]


@task
def doctest(c):
    """ Doctest the source files for the document. """

    for path in _get_book():
        filename = path.stem
        print("Testing", filename)
        c.run(f"python -m doctest -v {path}")


@task
def spellcheck(c):
    """ Check spelling, skipping over known words. """

    exit_codes = [0]
    for path in _get_book():

        print(f"Checking {path} 📖")
        latex = path.read_text()
        aspell_output = subprocess.check_output(
            ["aspell", "-t", "--list", "--lang=en_GB"], input=latex, text=True
        )

        errors = set(aspell_output.split("\n")) - {""}
        unknowns = set()
        for error in errors:
            if not any(
                re.fullmatch(word.lower(), error.lower())
                for word in known.words
            ):
                unknowns.add(error)

        if unknowns:
            print(f"⚠️   In {path} the following words are not known:")
            for string in sorted(unknowns):
                print("     -", string)

            exit_codes.append(1)
        else:
            exit_codes.append(0)

    sys.exit(max(exit_codes))


def collate_bibfiles(bibfiles, destination):

    print("Collating bibfiles...")
    with open(destination, "a") as outfile:
        for bibfile in bibfiles:
            print("Adding", bibfile)
            with open(bibfile, "r") as infile:
                for line in infile:
                    outfile.write(line)


def get_bibentries(bibfile):

    print("Getting bibentries...")
    with open(bibfile) as bibtexfile:
        parser = BibTexParser(common_strings=True)
        bibdatabase = bibtexparser.load(bibtex_file=bibtexfile, parser=parser)

    bibentries = pd.DataFrame(bibdatabase.entries)
    return bibentries


def get_citations_to_export(bibentries):

    print("Cleaning entries...")
    bibentries = bibentries.drop_duplicates(subset=["title"], keep="last")
    duplicate_keys = [
        key for key, count in Counter(bibentries["ID"]).items() if count > 1
    ]

    citations_to_export = bibentries[~bibentries["ID"].isin(duplicate_keys)]
    entries_to_check = bibentries[
        bibentries["ID"].isin(duplicate_keys)
    ].groupby("ID")
    for key, entries in entries_to_check:
        print("Checking", key)
        titles = entries["title"].unique()
        if SequenceMatcher(None, *titles).ratio() > 0.7:
            citations_to_export = citations_to_export.append(
                entries.iloc[-1, :]
            )

        else:
            print(f"Must reconcile {len(entries)} keys for {key}.")
            citations_to_export = citations_to_export.append(entries)

    return citations_to_export


def export_citations(citations, destination):

    db = BibDatabase()
    citation_dicts = (dict(row) for _, row in citations.iterrows())
    citation_dicts = [
        {
            attribute: value
            for attribute, value in citation.items()
            if value is not np.nan
        }
        for citation in citation_dicts
    ]

    db.entries = citation_dicts

    with open(destination, "w") as bibtexfile:
        writer = BibTexWriter()
        writer.indent = "    "
        bibtexparser.dump(db, bibtexfile, writer)


@task
def bibliography(c, path="bibliography.bib", backup=True):
    """Merges the bibliography files for each chapter into one and cleans the
    entries."""

    current = []
    path = pathlib.Path(path)
    if backup and path.exists():
        name, ext = path.stem, path.suffix
        backup = f".{name}{ext}"
        print("Backing up current bibliography.")
        c.run(f"mv {path} {backup}")
        current = [backup]

    filenames = glob.glob("./*/*/paper/*.bib") + current
    collate_bibfiles(filenames, "bibliography.bib")
    bibentries = get_bibentries("bibliography.bib")
    citations_to_export = get_citations_to_export(bibentries)
    export_citations(citations_to_export, "bibliography.bib")
