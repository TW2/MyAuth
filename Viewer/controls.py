import wx

class Button(wx.Rect):
    r_btn = wx.Rect
    r_img = ''

    # Constructeur de la classe
    def __init__(self, x, y, image_src):
        self.r_btn = wx.Rect.__init__(self, x, y, 32, 32)
        self.r_img = image_src

    def Contains(self, x, y) -> bool:
        xa = self.r_btn.x
        ya = self.r_btn.y
        wa = self.r_btn.width
        ha = self.r_btn.height
        
        is_in_x = True if(xa <= x and x <= xa + wa) else False
        is_in_y = True if(ya <= y and y <= ya + ha) else False
        return is_in_x == True and is_in_y == True
    
    def GetImage(self):
        return 'resources/images/%s' % self.r_img