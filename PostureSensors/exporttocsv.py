import csv

PATH = '/home/pi/Dissertation/csv/log.csv'

def WriteRows(rows):
    # open the file in the write mode
    with open(PATH, 'a', newline='') as f:
        
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerows(rows)


def WriteHeaderRow(header):
    with open(PATH, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)