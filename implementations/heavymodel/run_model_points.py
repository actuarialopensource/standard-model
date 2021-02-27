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

df_model_points["monthly_premium"] = df_model_points.apply(get_premium, axis=1)
# %%
