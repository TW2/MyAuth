import wx

class MyRect():
    rect = wx.Rect()
    
    image: str = None
    media: str = None
    title: str = None
    title_X = 'center'
    title_Y = 'bottom'

    def __init__(self, x=0, y=0, width=0, height=0):
        self.rect = wx.Rect(x, y, width, height)

    def GetMedia(self) -> str:
        return "resources/videos/%s" % self.media

    def SetMedia(self, media: str):
        self.media = media

    def GeTitle(self) -> str:
        return self.title

    def SetTitle(self, title: str):
        self.title = title

    def GetImage(self) -> str:
        return "resources/images/%s" % self.image

    def SetImage(self, image: str):
        self.image = image

    def GetTextLocationX(self):
        return self.title_X
    
    def SetTextLocationX(self, title_X):
        self.title_X = title_X
    
    def GetTextLocationY(self):
        return self.title_Y
    
    def SetTextLocationY(self, title_Y):
        self.title_Y = title_Y

    def Contains(self, x, y) -> bool:
        xa = self.rect.x
        ya = self.rect.y
        wa = self.rect.width
        ha = self.rect.height

        is_in_x = True if(xa <= x and x <= xa + wa) else False
        is_in_y = True if(ya <= y and y <= ya + ha) else False
        return is_in_x == True and is_in_y == True


class Handler():

    rects = []
    sel = MyRect()
    count = 0

    def __init__(self):
        self.rects = []
        self.sel = MyRect()
        self.count = 0

    def Add(self, r: MyRect):
        self.rects.append(r)
        self.count+=1

    def ItemsCount(self) -> int:
        return self.count

    def GetItem(self, i) -> MyRect:
        return self.rects[i]

    def GetSelected(self, x, y) -> MyRect:
        i=0
        while(i<self.ItemsCount()):
            r = self.GetItem(i)
            if(r.Contains(x, y)):
                return r
            i+=1
        return None
    