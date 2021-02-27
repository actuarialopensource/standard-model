import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

from models.protection_model import TermAssurance
from heavymodel import Data, Basis
from models.valuation_functions import solve_prot_premium, get_bel

pricing_basis = Basis.read_yaml(r"models/term_basis.yaml")

st.set_page_config(layout="wide")

st.sidebar.title("Policy Data")

sum_assured = st.sidebar.number_input("Sum Assured",
                                      min_value=10_000,
                                      max_value=1_000_000,
                                      value=100000)

shape = st.sidebar.radio("Benefit Shape", ["level", "decreasing"])

if st.sidebar.checkbox("Smoker"):
    smoker_status = "S"
else:
    smoker_status = "N"


age_at_entry = st.sidebar.slider("Age At Entry", min_value=18, max_value=75, value=30, step=1)

term = st.sidebar.slider("Policy Term", min_value=5, max_value=35, value=20, step=1)


quote = {
        "sum_assured":sum_assured,
        "age_at_entry":age_at_entry,
        "term_y":term,
        "smoker_status":smoker_status,
        "shape":shape,
        "annual_premium":1,
        "init_pols_if":1,
        "extra_mortality":0,
        "sex":"F"
    }

data = Data(quote)

st.sidebar.title("Result")
st.title("Projection Information")

col1, col2 = st.beta_columns(2)

try:
    monthly_premium = solve_prot_premium(TermAssurance, data, pricing_basis)
    st.sidebar.write(f"## Monthly Premium: {monthly_premium:0.2f}")

    data.annual_premium = 12 * monthly_premium

    model = TermAssurance(data=data, basis=pricing_basis)

    model._run(data.term_y*12+1)

    df = model._dataframe()
    df.index = df["t"]
    df["year"] = df["t"] // 12
    df_summed = df.groupby("year").sum()
    
    df_annual = df.iloc[::12, :]
    df_annual.index = df_annual["year"]

    with col1:
        st.write("## Benefit Shape")
        st.bar_chart(df_annual["claim_pp"])
        st.write("## Net Cashflow")
        st.bar_chart(df_summed["net_cf"])

    with col2:
        st.write("## Cashflow Results")
        st.write(df)

        st.write("## Projection of Premiums and Claims")
        st.line_chart(df[["premiums", "claims"]])
except KeyError:
    st.write("Invalid Combination of parameters")



