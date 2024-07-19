import logging

def string2integerList(in_str):
    """
    Convert a string to a list of integers.
    a -> [a]
    b -> [b]
    a:b -> [a,...,b]
    These expression can be combined.
    a b c:d e e:f -> [a,b,c,...,d,e,...,f] (duplicate elements are removed)
    """

    logger = logging.getLogger("VLMP")

    if in_str.strip() == "":
        return []

    # Check if there is any invalid character
    # Only whitespace, numbers and ':' are allowed
    for c in in_str:
        if not c.isdigit() and c != ':' and not c.isspace():
            logger.error("Invalid character in the input string: %s" % c)
            raise ValueError("Invalid character")

    processed_str = in_str.split()
    processed_str = [x.strip() for x in processed_str]

    # Check if some expression contains ':', then it must be surrounded by numbers

    for i in range(len(processed_str)):
        if ':' in processed_str[i]:
            if not processed_str[i][0].isdigit() or not processed_str[i][-1].isdigit():
                logger.error("Invalid expression: %s" % processed_str[i])
                raise ValueError("Invalid expression")

    # Convert the string to a list of integers
    interger_list = []
    for expression in processed_str:
        if ':' in expression:
            start, end = expression.split(':')
            start = int(start)
            end = int(end)
            interger_list += list(range(start, end + 1))
        else:
            interger_list.append(int(expression))

    return sorted(list(set(interger_list))) # Remove duplicate elements and sort the list


