import sys
import csv
import sqlite3

def main(formula):
  length = len(formula)
  MW = 0
  if formula[length - 1] == "+" or formula[length - 1] == "-":
    print("This program does not support the use of ions to calulate molecular weight. Note that the molecular weight of ions is the same as that of their non-ionic counterpart.")
    return
  else:
    for i in length - 1:
      if formula[i].isupper() and formula[i+1].islower():  # checks if the element is 2 letters
        with open('values.csv') as csvfile:
          data = csv.reader(csvfile)
          for row in data:
            if row[0] == formula[i:i+1]:
              MW += row[1]
      elif formula[i].islower():
        MW += 0
      elif formula[i].isupper() and formula[i+1].isupper(): #checks if element is 1 letter
        with open('values.csv') as csvfile:
          data = csv.reader(csvfile)
          for row in data:
            if row[0] == formula[i]:
              MW += row[1]
      elif formula[i] == NULL:
        return MW
