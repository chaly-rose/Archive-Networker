import sys
from numpy import shape
from authorizer import DataManager
from authorizer import Authorizer
from key_services import Messenger
import os
import io
from bson import ObjectId
import json
import pandas as pd
import openpyxl


class GraphAI():
    def __init__(self):
        self.configfile = os.getcwd() + f"/src/security/config"
        self.keyfile = os.getcwd() + f"/src/security/private_key.pem"
        self.security_manager: Authorizer = Authorizer()
        self.key_service: Messenger = Messenger()
        self.key_service.init(configfile=self.configfile, keyfile=self.keyfile)
        self.server = self.key_service.config['cloud.mongodb']

    def create_entities_graph(self, subject, location):
        user = self.key_service.config['cloud.mongodb']['data_reader']
        self.security_manager.set_connection_id(user['username'], user['password'], self.server['connection_url'])
        db = self.security_manager.DbManager.getDatabase(subject)
        # grab all docs
        ship_list = []
        destination_list = []
        types = []
        names = []
        sources = []
        targets = []
        weights = []
        scores = []

        # setup DataFrame for excel graphing
        columns = ['Type', 'Name', 'Source', 'Target', 'Weight', 'Score']
        df = pd.DataFrame(columns=columns)

        documents = db[location].find()
        for e in documents:
            # move through entities data_set
            ents_data = e['data']['entities']
            for d in ents_data:
                js = json.loads(d)['entities']
                for j in js:
                    types += [j['type']]
                    names += [j['text']]
                    sources += [e['ship']]
                    targets += [e['to_location']]
                    weights += [j['count']]
                    scores += [j['relevance']]

        df = ({
            'Type': types,
            'Name': names,
            'Source': sources,
            'Target': targets,
            'Weight': weights,
            'Score': scores
        })

        # load data into pandas
        dataset_df = pd.DataFrame(df, columns=columns)
        try:
            dataset_df.to_excel(os.getcwd() + "/" + subject + "_to_location_" + location + "_directed_graph.xlsx")
            print("Graph Excel File saved to: " + os.getcwd() + "/" + subject + "_to_location_" + location + "_directed_graph.xlsx")
        except FileNotFoundError as e:
            print(e)
        return dataset_df

    def export_graph_model(self, data_file):
        file = open(os.getcwd() + "/" + data_file, 'r')

def main():
    subject = ""
    location = ""
    command = sys.argv
    if len(sys.argv) > 0:
        for i, c in enumerate(command):
            if "--subject" in c:
                subject = command[i + 1]
            if "--location" in c:
                location = command[i + 1]
    else:
        print("no parameters give: --subject [name] --location [place]")
        exit(1)

    print("Creating File for " + subject + " at location: " + location)
    grapher = GraphAI()
    df = grapher.create_entities_graph(subject, location)
    print("Graph Data Sheet completed with rows " + str(shape(df)[0]) + " and " + str(shape(df)[1]) + " columns.")


if __name__ == "__main__":
    main()
