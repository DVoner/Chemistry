import csv

def main(formula, lib):
    length = len(formula)
    mw, valinside, opencount, closecount = 0, 0, 0, 0
    starts = []
    closes = []
    psubs = []


    # check for ions
    if formula[length - 1] == "+" or formula[length - 1] == "-":
        print("This program does not support the use of ions to calulate molecular weight. Note that the molecular weight of ions is the same as that of their non-ionic counterpart.")
        return -1

    else:

        # Do all ()subscript work first, noting where ( is as the starting point and where the subscript is as the end point

        # count number of () where it is followed by a subscript
        for i in range(length):
            if formula[i] == "(":
                opencount += 1
            elif i != length - 1 and formula[i] == ")" and formula[i + 1].isnumeric():
                closecount += 1
            elif i != length - 1 and formula[i] == ")" and not formula[i + 1].isnumeric():
                print("Sorry, this program does not support the use of parentheses when there is no subscript following them.")
                return -2
            elif i == length - 1 and formula[i] == ")":
                print("Sorry, this program does not support the use of parentheses when there is no subscript following them.")
                return -2
        if opencount != closecount:
            print("There was an error in your formula concerning parentheses.")
            return -3
        else:

            # adds the start and end of parentheses to lists
            for i in range(length):
                if formula[i] == "(":
                    starts.append(f"{i}")
                elif formula[i] == ")":
                    if i + 1 == length - 1 or not formula[i + 2].isnumeric():
                        closes.append(f"{i + 1}")
                        psubs.append(f"{int(formula[i + 1])}")
                    elif formula[i + 2].isnumeric():
                        closes.append(f"{i + 2}")
                        psubs.append(f"{int(formula[i + 1:i + 3])}")


        # we now have lists of where parentheses open, close, and the subscripts next to them

        # if there are parentheses
        if opencount != 0:
            # loop through the lists of parentheses
            for i in range(opencount):
                valinside = 0

                # when j (the letter we're on in the formula) is between the parentheses, get the value of MW between the parentheses
                j = int(starts[i])
                while j >= int(starts[i]) and j < int(closes[i]):

                    #checks if element is 1 letter or if we're at the end of the formula
                    if formula[j].isupper() and (formula[j + 1] == ")" or formula[j + 1].isupper()):
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[j]:
                                    valinside += float(row[lib])
                                    j += 1
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # checks if the element is 2 letters
                    elif formula[j].isupper() and formula[j + 1].islower():
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[j:j+2]:
                                    valinside += float(row[lib])
                                    j += 1
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # if it is lowercase or a parenthese or a number, don't do anything
                    # if the letter is lowercase then it is part of a two letter element, which has already been taken care of
                    elif formula[j].islower() or formula[j] == "(" or formula[j] == ")" or (formula[j].isupper() and formula[j+1].isnumeric()):
                        valinside += 0
                        j += 1
                    # checks if it is a subscript
                    elif formula[j].isnumeric():
                        # checks if the subscript is 1 or 2 digits
                        if formula[j + 1].isnumeric():
                            subscript = int(formula[j:j+2])
                        else:
                            subscript = int(formula[j])
                        if j == 0:
                            print("Sorry, this program only supports one molecular formula at a time without coefficients.")
                            return -4
                        # checks if it is a subscript of just a single one-letter element
                        elif formula[j - 1].isalpha() and formula[j - 1].isupper():
                            with open('values.csv') as csvfile:
                                data = csv.reader(csvfile)
                                for row in data:
                                    if row[0] == formula[j - 1]:
                                        element = float(row[lib])
                                        valinside += element * subscript
                                        j += 1
                                        break
                                    if row[0] == "error":
                                        print("Invalid formula")
                                        return -6
                        # checks if it is a subscript of just a single two-letter element
                        elif formula[j - 1].isalpha() and formula[j - 1].islower():
                            with open('values.csv') as csvfile:
                                data = csv.reader(csvfile)
                                if j - 1 == 0:
                                    print("Error: You have started with a lowercase letter. Note that this program is case-sensitive in order to determine the elements in the formula.")
                                    return -5
                                for row in data:
                                    if row[0] == formula[(j - 2):(j)]:
                                        element = float(row[lib])
                                        valinside += element * subscript
                                        j += 1
                                        break
                                    if row[0] == "error":
                                        print("Invalid formula")
                                        return -6
                        elif formula[j - 1].isnumeric() or formula[j - 1] == ")":
                            valinside += 0
                            j += 1


                # add to MW
                mw += valinside * int(psubs[i])

            # Do all non () work, skipping the addition of whatever is in the () TODO
            # might want to do this: have a loop start at the beginning or wherever the last ) was and end at the next ( or the end, and add the MWs for that
            # this might include one big loop containing some smaller loops
            # might break it into: get MW until first (, then get MW using below loop? while there are still (), then get MW from last ) until end
            for i in range(int(starts[0])):
                #checks if element is 1 letter or if we're at the end of the formula
                if formula[i].isupper() and (i == length - 1 or formula[i + 1].isupper()):
                    with open('values.csv') as csvfile:
                        data = csv.reader(csvfile)
                        for row in data:
                            if row[0] == formula[i]:
                                mw += float(row[lib])
                                break
                            if row[0] == "error":
                                print("Invalid formula")
                                return -6
                # checks if the element is 2 letters
                elif formula[i].isupper() and formula[i + 1].islower():
                    with open('values.csv') as csvfile:
                        data = csv.reader(csvfile)
                        for row in data:
                            if row[0] == formula[i:i+2]:
                                mw += float(row[lib])
                                break
                            if row[0] == "error":
                                print("Invalid formula")
                                return -6
                # if the letter is lowercase then it is part of a two letter element, which has already been taken care of
                elif formula[i].islower():
                    mw += 0
                # checks if it is a subscript
                elif formula[i].isnumeric():
                    # checks if the subscript is 1 or 2 digits
                    if formula[i + 1].isnumeric():
                        subscript = int(formula[i:i+2])
                    else:
                        subscript = int(formula[i])
                    if i == 0:
                        print("Sorry, this program only supports one molecular formula at a time without coefficients.")
                        return -4
                    # checks if it is a subscript of just a single one-letter element
                    elif formula[i - 1].isalpha() and formula[i - 1].isupper():
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[i - 1]:
                                    element = float(row[lib])
                                    mw += element * subscript
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # checks if it is a subscript of just a single two-letter element
                    elif formula[i - 1].isalpha() and formula[i - 1].islower():
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            if i - 1 == 0:
                                print("Error: You have started with a lowercase letter. Note that this program is case-sensitive in order to determine the elements in the formula.")
                                return -5
                            for row in data:
                                if row[0] == formula[(i - 2):(i)]:
                                    element = float(row[lib])
                                    mw += element * subscript
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    elif formula[i - 1].isnumeric():
                        mw += 0

            j = int(closes[0]) + 1
            l = 1
            while l < opencount:
                while j < int(starts[l]):
                    # get MW
                    #checks if element is 1 letter or if we're at the end of the formula
                    if formula[j].isupper() and (j == int(starts[l]) - 1 or formula[j + 1].isupper()):
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[j]:
                                    mw += float(row[lib])
                                    j += 1
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # checks if the element is 2 letters
                    elif formula[j].isupper() and formula[j + 1].islower() and (j == int(starts[l]) - 2 or formula[j + 1].isupper()):
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[j:j+2]:
                                    mw += float(row[lib])
                                    j += 1
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # if the letter is lowercase then it is part of a two letter element, which has already been taken care of
                    elif formula[j].islower() or (formula[j].isupper() and formula[j + 1].isnumeric()) or (formula[j].isupper() and formula[j + 1].islower() and formula[j + 2].isnumeric()):
                        mw += 0
                        j += 1
                    # checks if it is a subscript
                    elif formula[j].isnumeric():
                        # checks if the subscript is 1 or 2 digits
                        if formula[j + 1].isnumeric():
                            subscript = int(formula[j:j+2])
                        else:
                            subscript = int(formula[j])
                        # checks if it is a subscript of just a single one-letter element
                        if formula[j - 1].isalpha() and formula[j - 1].isupper():
                            with open('values.csv') as csvfile:
                                data = csv.reader(csvfile)
                                for row in data:
                                    if row[0] == formula[j - 1]:
                                        element = float(row[lib])
                                        mw += element * subscript
                                        j += 1
                                        break
                                    if row[0] == "error":
                                        print("Invalid formula")
                                        return -6
                        # checks if it is a subscript of just a single two-letter element
                        elif formula[j - 1].isalpha() and formula[j - 1].islower():
                            with open('values.csv') as csvfile:
                                data = csv.reader(csvfile)
                                if j - 1 == "(":
                                    print("Error: You have started with a lowercase letter. Note that this program is case-sensitive in order to determine the elements in the formula.")
                                    return -5
                                for row in data:
                                    if row[0] == formula[(j - 2):(j)]:
                                        element = float(row[lib])
                                        mw += element * subscript
                                        j += 1
                                        break
                                    if row[0] == "error":
                                        print("Invalid formula")
                                        return -6
                        elif formula[j].isnumeric():
                            mw += 0
                            j += 1
                j = int(closes[l])
                l += 1
            k = int(closes[closecount - 1]) + 1
            while k < length:
                #checks if element is 1 letter or if we're at the end of the formula
                if formula[k].isupper() and (k == length - 1 or formula[k + 1].isupper()):
                    with open('values.csv') as csvfile:
                        data = csv.reader(csvfile)
                        for row in data:
                            if row[0] == formula[k]:
                                mw += float(row[lib])
                                k += 1
                                break
                            if row[0] == "error":
                                print("Invalid formula")
                                return -6
                # checks if the element is 2 letters
                elif formula[k].isupper() and formula[k + 1].islower() and (k == length - 2 or formula[k + 2].isupper()):
                    with open('values.csv') as csvfile:
                        data = csv.reader(csvfile)
                        for row in data:
                            if row[0] == formula[k:k+2]:
                                mw += float(row[lib])
                                k += 1
                                break
                            if row[0] == "error":
                                print("Invalid formula")
                                return -6
                # if the letter is lowercase then it is part of a two letter element, which has already been taken care of
                elif formula[k].islower() or (formula[k].isupper() and formula[k + 1].isnumeric()) or (formula[k].isupper() and formula[k + 1].islower() and formula[k + 2].isnumeric()):
                    mw += 0
                    k += 1
                # checks if it is a subscript
                elif formula[k].isnumeric():
                    # checks if the subscript is 1 or 2 digits
                    if k == length - 1 or not formula[k + 1].isnumeric():
                        subscript = int(formula[k])
                    elif formula[k + 1].isnumeric():
                        subscript = int(formula[k:k+2])
                    # checks if it is a subscript of just a single one-letter element
                    if formula[k - 1].isalpha() and (formula[k - 1].isupper() or formula[k - 1] == "("):
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[k - 1]:
                                    element = float(row[lib])
                                    mw += element * subscript
                                    k += 1
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # checks if it is a subscript of just a single two-letter element
                    elif formula[k - 1].isalpha() and formula[k - 1].islower():
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            if k - 1 == 0:
                                print("Error: You have started with a lowercase letter. Note that this program is case-sensitive in order to determine the elements in the formula.")
                                return -5
                            for row in data:
                                if row[0] == formula[(k - 2):(k)]:
                                    element = float(row[lib])
                                    mw += element * subscript
                                    k += 1
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    elif formula[k - 1].isnumeric():
                        mw += 0
                        k += 1


        # if there are not parentheses
        else:
            for i in range(length):
                #checks if element is 1 letter or if we're at the end of the formula
                if formula[i].isupper() and (i == length - 1 or formula[i + 1].isupper()):
                    with open('values.csv') as csvfile:
                        data = csv.reader(csvfile)
                        for row in data:
                            if row[0] == formula[i]:
                                mw += float(row[lib])
                                break
                            if row[0] == "error":
                                print("Invalid formula")
                                return -6
                # checks if the element is 2 letters
                elif formula[i].isupper() and formula[i + 1].islower() and (i + 1 == length - 1 or formula[i + 2].isalpha()):
                    with open('values.csv') as csvfile:
                        data = csv.reader(csvfile)
                        for row in data:
                            if row[0] == formula[i:i+2]:
                                mw += float(row[lib])
                                break
                            if row[0] == "error":
                                print("Invalid formula")
                                return -6
                # if the letter is lowercase then it is part of a two letter element, which has already been taken care of
                elif formula[i].islower():
                    mw += 0
                # checks if it is a subscript
                elif formula[i].isnumeric():
                    if i == length - 1 or not formula[i + 1].isnumeric():
                        subscript = int(formula[i])
                    elif formula[i + 1].isnumeric():
                        subscript = int(formula[i:i + 2])
                    if i == 0:
                        print("Sorry, this program only supports one molecular formula at a time without coefficients.")
                        return -4
                    # checks if it is a subscript of just a single one-letter element
                    elif formula[i - 1].isalpha() and formula[i - 1].isupper():
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            for row in data:
                                if row[0] == formula[i - 1]:
                                    element = float(row[lib])
                                    mw += element * subscript
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    # checks if it is a subscript of just a single two-letter element
                    elif formula[i - 1].isalpha() and formula[i - 1].islower():
                        with open('values.csv') as csvfile:
                            data = csv.reader(csvfile)
                            if i - 1 == 0:
                                print("Error: You have started with a lowercase letter. Note that this program is case-sensitive in order to determine the elements in the formula.")
                                return -5
                            for row in data:
                                if row[0] == formula[(i - 2):(i)]:
                                    element = float(row[lib])
                                    mw += element * subscript
                                    break
                                if row[0] == "error":
                                    print("Invalid formula")
                                    return -6
                    elif formula[i - 1].isnumeric():
                        mw += 0
        mw = round(mw, 3)
        if mw == 0:
            print("Invalid formula")
            return -6
        else:
            return mw
