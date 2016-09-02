import pandas as pd


"""antibiotics.csv =
Event title,                     prefearfactor,     postfearfactor,      fear type
Toastmasters speech,             8,                       5,           public speaking
Presentation,                    10,                      3,           public speaking
Meeting with boss,               4,                       2,           performance
Meeting with enemy,              8,                       4,           relationships"""

df = pd.read_csv(StringIO(antibiotics), skiprows=1, skipinitialspace=True)
x = np.zeros(len(df))
y = np.zeros(len(df))

"""
Arch comments:
As far as I understand and how it looks in the code is that if you are
reading csv file data like above, df will be a series of lists like this:
df.prefearfactor = [8, 10, 4, 8]
print factor for factor in df.fearfactor will give- 8 10 4 8
"""