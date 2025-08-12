import wx
import vlc
import yaml
import rect
import sys

from os.path import basename, isfile
from enum import Enum

# Python 3
unicode = str

class Status(Enum):
    StandBy = 1 # File is set, waiting for initialization or Stop
    Load = 2 # File is set and initialized
    Play = 3 # Play
    Pause = 4 # Pause

# =========================================================================
# == FRAME ================================================================
# =========================================================================
# Ma classe pour afficher le menu
class MyAuthViewer(wx.Frame):

    my_frame = None # This frame
    my_panel = None # The CD/DVD/BluRay/USB/SSD/HDD menu
    my_video = None
    config = None # Dictionnaire
    sel_handler = rect.Handler()

    # The last selected rect.MyRect item
    last_sel = None
    # The last selected video path, actually the played one
    # When no play then None
    last_play = None
    # The state determinate status for the vlc element
    last_play_state = Status.StandBy

    mouse_x = -100
    mouse_y = -100
    
    # Constructeur de la classe
    def __init__(self):
        self.my_frame = wx.Frame.__init__(self, None, -1, 'wxVLC', pos=wx.DefaultPosition, size=(550, 500))        
        
        # On vient ouvrir et remplir notre dictionnaire
        self.LoadMenu()

        ####################
        ###########---------
        # Menu - Panel -----
        ###########---------
        ####################
        self.my_panel = wx.Panel(self, -1)
        self.my_panel.SetDoubleBuffered(True) # To stabilize image rendering in paint
        self.my_panel.SetBackgroundColour(wx.BLACK)
        self.my_panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.my_panel.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)
        self.my_panel.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.my_panel.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        self.my_video = wx.Panel(self.my_panel, -1)
        self.my_video.SetSize(0, 0)
        self.my_video.SetBackgroundColour(wx.BLACK)
        self.my_video.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

    # ---------------------------------------------------------------------------------

    def OnPaint(self, event):        
        pdc = wx.PaintDC(self.my_panel)
        gc = wx.GCDC(pdc)
        gc.Clear()
        
        # ----------------
        # Fond de l'écran
        # ----------------

        gc.DrawBitmap(wx.Bitmap("resources/images/%s" % self.config['main_config']['image']), 0, 0, True)

        # ----------------
        # Accès aux vidéos
        # ----------------

        i=0
        while(i<self.sel_handler.ItemsCount()):
            gc.SetPen(wx.Pen(self.config['main_config']['fore'], 6))
            gc.SetBrush(wx.Brush(self.config['main_config']['back']))

            item = self.sel_handler.GetItem(i)
            x = item.rect.GetX()
            y = item.rect.GetY()
            w = item.rect.GetWidth()
            h = item.rect.GetHeight()
            gc.DrawRectangle(x , y, w+1, h+1)

            if(item.Contains(self.mouse_x, self.mouse_y)):
                gc.SetPen(wx.Pen(self.config['main_config']['sel_fore'], 6))
                gc.SetBrush(wx.Brush(self.config['main_config']['sel_back']))
                gc.DrawRectangle(x , y, w+1, h+1)

            gc.DrawBitmap(wx.Bitmap(item.GetImage()), x, y, True)

            i+=1
        

        if(self.config['main_config']['int_back'] != 'transparent'):
            gc.SetBrush(wx.Brush(self.config['main_config']['int_back']))
            


    # ---------------------------------------------------------------------------------
            
    def OnLeftClick(self, event):
        # On accède aux coordonnées de la souris
        pos = self.my_panel.ScreenToClient(event.GetPosition())
        screen_pos = self.my_panel.GetScreenPosition()
        self.mouse_x = pos[0] + screen_pos[0]
        self.mouse_y = pos[1] + screen_pos[1]

        if(self.last_play_state == Status.StandBy):
            sel = self.sel_handler.GetSelected(self.mouse_x, self.mouse_y)

            if(sel != None):
                self.last_play = sel.GetMedia()
                self.SetUpVideo(self.last_play)

        if(self.last_play_state == Status.Load or self.last_play_state == Status.Pause):
            self.Play()
            self.last_play_state = Status.Play
        elif(self.last_play_state == Status.Play):
            self.Pause()
            self.last_play_state = Status.Pause

    # ---------------------------------------------------------------------------------

    def OnMouseMove(self, event):
        # On accède aux coordonnées de la souris
        pos = self.my_panel.ScreenToClient(event.GetPosition())
        screen_pos = self.my_panel.GetScreenPosition()
        self.mouse_x = pos[0] + screen_pos[0]
        self.mouse_y = pos[1] + screen_pos[1]

        sel = self.sel_handler.GetSelected(self.mouse_x, self.mouse_y)

        if(sel != self.last_sel):
            self.my_panel.Refresh()
            self.last_sel = sel

    # ---------------------------------------------------------------------------------

    def OnKeyUp(self, event):
        code = event.GetKeyCode()
        if(code == wx.WXK_SPACE):
            if(self.last_play_state == Status.Load):
                self.Play()
                self.last_play_state = Status.Play
            elif(self.last_play_state == Status.Pause):
                self.Play()
                self.last_play_state = Status.Play
            elif(self.last_play_state == Status.Play):
                self.Pause()
                self.last_play_state = Status.Pause
        elif(code == wx.WXK_ESCAPE):
            self.Stop()
            self.my_video.SetSize(0, 0)
            self.last_play_state = Status.StandBy

    # ---------------------------------------------------------------------------------

    def SetUpVideo(self, video=None):
        if(video != None):
            # Creation
            if(isfile(video)):
                if(self.last_play_state == Status.StandBy):
                    self.Media = self.Instance.media_new(unicode(video))
                    self.player.set_media(self.Media)
                    # Report the title of the file chosen
                    title = self.player.get_title()
                    # if an error was encountred while retrieving the title,
                    # otherwise use filename
                    self.SetTitle("%s - %s" % (title if title != -1 else 'wxVLC', basename(video)))

                    # set the window id where to render VLC's video output
                    handle = self.my_video.GetHandle()
                    full_height = 1080 - 100
                    full_width = int(full_height * 16 / 9)
                    insert_x = int((1920 - full_width) / 2)
                    insert_y = 0
                    self.my_video.SetSize(insert_x, insert_y, full_width, full_height)
                    if sys.platform.startswith('linux'):  # for Linux using the X Server
                        self.player.set_xwindow(handle)
                    elif sys.platform == "win32":  # for Windows
                        self.player.set_hwnd(handle)
                    elif sys.platform == "darwin":  # for MacOS
                        self.player.set_nsobject(handle)
                    self.last_play_state = Status.Load

    # ---------------------------------------------------------------------------------

    def Play(self):
        # Try to launch the media, if this fails display an error message
        if self.player.play():  # == -1:
            self.errorDialog("Unable to play.")

    # ---------------------------------------------------------------------------------

    def Pause(self):
        self.player.pause()

    # ---------------------------------------------------------------------------------

    def Stop(self):
        self.player.stop()

    # ---------------------------------------------------------------------------------

    def LoadMenu(self):
        with open("resources/media.yml", "r") as file:
            self.config = yaml.safe_load(file)
        
        # Add title_xxx to collection
        iterate = True
        i = 0
        while(iterate):
            # Incrémente la valeur qui doit être strictement supérieure à 0
            i+=1

            try:
                title = "title_%d" % i
                x = self.config[title]['x']
                y = self.config[title]['y']
                w = self.config[title]['width']
                h = self.config[title]['height']
                image = self.config[title]['image']
                media = self.config[title]['media']
                title_C = self.config[title]['title']
                title_X = self.config[title]['title_X']
                title_Y = self.config[title]['title_Y']


                r = rect.MyRect(x, y, w, h)
                r.SetImage(image)
                r.SetMedia(media)
                r.SetTitle(title_C)
                r.SetTextLocationX(title_X)
                r.SetTextLocationY(title_Y)

                self.sel_handler.Add(r)

            except:
                iterate = False
                
# =========================================================================
# == MAIN ---------------------------------------------------------------==
# =========================================================================
if __name__ == "__main__":
    app = wx.App()
    viewer = MyAuthViewer()
    viewer.SetTitle("MyAuth Viewer")
    viewer.SetSize(1920, 1080)
    viewer.Centre()
    viewer.Show()
    app.MainLoop()