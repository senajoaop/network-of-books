from fileinput import filename
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



class BookNetwork:
    def __init__(self):
        pass

    def get_text_from_pdf(filePath, fileName, pages=None):
        bookText = ""

        with pdfplumber.open(filePath) as pdf:
            for page in pdf.pages:
                bookText += page.extract_text() + "\n"

            bookText = bookText.replace("\t", " ")

        with open(fileName, 'w') as file:
            file.write(bookText)


if __name__=="__main__":
    BookNetwork()