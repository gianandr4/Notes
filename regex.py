import re

# find the numbers between brackets -> [ ]
txt = 'agda [12345] [12342]'
regex = r'\[(\d+)\]'

# Return first match
result = re.search(regex,txt)
result[1] # 12345

# Return all matches
result = re.findall(regex,txt)
result[0] # 12345
result[1] # 12342


