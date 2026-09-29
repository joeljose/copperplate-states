# Copperplate states. Everything runs in a container; nothing is installed on the host.
#
#   make image                      build the container (once)
#   make fetch                      download the 24 scans from the Allard Pierson IIIF server (~860 MB)
#   make compare                    compare every pair -> results/<pair>.json, results/<pair>.jpg
#   make compare PAIR=K1-01         one pair
#   make figures                    the README gallery -> results/gallery/
#   make lint                       ruff: lint and format check
#   make format                     ruff: apply formatting
#   make shell                      interactive python in the container

IMG  = copperplate-states
# Cap the container's RAM so a runaway job is killed alone. MEM=12g to raise.
MEM ?= 8g
RUN  = docker run --rm --memory=$(MEM) --memory-swap=$(MEM) -u $$(id -u):$$(id -g) -v $(CURDIR):/w -w /w $(IMG)

image:
	docker build -t $(IMG) -f docker/Dockerfile docker
fetch:
	$(RUN) python -m copperplate.fetch
compare:
	$(RUN) python -m copperplate.compare $(if $(PAIR),--pair $(PAIR))
figures:
	$(RUN) python -m copperplate.figures
lint:
	$(RUN) sh -c 'ruff check . && ruff format --check .'
format:
	$(RUN) sh -c 'ruff check --fix . && ruff format .'
shell:
	docker run --rm -it -u $$(id -u):$$(id -g) -v $(CURDIR):/w -w /w $(IMG) bash

.PHONY: image fetch compare figures lint format shell
