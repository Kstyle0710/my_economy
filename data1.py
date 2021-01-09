import pandas as pd
import FinanceDataReader as fdr
from A1_companycode import *


# 기업별 주가정보 호출 함수
def comp_info(name):
    print(name)
    code = company_df.loc[[company_df['회사']==name],"종목코드"]
    print(code)
    print(type(code))
    result = fdr.DataReader(code)
    return result

# df_samsung = comp_info("삼성전자")
# print(df_samsung)
df_hynix = comp_info("SK하이닉스")
print(df_hynix)
# df_LGcham = comp_info("LG화학")


