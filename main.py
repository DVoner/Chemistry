import sys
import MW.py

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py function formula")
    
    # uses molecular weight function to calculate molecular weight of the inputted formula
    if sys.argv[2] == MW:
        MW.main(argv[1])
        return
    
