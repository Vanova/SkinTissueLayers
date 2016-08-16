from lxml import etree

# file = open("tissue_specificity_rna_skin_elevated.xml")

# root = etree.XML(file.read())

currentgene = str("")

for event, elem in etree.iterparse("data/1000_000.xml"):
    if elem.tag == "name":
        gn = str(elem.text);
    elif elem.tag == "antibody":
        for child in elem:
            if child.tag == "tissueExpression":
                for child2 in child:
                    if child2.tag == "data":
                        for child3 in child2:
                            if child3.tag == "tissue" and (child3.attrib == 'skin 1' or child3.attrib == 'skin 2') :
                                print child3.attribute

                            elif child3.tag == "patient":
                                for child4 in child3:
                                    if child4.tag == "sample":
                                        for child5 in child4:
                                            if child5.tag == "snomedParameters":
                                                for child6_2 in child5:

                                                    if child6_2.tag == "snomed":
                                                        if "Skin" in str(etree.tostring(child6_2, pretty_print=True)):
                                                            print the_image_link;
                                            elif child5.tag == "assayImage":
                                                for child6 in child5:
                                                    if child6.tag == "image":

                                                        for child7 in child6:
                                                            the_image_link = child7.text
