import ctypes
import pygetwindow as gw
import argparse

# Constantes da API do Windows
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x00000002

def is_valid_tibia_title(title):
    """
    Valida se o título é exatamente 'Tibia' ou começa com 'Tibia - '
    Ignora títulos como 'Tibia123', 'holaTibia' ou 'tibiaWiki'.
    """
    clean_title = title.strip()
    return clean_title == "Tibia" or clean_title.startswith("Tibia - ")

def apply_opacity_to_tibia(opacity):
    # Obter todas as janelas que contenham pelo menos "Tibia" no título
    potential_windows = gw.getWindowsWithTitle("Tibia")
    
    # Filtrar estritamente de acordo com as nossas regras
    valid_windows = [win for win in potential_windows if is_valid_tibia_title(win.title)]
    
    if not valid_windows:
        print("Erro: Nenhuma janela válida do Tibia foi encontrada.")
        return

    for target_window in valid_windows:
        print(f"Janela válida detectada: '{target_window.title}'")
        target_hwnd = target_window._hWnd
        
        try:
            ex_style = ctypes.windll.user32.GetWindowLongW(target_hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(target_hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED)
            ctypes.windll.user32.SetLayeredWindowAttributes(target_hwnd, 0, opacity, LWA_ALPHA)
            
            print(f" -> Opacidade aplicada com sucesso a '{target_window.title}' com valor {opacity}/255.\n")
        except Exception as e:
            print(f" -> Ocorreu um erro ao tentar modificar '{target_window.title}': {e}\n")

if __name__ == "__main__":
    # Configurar o analisador de argumentos do terminal
    parser = argparse.ArgumentParser(description="Ajusta a opacidade das janelas do jogo.")
    
    # Adicionar o argumento opcional para a opacidade
    parser.add_argument(
        "opacity", 
        nargs="?", # Significa que o argumento é opcional (0 ou 1 argumento)
        type=int, 
        default=200, 
        help="Nível de opacidade (0 a 255). O padrão é 200."
    )
    
    args = parser.parse_args()

    # Validar se o valor inserido está dentro dos limites do Windows
    if not (0 <= args.opacity <= 255):
        print("Erro: O valor da opacidade deve ser um número inteiro entre 0 e 255.")
    else:
        apply_opacity_to_tibia(args.opacity)
