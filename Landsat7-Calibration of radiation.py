from osgeo import gdal
import re



def rad_cai():
    '''辐射定标参数'''
    # 读取'MTL.txt'内容
    global banddata, RaCalRaster
    with open(r'D:\mapdata\landsat-07\1\LE07_L1TP_121029_20070404_20170104_01_T1_MTL.txt') as f:
        content = f.read()
    # 利用正则表达式匹配参数
    global gain, bias
    gain = re.findall(r'RADIANCE_MULT_BAND_\d\s=\s(\S*)', content)
    bias = re.findall(r'RADIANCE_ADD_BAND_\d\s=\s(\S*)', content)
    del gain[6], bias[6]
    return gain, bias


def readtifname():
    input_path = r'D:\mapdata\landsat-07\1\LE07_L1TP_121029_20070404_20170104_01_T1'
    TIFfile = []
    for i in range(7):
        band_name = input_path + "_B" + str(i + 1) + ".TIF"
        if i == 5:
            continue
        TIFfile.append(band_name)
    return TIFfile


if __name__ == '__main__':
    readtiffile = readtifname()
    i = 0
    for file in readtiffile:
        dataset = gdal.Open(file,gdal.GA_ReadOnly)
        databand = dataset.GetRasterBand(1)
        cols, rows = dataset.RasterXSize, dataset.RasterYSize
        dataArray = databand.ReadAsArray(0, 0, cols, rows)
        parameters1, parameters2 = rad_cai()
        RaCalRaster = dataArray * float(parameters1[i]) + float(parameters2[i])
        # 设置驱动输出文件路径及名字
        driver=gdal.GetDriverByName('GTiff')
        outputfile = driver.Create(r'D:\mapdata\landsat-07\4\\' + str(i + 1) + '.TIF', cols, rows, 1, 6)
        # 设置投影和地理变换
        Trans = dataset.GetGeoTransform()
        outputfile.SetGeoTransform(Trans)
        Proj = dataset.GetProjection()
        outputfile.SetProjection(Proj)
        # 把辐射定标数据写入输出文件
        outband = outputfile.GetRasterBand(1)
        outband.WriteArray(RaCalRaster)
        #print('{}辐射定标完成'.format(file))
        if i == 7:
            break
        print(i)
        i+=1
