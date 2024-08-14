import improvedmw

def main(formula, moles, lib):
    mw = float(improvedmw.main(formula, lib))
    grams = mw * float(moles)
    grams = round(grams, 3)
    return grams
