byte_object= b"test" # byte object by literally typing characters
print(byte_object) # Prints b'test'
print(byte_object.decode('utf8')) # Prints "test" without quotations
# initializing integer and iterables 
a = 4
lis1 = [1, 2, 3, 4, 5] 
  
# No argument case 
print ("Byte conversion with no arguments : " + str(bytes()))  
  
# conversion to bytes  
print ("The integer conversion results in : "  + str(bytes(a))) 
print ("The iterable conversion results in : "  + str(bytes(lis1))) 
