import numpy as np
import netCDF4

# this load the file into a Nx3 array (three columns)
data = np.genfromtxt('1763.csv', dtype=str, delimiter=',')


# create a netcdf Data object

with netCDF4.Dataset('TEST_file.nc', mode="w", format='NETCDF4') as ds:
    # some file-level meta-data attributes:
    ds.Conventions = "CF-1.6" # if you comply with the convension -- which you should!
    ds.title = 'A succinct description of what is in the dataset.'
    ds.institution = 'Specifies where the original data was produced.'
    ds.source = 'Source'
    ds.history = 'History'
    ds.references = 'References'
    ds.comment = 'whatever comment you may want to add'

    # defining the dimensions of your arrays:
    level = ds.createDimension('level', data.shape[0])

    # variables for the columns -- you should use real names
    for i in range(data.shape[1]):
        var = ds.createVariable('var%i'%i,data.dtype, ('level',))
        var[:] = data[:,i]
        ## adds some attributes
        var.units = 'the_proper_unit_string'
        var.long_name = 'a nice long name that describes the data'
        var.standard_name = 'a_CF_standard_name'
    print ds