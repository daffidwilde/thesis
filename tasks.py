""" A script containing `invoke` tasks for the compilation of this thesis. """

import glob
import pathlib
import subprocess
import sys
from collections import Counter
from difflib import SequenceMatcher

import bibtexparser

import known
import pandas as pd
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from invoke import task


@task
def compile(c):
    """ Compile the LaTeX document. """

    c.run("latexmk -interaction=nonstopmode -shell-escape main.tex")


@task
def spellcheck(c):
    """ Check spelling. """

    book = pathlib.Path("./chapters/").glob("0*/main.tex")
    exit_codes = [0]
    for path in book:

        latex = path.read_text()
        aspell_output = subprocess.check_output(
            ["aspell", "-t", "--list", "--lang=en_GB"], input=latex, text=True
        )

        errors = set(aspell_output.split("\n")) - {""} - known.words
        if len(errors):
            print(f"In {path} the following words are not known: ")
            for string in sorted(errors):
                print(string)
            exit_codes.append(1)

    sys.exit(max(exit_codes))


def collate_bibfiles(bibfiles, destination):

    with open(destination, "w") as outfile:
        for bibfile in bibfiles:
            with open(bibfile, "r") as infile:
                for line in infile:
                    outfile.write(line)

    return destination


def get_bibentries(bibfile):

    with open(bibfile) as bibtexfile:
        parser = BibTexParser(common_strings=True)
        bibdatabase = bibtexparser.load(bibtex_file=bibtexfile, parser=parser)

    bibentries = pd.DataFrame(bibdatabase.entries)
    return bibentries


def get_citations_to_export(bibentries):

    bibentries = bibentries.drop_duplicates(subset=["title"])
    duplicate_keys = [
        key for key, count in Counter(bibentries["ID"]).items() if count > 1
    ]

    citations_to_export = bibentries[~bibentries["ID"].isin(duplicate_keys)]
    entries_to_check = bibentries[
        bibentries["ID"].isin(duplicate_keys)
    ].groupby("ID")
    for key, entries in entries_to_check:
        titles = entries["title"].unique()
        if SequenceMatcher(None, *titles).ratio() > 0.7:
            citations_to_export = citations_to_export.append(entries.iloc[0, :])

        else:
            for i, entry in enumerate(entries):
                entry["ID"] = entry["ID"] + f"_{i}"
                citations_to_export = citations_to_export.append(entry)

    return citations_to_export


def export_citations(citations, destination):

    db = BibDatabase()
    citation_dicts = (dict(row) for _, row in citations.iterrows())
    citation_dicts = [
        {
            attribute: value
            for attribute, value in citation.items()
            if not value is pd.np.nan
        }
        for citation in citation_dicts
    ]

    db.entries = citation_dicts

    with open(destination, "w") as bibtexfile:
        writer = BibTexWriter()
        writer.indent = "    "
        bibtexparser.dump(db, bibtexfile, writer)


@task
def bibliography(c):
    """ Merges the bibliography files for each chapter into one and cleans the
    entries. """

    filenames = glob.glob("chapters/*/bibliography.bib")
    collate_bibfiles(filenames, "bibliography.bib")
    bibentries = get_bibentries("bibliography.bib")
    citations_to_export = get_citations_to_export(bibentries)
    export_citations(citations_to_export, "bibliography.bib")
