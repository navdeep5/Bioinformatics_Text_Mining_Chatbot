main_prompt = """
The task is to extract biology-related triples from scientific research papers.
The rules are:
1. Only use the following predicates in the triple: “causes”, ”biolocation is”, “exposed through”, “sourced through”, “has role of”, “involved in”.
2. If there is more than one noun in the object, separate it into multiple triples.
3. If you don't find relevant biology-related triples in the paper or you are not sure, return: null.
4. The response is an array of the relevant triples in the form: [subject, predicate, object]. 
Q: Interaction of TMPC with ANXA2 mediated attachment and colonization of S. anginosus and induced mitogen-activated protein kinase (MAPK) activation.
A: ["TMPC", "involved in", "MAPK activation"],
["ANXA2", "involved in", "MAPK activation"]
Q: α-Lipoic acid plays an essential role in mitochondrial dehydrogenase reactions.
A: ["alpha-Lipoic acid", "involved in", "mitochondrial dehydrogenase reactions"]
Q: Ferroptosis, a form of regulated cell death that is driven by iron-dependent phospholipid peroxidation, has been implicated in multiple diseases, including cancer
A: ["Ferroptosis", "causes", "cancer"]
Q: These transporters and other biotin-binding proteins partition biotin to the cytoplasm and mitochondria cell compartments.
A: ["Biotin", "biolocation is", "cytoplasm"],
["Biotin", "biolocation is", "mitochondria"]
"""

abstract = """Title: The Role of Palmityl-CoA in Cardiolipin Biosynthesis: A Comprehensive Analysis of Different Cardiolipin Molecular Species\n\nBackground: Cardiolipin (CL) is an essential phospholipid found primarily in the inner mitochondrial membrane, playing a vital role in various cellular processes. The biosynthesis of cardiolipin involves several enzymatic reactions, including the participation of Palmityl-CoA. In this study, we aimed to investigate the role of Palmityl-CoA in cardiolipin biosynthesis and its influence on different cardiolipin molecular species.\n\nMethods: We conducted an extensive literature review and analyzed various studies to identify and characterize the different cardiolipin molecular species formed during cardiolipin biosynthesis involving Palmityl-CoA. We also examined the effects of Palmityl-CoA on cardiolipin molecular species composition and its potential implications on cellular functions.\n\nResults: Our analysis revealed that Palmityl-CoA is involved in the biosynthesis of several cardiolipin molecular species, including CL(16:1(11Z)/16:1(11Z)/16:1(9Z)/18:1(11Z)), CL(15:1(11Z)/15:1(9Z)/15:1(11Z)/25:1(9Z)), CL(14:1(9Z)/15:0/15:1(9Z)/18:0), and CL(16:0/18:1(11Z)/18:3(9Z,12Z,15Z)/20:3(5Z,8Z,11Z)). The presence of Palmityl-CoA affects the composition of cardiolipin molecular species, leading to variations in their physicochemical properties and potential cellular functions.\n\nConclusion: This study highlights the importance of Palmityl-CoA in cardiolipin biosynthesis and its influence on different cardiolipin molecular species. Further research is needed to elucidate the specific mechanisms underlying these interactions and their potential implications on cellular functions and overall mitochondrial health."""

print(abstract)