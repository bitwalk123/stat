import pandas as pd

# Reference
# https://note.nkmk.me/python-pandas-to-excel/
# pip install openpyxl
# pip install xlwt
print(pd.__version__)

df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                  index=['one', 'two', 'three'],
                  columns=['a', 'b', 'c'])

print(df)
#         a   b   c
# one    11  21  31
# two    12  22  32
# three  31  32  33

df.to_excel('pandas_to_excel_no_index.xlsx', index=False, header=True)
