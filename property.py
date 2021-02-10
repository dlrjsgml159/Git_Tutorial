property = {"General Information": [["Description"],
                                     ["Display Name"],
                                     ["Domain Object"],
                                     ["ID"],
                                     ["Name"]
                                     ],
             "Specific Information":[["Erase History When Reset"],
                                     ["Maximum Unknown Inputs"],
                                     ["Require Full History"],
                                     ["Sample Size"],
                                     ["Sample Type"],
                                     ["Status on Initialization"],
                                     ["Threshold"],
                                     ["Threshold Uncertainty"],
                                     ["Threshold Variable"],
                                     ["Trigger Count"]
                                     ]}

for index, name in enumerate(property):
    for index2, name2 in enumerate(property[name]):
        a = "self."
        b = name2[0]
        ab = a+b.replace(" ", "_")
        print(ab,"= ''")