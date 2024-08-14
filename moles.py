import improvedmw

def main(formula, grams, lib):
    mw = float(improvedmw.main(formula, lib))
    moles = mw * (1 / float(grams))
    moles = round(moles, 3)
    return moles
