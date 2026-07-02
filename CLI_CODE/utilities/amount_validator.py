#! For validating if user's entered income/expense amount is a float
def isItFloat(val):
    try:
        check = float(val)
    except:
        hasFloat = False
    else:
        hasFloat = True
    return hasFloat
