.PHONY: all


all:
	make nist_spectrum.json


nist_spectrum.json: nist_spectrum.py raw/nist_spectra.html
	python nist_spectrum.py
	cp nist_spectrum.json ../old/chemdata/chemdata