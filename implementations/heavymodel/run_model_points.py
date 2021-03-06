# -*- coding: utf-8 -*-
# required libraries:
# heavymodel-lewisfogden pyyaml
# pip install heavymodel-lewisfogden pyyaml

# %%
from models.protection_model import TermAssurance
from heavymodel import Data, Basis
from models.valuation_functions import solve_prot_premium

import pandas as pd

pricing_basis = Basis.read_yaml(r"models/term_basis.yaml")

# %%

df_model_points = pd.read_csv(r"data/term_data_1k.csv")

# %%

def get_premium(row):
    try:
        data = Data(row)
        monthly_premium = solve_prot_premium(TermAssurance, data, pricing_basis)
        return monthly_premium
    except Exception as err:
        return repr(err)

#def npv(cashflow, yield_curve):
#    pv = 0.0
#    for t in range(len(cashflow.values)):
#        pv += yield_curve.v[t] * cashflow(t)
#    return pv

def get_npv(row, model_variables):
    # We call the model directly here as we want to get several NPVs without recalculating it all
    try:
        data = Data(row)
        model = TermAssurance(data, pricing_basis)
        proj_term = data.term_y * 12 + 1
        model._run(proj_len = proj_term)
        results = {}
        for field_name in model_variables:
            field_object = getattr(model, field_name)
            results[field_name] = pricing_basis.rfr.npv(field_object, proj_term)
        return results
    except Exception as err:
        return repr(err)


# %%

df_model_points["monthly_premium"] = df_model_points.apply(get_premium, axis=1)
df_model_points["annual_premium"] = df_model_points["monthly_premium"] * 12

# %%


output_columns = ["net_cf", "claims", "premiums"]

#df_model_points2 = df_model_points.apply(func=lambda row: get_npv(row, output_columns),
#                                         result_type="expand",
#                                         axis=1)

# %%

df_model_points2 = df_model_points.apply(func=get_npv,
                                         model_variables = output_columns,
                                         result_type="expand",
                                         axis=1)
# %%
