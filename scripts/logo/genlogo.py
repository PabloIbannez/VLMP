from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from colorama import init, Fore, Style, AnsiToWin32
import io
import sys

# Initialize colorama
init()

def create_image_from_ascii(ascii_art, font_size=20, padding=20, selection="all"):

    available_selections = ["all", "main", "shadow","text"]

    if selection not in available_selections:
        raise ValueError(f"Invalid selection: {selection}. Available selections: {available_selections}")

    # Calculate image size
    max_width = max(len(line) for line in ascii_art)
    num_lines = len(ascii_art)
    img_width = max_width * font_size // 2 + padding * 2
    img_height = num_lines * font_size + padding * 2

    # Create image with transparent background
    image = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Load a monospace font
    try:
        #Bold
        font = ImageFont.truetype("FreeMonoBold.ttf", font_size)
    except IOError:
        print("Font not found. Using default font.")
        #List of available fonts
        fonts = [f.name for f in font_manager.fontManager.ttflist]
        fonts = sorted(set(fonts))
        for f in fonts:
            print(f)

        font = ImageFont.load_default()

    # Darcula-like color palette
    colors = {
        'default': (170, 170, 170, 255),  # Light gray
        'light_green': (152, 195, 121, 255),  # Darcula light green
        'light_blue': (104, 151, 187, 255),  # Darcula light blue
        'light_red': (224, 108, 117, 255),  # Darcula light red
        'light_yellow': (229, 192, 123, 255),  # Darcula light yellow
        'black': (0, 0, 0, 255),  # Black
    }

    # Draw text
    y = padding
    current_color = colors['default']
    for line in ascii_art:
        x = padding
        color_code = None
        i = 0
        while i < len(line):
            char = line[i]
            if char == '\033':
                color_code = ''
                i += 1
                continue
            if char == '[' and color_code is not None:
                i += 1
                continue
            if color_code is not None:
                if char == 'm':
                    if color_code == '92':
                        current_color = colors['light_green']
                    elif color_code == '94':
                        current_color = colors['light_blue']
                    elif color_code == '91':
                        current_color = colors['light_red']
                    elif color_code == '93':
                        current_color = colors['light_yellow']
                    elif color_code == '30':
                        current_color = colors['black']
                    else:
                        current_color = colors['default']
                    color_code = None
                else:
                    color_code += char
                i += 1
                continue
            if selection == "all":
                charToDraw = char
            elif selection == "main":
                if char == "█":
                    charToDraw = char
                else:
                    charToDraw = " "
            elif selection == "shadow":
                if char in ["║", "═", "╔", "╗", "╚", "╝"]:
                    charToDraw = char
                else:
                    charToDraw = " "
            elif selection == "text":
                # Check if char is a text character
                if char.isalpha() or char.isdigit() or char in " _-.,;:!?":
                    charToDraw = char
                else:
                    charToDraw = " "

            draw.text((x, y), charToDraw, font=font, fill=current_color)

            x += font_size // 2
            i += 1
        y += font_size

    return image

width = 41

v_color = Fore.LIGHTGREEN_EX
l_color = Fore.LIGHTBLUE_EX
m_color = Fore.LIGHTRED_EX
p_color = Fore.LIGHTYELLOW_EX

# Define the ASCII art with colors
vlmp_art = [
    f"   {v_color}██╗   ██╗{l_color}██╗     {m_color}███╗   ███╗{p_color}██████╗{Style.RESET_ALL}",
    f"   {v_color}██║   ██║{l_color}██║     {m_color}████╗ ████║{p_color}██╔══██╗{Style.RESET_ALL}",
    f"   {v_color}██║   ██║{l_color}██║     {m_color}██╔████╔██║{p_color}██████╔╝{Style.RESET_ALL}",
    f"   {v_color}╚██╗ ██╔╝{l_color}██║     {m_color}██║╚██╔╝██║{p_color}██╔═══╝{Style.RESET_ALL}",
    f"   {v_color} ╚████╔╝ {l_color}███████╗{m_color}██║ ╚═╝ ██║{p_color}██║{Style.RESET_ALL}",
    f"   {v_color}  ╚═══╝  {l_color}╚══════╝{m_color}╚═╝     ╚═╝{p_color}╚═╝{Style.RESET_ALL}"
]

v_color = Fore.BLACK
l_color = Fore.BLACK
m_color = Fore.BLACK
p_color = Fore.BLACK

#vlmp_subtext = [f"    {v_color}Virtual   {l_color}Lab    {m_color}Modeling {p_color} Platform{Style.RESET_ALL}"]
vlmp_subtext = [f"    {v_color}VIRTUAL   {l_color}LAB    {m_color}MODELING {p_color} PLATFORM{Style.RESET_ALL}"]

for line in vlmp_art + vlmp_subtext:
    print(line)
print("="*width)

# Print width by stderr
print("width:", width, file=sys.stderr)

ascii_logo = vlmp_art + vlmp_subtext

# Print the ASCII art
for line in ascii_logo:
    print(line)
print("="*width)

fsize = 40

image = create_image_from_ascii(ascii_logo, font_size=fsize, padding=20)
image.save("logo.png")

image = create_image_from_ascii(ascii_logo, font_size=fsize, padding=20, selection="main")
image.save("logo_main.png")

image = create_image_from_ascii(ascii_logo, font_size=fsize, padding=20, selection="shadow")
image.save("logo_shadow.png")

image = create_image_from_ascii(ascii_logo, font_size=fsize, padding=20, selection="text")
image.save("logo_text.png")
