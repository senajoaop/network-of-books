from fileinput import filename
from isort import file
from matplotlib import fontconfig_pattern
import pdfplumber
import pandas as pd
import numpy as np
import spacy
from spacy import displacy
import networkx as nx
import matplotlib.pyplot as plt
import os
import re
from pyvis.network import Network
from sympy import N, degree
import community as community_louvain
import sys


class BookNetwork:
    def __init__(self):
        pass


    def _replace_nickname(self, ent):
        if ent in self.dfChar["character"].values:
            return self.dfChar.loc[self.dfChar["character"] == ent, "character_firstname"].iloc[0]
        elif ent in self.dfChar["character_firstname"]:
            return ent
        else:
            for col in self.dfChar.columns:
                if ent in self.dfChar[col].values:
                    return self.dfChar.loc[self.dfChar[col] == ent, "character_firstname"].iloc[0]


    def _filter_entity(self, ents):
        return [ent for ent in ents if ent in self.dfChar.stack().tolist()]


    def get_text_from_pdf(self, filePath, fileName, pages=None):
        bookText = ""

        with pdfplumber.open(filePath) as pdf:
            for page in pdf.pages:
                bookText += page.extract_text() + "\n"

            bookText = bookText.replace("\t", " ")

        with open(fileName, 'w') as file:
            file.write(bookText)


    def load_list_of_characters(self, filePath):
        dfChar = pd.read_csv(filePath)
        nNicknames = len(dfChar) - 1

        dfChar["character_firstname"] = dfChar["character"].apply(lambda ch: ch.split(' ', 1)[0])
        dfChar = dfChar.fillna("")

        self.dfChar = dfChar


    def load_book(self, bookPath):
        NER = spacy.load("en_core_web_sm")

        self.book = NER(open(bookPath).read())


    def create_entity_df(self):
        dfSentEntity = []

        for sent in self.book.sents:
            entities = [ent.text for ent in sent.ents]
            dfSentEntity.append({"sentence": sent, "entities": entities})

        dfSentEntity = pd.DataFrame(dfSentEntity)

        dfSentEntity["character_entities"] = dfSentEntity["entities"].apply(lambda e: self._filter_entity(e))
        dfSentEntity = dfSentEntity[dfSentEntity["character_entities"].map(len) > 0]
        dfSentEntity["character_entities"] = dfSentEntity["character_entities"].apply(lambda e: [self._replace_nickname(item) for item in e])

        self.dfSentEntity = dfSentEntity


    def generate_relationship(self, windowSize=5):
        relation = []

        for i in range(self.dfSentEntity.index[-1]):
            end_i = min(i + windowSize, self.dfSentEntity.index[-1])

            chars = sum((self.dfSentEntity.loc[i:end_i].character_entities), [])
            chars = [chars[i] for i in range(len(chars)) if (i==0) or chars[i] != chars[i-1]]

            if len(chars) > 1:
                for idx, ch1 in enumerate(chars[:-1]):
                    ch2 = chars[idx+1]
                    relation.append({"source": ch1, "target": ch2})

        dfRelation = pd.DataFrame(relation)
        dfRelation = pd.DataFrame(np.sort(dfRelation.values, axis=1), columns=dfRelation.columns)

        dfRelation["value"] = 1
        dfRelation = dfRelation.groupby(["source", "target"], sort=False, as_index=False).sum()

        self.dfRelation = dfRelation


    def plot_graph(self, graphFolder, community=True, graphWidth="1000px", graphHeight="700px", bgColor="#222222", fontColor="white"):
        G = nx.from_pandas_edgelist(self.dfRelation, source="source", target="target", edge_attr="value", create_using=nx.Graph())

        self.G = G

        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, with_labels=True, node_color="skyblue", edge_cmap=plt.cm.Blues, pos=pos)

        nodeDegree = dict(G.degree)
        nx.set_node_attributes(G, nodeDegree, "size")

        net = Network(notebook=False, width=graphWidth, height=graphHeight, bgcolor=bgColor, font_color=fontColor)
        net.repulsion()
        net.from_nx(G)
        net.show(f"{graphFolder}/network_result.html")

        degreeDict = nx.degree_centrality(G)
        betweennessDict = nx.betweenness_centrality(G)
        closenessDict = nx.closeness_centrality(G)

        dfDegree = pd.DataFrame.from_dict(degreeDict, orient="index", columns=["centrality"])
        dfBetweenness = pd.DataFrame.from_dict(betweennessDict, orient="index", columns=["centrality"])
        dfCloseness = pd.DataFrame.from_dict(closenessDict, orient="index", columns=["centrality"])

        nx.set_node_attributes(G, degreeDict, "degree_centrality")
        nx.set_node_attributes(G, betweennessDict, "betweenness_centrality")
        nx.set_node_attributes(G, closenessDict, "closeness_centrality")

        communities = community_louvain.best_partition(G)

        nx.set_node_attributes(G, communities, "group")

        net_com = Network(notebook=False, width=graphWidth, height=graphHeight, bgcolor=bgColor, font_color=fontColor)
        net_com.repulsion()
        net_com.from_nx(G)
        net_com.show(f"{graphFolder}/network_com_result.html")



if __name__=="__main__":
    books = []
    for i in range(4):
        book = BookNetwork()
        book.load_list_of_characters("data/characters.txt")
        book.load_book(f"data/book{i+1}.txt")
        book.create_entity_df()
        book.generate_relationship()
        book.plot_graph("data")

        books.append(book.G)

    evol = [nx.degree_centrality(book) for book in books]

    dfDegreeEvol = pd.DataFrame.from_records(evol)

    print(dfDegreeEvol)

    plt.cla()
    plt.clf()
    dfDegreeEvol[["Raffaella", "Elena", "Rino", "Nino", "Guido"]].plot()
    plt.show()

