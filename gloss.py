#!/usr/bin/env python3

import string
import sys
import re

glossTemplate = string.Template("*[$k]: $v")
usage = "Usage: gloss <type> <word> <pluralizer> <definition>\n"
exampleUsage = "gloss def ReplicaSet s \"a management layer over pods\""
typeInfo = "type: (abbr | def)\n"
abbrInfo = " - abbr e.g.: aks -> (aks, AKS)\n"
defInfo = " - def e.g.: pod -> (pod, Pod, pods, Pods)\n"
multiCapNote = "   NOTE: for entries with multiple capital letters e.g. ReplicaSet, enter it that way."
usageMessage = usage + exampleUsage + typeInfo + abbrInfo + defInfo + multiCapNote

def printUsage():
	print(usageMessage)

tokenizedInput = sys.argv
normalizedInput = sys.argv[1:]
if(len(normalizedInput)) == 0:
	printUsage()
	sys.exit(0)

type = normalizedInput[0]
word = normalizedInput[1]
pluralizer = normalizedInput[2]
definition = normalizedInput[3]

def wordHasMultiCaps(word):
	capital_letters = re.findall(r'[A-Z]', word)
	if(len(capital_letters) > 1):
		return True
	else:
		return False
	

def getAbbrKeys(word):
	lowerWordSingular = word.lower()
	upperWordPlural = word.upper()
	lowerWordPlural = lowerWordSingular + "s"
	upperWordSingular = upperWordPlural + "s"
	return [lowerWordSingular, lowerWordPlural, upperWordPlural, upperWordSingular]

def getDefKeys(word):
	entries = []
	uncap = word.lower()
	entries.append(uncap)
	entries.append(uncap + "s")
	capitalized = uncap.capitalize()
	entries.append(capitalized)
	entries.append(capitalized + "s")

	if(wordHasMultiCaps(word)):
		entries.append(word)
		entries.append(word + "s")
	return entries
	
entries = getAbbrKeys(word) if(type == "abbr") else getDefKeys(word)

def writeToAbbr(entries):
	with open("./glossary/abbreviations.md", "a") as file:
		file.write("\n")
		for entry in entries:
			output = glossTemplate.substitute(k=entry, v=definition) + "\n"
			file.write(output)

def writeToDef(entries):
	with open("glossary/definitions.md", "a") as file:
		file.write("\n")
		for entry in entries:
			output = glossTemplate.substitute(k=entry, v=definition) + "\n"
			file.write(output)

if(type == "abbr"):
	writeToAbbr(entries)
else:
	writeToDef(entries)
