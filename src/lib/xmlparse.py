from lxml import etree
import pandas as pd

XML_META_FILE = "data/1000_000.xml"
LABELS_FILE = "data/DataLabels.csv"

# this oftens genes preanalysed
Data_labeled = pd.read_csv(LABELS_FILE, index_col=False)
gene_names = Data_labeled['Gene']
tissue_loc = Data_labeled['Tissue Location']
####
indexed_df = Data_labeled.set_index(['Gene'])
print indexed_df

dataset_gn = Data_labeled.iloc[:, 0]
dataset_gn = dataset_gn.tolist()
currentgene = ""

def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx + 1)
            indices.append(idx)
        except ValueError:
            break
    return indices


for event, elem in etree.iterparse(XML_META_FILE):  # here we load the big XML file.
    if elem.tag == "name":
        gn = str(elem.text);
        print gn;
        if gn in dataset_gn:
            do_analysis = "yes"
            print "yes!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!";
            Tissue_location = indexed_df.loc[gn, 'Tissue Location']

        else:
            do_analysis = "no"
    if do_analysis == "yes":
        if elem.tag == "antibody":
            for child in elem:
                if child.tag == "tissueExpression":
                    for child2 in child:
                        if child2.tag == "data":
                            tissuefound = "no"
                            list_with_levels = [];
                            Cell_type = [];
                            for child3 in child2:
                                if child3.tag == "tissue":
                                    tisuefound = "No";
                                    textTissue = child3.text;
                                    if ("skin 1" in textTissue) or ("skin 2" in textTissue):
                                        tissuefound = "yes"

                                elif child3.tag == "tissueCell":
                                    for child4_B in child3:
                                        if child4_B.tag == "cellType":
                                            Cell_type1 = child4_B.text

                                        elif child4_B.tag == "level":
                                            the_first = child4_B.text
                                    list_with_levels.append(Cell_type1);
                                    list_with_levels.append(the_first);



                                elif child3.tag == "patient":
                                    for child4 in child3:
                                        if child4.tag == "sample":
                                            for child5 in child4:
                                                # here we need an if statement that determines whether snomedParameters contains skin1 and skin2 and then if
                                                # it does we extract image

                                                if child5.tag == "snomedParameters":
                                                    for child6_2 in child5:

                                                        if child6_2.tag == "snomed":
                                                            if "Skin" in str(
                                                                    etree.tostring(child6_2, pretty_print=True)):
                                                                data = [];
                                                elif child5.tag == "assayImage":
                                                    for child6 in child5:
                                                        if child6.tag == "image":

                                                            for child7 in child6:

                                                                the_image_link = child7.text
                                                                if tissuefound == "yes":
                                                                    level_information = ": ".join(list_with_levels)
                                                                    with open(
                                                                            "tissue_specificity_rna_skin_elevated.csv",
                                                                            "a") as file_to_write:
                                                                        file_to_write.write(
                                                                            gn + ',' + the_image_link + ',' + level_information + ',' + Tissue_location + "\n")  # this prints it to the file?
                                                                        file_to_write.close();
                                                                    data = [];

                                    tissuefound = "no"
