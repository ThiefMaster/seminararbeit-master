NAME=Seminararbeit_Flask
SLIDES=Seminararbeit_Flask_Slides
ARGS=-shell-escape -interaction=nonstopmode
VIEWER="F:/Foxit Reader/Foxit Reader.exe"

pdf:
	@echo Building PDF
	@pdflatex $(ARGS) -draftmode $(NAME)
	@bibtex $(NAME)
	@pdflatex $(ARGS) -draftmode $(NAME)
	@pdflatex $(ARGS) $(NAME)
	@start $(VIEWER) $(NAME).pdf

slides:
	@echo Building slides PDF
	@pdflatex $(ARGS) -draftmode $(SLIDES)
	@pdflatex $(ARGS) $(SLIDES)
	@start $(VIEWER) $(SLIDES).pdf

clean:
	@echo Cleaning up
	@rm -f $(NAME).pdf $(SLIDES).pdf *.aux *.log *.out *.toc *.lof *.lot *.blg *.bbl
