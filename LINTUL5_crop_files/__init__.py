import sys, os
import glob
from pcse.fileinput import CABOFileReader
param_name_mapping = {
    "DVSNLT":"DVS_NPK_STOP",
    "DVSNT":"DVS_NPK_TRANSL",
    "FNTRT":"NPK_TRANSLRT_FR",
    "FRKX":"KCRIT_FR",
    "FRNX":"NCRIT_FR",
    "FRPX":"PCRIT_FR",
    "KMAXSO":"KMAXSO",
    "KMXLV":"KMAXLV_TB",
    "LRKR":"KMAXRT_FR",
    "LRNR":"NMAXRT_FR",
    "LRPR":"PMAXRT_FR",
    "LSKR":"KMAXST_FR",
    "LSNR":"NMAXST_FR",
    "LSPR":"PMAXST_FR",
    "NFIXF":"NFIX_FR",
    "NLUE":"NLUE_NPK",
    "NMAXSO":"NMAXSO",
    "NMXLV":"NMAXLV_TB",
    "PMAXSO":"PMAXSO",
    "PMXLV":"PMAXLV_TB",
    "RKFLV":"KRESIDLV",
    "RKFRT":"KRESIDRT",
    "RKFST":"KRESIDST",
    "RNFLV":"NRESIDLV",
    "RNFRT":"NRESIDRT",
    "RNFST":"NRESIDST",
    "RPFLV":"PRESIDLV",
    "RPFRT":"PRESIDRT",
    "RPFST":"PRESIDST",
    "TCKT":"TCKT",
    "TCNT":"TCNT",
    "TCPT":"TCPT",
    "RDRNS":"RDRLV_NPK",
    "NLAI ":"NLAI_NPK",
    "NSLA ":"NSLA_NPK",
	"NPART":"NPART"}

LINTUL5_dir = os.path.dirname(__file__)
WOFOST_nutrient_parameters = {}
for fname in glob.glob(LINTUL5_dir + "/*.DATp"):
    fname = os.path.abspath(fname)
    try:
        params = CABOFileReader(fname)
    except:
        msg = "Failed reading: %s" % fname
        print(msg)
        raise
    ecotype = params['ECOTYPE']
    tmp = {}
    for LINTUL_parname, WOFOST_parname in param_name_mapping.items():
        try:
            tmp[WOFOST_parname.strip()] = params[LINTUL_parname.strip()]
        except KeyError:
            msg = "failed retrieving parameter (%s: %s)" % (LINTUL_parname, WOFOST_parname)
            print(msg)
            raise
    WOFOST_nutrient_parameters[ecotype] = tmp

