import matplotlib.pyplot as plt
import file_helper as fh
import pose_helper as ph
from PIL import Image

class Trans:
  # o -> origin, origin at left-bottom, x grows right, y grows up
  # k -> resolution
  ox = oy = kx = ky = 0.0
  def Valid(self):
    if self.kx == 0.0 or self.ky == 0.0:
      return False
    else:
      return True
  # def PicToCoor(self, coor):
  #   x = coor[0] * self.kx - self.ox
  #   y = coor[1] * self.ky - self.oy
  #   return ph.Point([x, y])
  def ConvertToExtent(self, size):
    # size [y(vertical), x(horizon)]
    lb = [self.oy, self.ox]
    dx = size[1] * self.kx
    dy = size[0] * self.ky
    return [lb[1], lb[1] + dy, lb[0], lb[0] + dx]
  def Show(self):
    print('origin:{:2f}, {:2f}, resolution: {:2f}, {:2f}'.\
      format(self.ox, self.oy, self.ky, self.kx))

def ShowMap(map_file, tras_obj = None):
  img = Image.open(map_file)
  img = img.transpose(Image.FLIP_TOP_BOTTOM)
  if tras_obj == None:
    plt.imshow(img, plt.cm.get_cmap('gray'), origin='lower')
  else:
    plt.imshow(img, plt.cm.get_cmap('gray'), origin='lower', \
      extent = tras_obj.ConvertToExtent(img.size))

class Ax:
  def DrawLine(self, start, end, attr):
    dx = [start.x, end.x]
    dy = [start.y, end.y]
    ax = plt.gca()
    lines = ax.plot(dx, dy, attr)
    ax.figure.canvas.draw()
    l = lines.pop(0)
    l.remove()
    del l
# def DrawPoint(coor, attr):
#   plt.plot(coor[0], coor[1], attr)

# def MovePoint(old_coor, new_coor, attr):
#   DrawPoint(old_coor, '.w')
#   DrawPoint(new_coor, attr)

# def DrawLine(x, y, attr):
#   plt.plot(x, y, attr)

# def PutText(pose, text):
#   plt.text(pose.x, pose.y, text)
