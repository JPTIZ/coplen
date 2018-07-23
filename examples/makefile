OBJS   := plan.pdf
LATEX  := xelatex
BIBREF := references

all: $(OBJS)

%.pdf: %.tex $(BIBREF).bib
	$(LATEX) $(basename $@)
	bibtex  $(basename $@)
	$(LATEX) $(basename $@)
	$(LATEX) $(basename $@)

.PHONY: clean

clean:
	rm -f *.{aux,bbl,blg,pdf,log}
