import sys
import improvedmw
import grams
import moles
import pbm

def main():
    mw = improvedmw.main(f"{sys.argv[1]}")
    if len(sys.argv) == 3:
        # uses molecular weight function to calculate molecular weight of the inputted formula
        if sys.argv[2].lower() == "mw":
            if mw < 0:
                return
            else:
                mw = "{:.3f}".format(mw)
                print(f"{mw} g/mol")
        else:
            print("Incorrect usage. Please refer to the README on how to use this program.")
    elif len(sys.argv) == 4:
        if sys.argv[2].lower() == "grams" or sys.argv[2].lower() == "g":
            if mw < 0:
                return
            else:
                gram = grams.main(f"{sys.argv[1]}", f"{int(sys.argv[3])}")
                gram = "{:.3f}".format(gram)
                print(f"{gram} grams")
        elif sys.argv[2].lower() == "moles" or sys.argv[2].lower == "m":
            if mw < 0:
                return
            else:
                mole = moles.main(f"{sys.argv[1]}", f"{int(sys.argv[3])}")
                mole = "{:.3f}".format(mole)
                print(f"{mole} moles")
        elif sys.argv[2].lower() == "pbm":
            if mw < 0:
                return
            else:
                percent, elementmw = pbm.main(f"{sys.argv[1]}", f"{sys.argv[3]}")
                if percent < 0:
                    return
                else:
                    percent = "{:.3f}".format(percent)
                    formulamw = improvedmw.main(f"{sys.argv[1]}")
                    formulamw = "{:.3f}".format(formulamw)
                    elementmw = "{:.3f}".format(elementmw)
                    print(f"{percent}% ({elementmw} g/mol out of {formulamw} g/mol)")
        else:
            print("Incorrect usage. Please refer to the README on how to use this program.")
    else:
        print("Incorrect usage. Please refer to the README on how to use this program.")

main()
