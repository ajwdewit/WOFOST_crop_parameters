from __future__ import print_function
import sys, os
sys.path.append(r"D:\UserData\sources\pcse\pcse")
import glob
import datetime as dt
import pcse
from pcse.fileinput import CABOFileReader
import yaml
from final_npk_params import npk_params
from additional_params import add_params
from LINTUL5_crop_files import WOFOST_nutrient_parameters


# folders
src_dir = os.path.normpath(os.path.dirname(__file__))
root_dir = os.path.dirname(src_dir)
ecotypes_dir = os.path.join(root_dir, "CROPD", "ecotypes")
variety_dir = os.path.join(root_dir, "CROPD", "varieties")
output_dir = root_dir

# basic inputs
param_metadata = yaml.load(open(os.path.join(src_dir, 'parameter_description.yaml')))
ecotype_template = "".join(open(os.path.join(src_dir, "ecotype_template.txt")).readlines())
crop_generics_file = os.path.join(src_dir, "crop_generics.yaml")
yaml_generics_stream = open(crop_generics_file, "rb").read().format(cdate=dt.date.today())

# crop types
all_crops = ['cassava','chickpea','cotton','cowpea','fababean','maize','groundnut','millet',
             'mungbean','pigeonpea','potato','rapeseed','rice','sorghum','soybean','barley','sugarbeet',
             'sugarcane','sunflower','sweetpotato','tobacco','wheat']

WOFOST_parameters = \
    ["TBASEM","TEFFMX","TSUMEM","IDSL","DLO",
     "DLC","TSUM1","TSUM2","DTSMTB","DVSI","DVSEND","TDWI","RGRLAI","SLATB",
     "SPA","SSATB","SPAN","TBASE","KDIFTB","EFFTB","AMAXTB","TMPFTB","TMNFTB",
     "CVL","CVO","CVR","CVS","Q10","RML","RMO","RMR","RMS","RFSETB","FRTB",
     "FLTB","FSTB","FOTB","PERDL","RDRRTB","RDRSTB","CFET","DEPNR","IAIRDU",
     "RDI","RRI","RDMCR",
     "DVS_NPK_STOP", "DVS_NPK_TRANSL", "NPK_TRANSLRT_FR", "KCRIT_FR", "NCRIT_FR",
     "PCRIT_FR", "KMAXSO", "KMAXLV_TB", "KMAXRT_FR", "NMAXRT_FR", "PMAXRT_FR",
     "KMAXST_FR", "NMAXST_FR", "PMAXST_FR", "NFIX_FR", "NLUE_NPK", "NMAXSO",
     "NMAXLV_TB", "PMAXSO", "PMAXLV_TB", "KRESIDLV", "KRESIDRT", "KRESIDST",
     "NRESIDLV", "NRESIDRT", "NRESIDST", "PRESIDLV", "PRESIDRT", "PRESIDST",
     "TCKT", "TCNT", "TCPT", "RDRLV_NPK", "NLAI_NPK", "NSLA_NPK", "NPART",
     'VERNBASE', 'VERNRTB', 'VERNSAT', 'VERNDVS', 'IOX']
     # "CO2EFFTB","CO2TRATB","CO2AMAXTB",

class TabularParameter():

    def __init__(self, value, formatter):
        self.value = value
        self.fmt = formatter

    def __str__(self):
        s = "["
        try:
            for x, y in zip(self.value[0::2], self.value[1::2]):
                if s == "[":
                    s += "%s, %s,\n" % (self.fmt[0] % x, self.fmt[1] % y)
                else:
                    s += "   %s, %s,\n" % (self.fmt[0] % x, self.fmt[1] % y)
        except Exception as e:
            print("formatting failure: %s" % e)

        s = s[:-2] + "]"
        return s


class ScalarParameter():
    def __init__(self, value, formatter):
        self.value = value
        self.fmt = formatter

    def __str__(self):
        return str(self.fmt % self.value)


class ParameterDescription():
    """Provides value, description and units of a parameter. 
    
    Also takes care of formatting for YAML representation."""

    def __init__(self, value, description, unit, formatter):
        if isinstance(value, list):
            self.value = TabularParameter(value, formatter)
        else:
            self.value = ScalarParameter(value, formatter)
        self.description = description
        self.unit = unit
        self.formatter = formatter
        
    def __str__(self):
        template = ("- {value}\n" +
                    "- {desc}\n" +
                    "- {unit}")
        t = template.format(value=self.value, desc=self.description, unit=self.unit)
        return t


def yaml_indent(yaml_stream):
    """Indents the yaml_stream as needed for the WOFOST crop parameter file.

    This is NOT a generic YAML indenter

    :param yaml_stream: the given WOFOST parameter YAML stream
    :return: a properly indented YAML stream
    """

    lines = yaml_stream.split("\n")
    result = []
    for line in lines:
        emptyline = (line.strip()) == ""
        if emptyline:
            continue
        if line.startswith(";"):
            line = line[1:]
        else:
            line = 12 * " " + line
        result.append(line + "\n")
    return "".join(result)


def make_variety_yaml_stream(crop, ecotypes):
    """Build a YAML stream for variety parameters for given ecotypes

    :param ecotypes: a dict of ecotype parameters: {'ecotype_name':{<parameters>}}
    :return: a YAML stream of varieties for given ecotypes
    """

    WOFOST_NPK_params = WOFOST_nutrient_parameters[crop]

    variety_yaml_stream = ";    Varieties:\n"
    for ecotype_name in ecotypes:
        msg = "Searching for cultivars with ecotype: %s" % ecotype_name
        print(msg)

        for fname in glob.glob(variety_dir + "/*"):
            fname = os.path.abspath(fname)
            params = CABOFileReader(fname)

            # Check if the current crop file is for this ecotype
            if ecotype_name != params['ECOTYPE']:
                continue

            ecotype_params = ecotypes[ecotype_name]
            cultivar_name = params["CRPNAM"].strip()
            msg = "Found cultivar '%s' in file: %s" % (cultivar_name, fname)
            print(msg)

            variety_yaml_stream += (";        {cropname}:\n".format(cropname=cultivar_name) +
                                    ";            <<: *{ecotype}\n".format(ecotype=ecotype_name))
            template = "{parname}:\n{pardesc}\n"
            for name in WOFOST_parameters:
                if name in WOFOST_NPK_params: # or name in add_params:
                    # Default crop files do not contain the nutrient parameters and additional params
                    continue
                if name in add_params:
                    # For additional parameters,
                    # If name not in crop parameter file, then continue
                    if name not in params:
                        continue
                value = params[name]
                if name not in ecotype_params:
                    msg = "Warning: parameter '%s' not in ecotype!" % name
                    print(msg)
                    continue
                if name in ["TSUM1", "TSUM2"]:
                    add_param = True
                elif value != ecotype_params[name][0]:
                    add_param = True
                    msg = "%s('%s':%s) differs from ecotype %s('%s':%s)" % \
                          (cultivar_name, name, value, ecotype_name, name, ecotype_params[name][0])
                    print(msg)
                else:
                    add_param = False

                if add_param:
                    desc, unit, fmt = param_metadata[name]
                    p = ParameterDescription(value, desc, unit, fmt)
                    s = template.format(parname=name, pardesc=str(p))
                    variety_yaml_stream += str(s)

    return variety_yaml_stream


def make_ecotype_yaml_stream(crop, relevant_ecotypes):
    """Build a YAML stream for parameters for given crop and ecotypes

    This routine also pulls parameters from several sources together:
    1. The original WOFOST crop parameter file
    2. The N/P/K parameters from LINTUL5
    3. the additional parameters for the vernalisation module.

    :param relevant_ecotypes: a dict of ecotype parameters: {'ecotype_name':({<parameters>}, Ctype)}
    :return: a YAML stream of ecotypes for given crop
    """

    WOFOST_NPK_params = WOFOST_nutrient_parameters[crop]

    yaml_ecotypes_stream = ""
    for ecotype_name in relevant_ecotypes:
        params, Ctype = relevant_ecotypes[ecotype_name]
        parameter_descs = {"ECOTYPE": ecotype_name, "Ctype": Ctype}
        for name in WOFOST_parameters:
            if name in params:
                value = params[name]
            elif name in WOFOST_NPK_params:
                value = WOFOST_NPK_params[name]
            elif name in add_params:
                value = add_params[name]
            else:
                raise RuntimeError("'%s' not found!" % name)
            try:
                desc, unit, fmt = param_metadata[name]
            except:
                print("Failed retrieving desc for %s" % name)
                raise
            p = ParameterDescription(value, desc, unit, fmt)
            parameter_descs[name] = str(p)

        yaml_ecotypes_stream += ecotype_template.format(**parameter_descs)

    return yaml_ecotypes_stream


def find_ecotypes_for_crop(crop):
    """Find relevant parameter files with ecotypes for given crop.
    """
    relevant_ecotypes = {}

    fnames = glob.glob(ecotypes_dir + "/*")
    for fname in fnames:
        fname = os.path.abspath(fname)
        try:
            params = CABOFileReader(fname)
            crop_name = params['CRPNAM'].strip().replace(" ", "").lower()
        except Exception as e:
            msg = "Failed parsing file: %s" % fname
            print(msg)
            raise

        if crop_name == crop:
            print("Found %s ecotype in file: %s" % (crop, fname))
            ecotype_name = params['ECOTYPE'].strip().replace(" ", "").lower()
            Ctype = "C4" if crop_name in ["sorghum", "maize", "sugarcane", "millet"] else "C3"
            relevant_ecotypes[ecotype_name] = (params, Ctype)

    return relevant_ecotypes


def build_yaml_cropfiles():

    for crop in all_crops:
        msg = "Processing crop: %s" % crop
        print(msg)

        # first find the relevant ecotypes for this crop
        relevant_ecotypes = find_ecotypes_for_crop(crop)
        if not relevant_ecotypes:
            msg = "No ecotypes found for crop: %s" % crop
            print(msg)
            continue

        # create the YAML stream with parameter values for the ecotypes for this crop
        ecotype_yaml_stream = make_ecotype_yaml_stream(crop, relevant_ecotypes)

        # Add the YAML streams for generic parameters and ecotypes together and
        # parse the entire YAML stream to access the parameters of the ecotypes.
        yaml_tmp = yaml_indent(yaml_generics_stream) + yaml_indent(ecotype_yaml_stream)
        ecotype_params = yaml.load(yaml_tmp)
        ecotypes = ecotype_params['CropParameters']['EcoTypes']

        # Create YAML crop varieties, variety parameters will be compared to the EcoType parameters
        # only in case the variety is different from the ecotype, the parameter will be added to the
        # YAML stream.
        variety_yaml_stream = make_variety_yaml_stream(crop, ecotypes)

        # Add the three different yaml streams: generics, ecotypes and varieties.
        yaml_final = yaml_indent(yaml_generics_stream) + yaml_indent(ecotype_yaml_stream) + \
                     yaml_indent(variety_yaml_stream)

        fname_crop_par_yaml = os.path.join(output_dir, crop + ".yaml")
        with open(fname_crop_par_yaml, "wb") as fp:
            fp.write(yaml_final)


if __name__ == "__main__":
    build_yaml_cropfiles()
