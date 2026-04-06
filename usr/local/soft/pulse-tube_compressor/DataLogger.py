import csv
import os.path

class DataLogger:
    #constructor
    def __init__(self, fname, fieldnames):
        self.fname = fname #set the filename to write to
        self.fieldnames = fieldnames #define the headers

        #check if the file exists, if it doesn't write the headers to the file
        if not os.path.exists(self.fname):
            with open(self.fname, "w") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames) #create the writer object
                writer.writeheader() #write the header to the file

    #define the writing method
    def write(self, data):
        with open(self.fname, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames) #create the writer object
            writer.writerow(data)
