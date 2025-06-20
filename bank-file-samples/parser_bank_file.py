import zipfile
import pandas as pd

def parser_bank_csv(file_path: str) -> dict:
    """
    解析包含銀行交易數據的 CSV 文件並返回一個 DataFrame
    這裡假設 CSV 文件的編碼為 UTF-8，並且 TX_DATE, TX_TIME, AMOUNT欄位為字符串類型
    """
    df = pd.read_csv(file_path, encoding='utf-8', dtype={"TX_DATE": str, "TX_TIME": str, "AMOUNT": str}) 
    return df.to_dict(orient="records")


def parser_bank_txt(file_path: str, encoding: str = 'utf-8') -> dict:
    """
    解析包含銀行交易數據的 txt 文件並返回一個 dictionary
    這裡假設 txt 文件的編碼為指定的 encoding，這部分可以根據實際情況調整
    """
    # 先將檔案內資料讀出，並賦予 data 變數
    with open(file_path, 'r', encoding=encoding) as f:
        data = f.readlines()
    
    # 將每一行資料轉換為字典格式，並append 到 dataset 列表中
    dataset = []
    for i in data:
        row = {
            'CUSTNO': i[0:4],
            'TX_DATE': i[5:13],
            'TX_TIME': i[17:23],
            'AMOUNT': i[24:33].lstrip('0'),  # 去除前導零
            'VRNUM': i[38:51],
            'REMARK': i[57:62],
        }
        dataset.append(row)
    return dataset


def parser_bank_zip(filename: str, passwd: str) -> dict:
    """
    解析包含銀行交易數據的 zip 文件並返回一個 dictionary
    """
    with zipfile.ZipFile(filename) as zf:
        # 抓取壓縮檔內的檔案資訊
        archive = zf.infolist()[0]
        # 抓取檔案大小，判斷是否為空檔
        zfSize = archive.file_size
        # 將壓縮檔內的檔案名稱和副檔名分開
        zfName, zfext = archive.filename.split('.')
        # 為方便判斷，將副檔名轉為小寫
        zfext = zfext.lower()
        # 解壓縮至當前目錄
        zf.extract(archive, ".", pwd=passwd.encode('utf-8'))
        
        if zfSize == 0:
            # 如果檔案大小為0，則返回空字典
            print ('為空檔')
            return {}
        else:
            # 根據副檔名選擇解析函數
            if zfext == 'csv':
                return parser_bank_csv(zfName + '.' + zfext)
            if zfext == 'txt':
                return parser_bank_txt(zfName + '.' + zfext, encoding='big5')



# 解析範例檔案副檔名為 csv 且帶有標題，並轉換成字典
csv_data = parser_bank_csv("sample_a.csv")
print (f"parser_bank_csv --> {csv_data}")

# 解析範例檔案副檔名為 txt ，且按照規格賦予至字典中
txt_data = parser_bank_txt("sample_b.txt", encoding='big5')
print (f"parser_bank_txt --> {txt_data}")

# 解析範例檔案副檔名為 zip ，且帶有密碼，並判斷副檔名為 csv 或 txt，並轉換成字典
zip_data = parser_bank_zip("sample_c.zip", passwd="12345678")
print (f"parser_bank_zip --> {zip_data}")
    