list = [22, "tv', 2.11, 'wow", True, 33, [1,2], None] 
fool = dict()
for i in list:
    try:
        fool[i] = 1

    except: pass
print (fool)