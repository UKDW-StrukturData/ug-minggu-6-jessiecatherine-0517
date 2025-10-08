import pandas

# RULES:
# 1. JANGAN GANTI NAMA CLASS ATAU FUNGSI YANG ADA
# 2. JANGAN DELETE FUNGSI YANG ADA
# 3. JANGAN DELETE ATAU MENAMBAH PARAMETER PADA CONSTRUCTOR ATAU FUNGSI
# 4. GANTI NAMA PARAMETER DI PERBOLEHKAN
# 5. LARANGAN DI ATAS BOLEH DILANGGAR JIKA ANDA TAU APA YANG ANDA LAKUKAN (WAJIB BISA JELASKAN)
# GOODLUCK :)

class excelManager:
    def _init_(self,filePath:str,sheetName:str="Sheet1"):
        self.__filePath = filePath
        self.__sheetName = sheetName
        self.__data = pandas.read_excel(filePath,sheet_name=sheetName)
            
    
    def insertData(self,newData:dict,saveChange:bool=False):
        # kerjakan disini
        # clue cara insert row: df = pandas.concat([df, pandas.DataFrame([{"NIM":0,"Nama":"Udin","Nilai":1000}])], ignore_index=True)
        
        for col in self.__data.columns:
            if col not in newData:
                newData[col] = None

        self._data = pandas.concat([self._data, pandas.DataFrame([newData])], ignore_index=True)

        if (saveChange): 
            self.saveChange()

        
    def deleteData(self, targetedNim:str,saveChange:bool=False):
        # kerjakan disini
        # clue cara delete row: df.drop(indexBaris, inplace=True); contoh: df.drop(0,inplace=True)
        
        row_to_delete = None
        for i in self.__data.index:
            if str(self.__data.at[i, "NIM"]) == targetedNim:
                row_to_delete = i
                break
        
        if row_to_delete is not None:
            self.__data.drop(row_to_delete, inplace=True)
            self.__data.reset_index(drop=True, inplace=True)

            if saveChange:
                self.saveChange()
        else:
            pass
    
    def editData(self, targetedNim:str, newData:dict,saveChange:bool=False) -> dict:
        # kerjakan disini
        # clue cara ganti value: df.at[indexBaris,namaKolom] = value; contoh: df.at[0,ID] = 1
        row_to_edit = None
        for i in self.__data.index:
            if str(self.__data.at[i, "NIM"]) == targetedNim:
                row_to_edit = i
                break

        if row_to_edit is not None:
            for key, value in newData.items():
                if key in self.__data.columns:
                    self.__data.at[row_to_edit, key] = value
            
            if saveChange:
                self.saveChange()
            
            resultDict = {}
            for col in self.__data.columns:
                resultDict[col] = str(self.__data.at[row_to_edit, col])
            resultDict["Row"] = row_to_edit
            return resultDict
        else:
            return None
    
                    
    def getData(self, colName:str, data:str) -> dict:
        collumn = self.__data.columns # mendapatkan list dari nama kolom tabel
        
        # cari index dari nama kolom dan menjaganya dari typo atau spasi berlebih
        collumnIndex = [i for i in range(len(collumn)) if (collumn[i].lower().strip() == colName.lower().strip())] 
        
        # validasi jika input kolom tidak ada pada data excel
        if (len(collumnIndex) != 1): return None
        
        # nama kolom yang sudah pasti benar dan ada
        colName = collumn[collumnIndex[0]]
        
        
        resultDict = dict() # tempat untuk hasil
        
        for i in self.__data.index: # perulangan ke baris tabel
            cellData = str(self.__data.at[i,colName]) # isi tabel yand dijadikan str
            if (cellData == data): # jika data cell sama dengan data input
                for col in collumn: # perulangan ke nama-nama kolom
                    resultDict.update({str(col):str(self.__data.at[i,col])}) # masukan data {namaKolom : data pada cell} ke resultDict
                resultDict.update({"Row":i}) # tambahkan row nya pada resultDict
                return resultDict # kembalikan resultDict
        
        return None
    
    def saveChange(self):
        self._data.to_excel(self.filePath, sheet_name=self._sheetName , index=False)
    
    def getDataFrame(self):
        return self.__data
