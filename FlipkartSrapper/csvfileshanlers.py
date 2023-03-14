import csv, os

class CSVHandlers:

    def __init__(self, filename:str, mode:str):
        self.filename = filename
        self.mode     = mode
    
    def dict_csv_writer(self,  keys, dict_datas,filename=None,mode=None, is_initial=False):
        """This class will use to write dict data in any csv files"""

        # fields_name, dict_data = self.soup_data_extractor()

        if filename is None:
            filename = self.filename

        if mode is None:
            mode = self.mode

        
        if os.path.isfile(path=filename):


            with open(file=filename, mode=mode) as csvfile:

                if csvfile.writable():
                    csvdict_writer = csv.DictWriter(csvfile, fieldnames=keys)
                    
                    if is_initial==True:
                        try:
                            csvdict_writer.writeheader() # writting header
                        except:
                            print('Error While writing fields headers in csv file ')
                        
                    try:
                        # writing data here as dict
                        csvdict_writer.writerows(dict_datas)  
                    except:
                        print('Error while dict data writting in csv file' )
                    
                    print('Data successfuly written in csv file')

                else: 
                    print(" File Not Writtable Don't Have Write Permission")

        else:
            print('Enter file does not exist enter valid file name')
    
    def dict_csv_reader(self,filename=None,mode=None):
        """This class will use to write dict data in any csv files"""

        # fields_name, dict_data = self.soup_data_extractor()

        if filename is None:
            filename = self.filename

        if mode is None:
            mode = self.mode

        
        if os.path.isfile(path=filename):


            with open(file=filename, mode=mode) as csvfile:

                if csvfile.readable():
                    try:
                        csvread = csv.DictReader(csvfile)
                    except:
                        print('\n \n \n Error while csv file reading ')
                    else:
                        return csvread

                    
                else: 
                    print(" File Not Writtable Don't Have Write Permission")

        else:
            print('Enter file does not exist enter valid file name')
    

    