#!/usr/bin/python

import glob
import json
import urllib.request
import sys

from bs4 import BeautifulSoup
from tomark import  Tomark

if len(sys.argv) < 2:
    print('ERROR: Please provide the root directory containing the package.json files as an command line argument')
    exit(1)
if len(sys.argv) > 2:
    print('WARING: All command line arguments but the first one will be ignored')
rootDirectory = sys.argv[1]
files = glob.glob(rootDirectory + '/**/package.json', recursive=True)
packageNames = set()
for file in files:
    if 'node_modules' in file:
        continue
    with open(file, 'r') as packageJsonFile:
        content = json.load(packageJsonFile)
        dependencyKeys = [ 'dependencies', 'devDependencies' ]
        for dependencyKey in dependencyKeys:
            if not dependencyKey in content.keys():
                continue
            for packageName in content[dependencyKey].keys():
                packageNames.add(packageName)
licenses = []
missingLicenses = []
for packageName in packageNames:
    print('Getting license for {}... ({}/{})'.format(packageName, len(licenses) + 1, len(packageNames)))
    baseUrl = 'https://www.npmjs.com/package/'
    packageUrl = baseUrl + packageName
    try:
        page = urllib.request.urlopen(packageUrl)
        content = page.read()
        soup = BeautifulSoup(content,'html.parser')
        possibleLicenseDivs = soup.find_all('p', {'class': 'f2874b88'})
        license = possibleLicenseDivs[1].text
        licenses.append({'Package': packageName, 'License': license})
    except Exception as error:
        print('ERROR: Cannot get license for {}'.format(packageName))
        print(error)
        missingLicenses.append(missingLicenses)

markdown = Tomark.table(licenses)
print(markdown)
if len(missingLicenses) >  0:
    print('Missing licenses: {}'.format(', '.join(missingLicenses)))