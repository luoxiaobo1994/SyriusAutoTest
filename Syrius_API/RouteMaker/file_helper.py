import sys
import json
import yaml
import csv
import xlrd
import time
def GetTime():
  t = time.localtime(time.time())
  return '{}{}{}-{}:{}:{}'.format(t.tm_year, \
     t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

class JsonClass:
  def ToJsonStr(self):
    return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False)

  def FromJsonStr(self, json_string):
    data = json.loads(json_string)
    for key in self.__dict__.keys():
      setattr(self, key, data[key])

class LocationList(JsonClass):
  locations = None
  def add(self, binLocation, mapLocation):
    self.locations[binLocation] = mapLocation
  def __init__(self):
    self.locations = {}

class Yaml:
  def Load(self, file_name):
    try:
      file = open(file_name, 'r', encoding='utf-8')
      file_data = file.read()
      file.close()
      return yaml.load(file_data, Loader=yaml.FullLoader)
    except Exception:
      print(file_name + ' File Not Exists')
      return ''
  def HeaderDumper(self, header):
    res = ''
    space = ''
    if header != None:
      res += header + ':\n'
      space += '  '
    return res, space
  def MapDumper(self, data, header = None):
    res, space = self.HeaderDumper(header)
    for key in sorted(data.keys()):
      l = data[key]
      if len(l) == 0:
        continue
      res += space + key + ': [' + ', '\
          .join(['{:.4f}'.format(float(x)) for x in l]) + ']\n'
    return res
  def ArrayDumper(self, data, header = None):
    res, space = self.HeaderDumper(header)
    for item in data:
      res += space + '- [' + ', '\
          .join([str(x) for x in item]) + ']\n'
    return res


def LoadCsv(filePath, columns, format):
  try:
    csvFile = open(filePath, 'r', encoding=format)
    csvReader = csv.reader(csvFile)
    # next(csvReader)  # remove first line(header)
    data = []
    for row in csvReader:
      data_col = []
      for col in columns:
        try:
          data_col.append(row[col])
        except Exception:
          pass
      if data_col != []:
        data.append(data_col)
    csvFile.close()
    return data
  except Exception:
    pass

def LoadCsvDefault(filePath, columns):
  return LoadCsv(filePath, columns, 'utf-8')

def LoadExcel(filePath, sheet_index = 0):
  try:
    wb = xlrd.open_workbook(filePath)
    names = wb.sheet_names()
    if not sheet_index < len(names):
      print(__name__, 'sheet index overflow')
      return ''
    table = wb.sheets()[sheet_index]
    table.dropna()
    rows = table.nrows
    columns = table.ncols
    print("execl rows: %s, columns:%s" % (rows, columns))
    return table
  except Exception:
    print('No such file:', filePath)
    return ''

def WriteToFile(path, data):
  f = open(path, "w")
  f.write(data)
  f.close()

def WriteCsv(path, data, header):
  f = open(path, 'w',encoding='utf-8', newline='')
  new_csv = csv.writer(f)
  new_csv.writerow(header)
  new_csv.writerows(data)
  f.close()

def main(argv):
  if len(sys.argv) < 2:
    print("please input product_image_data filepath!")
  else:
    data = LoadCsvDefault(argv[1], [0,1])
    print(data)


if __name__ == '__main__':
  main(sys.argv)
