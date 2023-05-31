from ast import *
import astor

print(astor.to_source(eval(open('license_checker.ast').read())))
