import pandas as pd

input_file = "Email_Assistant_Dataset_100.xlsx"
output_file = "data/emails.csv"

df = pd.read_excel(input_file, sheet_name="emails")

df.to_csv(output_file, index=False)

print("Dataset converted successfully!")
print("Rows:", len(df))
print(df.head())