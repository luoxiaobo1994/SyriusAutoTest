import sys

import matplotlib.pyplot as plt

import pose_helper as ph
import route_helper as rh
import route_manager


class Mode:
    ADD_POINT = 1
    UPDATE_POINT = 2
    CONNECT_POINT = 3

    def Print(self, mode):
        print('change mode to :', mode)


kMaxClickDis = 0.2
location_file_name = 'locations.yaml'
mode = Mode().ADD_POINT


def EventPoint(event):
    return ph.Point([event.xdata, event.ydata])


def EventPose(event, pre_point):
    return ph.Pose([pre_point.x, pre_point.y, \
                    pre_point.GetDir(EventPoint(event))])


def ShowModeInfo(msg='', msg2=''):
    global mode, text0, fig
    if mode == Mode().ADD_POINT:
        text0.set_text('AddMode - please set: ' + msg)
    elif mode == Mode().UPDATE_POINT:
        text0.set_text('UpdateMode - current selected: ' + msg)
    elif mode == Mode().CONNECT_POINT:
        text0.set_text('ConnectMode : {} -> {}'.format(msg, msg2))
    fig.canvas.draw_idle()


def FindNearestLocation(xy, locations):
    min_dis = 100
    for location_key in locations:
        eular_dis = xy.Dis(locations[location_key])
        if eular_dis < min_dis:
            min_dis = eular_dis
        if eular_dis < kMaxClickDis:
            print(location_key)
            return location_key
    return ''


def OnClick(event):
    global LeftClickXY, RightClickXY
    global location_key
    global rm
    if event.button == 1:
        LeftClickXY = EventPoint(event)
        location_key = FindNearestLocation(LeftClickXY, rm.locations)
        ShowModeInfo(location_key)
    if event.button == 3:
        RightClickXY = EventPoint(event)
        location_key = FindNearestLocation(RightClickXY, rm.locations)


def OnMouseMotion(event):
    pass
    # if event.button == 3:
    #   painter.Ax().DrawLine(RightClickXY, EventPoint(event), 'b')


def OnRelease(event):
    global LeftClickXY
    global location_key, end_key
    global mode
    global rm
    # delete old point
    if event.button == 1:
        if mode == Mode().UPDATE_POINT:
            if location_key == '':
                return
            rm.locations[location_key].Move(EventPoint(event), '.b')
            ShowModeInfo(location_key)
        elif mode == Mode().ADD_POINT:
            new_pose = EventPose(event, LeftClickXY)
            print(new_pose.Show())
            print('current_index= ', rm.SetPoseAndGoNext(new_pose))
            new_pose.Draw()
            ShowModeInfo(rm.GetName())
    if mode == Mode().CONNECT_POINT:
        if location_key == '': return
        end_point = EventPoint(event)
        end_key = FindNearestLocation(end_point, rm.locations)
        if end_key == '' or location_key == end_key: return
        ShowModeInfo(location_key, end_key)
        if event.button == 1:
            if rm.routes.count([location_key, end_key]) == 0:
                rm.routes.append([location_key, end_key])
                rm.locations[location_key].DrawLine(rm.locations[end_key], 'yellow')
        elif event.button == 3:
            rm.routes.remove([location_key, end_key])
            rm.locations[location_key].DrawLine(rm.locations[end_key], 'w')
    plt.show()


def Refresh(folder):
    global rm, text0
    locations, routes, trans = rh.Load(folder)
    text0 = plt.text(trans.ox - 1, trans.oy - 2, '', fontsize=8)
    ShowModeInfo(rm.GetName())
    rm.locations = locations.copy()
    if len(routes) > 0:
        rm.routes = routes.copy()
    return trans


def OnKeyDown(event):
    global folder, location_key, end_key
    global mode
    global rm
    input_key = event.key.lower()
    if input_key == 'v':
        if mode == Mode().ADD_POINT or mode == Mode().CONNECT_POINT:
            locations = rm.locations.copy()
            new_locations = rm.Convert()
            if new_locations is not None:
                for key in new_locations:
                    locations[key] = ph.Pose(new_locations[key].ToArray())
            else:
                print('new locations is none')
            rm.locations = locations.copy()
            rh.Save(rm.locations, rm.routes, folder, location_file_name)
        elif mode == Mode().UPDATE_POINT:
            rh.Save(rm.locations, rm.routes, folder, location_file_name)
        print("Saving result")
        plt.cla()
        Refresh(folder)
        plt.show()
    elif input_key == 'l':
        plt.cla()
        Refresh(folder)
        plt.show()
    elif input_key == 'a':
        # add
        mode = Mode().ADD_POINT
        Mode().Print('ADD_POINT')
        ShowModeInfo()
    elif input_key == 'm':
        # modify
        mode = Mode().UPDATE_POINT
        Mode().Print('UPDATE_POINT')
        ShowModeInfo()
    elif input_key == 'c':
        # modify
        mode = Mode().CONNECT_POINT
        Mode().Print('CONNECT_POINT')
        ShowModeInfo()
    elif input_key == 'd':
        #  delete
        if mode == Mode().UPDATE_POINT:
            if location_key != '':
                rm.locations[location_key].Del()
                rm.locations.pop(location_key)
                location_key = ''


fig = plt.figure()
folder = str(sys.argv[1])
rm = route_manager.RouteManager()
rm.LoadRouteSeed(folder)
trans = Refresh(folder)
if rm.Valid():
    print(len(rm.seeds), ' Poses needed ', rm.PrintSeed(full_log=False))
mode = Mode().ADD_POINT
fig.canvas.mpl_connect('button_press_event', OnClick)
fig.canvas.mpl_connect('button_release_event', OnRelease)
fig.canvas.mpl_connect('key_press_event', OnKeyDown)
fig.canvas.mpl_connect('motion_notify_event', OnMouseMotion)
plt.show()
