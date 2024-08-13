import improvedmw

def main(formula, moles):
    mw = float(improvedmw.main(formula))
    grams = mw * float(moles)
    grams = round(grams, 3)
    return grams
