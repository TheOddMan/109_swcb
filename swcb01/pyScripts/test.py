s = "土石流潛勢溪流(高坔市DF051)於8月7日晚間爆發土石流"
a = '土石流潛勢溪流(高市DF051)於8月7日晚間爆發土石流'
try:
    print(s.encode('cp950'))
except UnicodeEncodeError as e:
    print(e.start)
    s = list(s)
    s[e.start] = '?'
    s = "".join(s)
    print(s)