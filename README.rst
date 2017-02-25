Parameter sets for the WOFOST crop simulation model
===================================================

This repository contains the parameter sets for 22 crops for the WOFOST
crop simulation model.

Format and structure of the parameter files
-------------------------------------------

The parameters are stored in a data serialization format called `YAML<http://yaml.org/>`_.
YAML is similar to XML or JSON but has a strong focus on human readability and therefore is
much more suited to store parameter sets that have to be edited regularly.

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
                <<: *GenericC3           # spring barley inherits from GenericC3
                ## All parameters specific for spring barley go here

        Varieties:
            Spring_barley_301:
                <<: *springbarley
                TSUM1:
                -  800
                - temperature sum from emergence to anthesis
                - ['C.d']
                TSUM2:
                -  750
                - temperature sum from anthesis to maturity
                - ['C.d']
