""" A script to create the repository summary table. """

import pandas as pd


def main():
    """Zip together chapter references, GitHub links and DOI names."""

    chapters = [
        r"Chapter~\ref{chp:" + chapter + "}"
        for chapter in ("lit", "edo", "kmodes", "copd")
    ]

    githubs = [
        r"\github{daffidwilde/" + repo + "}"
        for repo in (
            "literature-review",
            "edo-paper",
            "kmodes-paper",
            "copd-paper",
        )
    ]

    sources = [
        r"\doi{" + doi + "}" if doi else "---"
        for doi in (
            "10.5281/zenodo.4320050",
            "10.5281/zenodo.4000316",
            "10.5281/zenodo.3639282",
            "10.5281/zenodo.3936479",
        )
    ]

    datas = [
        r"\doi{" + doi + "}" if doi else "---"
        for doi in (
            "10.5281/zenodo.4320050",
            "10.5281/zenodo.4000327",
            "10.5281/zenodo.3638035",
        )
    ] + [
        r"\begin{tabular}{l}"
        r"\doi{10.5281/zenodo.3908167}\\"
        r"\doi{10.5281/zenodo.3924715}"
        r"\end{tabular}"
    ]

    repos = pd.DataFrame.from_records(
        zip(chapters, githubs, sources, datas),
        columns=(
            "Chapter",
            "GitHub repository",
            "Source code archive",
            "Data archive(s)",
        ),
    )

    repos.to_csv("main.csv", index=False)
    with pd.option_context("max_colwidth", 1000):
        repos.to_latex(
            "main.tex", index=False, escape=False, column_format="cccc"
        )


if __name__ == "__main__":
    main()
