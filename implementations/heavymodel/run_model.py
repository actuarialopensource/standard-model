# -*- coding: utf-8 -*-
# required libraries:
# heavymodel-lewisfogden pyyaml
# pip install heavymodel-lewisfogden pyyaml

# %%
from models.protection_model import TermAssurance
from heavymodel import Data, Basis
from models.valuation_functions import solve_prot_premium, get_bel

# %%
if __name__=='__main__':
    
    pricing_basis = Basis.read_yaml(r"models/term_basis.yaml")
    
    quote = {
        "sum_assured":100_000,
        "age_at_entry":49,
        "term_y":30,
        "smoker_status":"S",
        "shape":"level",
        "annual_premium":1,
        "init_pols_if":1,
        "extra_mortality":0,
        "sex":"F"
    }
    data = Data(quote)

    monthly_premium = solve_prot_premium(TermAssurance, data, pricing_basis)
    print("Premium: ", monthly_premium)
    
    bel_data = Data(quote)
    bel_data.annual_premium = monthly_premium * 12
    bel = get_bel(TermAssurance, bel_data, pricing_basis)
    print("PV Liab Check:", bel)
    print("This won't be zero due to rounding in solve_prot_premium")
    
