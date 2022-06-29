#!/usr/bin/python3
import os
import sys

import matplotlib.pyplot as plt
import yaml

import file_helper as fh
import painter
import pose_helper as ph

need_origin_file_backup = True


def IsSub(strA, strB):
  return strA.find(strB) > -1


class Display:
  def ColorSelector(self, start_name, end_name):
    kMainRoadPrefix = 'PICKING_1'
    kPickingPrefix = 'PICKING_0'
    color = 'b'  # default to blue
    if IsSub(end_name, kMainRoadPrefix):
      # green for all route end with main route
      color = 'c'
    elif IsSub(end_name, kPickingPrefix):
      # main to picking
      color = 'r'
    elif IsSub(start_name, kPickingPrefix) \
            and IsSub(end_name, kPickingPrefix):
      color = 'yellow'
    return color

  def ShortName(self, name):
    return name.replace('QPICKING_', 'Q').replace('PICKING_', 'P') \
      .replace('STANDBY_', 'S').replace('MAIN_', 'M')

  def Show(self, locations, routes, show_text=False):
    for key in locations:
      locations[key].Draw()
      if show_text:
        locations[key].ShowName(self.ShortName(key))
    for loc_pair in routes:
      start_name = loc_pair[0]
      end_name = loc_pair[1]
      locations[start_name].DrawArrow(
        locations[end_name], self.ColorSelector(start_name, end_name))


class Loader():
  def LoadLocationFile(self, file):
    data = fh.Yaml().Load(file)
    locations = {}
    routes = []
    if data == '':
      return locations, routes
    location_data = data['Locations']
    for key in location_data:
      locations[key] = ph.Pose(location_data[key])
    routes = data['Route']
    if routes == None:
      routes = []
    # TODO(shiyu) check file correctness
    return locations, routes

  def LoadTransFile(self, file):
    data = fh.Yaml().Load(file)
    trans = painter.Trans()
    trans.kx = trans.ky = data['resolution']
    trans.ox = data['origin']['x']
    trans.oy = data['origin']['y']
    trans.Show()
    return trans

  def ReservePartial(self, file, keys=['Weights', 'AreaResource']):
    data = fh.Yaml().Load(file)
    reserve = {}
    for key in data.keys():
      if key in keys:
        reserve[key] = data[key]
        print(key)
    if reserve == {}:
      return ''
    else:
      return yaml.dump(reserve, Dumper=yaml.Dumper)


################ key functions ###############
def Load(folder, loc_path=None):
  root = str(folder) + '/'
  location_file = root + "locations.yaml"
  if loc_path != None:
    location_file = root + loc_path
  trans = Loader().LoadTransFile(root + "global_map.yaml")
  painter.ShowMap(root + "global_map.pgm", trans)
  locations, routes = Loader().LoadLocationFile(location_file)
  Display().Show(locations, routes, True)
  return locations, routes, trans


def Save(locations, route, folder, loc_path):
  global need_origin_file_backup
  root = str(folder) + '/'
  location_file = root + loc_path
  text = ''
  if os.path.exists(location_file):
    text = Loader().ReservePartial(location_file)
    if need_origin_file_backup:
      history_folder = root + 'history'
      if not os.path.exists(history_folder):
        os.mkdir(history_folder)
      os.rename(location_file, history_folder + '/' + fh.GetTime() + '_' + loc_path)
      need_origin_file_backup = False
  loc2d = {}
  for key in locations.keys():
    loc2d[key] = locations[key].ToArray()
  loc = fh.Yaml().MapDumper(loc2d, 'Locations')
  route = fh.Yaml().ArrayDumper(route, 'Route')
  text = loc + '\n' + route + '\n' + text
  fh.WriteToFile(location_file, text)


if __name__ == '__main__':
  locations, route, trans = Load(str(sys.argv[1]))
  Save(locations, route, str(sys.argv[1]), 'loc.yaml')
  plt.show()
