import pandas as pd

company_df = pd.read_excel("./src/KRX종목코드.xlsx", dtype=object)
print(company_df.loc[company_df['회사']=="삼성전자"]["종목코드"])
