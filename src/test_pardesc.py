import yaml
r = yaml.load(open("parameter_description.yaml"))

for key in r:
    desc, units, fmt = r[key]
    if not isinstance(desc, str):
        print("1 problem with description: %s" % key)
    if isinstance(fmt, list):
        if r"%" not in fmt[0]:
            print("2 problem with format: %s" % key)
        if r"%" not in fmt[1]:
            print("3 problem with format: %s" % key)
    else:
        if r"%" not in fmt:
            print("4 problem with format: %s" % key)
