# GCMD KEYWORD CHECKER

## GCMD keyword checker that checks for valid GCMD <gmd:thesaurusName> keywords in ISO metadata XML files according to the CSV specs from here https://gcmdservices.gsfc.nasa.gov/static/kms/ 

### Questions/issues: thomas.jaensch@noaa.gov

## Requirements
This CLI tool has been written and tested for Python 2.7 without any use of 3rd party libraries.

## Usage

* CD into folder with the gcmd.py file

* Run "python2.7 gcmd.py -t *target file or folder*"

## Examples

`python2.7 gcmd.py -t .` for target XML files in current directory

`python2.7 gcmd.py -t ./blah` for target files in blah subdirectory of current directory

`python2.7 gcmd.py -t blah.xml` for target file blah.xml in current directory

`python2.7 gcmd.py -t *absolute file/folder path in file system*`

## Results

The program will generate command line output and also a CSV file if any invalid keywords were found inside of the directory where the program was run. If no invalid keywords were found, it will say so on the command line but no CSV file will be created. If the program fails to run it will say so on the command line.