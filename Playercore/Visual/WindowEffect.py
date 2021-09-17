
from ctypes import POINTER, c_bool, sizeof, windll,pointer,c_int,Structure,cdll
from ctypes.wintypes import DWORD, HWND, ULONG
from win32 import win32api, win32gui
from win32.lib import win32con

from enum import Enum


class WINDOWCOMPOSITIONATTRIB(Enum):
    WCA_UNDEFINED = 0,
    WCA_NCRENDERING_ENABLED = 1,
    WCA_NCRENDERING_POLICY = 2,
    WCA_TRANSITIONS_FORCEDISABLED = 3,
    WCA_ALLOW_NCPAINT = 4,
    WCA_CAPTION_BUTTON_BOUNDS = 5,
    WCA_NONCLIENT_RTL_LAYOUT = 6,
    WCA_FORCE_ICONIC_REPRESENTATION = 7,
    WCA_EXTENDED_FRAME_BOUNDS = 8,
    WCA_HAS_ICONIC_BITMAP = 9,
    WCA_THEME_ATTRIBUTES = 10,
    WCA_NCRENDERING_EXILED = 11,
    WCA_NCADORNMENTINFO = 12,
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13,
    WCA_VIDEO_OVERLAY_ACTIVE = 14,
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15,
    WCA_DISALLOW_PEEK = 16,
    WCA_CLOAK = 17,
    WCA_CLOAKED = 18,
    WCA_ACCENT_POLICY = 19,
    WCA_FREEZE_REPRESENTATION = 20,
    WCA_EVER_UNCLOAKED = 21,
    WCA_VISUAL_OWNER = 22,
    WCA_LAST = 23


class ACCENT_STATE(Enum):
    """ 客户区状态枚举类 """
    ACCENT_DISABLED = 0,
    ACCENT_ENABLE_GRADIENT = 1,
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2,
    ACCENT_ENABLE_BLURBEHIND = 3,          # Aero效果
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4,   # 亚克力效果
    ACCENT_INVALID_STATE = 5


class ACCENT_POLICY(Structure):
    """ 设置客户区的具体属性 """
    _fields_ = [
        ('AccentState',   DWORD),
        ('AccentFlags',   DWORD),
        ('GradientColor', DWORD),
        ('AnimationId',   DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ('Attribute',  DWORD),
        ('Data',       POINTER(ACCENT_POLICY)),
        ('SizeOfData', ULONG),
    ]


class WindowEffect():
    def __init__(self):
        self.SetWindowCompositionAttribute=windll.user32.SetWindowCompositionAttribute
        self.SetWindowCompositionAttribute.restype=c_bool
        self.SetWindowCompositionAttribute.argtypes=[c_int, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]

        self.accentPolicy=ACCENT_POLICY()
        self.winCompAttrData=WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute=WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value[0]
        self.winCompAttrData.SizeOfData=sizeof(self.accentPolicy)
        self.winCompAttrData.Data=pointer(self.accentPolicy)

    def moveWindow(self, hWnd:int):
        win32gui.ReleaseCapture()
        win32api.SendMessage(hWnd, win32con.WM_SYSCOMMAND,win32con.SC_MOVE+win32con.HTCAPTION, 0)
