import pandas as pd
import re
from shapely.geometry import Point
import geopandas as gpd
import os

def fileNamer(exportPath, fileName, extension, separator = "_#"):
    separator = separator.replace('#', '')
    specialChars = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', '\\']
    if len(separator) == 1:
        if os.path.exists(exportPath+f"\{fileName}"+'.'+extension):
            fileLst = []
            for file in os.listdir(exportPath):
                if (separator in specialChars):
                    # когато разделителя е един от специалните
                    # символи трябва да се сложи \ преди променливата
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(f'{fileName}\{separator}\d*.{extension}', file):
                        fileLst.append(file)
                else:
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(f'{fileName}{separator}\d*.{extension}', file):
                        fileLst.append(file)
            if (len(fileLst) == 1) and (fileLst[0] == f'{fileName}.{extension}'):
                finalName = exportPath + f'/{fileName}{separator}1' + f'.{extension}'
            else:
                maxNum = 0
                for filename in fileLst:
                    numberAtTheEnd_ext = re.search(fr'\d+.{extension}', filename)  # изтегля всички числа накрая заедно с ext
                    # ползвам го по този начин, защото може да има други числа в името, които не са накрая
                    if numberAtTheEnd_ext is not None:
                        numberAtTheEnd = re.findall(r'\d*', numberAtTheEnd_ext.group(0))  # изтеглям поредния номер на файла
                        if int(numberAtTheEnd[0]) > maxNum:
                            maxNum = int(numberAtTheEnd[0])
                maxNum = maxNum + 1
                finalName = exportPath + f'/{fileName}{separator}' + str(maxNum) + f'.{extension}'
        else:
            finalName = exportPath + f'/{fileName}' + f'.{extension}'
    else:
        separatorFirstHalf = separator[0]
        separatorSecondHalf = separator[1]
        specialChars = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', '\\']
        if os.path.exists(exportPath + fr"\{fileName}" + '.' + extension):
            fileLst = []
            for file in os.listdir(exportPath):
                if (separatorFirstHalf in specialChars) and (separatorSecondHalf in specialChars):
                    # когато разделителя е един от специалните
                    # символи трябва да се сложи \ преди променливата
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(fr'{fileName}\{separatorFirstHalf}\d*\{separatorSecondHalf}.{extension}', file):
                        fileLst.append(file)
                else:
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(fr'{fileName}{separatorFirstHalf}\d*{separatorSecondHalf}.{extension}', file):
                        fileLst.append(file)
            if (len(fileLst) == 1) and (fileLst[0] == f'{fileName}.{extension}'):
                finalName = exportPath + f'/{fileName}{separatorFirstHalf}1{separatorSecondHalf}' + f'.{extension}'
            else:
                maxNum = 0
                for filename in fileLst:
                    if (separatorFirstHalf in specialChars) and (separatorSecondHalf in specialChars):
                        numberAtTheEnd_ext = re.search(fr'\{separatorFirstHalf}\d+\{separatorSecondHalf}.{extension}', filename)  # изтегля всички числа накрая заедно с ext
                    # ползвам го по този начин, защото може да има други числа в името, които не са накрая
                    else:
                        numberAtTheEnd_ext = re.search(fr'{separatorFirstHalf}\d+{separatorSecondHalf}.{extension}', filename)  # изтегля всички числа накрая заедно с ext
                    if numberAtTheEnd_ext is not None:
                        numberAtTheEndLst = re.findall(r"\d*",numberAtTheEnd_ext.group())  # изтеглям поредния номер на файла
                        for ele in numberAtTheEndLst:
                            if ele != '':
                                numberAtTheEnd = ele
                        if int(numberAtTheEnd) > maxNum:
                            maxNum = int(numberAtTheEnd)
                maxNum = maxNum + 1
                finalName = exportPath + f'/{fileName}{separatorFirstHalf}' + str(maxNum) + f'{separatorSecondHalf}.{extension}'
        else:
            finalName = exportPath + f'/{fileName}' + f'.{extension}'
    return finalName

def createOutputA3A5(a3a5Path, label):
    label.setText('Reading A3A5 input file...')
    df_a3a5 = pd.read_excel(open(a3a5Path, 'rb'), header=None)
    result_a3a5 = pd.DataFrame(columns=['NR CELL', 'DN', 'Detected PCI', 'Count'])
    label.setText('Done.')
    label.setText('Formatting...')
    for k in range(len(df_a3a5)):
        matches = re.findall("NR-PCI = \d+ COUNT = \d+", df_a3a5.iloc[:, 8][k])
        nr_cell = df_a3a5.iloc[:, 1][k]
        dn = df_a3a5.iloc[:, 7][k]
        for i in range(len(matches)):
            numbers = re.findall("\d+", matches[i])
            tempDf = pd.DataFrame({'NR CELL': nr_cell,
                                   'DN': dn,
                                   'Detected PCI': int(numbers[0]),
                                   'Count': int(numbers[1])}, index=[0])
            result_a3a5 = pd.concat([result_a3a5, tempDf])
    result_a3a5.set_index('NR CELL', inplace=True, drop=True)
    result_a3a5.sort_values(["NR CELL", 'Count'], ascending=[False, False], inplace=True)
    label.setText('Done.')
    return result_a3a5

def createOutputDistance(cellsPath, result_a3a5, dist_threshold, c_threshold, label):
    label.setText('Reading 5G cells input file...')
    df_cells = pd.read_excel(open(cellsPath, 'rb'))
    label.setText('Done.')
    result_distance = pd.DataFrame(columns=['Src_SiteID',
                                            'Src_Cell_Name',
                                            'Src_PCI',
                                            'Src_TAC',
                                            'Tgt_PCI',
                                            '1st nearest Cell_Name',
                                            '1st nearest TAC',
                                            '1st nearest SiteID',
                                            'Dist 1st in km',
                                            '2nd nearest Cell_Name',
                                            '2nd nearest TAC',
                                            '2nd nearest SiteID',
                                            'Dist 2nd in km',
                                            'nth nearest Cell_Name|TAC|SiteID|Distance in km;'])
    df_cells = df_cells[['Cell_Name', 'PCI', 'SiteCode', 'TAC', 'Longitude', 'Latitude']]

    try:
        distance_threshold = int(dist_threshold)
    except:
        distance_threshold = 30
    try:
        count_threshold = int(c_threshold)
    except:
        count_threshold = 0

    label.setText("Modifying A3A5 result DF...")
    result_a3a5 = result_a3a5[result_a3a5.Count > count_threshold]
    result_a3a5.reset_index(inplace=True)
    result_a3a5 = result_a3a5.rename(columns={"NR CELL": "Cell_Name"})
    result_a3a5 = pd.merge(result_a3a5, df_cells[['Cell_Name', 'SiteCode', 'Longitude', 'Latitude', 'TAC', 'PCI']], on='Cell_Name', how='left')
    result_a3a5.reset_index(drop=True, inplace=True)
    label.setText("Done.")
    label.setText("Creating a GDF out of A3A5 result DF...")
    geometry = [Point(xy) for xy in zip(result_a3a5.Longitude, result_a3a5.Latitude)]
    gdf_a3a5 = gpd.GeoDataFrame(result_a3a5, geometry=geometry, crs="EPSG:4326")
    label.setText("Done.")
    if gdf_a3a5.isnull().values.any():
        label.setText("There are NaN values in the GDF, storing the xlsx file\n with NaN values in the 5G Cells DiR.")
        gdf_a3a5_NaN_Free = gdf_a3a5.dropna()
        only_NaN = gdf_a3a5[~gdf_a3a5.index.isin(gdf_a3a5_NaN_Free.index)]
        nanSitesPath = cellsPath.split('/')
        nanSitesPath.pop(-1)
        nanSitesPath = '\\'.join(nanSitesPath)
        nanSitesPath_Name = fileNamer(nanSitesPath, 'Missing Cells', 'xlsx')
        only_NaN.to_excel(nanSitesPath_Name)
    else:
        gdf_a3a5_NaN_Free = gdf_a3a5.copy()
    label.setText('Creating distance file...')
    missPCIdf = pd.DataFrame(columns=['PCI'])
    flagMissingCPI = False
    for ind, row in gdf_a3a5_NaN_Free.iterrows():
        detected_PCI = row['Detected PCI']
        main_cell_PCI = row['PCI']
        cell_name_main = row['Cell_Name']
        tac_main = row['TAC']
        main_point = row['geometry']
        src_id = row['SiteCode']

        tempDf = df_cells[df_cells.PCI == row['Detected PCI']]
        # tempDf = tempDf[tempDf.PCI == row['PCI']]
        if len(tempDf) == 0:
            flagMissingCPI = True
            temp_res_pci = pd.DataFrame({'Detected PCI': detected_PCI}, index=[0])
            missPCIdf = pd.concat([missPCIdf, temp_res_pci], ignore_index=True, axis=0)
            continue
        tempDf.reset_index(inplace=True, drop=True)
        geometry = [Point(xy) for xy in zip(tempDf.Longitude, tempDf.Latitude)]
        gdf_temp = gpd.GeoDataFrame(tempDf, geometry=geometry, crs="EPSG:4326")
        gdf_temp['Distance'] = None
        distances = []
        for ind2, row2 in gdf_temp.iterrows():
            secondary_point = row2['geometry']
            distance = main_point.distance(secondary_point)
            distances.append(distance)
        gdf_temp['Distance'] = distances
        #print(gdf_temp)
        minimal_distance = min(gdf_temp['Distance'])
        threshold_for_points = minimal_distance * distance_threshold / 100 + minimal_distance
        gdf_temp = gdf_temp[gdf_temp.Distance <= threshold_for_points]
        gdf_temp = gdf_temp[['Cell_Name', 'TAC', 'Distance', 'SiteCode']]
        gdf_temp.sort_values('Distance', ascending=True, inplace=True)
        gdf_temp.reset_index(inplace=True, drop=True)
        nthNearest = ''
        secondNearestCell_Name = ''
        secondNearestTAC = ''
        distanceSecond = ''
        secondSiteID = ''
        firstSiteID = gdf_temp.iloc[0, 3]
        firstNearestCell_Name = gdf_temp.iloc[0, 0]
        firstNearestTAC = gdf_temp.iloc[0, 1]
        distanceFirst = round(gdf_temp.iloc[0, 2]*100, 5)
        if len(gdf_temp) > 1:
            secondNearestCell_Name = gdf_temp.iloc[1, 0]
            secondNearestTAC = gdf_temp.iloc[1, 1]
            distanceSecond = round(gdf_temp.iloc[1, 2]*100,5)
            secondSiteID = gdf_temp.iloc[1, 3]
        if len(gdf_temp) > 2:
            leftoverDf = gdf_temp[gdf_temp.index >= 2]
            leftoverDf.reset_index(drop=True, inplace=True)
            for ind3, row3 in leftoverDf.iterrows():
                tempStr = str(row3['Cell_Name']) + '|' + str(row3['TAC']) + '|' + str(row3['SiteCode']) + '|' + str(round(row3['Distance']*100,3))
                nthNearest = nthNearest + '; ' + tempStr
        nthNearest = nthNearest[2::]
        temp_res = pd.DataFrame({'Src_SiteID':src_id,
                                'Src_Cell_Name':cell_name_main,
                                'Src_PCI':main_cell_PCI,
                                'Src_TAC':tac_main,
                                'Tgt_PCI':detected_PCI,
                                '1st nearest Cell_Name':firstNearestCell_Name,
                                '1st nearest TAC':firstNearestTAC,
                                '1st nearest SiteID':firstSiteID,
                                'Dist 1st in km':distanceFirst,
                                '2nd nearest Cell_Name':secondNearestCell_Name,
                                '2nd nearest TAC':secondNearestTAC,
                                '2nd nearest SiteID':secondSiteID,
                                'Dist 2nd in km':distanceSecond,
                                'nth nearest Cell_Name|TAC|SiteID|Distance in km;':nthNearest
                                }, index=[0])
        result_distance = pd.concat([result_distance, temp_res], ignore_index=True, axis=0)
    result_distance.set_index('Src_SiteID', inplace=True, drop=True)
    if flagMissingCPI is True:
        nanPCIPath = cellsPath.split('/')
        nanPCIPath.pop(-1)
        nanPCIPath = '\\'.join(nanPCIPath)
        nanPCIPath_Name = fileNamer(nanPCIPath, 'Missing PCI', 'xlsx')
        missPCIdf.drop_duplicates(inplace=True)
        missPCIdf.reset_index(inplace=True, drop = True)
        missPCIdf.to_excel(nanPCIPath_Name)
    label.setText('Done.')
    return result_distance
# cellsPath = 'C:\\Users\\a1bg511027\\Desktop\\5G_Cells.xlsx'
# resulta3a5 = pd.read_excel('C:\\Users\\a1bg511027\\Desktop\\a3a5\\A3A5_Result.xlsx')
# distance = createOutputDistance(cellsPath, resulta3a5, 30, 60000)
# distance.to_excel('C:\\Users\\a1bg511027\\Desktop\\res_dist.xlsx')
