# File: models.py 
# Author: Emily Yang (eyang4@bu.edu), 6/14/2025
# Description: The models python file which defines the database. 

from django.db import models

class Voter(models.Model): 
    '''
    Store/represent the data from a registered voter.
    ''' 
    last_name = models.TextField() 
    first_name = models.TextField() 
    street_number = models.TextField() 
    street_name = models.TextField() 
    apartment_number = models.TextField() 
    zip_code = models.IntegerField() 
    date_of_birth = models.TextField() 
    date_of_registration = models.TextField() 
    party_affiliation = models.CharField(max_length=2) 
    precinct_number = models.TextField() 

    v20state = models.TextField() 
    v21town = models.TextField() 
    v21primary = models.TextField() 
    v22general = models.TextField() 
    v23town = models.TextField() 

    voter_score = models.IntegerField() 

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'


def load_data(): 
    '''function to load data records from CSV file into the Django database. ''' 
    
    filename = '/Users/yange/django/newton_voters.csv' 
    f = open(filename) 
    f.readline() 
    for line in f: 

        try: 
            fields = line.strip().split(',') 
            # create a new instance of Voter object with this record from CSV 
            voter = Voter(last_name = fields[1],  
                        first_name = fields[2],  
                        street_number = fields[3],  
                        street_name = fields[4],  
                        apartment_number = fields[5],  
                        zip_code = fields[6],  
                        date_of_birth = fields[7],  
                        date_of_registration = fields[8],  
                        party_affiliation = fields[9],  
                        precinct_number = fields[10],  

                        v20state = fields[11],  
                        v21town = fields[12],  
                        v21primary = fields[13],  
                        v22general = fields[14],  
                        v23town = fields[15],  
                        voter_score = fields[16],   
                        ) 
            voter.save() 

        except: 
            print("Something went wrong! ") 
            print(f"line={line}") 
    print(f"Done. Created {len(Voter.objects.all())} Results. ")

  
