This is a README for ISCV19-SCC AI task 

The Training data is located here: https://mellanox.app.box.com/folder/65353801319
if for some reason you can't access the data, please email info@hpcadvisorycouncil.com 

Some information about the data:

The data is stored as h5 files.  

To load the data, you can use

`
import h5py as h5
fin = h5.File(FILENAME)
data = fin['climate']['data']
labels_0 = fin['climate']['labels_0']
labels_1 = fin['climate']['labels_1']
`

Atmospheric rivers are stored as "2" in the label fields, and tropical cyclones are stored as "1" in the label fields. Labels_0 refers to the default thresholds for finding atmospheric rivers and tropical cycles.  Labels_1 refers to relaxed thresholds for finding atmospheric rivers and tropical cyclones.

"Data" (sorry for the vague name) refers to the 16-channel climate simulation image.  The 16 channels are stored in the following order: [TMQ, U850, V850, UBOT, VBOT, QREFHT, PS, PSL, T200, T500, PRECT, TS, TREFHT, Z1000, Z200, ZBOT]

Here's the metadata about each field:

- 0. TMQ
	- long_name: Total (vertically integrated) precipitable water
	- units: kg/m^2
	- description: the total amount of water vapor at that lat/lon grid cell on earth
- 1. U850
	- long_name: Zonal wind at 850 mbar pressure surface
	- units: m/s
- 2. V850
	- long_name: Meridional wind at 850 mbar pressure surface
	- units: m/s
- 3. UBOT
	- long_name: lowest level zonal wind
	- units: m/s
- 4. VBOT
	- long_name: Lowest model level meridional wind
	- units: m/s
- 5. QREFHT
	- long_name: reference height humidity
	- units: kg/kg
- 6. PS
	- long_name: surface pressure
	- units: Pa
- 7. PSL
	- long_name: sea level pressure
	- units: Pa
- 8. T200
	- long_name: temperature at 200 mbar pressure surface
	- units: K
- 9. T500
	- long_name: temperature at 500 mbar pressure surface
	- units: K
- 10. PRECT
	- long_name: total (convective and large-scale) precipitation rate (liq + ice)
	- units: m/s
- 11. TS
	- long_name: surface temperature (radiative)
	- units: K
- 12. TREFHT
	- long_name: reference height temperature
	- units: K
- 13. Z1000
	- long_nname: geopotential Z at 1000 mbar pressure surface
	- units: m
	- description: the height (in meters) corresponding to 1000 mbar of pressure
- 14. Z200
	- long_name: geopotential Z at 200 mbar pressure surface
	- units: m
	- description: the height (in meters) corresponding to 200 mbar of pressure
- 15. ZBOT
	- long_name: lowest modal level height
	- units: m

Some notes: 

1. Climate models output some fields (T200, T500, Z200, ZBOT, U850, V850, UBOT, VBOT) at multiple different heights along the atmosphere.  In atmospheric science, height (the z dimension) is referenced by pressure, not by meters above sea level.  So for example, T500 refers to the temperature at all areas of the atmosphere where there is 500 mbar of pressure. (Thus, these areas may not necessarily be the same number of meters above sea level.)

2. Surface pressure is the pressure at the surface of the earth, but sea level pressure is (as the name implies) the pressure at sea leve.  These are different when the surface is at a higher elevation than the sea level.

3. Statistics for the fields are available in the following way:
Labels statistics:
	- for each time step, the statistics for the labels are in `['climate']['labels_0_stats']` or `['climate']['labels_1_stats']`
	- these stats are a (7,1) array with [mean, max, min, standard deviation, percent_background_class, percent_tropical_cycle, percent_atmospheric river]
	- percent_background_class corresponds to the percent of pixels belonging to the background class.  percent_tropical_cycle corresponds to the percent of pixels that are a tropical cyclone. likewise for percent_atmospheric river
Data (16-channel climate simulation) statistics
	 - for each time step, the statistics for the labels are in `['climate']['data_stats']`
	 - these stats are a (4,16) array.  For each of the 16 channels, the following 4 statistics are calculated: [mean, max, min, standard_deviation]

4. The file names are in the format: data-[year]-[month]-[day]-[timestep]-[run_number].h5

5. This is data from the Community Atmospheric Model (CAM5).  All-Hist represents simulations of past climate, whereas HAPPI15 and HAPPI20 are different scenarios for future climate.  Each model was run multiple times, corresponding to the "run_number" attribute above.

