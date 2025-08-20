import requests
import json
import random

class DiseaseAPIClient:
    def __init__(self):
        # Using mock data for demonstration - in real app, you'd use actual APIs
        self.mock_data = {
            'diabetes': {
                'global_cases': 537000000,
                'deaths_per_year': 1500000,
                'prevalence': '6.2%',
                'new_cases_daily': 1500,
                'countries_affected': 195
            },
            'heart_disease': {
                'global_cases': 523000000,
                'deaths_per_year': 17900000,
                'prevalence': '6.6%',
                'new_cases_daily': 2000,
                'countries_affected': 195
            },
            'hypertension': {
                'global_cases': 1280000000,
                'deaths_per_year': 10400000,
                'prevalence': '16.5%',
                'new_cases_daily': 3500,
                'countries_affected': 195
            },
            'asthma': {
                'global_cases': 262000000,
                'deaths_per_year': 455000,
                'prevalence': '3.4%',
                'new_cases_daily': 800,
                'countries_affected': 195
            },
            'cancer': {
                'global_cases': 19300000,
                'deaths_per_year': 10000000,
                'prevalence': '0.25%',
                'new_cases_daily': 53000,
                'countries_affected': 195
            },
            'stroke': {
                'global_cases': 101000000,
                'deaths_per_year': 6550000,
                'prevalence': '1.3%',
                'new_cases_daily': 1800,
                'countries_affected': 195
            }
        }
    
    def get_disease_stats(self, disease_name):
        """Get global disease statistics"""
        disease_key = disease_name.lower().replace(' ', '_')
        base_data = self.mock_data.get(disease_key, {
            'global_cases': 0,
            'deaths_per_year': 0,
            'prevalence': '0%',
            'new_cases_daily': 0,
            'countries_affected': 0
        })
        
        # Add some random variation to make it look more realistic
        variation = random.uniform(0.95, 1.05)
        base_data['global_cases'] = int(base_data['global_cases'] * variation)
        base_data['deaths_per_year'] = int(base_data['deaths_per_year'] * variation)
        base_data['new_cases_daily'] = int(base_data['new_cases_daily'] * variation)
        
        return base_data
    
    def get_all_disease_stats(self):
        """Get statistics for all diseases"""
        all_stats = {}
        for disease_name in self.mock_data.keys():
            all_stats[disease_name] = self.get_disease_stats(disease_name)
        return all_stats
    
    def get_trending_diseases(self):
        """Get trending diseases based on search volume"""
        trending = [
            {'name': 'COVID-19', 'trend': '+15%'},
            {'name': 'Diabetes', 'trend': '+8%'},
            {'name': 'Heart Disease', 'trend': '+5%'},
            {'name': 'Mental Health', 'trend': '+12%'},
        ]
        return trending
    
    def get_regional_data(self, disease_name, region='global'):
        """Get regional disease data"""
        base_stats = self.get_disease_stats(disease_name)
        
        # Mock regional variations
        regional_multipliers = {
            'north_america': 0.8,
            'europe': 0.9,
            'asia': 1.3,
            'africa': 1.1,
            'south_america': 1.0,
            'oceania': 0.7,
            'global': 1.0
        }
        
        multiplier = regional_multipliers.get(region, 1.0)
        
        return {
            'region': region.replace('_', ' ').title(),
            'cases': int(base_stats['global_cases'] * multiplier * 0.2),  # Regional portion
            'prevalence': f"{float(base_stats['prevalence'].rstrip('%')) * multiplier:.1f}%",
            'deaths_per_year': int(base_stats['deaths_per_year'] * multiplier * 0.2)
        }

# Global API client instance
api_client = DiseaseAPIClient()
