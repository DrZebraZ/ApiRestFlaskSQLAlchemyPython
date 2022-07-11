import string


def VerifyEmptyStr(string):
  res = string.replace(" ","")
  if (res == '' or res.isspace() or res==" "):
    print("ta vazia", True)
    return True
  else:
    print("n ta vazia", False)
    return False

def DeleteDoubleSpaces(string):
  for i in range(len(string)):
    res = string.replace("  "," ")
    string = res
  return res.strip()