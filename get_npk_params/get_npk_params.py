import glob
import os
from pcse.fileinput import CABOFileReader

crop_C_types = {
    'Spring barley': 'C3',
    'Cassava': 'C3',
    'Chickpea': 'C3',
    'Cotton': 'C3',
    'Cowpea': 'C3',
    'Soybean': 'C3',
    'Faba bean': 'C3',
    'Groundnut': 'C3',
    'Maize': 'C4',
    'Millet': 'C4',
    'Mung bean': 'C3',
    'Pigeon pea': 'C3',
    'Potato': 'C3',
    'Rapeseed': 'C3',
    'Rice': 'C3',
    'Sorghum': 'C4',
    'Sugar beet': 'C3',
    'Sugarcane': 'C4',
    'Sunflower': 'C3',
    'Sweet potato': 'C3',
    'Tobacco': 'C3',
    'Winter wheat': 'C3',
    'Spring wheat': 'C3',
}


co2_var_for_C_types = {
    'C3_crops': {
        'CO2EFFTB': [40., 0.00,
                     360., 1.00,
                     720., 1.11,
                     1000., 1.11,
                     2000., 1.11],
        'CO2TRATB': [40., 0.00,
                     360., 1.00,
                     720., 0.9,
                     1000., 0.9,
                     2000., 0.9],

        'CO2AMAXTB': [40., 0.00,
                      360., 1.00,
                      720., 1.60,
                      1000., 1.90,
                      2000., 1.90]},
    'C4_crops': {
        'CO2EFFTB': [40., 0.00,
                     360., 1.00,
                     720., 1.00,
                     1000., 1.00,
                     2000., 1.00],
        'CO2TRATB': [40., 0.00,
                     360., 1.00,
                     720., 0.74,
                     1000., 0.74,
                     2000., 0.74],
        'CO2AMAXTB': [40., 0.00,
                      360., 1.00,
                      720., 1.00,
                      1000., 1.00,
                      2000., 1.00]}
}

lintul2wofost_dict = {
    'NPART': 'NPART',
    'FRPX': 'PCRIT_FR',
    'LRNR': 'NMAXRT_FR',
    'NMAXSO': 'NMAXSO',
    'PMAXSO': 'PMAXSO',
    'KMAXSO': 'KMAXSO',
    'FERNTAB': 'FERNTAB', # not in files
    'FERPTAB': 'FERPTAB', # not in files
    'FERKTAB': 'FERKTAB', # not in files
    'NRFTAB': 'NRFTAB',
    'PRFTAB': 'PRFTAB',
    'KRFTAB': 'KRFTAB',
    'NMINS': 'NSOILBASE',
    'RTNMINS': 'NSOILBASE_FR',
    'PMINS': 'PSOILBASE',
    'RTPMINS': 'PSOILBASE_FR',
    'KMINS': 'KSOILBASE',
    'RTKMINS': 'KSOILBASE_FR',
    'NMXLV': 'NMAXLV_TB',
    'PMXLV': 'PMAXLV_TB',
    'KMXLV': 'KMAXLV_TB',
    'FRNX': 'NCRIT_FR',
    'FRKX': 'KCRIT_FR',
    'LSNR': 'NMAXST_FR',
    'LRPR': 'PMAXRT_FR',
    'LSPR': 'PMAXST_FR',
    'LRKR': 'KMAXRT_FR',
    'LSKR': 'KMAXST_FR',
    'NLUE': 'NLUE_NPK',
    'TCNT': 'TCNT',
    'TCPT': 'TCPT',
    'TCKT': 'TCKT',
    'RNFLV': 'NRESIDLV',
    'RNFST': 'NRESIDST',
    'RNFRT': 'NRESIDRT',
    'RPFLV': 'PRESIDLV',
    'RPFST': 'PRESIDST',
    'RPFRT': 'PRESIDRT',
    'RKFLV': 'KRESIDLV',
    'RKFST': 'KRESIDST',
    'RKFRT': 'KRESIDRT',
    'FNTRT': 'NPK_TRANSLRT_FR',
    'NFIXF': 'NFIX_FR',
    'DVSNT': 'DVSNPK_TRANSL',
    'DVSNLT': 'DVSNPK_STOP',
    'RDRNS': 'RDRLV_NPK',
    'NLAI': 'NLAI_NPK',
    'NSLA': 'NSLA_NPK',
}

crop_path_files = glob.glob('./LINTUL_params_for_WOFOST_npk/LINTUL5_crop_files/*')

npk_dict = {}

cnt = -1
for crop_path_file in sorted(crop_path_files):
    cnt += 1
    cropdata = CABOFileReader(crop_path_file)

    cropdata['CRPNAM'] = cropdata['CRPNAM'].strip()
    cropdata['crop_id'] = cropdata['crop_id'].strip()
    cropdata['countries'] = cropdata['countries'].strip()

    CRPNAM = cropdata['CRPNAM']
    print CRPNAM

    if CRPNAM not in npk_dict:
        npk_dict[CRPNAM] = {}

    for item in cropdata:
        if item in lintul2wofost_dict:
            item_npk = lintul2wofost_dict[item]
            npk_dict[CRPNAM][item_npk] = cropdata[item]

    crop_C_type = crop_C_types[CRPNAM]

    for co2_item in co2_var_for_C_types[crop_C_type + '_crops']:
        npk_dict[CRPNAM][co2_item] = co2_var_for_C_types[crop_C_type + '_crops'][co2_item]

    npk_dict[CRPNAM]['file_name'] = os.path.basename(crop_path_file)

print npk_dict
