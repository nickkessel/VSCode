import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
#config
CSV_FILE = 'test2.csv'
BACKGROUND_IMAGE = 'assets/blank_7dayGOODONE.png' # User needs to provide this file
ICONS_FOLDER = 'assets/icons/'
OUTPUT_FILE = '7day_forecast.png'
FIRST_ICON_SIZE = (170,170)
ICON_SIZE = (128, 128) # Resize icons to a consistent size
FONT_PATH = "assets/BAHNSCHRIFT.TTF"
FONT_SEMIBOLD = "SemiBold"
FONT_BOLD = "Bold"
MAX_DESC_WIDTH = 120

#fonts
def create_font(path, size, style_name=None):
    """
    Loads a font, sets its style variation, and returns the font object.
    """
    try:
        font = ImageFont.truetype(path, size)
        if style_name:
            font.set_variation_by_name(style_name)
        return font
    except (IOError, OSError):                               
        print(f"❌ Error: Could not load font from {path}")   
    except ValueError:                                       
        print(f"❌ Error: Style '{style_name}' not found in {path}")
    # Return a default font if loading fails                 
    return ImageFont.load_default()  
                        
#special day1 fonts
FONT_DAY1 = create_font(FONT_PATH, 32, FONT_SEMIBOLD)         
FONT_HIGHTEMP1 = create_font(FONT_PATH, 54, FONT_BOLD)        
FONT_LOWTEMP1 = create_font(FONT_PATH, 30, FONT_BOLD) #POPS AND TESMP BOLD FONT
FONT_WIND1 = create_font(FONT_PATH, 17, FONT_SEMIBOLD)        
FONT_DESC1 = create_font(FONT_PATH, 24, FONT_SEMIBOLD)        
FONT_AVG1 = create_font(FONT_PATH, 21, "Bold SemiCondensed")         
FONT_POP1 = create_font(FONT_PATH, 20, FONT_BOLD)       
#normal fonts                                                             
FONT_DAY = create_font(FONT_PATH, 32, FONT_SEMIBOLD)         
FONT_HIGHTEMP = create_font(FONT_PATH, 54, FONT_BOLD)        
FONT_LOWTEMP = create_font(FONT_PATH, 30, FONT_BOLD) #POPS AND TESMP BOLD FONT    
FONT_DESC = create_font(FONT_PATH, 20, FONT_SEMIBOLD)
FONT_MMWX = create_font(FONT_PATH, 16, FONT_SEMIBOLD)                 
FONT_POP = create_font(FONT_PATH, 22, FONT_BOLD)             

centered_text_x = 355 #desc and high temp, add to this for other days
low_x = 424
pop_x = 370                     
COORDINATES_D1 = [       # first day                                        
    # Day 1 (e.g., Monday)                                   
    {"icon": (75, 190), "desc": (170,375), "high_temp": (170, 460), "low_temp": (283, 585), "pop": (250, 275), "wind" : (170, 545), "avg": (1128,655)},
]
COORDINATES = [ #other da,ys
    {"icon": (290, 200), "desc": (centered_text_x,375), "high_temp": (centered_text_x,  460), "low_temp": (low_x, 585), "pop": (pop_x, 544)},
    {"icon": (425, 200), "desc": (centered_text_x + 138, 375), "high_temp": (centered_text_x + 138, 460), "low_temp": (low_x + 138, 585), "pop": (pop_x + 138, 544)},
    {"icon": (566, 200), "desc": (centered_text_x + 139*2, 375), "high_temp": (centered_text_x + 139*2, 460), "low_temp": (low_x + 277, 585), "pop": (pop_x + 277, 544)},
    {"icon": (709, 200), "desc": (centered_text_x + 139*3, 375), "high_temp": (centered_text_x + 139*3, 460), "low_temp": (low_x + 415, 585), "pop": (pop_x + 415, 544)},
    {"icon": (846, 200), "desc": (centered_text_x + 139*4, 375), "high_temp": (centered_text_x + 139*4, 460), "low_temp": (low_x + 554, 585), "pop": (pop_x + 554, 544)},
    {"icon": (985, 200), "desc": (centered_text_x + 696, 375), "high_temp": (centered_text_x + 696, 460), "low_temp": (low_x + 690, 585), "pop": (pop_x + 696, 544)}
]                                                   

def add_drop_shadow(image, offset=(5, 3), shadow_color=(0, 0, 0), blur_radius=3):
    """
    Adds a drop shadow to a PIL image.
    """
    # Create a shadow image in the specified color
    shadow = Image.new('RGBA', image.size, shadow_color)

    # Create a mask from the original image's alpha channel
    mask = image.split()[3]

    # Paste the shadow using the alpha mask, offsetting it
    shadow_with_offset = Image.new('RGBA', (
        image.width + abs(offset[0]),
        image.height + abs(offset[1])
    ))
    shadow_with_offset.paste(shadow, offset, mask)

    # Blur the shadow
    blurred_shadow = shadow_with_offset.filter(ImageFilter.GaussianBlur(blur_radius))

    # Paste the original image on top of the blurred shadow
    final_image = Image.new('RGBA', blurred_shadow.size)
    final_image.paste(image, (0, 0))
    final_image = Image.alpha_composite(blurred_shadow, final_image)

    return final_image
                                                             
def create_weather_graphic():                                
    """                                                      
    Generates a 7-day weather graphic by overlaying data from a CSV onto a background image.
    """                                                      
    try:                                                     
        df = pd.read_csv(CSV_FILE, index_col=0)              
        df = df.T                                            
        df.columns = df.columns.str.strip()                  
        df.reset_index(drop=True, inplace=True)              
        base_image = Image.open(BACKGROUND_IMAGE).convert("RGBA")
    except FileNotFoundError as e:
        print(f"Error: Could not find a required file. {e}")
        return

    draw = ImageDraw.Draw(base_image)
    draw.text((200,70),"@midmittenwx", font= FONT_MMWX, fill = 'yellow', anchor='mm') #draws on the account name bc i didnt ss it lol
    if not df.empty:
        day1_data = df.iloc[0] # Get the first row of data
        
        # Get data and prepare text
        desc1 = day1_data['DESC']
        high1 = f"{day1_data['HIGHTEMP']}"
        low1 = day1_data['LOWTEMP']
        pop1 = f"{day1_data['POP']}%"
        wind1 = day1_data['WIND']
        avg1 = day1_data['AVG']
        coords1 = COORDINATES_D1[0]
        #test text fit
        wrapped_lines = []
        words = desc1.split()
        
        if words:
            current_line = words[0]
            for word in words[1:]:
                # Check width of the line with the new word added
                bbox = draw.textbbox((0, 0), f"{current_line} {word}", font=FONT_DESC)
                if bbox[2] - bbox[0] <= MAX_DESC_WIDTH + 20: #first box a little wider
                    # Word fits, add it to the current line
                    current_line += f" {word}"
                else:
                    # Word doesn't fit, finalize the current line and start a new one
                    wrapped_lines.append(current_line)
                    current_line = word
            wrapped_lines.append(current_line) # Add the last line

        final_description = "\n".join(wrapped_lines)
        
        # Draw all text for Day 1
        draw.text(coords1['desc'], final_description, font=FONT_DESC1, fill='white', anchor='mm', align='center')
        draw.text(coords1['high_temp'], high1, font=FONT_HIGHTEMP1, fill="yellow", anchor="mm")
        draw.text(coords1['low_temp'], low1, font=FONT_LOWTEMP1, fill="yellow", anchor="mm")
        draw.text(coords1['pop'], pop1, font=FONT_POP1, fill="yellow", anchor="mm")
        draw.text(coords1['wind'], wind1, font=FONT_WIND1, fill='white', anchor='mm')
        draw.text(coords1['avg'], avg1, font= FONT_AVG1, fill='yellow', anchor='mm')
        
        # Draw icon for Day 1
        icon_path1 = os.path.join(ICONS_FOLDER, f"{day1_data['ICON'].strip()}.png")
        try:
            icon1 = Image.open(icon_path1).convert("RGBA").resize(FIRST_ICON_SIZE, Image.Resampling.LANCZOS)
            icon_with_shadow = add_drop_shadow(icon1)

            # Paste the new image with the shadow
            base_image.paste(icon_with_shadow, coords1['icon'], icon_with_shadow)
        except FileNotFoundError:
            print(f"Warning: Icon for Day 1 not found.")

    # 2. Loop through each day in the CSV (up to 7 days)
    for index, row in df.iloc[1:7].iterrows():
        loop_index = index -1 
        if loop_index >= len(COORDINATES):
            print(f"Warning: More than {len(COORDINATES)} days in CSV, skipping extra rows.")
            break

        # Get data for the current day
        #day_of_week = row['DAY']
        description = row['DESC']
        high_temp = row['HIGHTEMP']
        low_temp = row['LOWTEMP']
        pop = row['POP']
        icon = row['ICON']
        #wind = row['WIND']

        icon_name = icon.strip()
        icon_filename = f"{icon_name}.png"
        icon_path = os.path.join(ICONS_FOLDER, icon_filename)
        # Prepare text strings
        high_temp_text = f"{high_temp}"
        low_temp_text = low_temp
        pop_text = f"{pop}%"

        # Get coordinates for the current day
        coords = COORDINATES[loop_index]

        try:
            icon = Image.open(icon_path).convert("RGBA")
            if icon.size != ICON_SIZE:
                icon = icon.resize(ICON_SIZE, Image.Resampling.LANCZOS)
                
            icon_with_shadow = add_drop_shadow(icon)

            # Paste the new image with the shadow
            base_image.paste(icon_with_shadow, coords['icon'], icon_with_shadow)
            

        except FileNotFoundError:
            print(f"Warning: Icon '{icon_filename}' not found for description '{description}'.")

        #test text fit
        wrapped_lines = []
        words = description.split()
        
        if words:
            current_line = words[0]
            for word in words[1:]:
                # Check width of the line with the new word added
                bbox = draw.textbbox((0, 0), f"{current_line} {word}", font=FONT_DESC)
                if bbox[2] - bbox[0] <= MAX_DESC_WIDTH:
                    # Word fits, add it to the current line
                    current_line += f" {word}"
                else:
                    # Word doesn't fit, finalize the current line and start a new one
                    wrapped_lines.append(current_line)
                    current_line = word
            wrapped_lines.append(current_line) # Add the last line

        final_description = "\n".join(wrapped_lines)
                    
        # Anchor 'ms' means middle-start, aligning text from its center point horizontally
        
        draw.text(coords['desc'], final_description, font = FONT_DESC, fill = 'white', align = 'center', anchor = 'mm')
        draw.text(coords['high_temp'], high_temp_text, font=FONT_HIGHTEMP, fill="yellow", anchor="mm")
        draw.text(coords['low_temp'], low_temp_text, font=FONT_LOWTEMP, fill="yellow", anchor="mm")
        draw.text(coords['pop'], pop_text, font=FONT_POP, fill="yellow", anchor="mm")
        #draw.text(coords['wind'], wind, font = FONT_WIND, fill = 'white', anchor = 'mm')


    # 5. Save the final image
    base_image.save(OUTPUT_FILE)
    print(f"Successfully created  graphic: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_weather_graphic()