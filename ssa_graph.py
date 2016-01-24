from ssa_collector import Tweet_clt as clt
import re

lista = open("list", 'r')
lista=lista.read().split()
print lista

followers={}
clt=clt()
clt.userdb.drop()

for usr in lista:
    followers[usr]=clt.get_followers(usr)
    clt.userdb.insert({usr:followers[usr]})
