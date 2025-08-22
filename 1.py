import re
m = re.fullmatch(r'^[A-Z][a-z]+$', "Kyiv1")
print(bool(re.fullmatch(r'^[A-Z][a-z]+$', "Kyiv1")))