# ELIMINATE WRONG CHARACTER DETECTION
def deleteWrongCharacter(list_character):
    result = []
    for character in list_character:
        if character[4] >= 0.6:
            result.append(character)
    return result

# GET LINE BETWEEN 2 POINT
def linearEquation(p1, p2):
    if p1[0] == p2[0]:
        p1[0] = p2[0] + 1

    a = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - a * p1[0]
    return a, b

# CHECK PLATE TYPE (1 OR 2 LINE) AND SORT LIST CHARACTER
def sortCharacter(list_character):
    list_center = []
    list_y1y2 = []
    for character in list_character:
        center = [(character[0] + character[2]) // 2, (character[1] + character[3]) // 2]
        list_center.append(center)
        list_y1y2.append([character[1], character[3]])

    # Find 2 points to draw line
    list_center_x = [center[0] for center in list_center]
    x_min = min(list_center_x)
    x_max = max(list_center_x)
    center_x_min = list_center[list_center_x.index(x_min)]
    center_x_max = list_center[list_center_x.index(x_max)]

    a, b = linearEquation(center_x_min, center_x_max)

    # Check type and sort
    x = (x_min + x_max) // 2
    y = a*x + b
    for [y1, y2] in list_y1y2:
        if not (y > y1 and y < y2):     
            list_center_y = [center[1] for center in list_center]
            y_min = min(list_center_y)
            y_max = max(list_center_y)
            mean_y = (y_min + y_max) // 2

            line1 = []
            line2 = []
            for i in range(len(list_center)):
                if list_center[i][1] < mean_y:
                    line1.append(list_character[i])
                    line1.sort()
                else:
                    line2.append(list_character[i])
                    line2.sort()
            list_character = line1 + line2
            return list_character
    list_character.sort()
    return list_character

# SUMMARY
def getPlate(list_character):
    if not list_character:
        return ''

    list_character = deleteWrongCharacter(list_character)
    list_character = sortCharacter(list_character)

    plate = ''
    for i in range(len(list_character)):
        plate += list_character[i][6]

    return plate