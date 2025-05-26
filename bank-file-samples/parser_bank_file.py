import os
import zipfile

# Create directories to store updated samples
output_dir = "/mnt/data/bank_samples"
os.makedirs(output_dir, exist_ok=True)

# Updated Sample A: CSV file (UTF-8)
sample_a_content = """account_number,amount,ref_code,date
12345678,1500,RF20250521,2025-05-21
87654321,2200,RF20250522,2025-05-22
"""
sample_a_path = os.path.join(output_dir, "sample_a.csv")
with open(sample_a_path, "w", encoding="utf-8") as f:
    f.write(sample_a_content)

# Updated Sample B: TXT fixed-width file (Big5)
sample_b_lines = [
    "12345678901500002520250521RF20250521",
    "98765432102200003220250522RF20250522"
]
sample_b_path = os.path.join(output_dir, "sample_b.txt")
with open(sample_b_path, "w", encoding="big5") as f:
    f.write("\n".join(sample_b_lines))

# Updated Sample C: ZIP with CSV inside (UTF-8)
sample_c_inner_csv = """acct,amt,ref,date
34567890,1800,CZ20250521,2025-05-21
98761234,2400,CZ20250522,2025-05-22
"""
inner_csv_name = "C_reconciliation.csv"
inner_csv_path = os.path.join(output_dir, inner_csv_name)
with open(inner_csv_path, "w", encoding="utf-8") as f:
    f.write(sample_c_inner_csv)

# Create ZIP file
sample_c_zip_path = os.path.join(output_dir, "sample_c.zip")
with zipfile.ZipFile(sample_c_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(inner_csv_path, arcname=inner_csv_name)

# Clean up temporary CSV used in ZIP
os.remove(inner_csv_path)

sample_a_path, sample_b_path, sample_c_zip_path
