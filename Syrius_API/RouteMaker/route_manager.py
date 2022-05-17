import os
import yaml
import sys
import math
import file_helper as fh
import pose_helper as ph
location_seed_file = 'location_seed.csv'
route_seed_file = 'route_seed.csv'
def Debug(frame, obj):
  return
  # print(str(frame.f_lineno), obj)
def GetSuffix(name, index = -4):
  return name[index:]
def GetPreFix(name, index = -4):
  return name[:index]
def Bind(name, num, len = 4):
  return name + ('000' + str(num))[-4:]

class Seed:
  # seed is the locations generator
  # input file format as csv
  def __init__(self, name, has_pre = False):
    # TODO(shiyu) make this as pose
    self.name = name
    self.pose = ph.Pose([])
    self.has_pre = has_pre
  def Copy(self, rhs):
    self.name = rhs.name
    self.pose.CopyPos(rhs.pose)
    self.has_pre = rhs.has_pre
  def Valid(self):
    return self.name != '' and self.pose.Valid()
  def SetName(self, name):
    self.name = name
  def SetPos(self, coor):
    self.pose.SetXY(coor)
  def Show(self):
    if self.has_pre:
      return self.name + '(Continue):' + self.pose.Show()
    else:
      return self.name + ':' + self.pose.Show()

class RouteGenerator:
  def RepeatRule(self, start, target, num):
    routes = []
    start_name = GetPreFix(start)
    start_num = int(GetSuffix(start))
    target_name = GetPreFix(target)
    target_num = int(GetSuffix(target))
    for i in range(0, num):
      routes.append([Bind(start_name, start_num + i), \
              Bind(target_name, target_num + i)])
    return routes
  def CrossingRule(self, start, start_i, target, target_i):
    # TODO(shiyu)
    return []
  def SimpleRule(self, start, target):
    routes = []
    routes.append()
    return routes
  def Load(self, data):
    routes = []
    if data == '':
      print('RouteManager loaded nothing')
      return routes
    data = data[1:]
    for row in data:
      start = row[0].strip()
      target = row[1].strip()
      repeat = row[2].strip()
      crossing = row[3].strip()
      if repeat != '':
        routes = routes + self.RepeatRule(start, target, int(repeat))
      elif crossing != '':
        nums = crossing.split(',')
        routes = routes + \
            self.CrossingRule(start, target, int(nums[0]), int(nums[1]))
      else:
        routes.append([start, target])
      print(row)
    print('Generate routes: ', routes)
    return routes

class RouteManager:
  def __init__(self):
    self.index = 0
    self.seeds = []
    self.locations = {}
    self.names = []
  def Valid(self):
    return len(self.seeds) > 0
  def ValidIndex(self, index):
    return index >= 0 and index < len(self.seeds)

  def LoadRouteSeed(self, folder):
    print('Load ' + location_seed_file)
    data = fh.LoadCsvDefault(folder + '/' + location_seed_file, [0, 1])
    if data == '' or data == None:return ''
    data = data[1:]
    for row in data:
      for i in range(0, len(row)):
        if row[i] != '':
          self.seeds.append(Seed(row[i], has_pre=(i != 0)))
    Debug(sys._getframe(), 'Loaded ' + str(len(self.seeds)))
    # Load route seed
    self.routes = RouteGenerator().Load(
        fh.LoadCsvDefault(folder + '/' + route_seed_file, [0,1,2,3]))
    return data

  def PrintSeed(self, full_log = True):
    msg = []
    for seed in self.seeds:
      if full_log:
        msg.append(seed.Show())
      else:
        msg.append(seed.name)
    return msg

  def SetPose(self, pose, index =-1):
    if index == -1:
      index = self.index
    if self.ValidIndex(index):
      self.seeds[index].pose.CopyPos(pose)

  def GetName(self, index = -1):
    if index == -1:
      index = self.index
    if not self.ValidIndex(index):
      return ''
    return self.seeds[index].name

  def Previous(self):
    if self.index > 0:
      self.index = self.index - 1
    return self.index
  def Next(self):
    if self.index < len(self.seeds):
      self.index = self.index + 1
    return self.index
  def SetPoseAndGoNext(self, pose):
    self.SetPose(pose)
    return self.Next()

  def Convert(self):
    # convert seed to locations
    self.locations = {}
    self.names = []
    if not self.Valid():
      return
    pre_seed = Seed('dummy')
    for seed in self.seeds:
      Debug(sys._getframe(), seed.name)
      if not seed.Valid():
        Debug(sys._getframe(), 'Seed ' + seed.name + ' is NOT set!!!!!!!!!!')
        continue
      if not seed.has_pre:
        self.names.append(seed.name)
        self.locations[seed.name] = ph.Pose(seed.pose.ToArray())
      else:
        # interpolate
        base_name = pre_seed.name[0:-4]
        start_i = int(GetSuffix(pre_seed.name))
        end_i = int(GetSuffix(seed.name))
        if start_i >= end_i:
          Debug(sys._getframe(), pre_seed.name + ' has Equal/Greater suffix with ' + seed.name)
          print(pre_seed.Show())
          print(seed.Show())
          sys.exit(0)
        step = pre_seed.pose.Diff(seed.pose, end_i - start_i)
        # TODO(shiyu) make pose
        pose = ph.Pose(pre_seed.pose.ToArray())
        Debug(sys._getframe(), seed.pose.Show())
        Debug(sys._getframe(), pose.Show())
        for i in range(start_i + 1, end_i + 1):
          pose = pose.Plus(step)
          new_name = Bind(base_name, i)
          self.names.append(new_name)
          self.locations[new_name] = ph.Pose(pose.ToArray())
      pre_seed.Copy(seed)
    return self.locations

def Test(file):
  rm = RouteManager()
  Debug(sys._getframe(), rm.LoadRouteSeed(file))
  for i in range(0, len(rm.seeds)):
    rm.SetPoseAndGoNext(ph.Pose([i, i, 1]))
  Debug(sys._getframe(), rm.PrintSeed())
  rm.Convert()
  for key in rm.names:
    print(key, rm.locations[key].Show())

def TestName():
  test_name = 'PICKING_0001'
  print(GetPreFix(test_name))
  print(GetSuffix(test_name))

if __name__ == "__main__":
  file = 'test_map'
  TestName()
  Test(file)
  # Test(sys.argv[1])

