import datetime
import logging
import urllib2
import argparse
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--url', help='Enter a specific URL to download .csv file / Example: c:\>assignment2.py -url https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
args = parser.parse_args()

logging.basicConfig(filename='errors.log',level=logging.ERROR)
logger = logging.getLogger('assignment2')


def downloadData(url):
    csvdata = urllib2.urlopen(url)
    return csvdata
    

def processData(csvdata):
    newdata = csv.DictReader(csvdata)
    results = {}

    for num, line in enumerate(newdata):
        try:
            bday = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            results[line['id']] = (line['name'], bday)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(num, line['id']))
    return results


def displayPerson(id, personData):
    idnum = str(id)
    if idnum in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(id, personData[idnum][0],datetime.datetime.strftime(personData[idnum][1], '%Y-%m-%d'))
    else:
        print 'No user found with that ID'


def main():
    if not args.url:
        print 'ERROR: No URL provided'
	exit()
    try:
        csvData = downloadData(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL'
        exit()
    else:
        persondata = processData(csvData)
        selectid = raw_input('Please enter an ID#:')
        if selectid == '':
            print 'input positive integer number'
            main()
        selectid = int(selectid)
        if selectid <= 0:
            print 'ID# should be greater than zero. Try it again!'
            exit()
        else:
            displayPerson(selectid, persondata)
            main()


main()
