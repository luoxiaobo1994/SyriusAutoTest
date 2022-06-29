import matplotlib.pyplot as plt
import numpy as np

kFont = {'fontsize': 6}  # , 'fontweight': 'bold'}


class Point:
    def __init__(self, point):
        if len(point) == 0:
            self.x = self.y = 0.0
            self.valid = False
            return
        self.valid = True
        self.x = point[0]
        self.y = point[1]

    def Valid(self):
        return self.valid

    def Dis(self, rhs):
        return np.hypot(self.x - rhs.x, self.y - rhs.y)

    def Diff(self, rhs, div=1.0):
        return Point([(rhs.x - self.x) / div, (rhs.y - self.y) / div])

    def Plus(self, rhs):
        return Point([self.x + rhs.x, self.y + rhs.y])

    def GetDir(self, target):
        return np.arctan2(target.y - self.y, target.x - self.x)

    def GetStep(self, angle, dis):
        dx = np.cos(angle) * dis
        dy = np.sin(angle) * dis
        return Point([dx, dy])

    def Show(self):
        return "[{:.2f}, {:.2f}]".format(self.x, self.y)

    def CopyPos(self, point):
        self.valid = True
        self.x = point.x
        self.y = point.y

    def SetXY(self, coor):
        self.valid = True
        self.x = coor[0]
        self.y = coor[1]

    def Draw(self, attr):
        plt.plot(self.x, self.y, attr)

    def Del(self):
        self.Draw('.w')

    def Move(self, point, attr):
        self.Del()
        point.Draw(attr)
        self.CopyPos(point)

    def ShowName(self, text, font=kFont):
        plt.text(self.x, self.y, text, fontdict=font)

    def DrawLine(self, point, color):
        x = [self.x, point.x]
        y = [self.y, point.y]
        plt.plot(x, y, color)

    def DrawArrow(self, point, color):
        plt.arrow(self.x, self.y, point.x - self.x, point.y - self.y, length_includes_head=True,
                  head_width=0.2, head_length=0.1, fc=color, ec=color)

    def ToArray(self):
        return [self.x, self.y]


class Pose(Point):
    x = y = yaw = 0.0
    valid = False

    def __init__(self, pose):
        if len(pose) != 0:
            self.valid = True
            self.x = pose[0]
            self.y = pose[1]
            self.yaw = pose[2]

    def Extend(self, dis):
        step = self.GetStep(self.yaw, dis)
        return Pose([step.x + self.x, step.y + self.y, self.yaw])

    def Show(self):
        return "[{:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y, self.yaw)

    def ToArray(self):
        return [self.x, self.y, self.yaw]

    def Plus(self, rhs):
        return Pose([self.x + rhs.x, self.y + rhs.y, self.yaw])

    def CopyPos(self, pose):
        self.valid = True
        self.x = pose.x
        self.y = pose.y
        self.yaw = pose.yaw

    # TODO(shiyu) draw function
    def Draw(self, attr='lawngreen'):
        step = self.GetStep(self.yaw, 0.2)
        plt.arrow(self.x, self.y, step.x, step.y, length_includes_head=True,
                  head_width=0.2, head_length=0.1, fc=attr, ec=attr)

    def Del(self):
        self.Draw('w')

    def Move(self, pose, attr):
        self.Del()
        pose.Draw(attr)
        self.CopyPos(pose)


def Test():
    start = Point([0, 0])
    target = Point([1, 1])
    print(start.GetDir(target))
    print(target.Show())
    pose = Pose([0, 0, 0])
    print(pose.Extend(1.0).Show())


if __name__ == "__main__":
    Test()
