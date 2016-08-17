from lxml import etree
import pandas as pd


XML_META_FILE = "data/1000_000.xml"
LABELS_FILE = "data/DataLabels.csv"

csv_reader = pd.read_csv(LABELS_FILE, index_col=False)
genes = csv_reader['Gene']
locations = csv_reader['Tissue Location']
gene_loc = {}
for (k, v) in zip(genes, locations):
    gene_loc[k] = v



class TitleTarget(object):
    def __init__(self):
        self.text = []
    def start(self, tag, attrib):
        self.is_title = True if tag == 'name' else False
    def end(self, tag):
        pass
    def data(self, data):
        if self.is_title:
            self.text.append(data.encode('utf-8'))
    def close(self):
        return self.text

parser = etree.XMLParser(target = TitleTarget())

results = etree.parse(XML_META_FILE, parser)

# When iterated over, 'results' will contain the output from
# target parser's close() method

out = open(XML_META_FILE, 'w')
out.write('\n'.join(results))
out.close()