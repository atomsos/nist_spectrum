#!/usr/bin/env python

"""
NIST element spectrum
"""

import re
import requests
import chemdata
from bs4 import BeautifulSoup
import json

baseurl = 'https://physics.nist.gov/cgi-bin/ASD/ie.pl?encodedlist=XXT2&spectra={0}&submit=Retrieve+Data&units=1&format=0&order=0&at_num_out=on&sp_name_out=on&ion_charge_out=on&el_name_out=on&seq_out=on&shells_out=on&level_out=on&ion_conf_out=on&e_out=0&unc_out=on&biblio=on'


# items = [
#         "At. Num.",
#         "Sp. Name.",
#         "Ion Charge",
#         "El. name",
#         "Isoel. Seq.",
#         "Ground Shells",
#         "Ground Level",
#         "Ionized Level",
#         "Ionization Energy (eV)",
#         "Uncertainty (eV)",
#         "References",
#     ]


def get_nist_spectrums(element):
    url = baseurl.format(element)
    return requests.get(url).decode()

def get_webdata():
    all_data = ''
    for element in chemdata.chemical_symbols[1:]:
        data = get_nist_spectrums(element)
    all_data += data
    return all_data


def get_localdata():
    # with open('nist_sample.html') as fd:
    with open('raw/nist_spectra.html') as fd:
        data = fd.read()
    data = data.replace('&nbsp;', ' ')
    return data

def get_splited_html(nist_all_data):
    # import pdb; pdb.set_trace()
    html_pattern = r'<html[\s\S]*?</html>'
    for html in re.findall(html_pattern, nist_all_data):
        yield html

def get_headers(nist_data):
    # import pdb; pdb.set_trace()
    header_string_pattern = r'<tr[\s\S]*?<th[\s\S]*?</tr>'
    header_string = re.findall(header_string_pattern, nist_data)[0]
    bs = BeautifulSoup(header_string.encode(), 'lxml')
    header = [th.text.strip() for th in bs.findAll('th')]
    return header

def get_data(nist_data, headers, outdict):
    trbsl_pattern = r'<tr class="bsl">[\s\S]*?</tr>'
    data = re.findall(trbsl_pattern, nist_data)
    data =  '\n'.join(data)
    bs = BeautifulSoup(data.encode(), 'lxml')
    for tr in bs.findAll('tr', attrs={'class' : 'bsl'}):
        data = [td.text.strip() for td in tr.findAll('td')]
        # re.sub(r'\s', '', data)
        number = int(data[0])
        charge = int(data[2])
        if not number in outdict:
            outdict[number] = dict()
        outdict[number][charge] = dict(zip(headers, data))
    return outdict


def parse_all_data():
    outdict = dict()
    for html in get_splited_html(get_localdata()):
        headers = get_headers(html)
        outdict = get_data(html, headers, outdict)
    return outdict


def main():
    with open('nist_spectrum.json', 'w') as fd:
        json.dump(parse_all_data(), fd)
    # print(json.dumps(parse_all_data()))


if __name__ == '__main__':
    main()
