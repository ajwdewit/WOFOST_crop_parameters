Parameter sets for the WOFOST crop simulation model
===================================================

This repository contains the parameter sets for 22 crops for the WOFOST
crop simulation model.

Format and structure of the parameter files
-------------------------------------------

The parameters are stored in a data serialization format called `YAML <http://yaml.org/>`_.
YAML is similar to XML or JSON but has a strong focus on human readability and therefore is
much more suited to store parameter sets that often have to be edited manually. Moreover,
YAML is language independent and YAML parsers are available for a variety of languages.

The parameter files are organized by crop type and within each file different crop ecotypes and
crop varieties can be defined. To accomodate the definition of different crop varieties
in one file, the parameter files have been organized in a clear structure.  This can be most easily
explained with an example (barley in this case):

.. code-block:: yaml

    Version: 1.0.0
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
                TSUM1:
                -  800
                - temperature sum from emergence to anthesis
                - ['C.d']
                TSUM2:
                -  750
                - temperature sum from anthesis to maturity
                - ['C.d']

The parameter file starts with a version number that is used to identify the file structure.
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
variety.

Parameters themselves are defined by a tag that is the name of the parameter and a list of three
items: 1) the value of the parameter, 2) a description of the parameter and 3) the units of the
parameter. The units are defined in such way that they can be easily parsed and used by software
that supports units during model definition and simulation.

The indenting and general structure of the parameter files are part of the YAML syntax and not only
enhance readability of the file, but also are essential for YAML to parse it.


.. _cultivars: https://en.wikipedia.org/wiki/Cultivar
.. _EcoTypes: https://en.wikipedia.org/wiki/Ecotype


How to use the parameter files
------------------------------

The crop parameter files have been designed to work with the Python Crop Simulation Environment (`PCSE`_)
which provides a DataProvider that can directly use the YAML crop parameter files:

.. code-block:: python

    >>> from pcse.fileinput import YAMLCropDataProvider
    >>> cropd = YAMLCropDataProvider()
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
    YAMLCropDataProvider - current active crop 'soybean' with variety 'Soybean_906'
    Available crop parameters:
     {'DTSMTB': [0.0, 0.0, 7.0, 0.0, 30.0, 23.0, 45.0, 38.0], 'NLAI_NPK': 1.0, 'NRESIDLV': 0.0093, 'KCRIT_FR': 1.0,

     ....

     720.0, 0.9, 1000.0, 0.9, 2000.0, 0.9], 'TSUM2': 1300, 'TSUM1': 500, 'TSUMEM': 90}

.. _PCSE: http://pcse.readthedocs.io

Moreover, the PCSE `AgroManager`_ is designed to work with the YAMLCropDataProvider and the parameters files
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

Limitations
-----------

A limitation of the current version of the parameter files is that the metadata concerning the
different ecotypes and varieties has not yet been defined in the file. In a subsequent version
of the parameter files this will be taken into account including information like:

* region where the variety can be applied

* contact person

* reference dataset

* reference publication

* etc.


.. |CO2| replace:: CO\ :sub:`2`\
