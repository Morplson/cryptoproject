import json
import os, sys, re


os.chdir(os.path.dirname(os.path.abspath(__file__)))

file = open(r'C:\Users\morpl\Documents\JS\Hackphp\tweepy\crypto_datadump.json-plus', "r");

for line in file.readlines():
	for j in re.split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line):
		print(json.dump(j))


