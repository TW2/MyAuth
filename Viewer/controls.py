import wx

class Button():
    r_btn = wx.Rect()
    r_img = None

    # Constructeur de la classe
    def __init__(self, x, y, image_src):
        self.r_btn = wx.Rect(x, y, 32, 32)
        self.r_img = image_src

    def Contains(self, x, y) -> bool:
        xa = self.r_btn.GetX()
        ya = self.r_btn.GetY()
        wa = self.r_btn.GetWidth()
        ha = self.r_btn.GetHeight()
        
        is_in_x = True if(xa <= x and x <= xa + wa) else False
        is_in_y = True if(ya <= y and y <= ya + ha) else False
        return is_in_x == True and is_in_y == True
    
    def GetImage(self):
        return 'resources/images/%s' % self.r_img
    
    def GetX(self) -> int:
        return self.r_btn.GetX()
    
    def GetY(self) -> int:
        return self.r_btn.GetY()
    
    def GetWidth(self) -> int:
        return self.r_btn.GetWidth()
    
    def GetHeight(self) -> int:
        return self.r_btn.GetHeight()