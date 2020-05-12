#!/bin/sh

set -ev
Rscript -e "bookdown::render_book('index.Rmd', 'bookdown::pdf_book')"
texcount "/Common/University/Year 3/Final Year Project/git-repository/Rmarkdown Report/_book/Translating-Natural-Language-Queries-into-SQL.tex"

