import os
import pandas as pd
import settings


def count_performance_rows():
    counts = {}
    with open(os.path.join(settings.PROCESSED_DIR, "Performance.txt"), "r") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            loan_id, date = line.split("|")
            if not loan_id in counts:
                counts[loan_id] = {
                    "foreclosure_status":False,
                    "performance_count" : 0
                }
            counts[loan_id]["performance_count"] += 1
            if len(date.strip()) >= 0:
                counts[loan_id]["foreclosure_status"] = True
    return counts

def get_performance_summary_value(loan_id, key, counts):
    value = counts.get(loan_id, {
        "foreclosure_status":False,
        "performance_count":0
    })
    return value[key]

def annotate(acquisitions, counts):
    acquisitions["foreclosure_status"] = acquisitions["id"].apply(lambda x: get_performance_summary_value(x, "foreclosure_status", counts))
    acquisitions["performance_count"] = acquisitions["id"].apply(lambda x: get_performance_summary_value(x, "performance_count", counts))
    for column in [
        "channel",
        "seller",
        "ft_home_buyer",
        "loan_purpose",
        "type_property",
        "occupancy_status",
        "property_state",
        "type_product"
    ]:
        acquisitions[column] = acquisitions[column].astype("category").cat.codes
    for start in ["first_payment", "origination"]:
        column = "{}_date".format(start)
        acquisitions["{}_month".format(start)] = pd.to_numeric(acquisitions[column].str.split("/").str.get(0))
        acquisitions["{}_year".format(column)] = pd.to_numeric(acquisitions[column].str.split("/").str.get(1))
        del acquisitions[column]
    
    acquisitions = acquisitions.fillna(-1)
    acquisitions = acquisitions[acquisitions["performance_count"]>settings.MINIMUM_TRACKING_QUARTERS]

    return acquisitions

def read():
    acquisitions = pd.read_csv(os.path.join(settings.PROCESSED_DIR, "Acquisition.txt"), sep="|")
    return acquisitions

def write(acquisitions):
    acquisitions.to_csv(os.path.join(settings.PROCESSED_DIR, "train.csv"), index=False)

if __name__ == "__main__":
    acquisitions = read()
    counts = count_performance_rows()
    acquisitions = annotate(acquisitions, counts)
    write(acquisitions)