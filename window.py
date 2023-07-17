import ctypes
import pygetwindow as gw

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x00000002

OPACITY = 1 # 0 -- 255
WINDOW_TITLE = "Tibia - Devmau"
target_window = gw.getWindowsWithTitle(WINDOW_TITLE)[0]

if target_window is not None:
    target_hwnd = target_window._hWnd

    ex_style = ctypes.windll.user32.GetWindowLongA(target_hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongA(target_hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED)

    ctypes.windll.user32.SetLayeredWindowAttributes(target_hwnd, 0, OPACITY, LWA_ALPHA)

    print("Opacidade da janela modificada.")
else:
    print("Janela não encontrada.")