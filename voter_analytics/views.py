# File: views.py
# Author: Emily Yang (eyang4@bu.edu), 6/14/2025
# Description: The views python file which creates the views to handle each page request.   

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from . models import Voter

import plotly
import plotly.graph_objs as go 
from django.db.models import Count 

YEARS = list(range(1915, 2010))  
YEARS.reverse()  

class VotersListView(ListView): 
    '''View to display voters. ''' 

    model = Voter 
    template_name = 'voter_analytics/voters.html' 
    context_object_name = 'voters' 
    paginate_by = 100 

    def get_context_data(self, **kwargs): 
        '''provide context variables for use in template. '''
        context = super().get_context_data(**kwargs)
        years = list(range(1915, 2010))  
        years.reverse()  
        context['years'] = years
        return context 
    
    def get_queryset(self):
        '''filter the voters ''' 
        results = super().get_queryset()

        # filter results by these field(s): 
        print(self.request.GET) 
        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation:
                results = results.filter(party_affiliation=party_affiliation) 


        # Birth Year filtering 
        if ('min_birth_year' in self.request.GET) or ('max_birth_year' in self.request.GET): 
            min_birth_year = 1915 
            max_birth_year = 2010

            if self.request.GET['min_birth_year']: 
                min_birth_year = int(self.request.GET['min_birth_year'])

            if self.request.GET['max_birth_year']: 
                max_birth_year = int(self.request.GET['max_birth_year'])

            years = list(range(min_birth_year, max_birth_year + 1)) 
            selection = results.filter(date_of_birth__contains=str(years[0])) 
            if len(years) >= 2:  
                for year in years[1:]: 
                    selection = selection | results.filter(date_of_birth__contains=str(year)) 
            results = selection 


        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score) 

        if 'v20state' in self.request.GET:
            results = results.filter(v20state='TRUE')
        if 'v21town' in self.request.GET:
            results = results.filter(v21town='TRUE')
        if 'v21primary' in self.request.GET:
            results = results.filter(v21primary='TRUE')
        if 'v22general' in self.request.GET:
            results = results.filter(v22general='TRUE')
        if 'v23town' in self.request.GET:
            results = results.filter(v23town='TRUE')
                
        return results 
    

class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter 
    context_object_name = 'v'


class GraphsListView(ListView):
    '''View to show detail page for one voter.'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter 
    context_object_name = 'v' 
    
    def get_queryset(self):
        '''filter the voters ''' 
        results = super().get_queryset()

        # filter results by these field(s): 
        print(self.request.GET) 
        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation:
                results = results.filter(party_affiliation=party_affiliation) 


        # Birth Year filtering 
        if ('min_birth_year' in self.request.GET) or ('max_birth_year' in self.request.GET): 
            min_birth_year = 1915 
            max_birth_year = 2010

            if self.request.GET['min_birth_year']: 
                min_birth_year = int(self.request.GET['min_birth_year'])

            if self.request.GET['max_birth_year']: 
                max_birth_year = int(self.request.GET['max_birth_year'])

            years = list(range(min_birth_year, max_birth_year + 1)) 
            selection = results.filter(date_of_birth__contains=str(years[0])) 
            if len(years) >= 2:  
                for year in years[1:]: 
                    selection = selection | results.filter(date_of_birth__contains=str(year)) 
            results = selection 
            

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score) 

        if 'v20state' in self.request.GET:
            results = results.filter(v20state='TRUE')
        if 'v21town' in self.request.GET:
            results = results.filter(v21town='TRUE')
        if 'v21primary' in self.request.GET:
            results = results.filter(v21primary='TRUE')
        if 'v22general' in self.request.GET:
            results = results.filter(v22general='TRUE')
        if 'v23town' in self.request.GET:
            results = results.filter(v23town='TRUE')
                
        return results 
    
    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        ''' 
    
        # start with superclass context
        context = super().get_context_data(**kwargs)
        v = context['v']            
        context['years'] = YEARS 

        # create graph of voter distribution by year of birth as bar chart: 

        qs = self.get_queryset().exclude(date_of_birth__isnull=True)
        year_count_dict = {}

        for voter in qs:
            dob = voter.date_of_birth.strip()
            if '/' in dob:
                parts = dob.split('/')
                year = parts[-1]  
                if year.isdigit():
                    year = int(year)
                    if 1915 <= year <= 2025:
                        year_count_dict[year] = year_count_dict.get(year, 0) + 1

        x = list(range(1915, 2026))
        y = [year_count_dict.get(year, 0) for year in x]
        
        fig = go.Bar(x=x, y=y)
        title_text = f"Voter Distribution by Year of Birth"
        graph_div_birth_year = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 

        context['graph_div_birth_year'] = graph_div_birth_year  
        
        # generate the Pie chart of voter distribution by party affiliation 
        party_counts = self.get_queryset().values('party_affiliation').annotate(count=Count('id'))
        party_dict = {item['party_affiliation']: item['count'] for item in party_counts}

        labels = ['U ', 'D ', 'R ', 'CC', 'L ', 'T ', 'O ', 'G ', 'J ', 'Q ', 'FF']
        values = [party_dict.get(p, 0) for p in labels]
        
        fig = go.Pie(labels=labels, values=values) 
        title_text = f"Voter Distribution by Party Affiliation"
        graph_div_party = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_party'] = graph_div_party 

        # create graph of voter distribution by year of birth as bar chart: 
        qs = self.get_queryset()
        x= ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'] 
        y = [len(qs.filter(v20state='TRUE')), 
             len(qs.filter(v21town='TRUE')), 
             len(qs.filter(v21primary='TRUE')), 
             len(qs.filter(v22general='TRUE')), 
             len(qs.filter(v23town='TRUE'))
            ]
        
        fig = go.Bar(x=x, y=y)
        title_text = f"Vote Count by Election" 
        graph_div_election = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 

        context['graph_div_election'] = graph_div_election   
                
        return context 

