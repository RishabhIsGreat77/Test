print("Hello, This is RishabhIsGreat!")
import hashlib
data = "hello"
hash = hashlib.md5(data.encode()).hexdigest()
print (hash)