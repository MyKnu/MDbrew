from .analysis import *
from .brew import *

__version__ = "2.0.13"
__name__ = "MDbrew"


""" How to use

## ZERO. import MDbrew as mdb


## First. Openr your file
>>> file_path = './test.lammpstrj'
>>> opener = mdb.LAMMPSOpener('./test.lammpstrj')


## Second. Extract your data
>>> extractor = mdb.Extractor(opener=opener)
>>> system_size = extractor.system_size
>>> type_list = extractor.extract_type_list()
>>> type_info = extractor.extract_type_info()
>>> id_list = extractor.extract_id_list()
>>> atom_list = extractor.extract_atom_list(dict_type = dict_type)  # dict_typ : set[int:str] = {1:'O', 2:'N'}
>>> one_position = extractor.extract_position(type_=1.0)
>>> two_position = extractor.extract_position(type_=2.0)

>>> one_position_unwrapped = extractor.extract_position(type_=1.0, wrapped=False)


## Third. analyze the data 

### RDF
>>> rdf = mdb.RDF(one_position, two_position, system_size)
>>> rdf_result = rdf.result
>>> rdf.plot_result()

### MSD
>>> msd = mdb.MSD(one_position_unwrapped)
>>> msd_result = msd.result
>>> msd.plot_result()

"""
