# nist_spectrum
spider for https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html




## Install requirements

`pip install -r requirements.txt`



## Get raw data

We can get raw data using curl 

```bash
for element in `python -c 'import chemdata; print(" ".join(chemdata.chemical_symbols[1:]))'`; do 
curl "https://physics.nist.gov/cgi-bin/ASD/ie.pl?encodedlist=XXT2&spectra=$element&submit=Retrieve+Data&units=1&format=0&order=0&at_num_out=on&sp_name_out=on&ion_charge_out=on&el_name_out=on&seq_out=on&shells_out=on&level_out=on&ion_conf_out=on&e_out=0&unc_out=on&biblio=on" >> raw/nist_spectra.html ; 
done
```


## Get json file

Directly use make command

```bash
make nist_spectrum.json
```




##　TODOS

* [ ] https://physics.nist.gov/PhysRefData/ASD/lines_form.html
