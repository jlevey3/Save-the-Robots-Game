"""
For all of the animation goodies that may come into play
"""

from tools import load_image

def draw_background(self, surf):
    tw, th = self.bg_tile.get_size()
    sw, sh = surf.get_size()

    for y in range(0, sh, th):
        for x in range(0, sw, tw):
            surf.blit(self.bg_tile, (x,y))


#####################################################
#animations
class AnimationFrames(object):
    def __init__(self, frames, loops=-1):
        self._times = []
        self._data = []
        total = 0
        for t, data in frames:
            total += t
            self._times.append(total)
            self._data.append(data)

        self.end = total
        self.loops = loops
            

    def get(self, time):
        # if looping forever or within the number of loops, wrap time
        if self.loops == -1 or time < self.loops * self.end:
            time %= self.end
       
        # return last frame if we've gone too far
        if time > self.end:
            return self._data[-1]
        
        # otherwise loop until we get the right frame
        idx = 0
        while self._times[idx] < time:
            idx += 1

        return self._data[idx]




class Animation(object):
    def __init__(self, spritesheet, frames):
        if not isinstance(frames, AnimationFrames):
            frames = AnimationFrames(frames)

        self.spritesheet = spritesheet
        self.frames = frames
        self.time = 0
        self.update(0)

    def get_frame_data(self, time):
        return self.frames.get(time)

    def get_current_frame(self):
        return self.spritesheet.get(self.x, self.y)

    def update(self, dt):
        self.time += dt
        self.x, self.y = self.get_frame_data(self.time)




class SpriteSheet(object):
    def __init__(self, image, dimensions, colorkey=-1):

        # load the image
        if type(image) is str:
            image = load_image(image)

        if colorkey == -1:
            colorkey = image.get_at((0,0))
            
        if colorkey:
            image.set_colorkey(colorkey)

        cols, rows = dimensions
        w = self.width = 1.0 * image.get_width() / cols
        h = self.height = 1.0 * image.get_height() / rows

        # build the images
        self._images = []
        for y in range(rows):
            row = []
            for x in range(cols):
                row.append(image.subsurface((x*w, y*h, w, h)))
            self._images.append(row)

    def get(self, x, y):
        return self._images[y][x]