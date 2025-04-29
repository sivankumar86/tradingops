a=["k","v","k1","v1"]
k=a[::2]
v=a[1::2]
d=dict(zip(k,v))
print(d["k"])

