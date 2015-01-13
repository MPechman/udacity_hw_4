import hashlib

x = hashlib.md5("test")
y = hashlib.md5("Test")
z = hashlib.sha256("test")

print x.hexdigest()
print y.hexdigest()
print z.hexdigest()