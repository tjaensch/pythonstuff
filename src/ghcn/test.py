import numpy as np
import netCDF4

# Load source CSV file into variable
data = np.genfromtxt('/nodc/projects/satdata/Granule_OneStop/GHCN/source_csv_by_year/1763.csv', dtype=str, delimiter=',')

# Create a netcdf Data object
with netCDF4.Dataset('TEST_file.nc', mode="w", format='NETCDF4') as ds:
    # File-level metadata attributes:
    ds.Conventions = "CF-1.6" # if you comply with the convension -- which you should!
    ds.title = 'A succinct description of what is in the dataset.'
    ds.institution = 'Specifies where the original data was produced.'
    ds.source = 'Source'
    ds.history = 'History'
    ds.references = 'References'
    ds.comment = 'whatever comment you may want to add'

    # Defining array dimensions
    level = ds.createDimension('level', data.shape[0])

    # variables for the columns -- you should use real names
    for i in range(data.shape[1]):
        var = ds.createVariable('var%i'%i,data.dtype, ('level',))
        var[:] = data[:,i]
        # Add attributes
        # var.units = 'the_proper_unit_string'
        # var.long_name = 'long name that describes the data'
        # var.standard_name = 'CF_standard_name'
    print ds