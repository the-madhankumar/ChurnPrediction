import sys
import os

sys.path.append(os.path.abspath(".."))

import pandas as pd
from CP2.customer_cleaner import CustomerCleaner

df = pd.read_csv("../../dataset/telco_customer.csv")

customclean = CustomerCleaner(data_frame=df)
df = customclean.clean()
