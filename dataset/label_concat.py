def concat(filename):
  f= open(filename,mode= 'a')
  for i in range(33,127):
    f.write(str(chr(i))+"\n")
  f.close()

concat("./labels/2350-common-hangul.txt")
