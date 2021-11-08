import numpy as np
import rasterio

from giga.utils.geom import points_in_circle


OPTIONAL_ARGUMENTS = {'max_census_radius': 200.0, # km
                      'census_radius': 10.0, # km
                      'pixel_resolution': 0.100, # km per pixel
                      'location_input': ['Lat', 'Lon']}


class PopulationNode:

    """
        Census computation node used for
        inferring the population within a circular region of interest
    """

    def __init__(self, name,
                       population_data,
                       ll_to_pixel_transform_callback,
                       **kwargs):
        """
            Inputs:
            - population_data: 2D numpy array representing population density
            - ll_to_pixel_transform_callback: callback fn that trasnforms
                    (lon, lat) pairs into pixels/indeces that can be used to retreive population data
        """
        self.name = name
        self.population_data = population_data
        self.dataset_height = population_data.shape[0]
        self.dataset_width = population_data.shape[1]
        self.ll_to_pixel_transform = ll_to_pixel_transform_callback
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    @staticmethod
    def from_tiff(node_name, tiff_file, **kwargs):
        """
            Loads population data from a tiff file,
            creates a lon,lat -> pixel trasnform callback function and
            returns a CensusNode instance
        """
        raw_dataset = rasterio.open(tiff_file)
        population_data = raw_dataset.read(1)
        # clip values below zero
        population_data[population_data < 0] = 0
        # lon, lat -> pixel transform callback
        transform = ~raw_dataset.transform
        transform_cb = lambda x: np.floor(transform * [x[0], x[1]])
        return PopulationNode(node_name, population_data, transform_cb, **kwargs)

    def out_of_country(self, popidx_x, popidx_y, radius_pixels):
        # TODO (max): there's a more robust way to check if lon/lat is in country bounds
        if ((popidx_x < radius_pixels) or
            (popidx_x > self.dataset_width - radius_pixels) or
            (popidx_y < radius_pixels) or
            (popidx_y > self.dataset_height - radius_pixels)):
            return True
        else:
            return False

    def compute_nearby_population(self, datarow, radius):
        lat, lon = datarow[self.location_input]
        xidx, yidx = self.ll_to_pixel_transform((lon, lat))
        radius_catchment = radius / self.pixel_resolution
        if self.out_of_country(xidx, yidx, radius_catchment):
            return 0.0
        x_catchment, y_catchment = points_in_circle(xidx, yidx, np.floor(radius_catchment))
        pop_catchment = self.population_data[y_catchment, x_catchment]
        return np.floor(np.sum(pop_catchment))

    def run(self, data, parameters):
        radius = parameters.get('radius', self.census_radius)
        nearby_population = data.apply(lambda row: self.compute_nearby_population(row, radius), axis=1)
        return nearby_population

