#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv

import urllib.request
import argparse
import logging
import csv
import datetime
import re


LOG_FILENAME = 'errors.log'


def downloadData():
    required_args = ['url']
    parser = argparse.ArgumentParser()
    for r in required_args:
        parser.add_argument("--{0}".format(r), required=True)
    args = parser.parse_args()
    urllib.request.urlretrieve(args.url, 'csvData.csv')


def setup_logging(id, line_num=0):
    logger = logging.getLogger('assignment2')
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.ERROR,
    )
    if line_num:
        logger.error('Error processing line #{} for ID #{}'.format(
            id,
            line_num)
        )
    else:
        logger.error("Can't find data for ID #{}".format(id))
        raise ValueError("can't find your ID")


def processData():
    request = int(input("gimme ID: \n"))
    with open('csvData.csv', 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        new_dict = {}
        for line in csvreader:
            new_dict[line[0]] = (line[1], line[2])
    if str(request) not in new_dict:
        setup_logging(request)
        raise ValueError("Can't find your ID")
    for key, value in new_dict.items():
        if request == int(key):
            date = re.split('[/ *]', value[1])
            if len(date) < 3:
                if str(date[1]) in value[1]:
                    line_num = int(key) + 1
                    setup_logging(request, line_num)
                raise ValueError("Correct your data")
            day, month, year = int(date[0]), int(date[1]), int(date[2])
            d = datetime.datetime(year=year, month=month, day=day)
            updated_date = d.strftime("%d/%m/%Y")

            print("Person #{} is {} with a birthday of {}".format(
                request,
                value[0],
                updated_date
            ))
            f.close()


if __name__ == "__main__":
    downloadData()
    processData()
    

