# Requirements: cfgrib, folium, matplotlib, branca
import cfgrib
import folium
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from branca.colormap import linear

# --- Plot 1: 2m Temperature ---
ds_t2m = cfgrib.open_dataset(
    "data.grb",
    filter_by_keys={"typeOfLevel": "surface"}
)
t2m = ds_t2m["t"].values - 273.15
lat = ds_t2m.latitude.values
lon = ds_t2m.longitude.values
lon2d, lat2d = np.meshgrid(lon, lat)

cmap_temp = plt.cm.jet
norm = mcolors.Normalize(vmin=np.min(t2m), vmax=np.max(t2m))
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis("off")
ax.pcolormesh(lon2d, lat2d, t2m, cmap=cmap_temp, norm=norm)
plt.savefig("t2m_map.png", bbox_inches="tight", pad_inches=0, transparent=True)
plt.close()

# --- Plot 2: 500 hPa Temperature ---
ds_500 = cfgrib.open_dataset(
    "data.grb",
    filter_by_keys={"typeOfLevel": "isobaricInhPa", "level": 500}
)
t_500 = ds_500["t"].values - 273.15
lat_500 = ds_500.latitude.values
lon_500 = ds_500.longitude.values
lon2d_500, lat2d_500 = np.meshgrid(lon_500, lat_500)

norm_500 = mcolors.Normalize(vmin=np.min(t_500), vmax=np.max(t_500))
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis("off")
ax.pcolormesh(lon2d_500, lat2d_500, t_500, cmap=cmap_temp, norm=norm_500)
plt.savefig("t500_map.png", bbox_inches="tight", pad_inches=0, transparent=True)
plt.close()

# --- Plot 3: Wind speed at 10m ---
ds_wind = cfgrib.open_dataset(
    "data.grb",
    filter_by_keys={"typeOfLevel": "heightAboveGround", "level": 10}
)
u10 = ds_wind["u10"].values
v10 = ds_wind["v10"].values
wind_speed = np.sqrt(u10**2 + v10**2)
lat_wind = ds_wind.latitude.values
lon_wind = ds_wind.longitude.values
lon2d_wind, lat2d_wind = np.meshgrid(lon_wind, lat_wind)

cmap_wind = plt.cm.viridis
norm_wind = mcolors.Normalize(vmin=np.min(wind_speed), vmax=np.max(wind_speed))
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis("off")
ax.pcolormesh(lon2d_wind, lat2d_wind, wind_speed, cmap=cmap_wind, norm=norm_wind)
plt.savefig("wind_map.png", bbox_inches="tight", pad_inches=0, transparent=True)
plt.close()

# --- Create Folium Map ---
center_lat = np.mean(lat)
center_lon = np.mean(lon)
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# Add overlays
bounds = [[np.min(lat), np.min(lon)], [np.max(lat), np.max(lon)]]
t2m_layer = folium.raster_layers.ImageOverlay(
    name="2m Temperature",
    image="t2m_map.png",
    bounds=bounds,
    opacity=0.7,
    show=True,     # visible by default
)
t2m_layer.add_to(m)

bounds_500 = [[np.min(lat_500), np.min(lon_500)], [np.max(lat_500), np.max(lon_500)]]
t500_layer = folium.raster_layers.ImageOverlay(
    name="500 hPa Temperature",
    image="t500_map.png",
    bounds=bounds_500,
    opacity=0.7,
    show=False,    # not visible by default
)
t500_layer.add_to(m)

bounds_wind = [[np.min(lat_wind), np.min(lon_wind)], [np.max(lat_wind), np.max(lon_wind)]]
wind_layer = folium.raster_layers.ImageOverlay(
    name="10m Wind Speed",
    image="wind_map.png",
    bounds=bounds_wind,
    opacity=0.7,
    show=False,    # not visible by default
)
wind_layer.add_to(m)

from branca.colormap import LinearColormap

# Create jet-like colormap with dynamic range
colormap_t2m = LinearColormap(
    colors=['blue', 'cyan', 'green', 'yellow', 'red'],
    vmin=np.min(t2m),
    vmax=np.max(t2m)
)
colormap_t2m.caption = "Temperature at 2m (°C)"
colormap_t2m.add_to(m)

colormap_t500 = LinearColormap(
    colors=['blue', 'cyan', 'green', 'yellow', 'red'],
    vmin=np.min(t_500),
    vmax=np.max(t_500)
)
colormap_t500.caption = "Temperature at 500 hPa (°C)"
colormap_t500.add_to(m)


colormap_wind = linear.viridis.scale(0, 25)
colormap_wind.caption = "Wind Speed at 10m (m/s)"
colormap_wind.add_to(m)

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)

# Save map
m.save("interactive_forecast.html")

print("Interactive map created with all legends and only t2m visible by default.")

