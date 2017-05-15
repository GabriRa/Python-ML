import os
import settings
import pandas as pd

HEADERS = {
    "Acquisition" : [
        "id",
        "channel",
        "seller", 
        "interest_rate",
        "debt_balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "ltv",
        "cltv",
        "borrowers",
        "dti",
        "credit_score",
        "ft_home_buyer",
        "loan_purpose",
        "type_property",
        "number_units",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "type_product",
        "co_borrower_credit_score",
        "type_insurance",
        "relocation_mortage"
    ],
    "Performance" : [
        "id",
        "reporting_period",
        "servicer_name",
        "interest_rate",
        "debt_balance",
        "loan_age",
        "months_to_maturity",
        "adjusted_months_to_maturity"
        "maturity_date",
        "msa",
        "delinquency_status",
        "modification_flag",
        "zero_balance_code",
        "zero_balance_date",
        "last_paid_installment_date",
        "foreclosure_date",
        "disposition_date",
        "foreclosure_costs",
        "property_repair_costs",
        "recovery_costs",
        "misc_costs",
        "tax_costs",
        "sale_proceeds",
        "credit_enhancement_proceeds",
        "repurchase_proceeds",
        "other_foreclosure_proceeds",
        "non_interest_bearing_balance",
        "principal_forgiveness_balance",
        "repurchase_proceeds_flag",
        "principal_write_off_amount",
        "serving_activity"
    ]
}

SELECT = {
    "Acquisition": HEADERS["Acquisition"],
    "Performance": [
        "id",
        "foreclosure_date"
    ]
}


def concatenate(prefix="Acquisition"):
    files = os.listdir(settings.DATA_DIR)
    full = []
    for f in files:
        if not f.startswith(prefix):
            continue
        data = pd.read_csv(os.path.join(settings.DATA_DIR, f), sep="|", header=None, names=HEADERS[prefix], index_col=False)
        data = data[SELECT[prefix]]
        full.append(data)
    
    full = pd.concat(full, axis=0)

    full.to_csv(os.path.join(settings.PROCESSED_DIR, "{}.txt".format(prefix)), sep="|", header=SELECT[prefix], index=False)

if __name__=="__main__":
    concatenate("Acquisition")
    concatenate("Performance")
