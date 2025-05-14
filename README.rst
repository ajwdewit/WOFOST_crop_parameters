Parameter sets for the WOFOST cropping system model
===================================================

This repository contains the parameter sets for 23 crops for the WOFOST
cropping system model.

WOFOST versions and parameter files
-----------------------------------

Since the release of PCSE 6.0, there are several versions of WOFOST available (7.2, 7.3, 8.1 and 
the deprecated version 8.0-beta). The parameter files for the different model version reside on different
branches within this repository. The parameter files that are currently on the master branch of this 
repository will remain available for backwards compatibility with PCSE 5.5 and are suitable for WOFOST 
versions 7.2 and 8.0-beta. However, they will probably be deleted at some point in the future in
order to reduce the burden of maintaining the files.

Format and structure of the parameter files
-------------------------------------------

The parameters are stored in a data serialization format called `YAML <http://yaml.org/>`_.
YAML is similar to XML or JSON but has a strong focus on human readability and therefore is
much more suited to store parameter sets that often have to be edited manually. Moreover,
YAML is language independent and YAML parsers are available for a variety of languages.

The parameter files are organized by crop type and within each file different crop ecotypes and
crop varieties can be defined. To accommodate the definition of different crop varieties
in one file, the parameter files have been organized in a clear structure.  This can be most easily
explained with an example (barley in this case):

.. code-block:: yaml

    Version: 1.0.0
    Metadata:
        ## Meta data at the crop level goes here

    CropParameters:
        GenericC3: &GenericC3

            ## All parameters for C3 crops go here

        GenericC4: &GenericC4

            ## All parameters for C4 crops go here

        EcoTypes:
            springbarley: &springbarley
                <<: *GenericC3           # Ecotype springbarley inherits from GenericC3

                ## All parameters specific for springbarley go here

        Varieties:
            Spring_barley_301:
                <<: *springbarley        # Variety Spring_barley_301 inherits from ecotype springbarley
                Metadata:
                    <<: *meta
                    ## Metadata at the variety level goes here
                TSUM1:
                -  800
                - temperature sum from emergence to anthesis
                - ['C.d']
                TSUM2:
                -  750
                - temperature sum from anthesis to maturity
                - ['C.d']

The parameter file starts with a version number that is used to identify the file structure and the
metadata at the crop level.
Next, the crop parameters are defined starting at the tag ``CropParameters``. First all parameters
that are generic for C3 and C4 crops are defined by the tags ``GenericC3`` and ``GenericC4``.
These parameters mainly have to do with |CO2| response on assimilation and transpiration.
Moreover they define two anchors ``&GenericC3`` and ``&GenericC4`` that can be used to refer to in
later sections.

Second, the parameter file defines the `EcoTypes`_. These can be regarded as distinct sets of
crop parameters that define the properties of groups of varieties. The parameter definitions of
EcoTypes have to be complete (all crop parameters have to be present) and they have to
inherit from either ``GenericC3`` or ``GenericC4`` by providing a reference to the anchor. For example,
the ecotype 'springbarley' refers to the anchor ``GenericC3`` through the syntax ``<<: *GenericC3``.
Each ecotype defines an anchor to itself that can be used to refer to later on.

Finally, the parameter file defines the varieties for the given crop (often called
`cultivars`_). Varieties in the parameter file inherit all parameters from one of the defined
EcoTypes and redefine one or more parameters that are specific for the given variety. In the
example above, the variety 'Spring_barley_301' inherits its parameters from the EcoType
'springbarley' while it redefines the parameters TSUM1 and TSUM2 to values specific for this
variety. Moreover, a variety also inherits its metadata from the main metadata at the crop level
but in many cases specific metadata at the variety level is available.

Parameters themselves are defined by a tag that is the name of the parameter and a list of three
items: 1) the value of the parameter, 2) a description of the parameter and 3) the units of the
parameter. The units are defined in such way that they can be easily parsed and used by software
that supports units during model definition and simulation.

The indenting and general structure of the parameter files are part of the YAML syntax and not only
enhance readability of the file, but also are essential for YAML to parse it.

The repository contains one additional file (crops.yaml) which lists all the crops that
are available in the repository. the crops.yaml file is used as an entrypoint for the
`YAMLCropDataProvider` (see below) which uses it to fetch all parameter files. This approach ensures
that the same data provider can be used for other repositories with parameter files, for example
those for the `LINGRA`_ model.

.. _LINGRA: https://github.com/ajwdewit/lingra_crop_parameters
.. _cultivars: https://en.wikipedia.org/wiki/Cultivar
.. _EcoTypes: https://en.wikipedia.org/wiki/Ecotype


How to use the parameter files
------------------------------


**Important Notice**
    Some people are reading WOFOST parameter files with R using: ``read_yaml(file = file_yaml)``
    
    However, by default R does not respect the Anchors and Aliases that are used to overwrite 
    certain parameters for different crop varieties. You have to explicitly use:    
    ``read_yaml(file = file_yaml, merge.precedence = "override")``   
    To get the appropriate values for varieties.

The crop parameter files have been designed to work with the Python Crop Simulation Environment (`PCSE`_)
which provides a DataProvider that can directly use the YAML crop parameter files. From PCSE 6.0
onward it is required to provide the WOFOST model object as input for the YAMLCropDataProvider. This
way, the YAMLCropDataProvider can select the correct branch from the repository:

.. code-block:: python

    >>> from pcse.input import YAMLCropDataProvider
    >>> from pcse.models import Wofost81_PP
    >>> cropd = YAMLCropDataProvider(Wofost81_PP)
    >>> cropd.print_crops_varieties()
    crop 'mungbean', available varieties:
     - 'Mungbean_VanHeemst_1988'
    crop 'millet', available varieties:
     - 'Millet_VanHeemst_1988'
    crop 'chickpea', available varieties:
     - 'Chickpea_VanHeemst_1988'
    crop 'soybean', available varieties:
     - 'Soybean_906'
     - 'Soybean_904'

    .....

    crop 'potato', available varieties:
     - 'Potato_701'
     - 'Potato_703'
     - 'Potato_702'
     - 'Potato_704'
    crop 'sorghum', available varieties:
     - 'Sorghum_VanHeemst_1988'
    >>> cropd.set_active_crop('soybean', 'Soybean_906')
    >>> print(cropd)
    Crop parameters loaded from: https://raw.githubusercontent.com/ajwdewit/WOFOST_crop_parameters/wofost81
    YAMLCropDataProvider - current active crop 'soybean' with variety 'Soybean_906'
    Available crop parameters:
     {'CO2EFFTB': [40.0, 0.0, 360.0, 1.0, 720.0, 1.11, 1000.0, 1.11, 2000.0, 1.11], 'CO2TRATB': [40.0, 0.0, 360.0, 1.0, 720.0,
    ...
    'REALLOC_DVS': 3.0, 'REALLOC_STEM_FRACTION': 0.2, 'REALLOC_LEAF_FRACTION': 0.0, 'REALLOC_STEM_RATE': 0.0415,
     'REALLOC_LEAF_RATE': 0.0, 'REALLOC_EFFICIENCY': 0.95}

    YAMLCropDataProvider - current active crop 'soybean' with variety 'Soybean_906'
    Available crop parameters:
     {'DTSMTB': [0.0, 0.0, 7.0, 0.0, 30.0, 23.0, 45.0, 38.0], 'NLAI_NPK': 1.0, 'NRESIDLV': 0.0093, 'KCRIT_FR': 1.0,

     ....

     720.0, 0.9, 1000.0, 0.9, 2000.0, 0.9], 'TSUM2': 1300, 'TSUM1': 500, 'TSUMEM': 90}


For PCSE 5.X releases, the following code is still sufficient:

.. code-block:: python

    >>> from pcse.fileinput import YAMLCropDataProvider
    >>> cropd = YAMLCropDataProvider()

.. _PCSE: http://pcse.readthedocs.io


Connecting crop parameters and agromanagement
---------------------------------------------

the PCSE `AgroManager`_ is designed to work with the YAMLCropDataProvider and the parameters files
by referring to the crop type (``crop_name``) and crop variety (``variety_name``) in its definition of the
agromanagement:

.. _AgroManager: http://pcse.readthedocs.io/en/master/reference_guide.html#the-agromanager

.. code-block:: yaml

    Version: 1.0.0
    AgroManagement:
    - 1998-01-01:
        CropCalendar:
            crop_name: soybean
            variety_name: Soybean_906
            crop_start_date: 1998-05-15
            crop_start_type: sowing
            crop_end_date:
            crop_end_type: maturity
            max_duration: 150
        TimedEvents:
        StateEvents:
    - 1999-01-01:

Within the agromanagement definition (also defined in YAML) the ``crop_name`` and ``variety_name`` tags within
the ``CropCalendar`` definition directly refer to the name of the parameter file ('soybean') and the variety
('Soybean_906') that is defined in the crop parameter file.

Note that ``crop_name`` and ``variety_name`` in the agromanagement definition are **case sensitive**!


.. |CO2| replace:: CO\ :sub:`2`\
