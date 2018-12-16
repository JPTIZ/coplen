OBJS   := plan.pdf
LATEX  := xelatex
BIBREF := refs

all: $(OBJS)

%.pdf: %.tex $(BIBREF).bib
	$(LATEX) $(basename $@)
	bibtex  $(basename $@)
	$(LATEX) $(basename $@)
	$(LATEX) $(basename $@)

.PHONY: clean

clean: clean-temp clean-pdf

clean-temp:
	rm -f *.{tex,out,aux,bbl,blg,log}

clean-pdf:
	rm -f *.pdf
