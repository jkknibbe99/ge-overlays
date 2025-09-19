import os
from PIL import Image

# === INPUTS ===
image_path = 'orthophotos/1-90.png'
north, south = 42.976797, 42.964896
east, west = -85.874986, -85.876864
tile_size = 2048  # pixels per tile
kml_path = "overlay.kml"
output_dir = 'tiles'
    
# === STEP 1: Make output directory ===
os.makedirs(output_dir, exist_ok=True)

# === STEP 2: Open image ===
img = Image.open(image_path)
width, height = img.size
print(f"Image size: {width} x {height}")

# === STEP 3: Degrees per pixel ===
lat_per_pixel = (north - south) / height
lon_per_pixel = (east - west) / width

# === STEP 4: Slice image into tiles ===
tile_index = 0
ground_overlays = []

for y in range(0, height, tile_size):
    for x in range(0, width, tile_size):
        # Pixel bounds
        x_end = min(x + tile_size, width)
        y_end = min(y + tile_size, height)

        # Crop tile
        tile = img.crop((x, y, x_end, y_end))
        tile_filename = f"tile_{tile_index}.png"
        tile.save(os.path.join(output_dir, tile_filename))

        # tile URL
        tile_url = f'https://jkknibbe99.github.io/ge-overlays/tiles/{tile_filename}'

        # LatLon bounds
        tile_north = north - (y * lat_per_pixel)
        tile_south = north - (y_end * lat_per_pixel)
        tile_west  = west  + (x * lon_per_pixel)
        tile_east  = west  + (x_end * lon_per_pixel)

        # Build GroundOverlay XML
        overlay = f"""
        <GroundOverlay>
        <Icon>
            <href>{tile_url}</href>
        </Icon>
        <LatLonBox>
            <north>{tile_north}</north>
            <south>{tile_south}</south>
            <east>{tile_east}</east>
            <west>{tile_west}</west>
        </LatLonBox>
        </GroundOverlay>
        """
        ground_overlays.append(overlay)
        tile_index += 1

# === STEP 5: Write KML ===
kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    {''.join(ground_overlays)}
</Document>
</kml>
"""

with open(kml_path, "w") as f:
    f.write(kml_content)

print(f"✅ Done! {tile_index} tiles written to {output_dir}/ and KML saved as {kml_path}")
