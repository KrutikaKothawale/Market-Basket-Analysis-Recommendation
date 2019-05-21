# Filename: run_luigi.py
import luigi
from datacleaning import data_load_clean
from featureengg import feature_engineering
from buildmodel import build_model

 
class DataCleaningAndLoading(luigi.Task):
 
    def requires(self):
        return []
 
    def output(self):
        return []
 
    def run(self):
        data_load_clean()
        
        

class FeatureEngineering(luigi.Task):
 
    def requires(self):
        return [DataCleaningAndLoading()]
 
    def output(self):
        return []
 
    def run(self):
        feature_engineering()
 

class CreateModel(luigi.Task):
 
    def requires(self):
        return [FeatureEngineering()]
 
    def output(self):
        return []
 
    def run(self):
        build_model()  
        
                 
if __name__ == '__main__':
    luigi.run()
