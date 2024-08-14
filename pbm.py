import improvedmw


def subcheck(elementlen, element):
    for j in range(elementlen):
        if element[j].isnumeric():
             return True
    return False


def parencheck(k, elementlen, formlen, formula):
    l = k + elementlen
    while l < formlen:
        if formula[l] == "(":
            return False
        elif formula[l] == ")":
            return True
        else:
            l += 1
    return False


def parensub(k, elementlen, formlen, formula):
    l = k + elementlen
    while l < formlen:
        if formula[l] == ")":
            if l + 1 == formlen - 1 or not formula[l + 2].isnumeric():
                return int(formula[l + 1])
            elif formula[l + 2].isnumeric():
                return int(formula[l + 1:l + 3])
        l += 1



def main(formula, element):
    formlen = len(formula)
    elementlen = len(element)
    if elementlen > formlen:
        print("Error in defining the formula or the element that you are calculating for")
        return -1, None
    elif (elementlen < 1 and elementlen > 2) or (elementlen == 2 and element[1].isupper()):
        print("You may only select one element at a time to find the percent by mass")
        return -2, None
    else:
        # checks if the element includes any subscripts
        if subcheck(elementlen, element) == True:
            print("You have included a subscript in the element you are calulating for. Please do not do that; this program will calculate the entire percent by mass of whatever element you are looking for.")
            return -3, None
        else:
            # if we've gotten to this point there are no subscripts
            count = 0
            countinside = []
            k = 0
            # we must separate between 2 lettered elements and 1 lettered elements
            # this is 2 lettered elements
            if elementlen == 2:
                # count how many times the part comes up in the formula
                while (k + 1) < formlen:
                    if formula[k:(k + 2)] == element:
                        # checks if the element doesn't have a subscript
                        if (k + 1) == formlen - 1 or formula[k + 2].isalpha() or formula[k + 2] == ")" or formula[k + 2] == "(":
                            # checks if its within ()
                            if parencheck(k, 2, formlen, formula) == False:
                                count += 1
                                k += 1
                            elif parencheck(k, 2, formlen, formula) == True:
                                subscript = parensub(k, 2, formlen, formula)
                                countinside.append(subscript)
                                k += 1
                        # checks if element does have a subscript
                        elif formula[k + 2].isnumeric():
                            if k + 2 == formlen - 1 or not formula[k + 3].isnumeric():
                                subelement = int(formula[k + 2])
                            elif formula[k + 3].isnumeric():
                                subelement = int(formula[k + 2:k + 4])
                            # checks if the element is within ()
                            if parencheck(k, 2, formlen, formula) == False:
                                count += subelement
                                k += 1
                            elif parencheck(k, 2, formlen, formula) == True:
                                subparen = parensub(k, 2, formlen, formula)
                                countinside.append(subelement * subparen)
                                k += 1
                    else:
                        k += 1
            # this is 1 lettered elements
            elif elementlen == 1:
                # count how many times the part comes up in the formula
                while k < formlen:
                    if formula[k] == element and (k == formlen - 1 or formula[k + 1].isupper() or formula[k + 1] == ")" or formula[k + 1].isnumeric() or formula[k + 1] == "("):
                        # checks if the element doesn't have a subscript
                        if k == formlen - 1 or formula[k + 1].isalpha() or formula[k + 1] == ")" or formula[k + 1] == "(":
                            # checks if its within ()
                            if parencheck(k, 1, formlen, formula) == False:
                                count += 1
                                k += 1
                            elif parencheck(k, 1, formlen, formula) == True:
                                subscript = parensub(k, 1, formlen, formula)
                                countinside.append(subscript)
                                k += 1
                        # checks if element does have a subscript
                        elif formula[k + 1].isnumeric():
                            if k + 1 == formlen - 1 or not formula[k + 2].isnumeric():
                                subelement = int(formula[k + 1])
                            elif formula[k + 2].isnumeric():
                                subelement = int(formula[k + 1:k + 3])
                            # checks if the element is within ()
                            if parencheck(k, 1, formlen, formula) == False:
                                count += subelement
                                k += 1
                            elif parencheck(k, 1, formlen, formula) == True:
                                subparen = parensub(k, 1, formlen, formula)
                                countinside.append(subelement * subparen)
                                k += 1
                    # this would be the case where the letter is the start of a 2 lettered element in the formula
                    else:
                        k += 1




            totalmw = float(improvedmw.main(formula))
            elementmw = float(improvedmw.main(element))
            count += sum(countinside)
            elementmw = elementmw * count
            if elementmw == 0:
                print("It seems that you have not chosen an element which is part of the formula.")
                return -4, None
            else:
                pbm = (elementmw / totalmw) * 100
                pbm = round(pbm, 3)
                return pbm, elementmw

