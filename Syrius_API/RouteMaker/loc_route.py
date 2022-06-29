import math
import os
import sys


def LoadRouteSeed(self, file):
    data = fh.Yaml().Load(file)
    locations = {}
    routes = []
    if data == '':
        return locations, routes
    location_data = data['Locations']
    for key in location_data:
        locations[key] = ph.Pose(location_data[key])
    routes = data['Route']
    # TODO(shiyu) check file correctness
    return locations, routes


print(Loader().RouteSeed)

num_per_line = 7
picking_group_index_end = 40
main_road_group_index_start = 1001
extend_dis = 0


def GetPickingIndex(index):
    if index > picking_group_index_end:
        gap = main_road_group_index_start - picking_group_index_end - 1
        return gap + index
    return index


def ExtractPose(file, interpolate_num):
    pose = []
    extend_poses = []
    count = 0
    picking_index = 0
    for line in file.readlines():
        line = line.strip()
        start_pattern = 'received from rvizx: '
        start_index = line.find(start_pattern)
        if start_index >= 0:
            count = count + 1
            line = line[start_index + len(start_pattern): -1]
            line = line.replace('y:', '').replace(', ', '').replace('theta:', '')
            if count > 2 and count % 2 == 0 and interpolate_num > 0:
                [b1, b2, b3] = pose[-1].split(' ')
                [e1, e2, e3] = line.split(' ')
                xb = float(b1)
                yb = float(b2)
                tb = float(b3)
                xe = float(e1)
                ye = float(e2)
                dx = (xe - xb) / (interpolate_num + 1)
                dy = (ye - yb) / (interpolate_num + 1)
                # add extend pose
                if extend_dis > 0:
                    extend_ratio = extend_dis / math.sqrt(dx * dx + dy * dy)
                    picking_index = picking_index + 1
                    node = {'Extend_' + str('0000' + str(GetPickingIndex(picking_index)))[-4:] \
                                : [str(xb - dx * extend_ratio), str(yb - dy * extend_ratio), str(tb)]}
                    extend_poses.append(node)
                    picking_index = picking_index + interpolate_num + 1
                    node = {'Extend_' + str('0000' + str(GetPickingIndex(picking_index)))[-4:] \
                                : [str(xe + dx * extend_ratio), str(ye + dy * extend_ratio), str(tb)]}
                    extend_poses.append(node)
                for iters in range(0, interpolate_num):
                    xb = xb + dx
                    yb = yb + dy
                    pose.append(str(xb) + ' ' + str(yb) + ' ' + str(tb))
            pose.append(line)

    last = pose.pop()
    for i in range(0, interpolate_num):
        pose.pop()
    pose.append(last)
    return pose, extend_pose


# main start here
path = os.getcwd()
f = open(str(sys.argv[1]), 'r')
(poses, extend_poses) = ExtractPose(f, num_per_line - 2)
print(extend_poses)
PICKING_POINT_NUM = len(poses) - 3
standby_id = ['0001']
bind_id = ['0001']
POI = []
index_gap = main_road_group_index_start - picking_group_index_end - 1
for i in range(1, PICKING_POINT_NUM + 1):
    num = i
    if i > picking_group_index_end:
        num = i + index_gap
    POI.append(str('PICKING_000' + str(num))[-4:])
unbind_id = ['0001']
AddPrefixForAll(standby_id, bind_id, POI, unbind_id)
route_names = standby_id + bind_id + POI + unbind_id

location = MatchPoseWithRouteName(poses, route_names)

mode = str(sys.argv[2])
print('mode', mode)
unbind_start_index = len(route_names) - 2
route_names[unbind_start_index] = 'UNBIND_START_POINT'
node = {'UNBIND_START_POINT': list(location[unbind_start_index].values())[0]}
location[unbind_start_index] = node
if mode[0:5] == 'snake':
    path = GenerateSnakePathRoute(route_names)
elif mode == 'gogopick':
    path = GenerateGoGoPick(route_names)
else:
    print('Unknonwn Point')
print(location[1:5])
print(extend_poses[1:5])
file = YamlFileFormatter(location, extend_poses, path)
out = open('locations.yaml', 'w')
out.write(file)
print("--------------------------------File preview--------------------------------")
# print(file)
