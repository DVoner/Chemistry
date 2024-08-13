import improvedmw

def main(formula, grams):
    mw = float(improvedmw.main(formula))
    moles = mw * (1 / float(grams))
    moles = round(moles, 3)
    return moles
