"""
Ce module permet de reconnaitre les emotions sur une image ou une video
"""
import operator
import cv2
from face_detect import findfaces, locatefaces

def emotionspresent(model, sourcefilepath, filteremotion):
    """
    Cette fonction permet de recuperer les emotions presentes
    :param model: Matrice XML des emotions
    :param sourcefilepath: Source du fichier
    :param filteremotion: Filtre des emotions selectionnes
    """
    dict_emotion = {"Neutre": 0, "Enerve": 0, "Degout": 0,
                    "Joyeux": 0, "Triste": 0, "Surpris": 0}
    bmatch = False

    readsource = cv2.VideoCapture(sourcefilepath)
    if readsource.isOpened():
        read_value, webcam_image = readsource.read()
    else:
        return

    faces = len(locatefaces(webcam_image))
    while read_value:
        for normalized_face, (x_coord, y_coord, w_coord, h_coord) in findfaces(webcam_image):
            prediction = model.predict(normalized_face)
            if cv2.__version__ != '3.1.0':
                prediction = prediction[0]

            if prediction == 0:
                dict_emotion["Neutre"] += 1
            if prediction == 1:
                dict_emotion["Enerve"] += 1
            if prediction == 2:
                dict_emotion["Degout"] += 1
            if prediction == 3:
                dict_emotion["Joyeux"] += 1
            if prediction == 4:
                dict_emotion["Triste"] += 1
            if prediction == 5:
                dict_emotion["Surpris"] += 1

            drawrectangle(webcam_image, (x_coord, y_coord,
                                         w_coord, h_coord), sourcefilepath)
        read_value, webcam_image = readsource.read()

        dict_emotion = sorted(dict_emotion.iteritems(),
                              key=operator.itemgetter(1), reverse=True)

        if filteremotion:
            bmatch = emotionsmatch(dict_emotion, filteremotion)

        return dict_emotion, faces, bmatch


def emotionsmatch(dictemotion, indexchoose):
    """
    Cette fonction permet de determiner si les emotions presentes sont celles selectionnees
    :param dictemotion: Liste des emotions
    :param indexchoose: Index des emotions choisis
    """
    position_1, position_2, position_3, position_4, position_5, position_6 = positionemotion(
        dictemotion)

    if len(indexchoose) == 1:
        b_match = bool(indexchoose[0] in position_1.keys())

    if len(indexchoose) == 2:
        for index in indexchoose:
            if index in position_1.keys() or index in position_2.keys():
                b_match = True
            else:
                b_match = False
                break

    if len(indexchoose) == 3:
        for index in indexchoose:
            if index in position_1.keys() or index in position_2.keys() or index in position_3.keys():
                b_match = True
            else:
                b_match = False
                break

    if len(indexchoose) == 4:
        for index in indexchoose:
            if index in position_1.keys() or index in position_2.keys() or index in position_3.keys() or index in position_4.keys():
                b_match = True
            else:
                b_match = False
                break

    if len(indexchoose) == 5:
        for index in indexchoose:
            if index in position_1.keys() or index in position_2.keys() or index in position_3.keys() or index in position_4.keys() or index in position_5.keys():
                b_match = True
            else:
                b_match = False
                break

    if len(indexchoose) == 6:
        for index in indexchoose:
            if index in position_1.keys() or index in position_2.keys() or index in position_3.keys() or index in position_4.keys() or index in position_5.keys() or index in position_6.keys():
                b_match = True
            else:
                b_match = False
                break

    return b_match

def positionemotion(dictemotion):
    """
    Cette fonction permet de determiner les position des emotions presentes
    :param dictemotion: Liste des emotions
    """
    position_1 = {}
    position_2 = {}
    position_3 = {}
    position_4 = {}
    position_5 = {}
    position_6 = {}

    for emotion in dictemotion:
        b_use = False
        if emotion[1] != 0:
            if len(position_1.keys()) >= 0:
                if len(position_1.keys()) == 0:
                    position_1[emotion[0]] = emotion[1]
                else:
                    for value in position_1.values():
                        if value == emotion[1]:
                            position_1[emotion[0]] = emotion[1]
                            b_use = True
                        else:
                            break
                    if len(position_2.keys()) >= 0 and not b_use:
                        if len(position_2.keys()) == 0:
                            position_2[emotion[0]] = emotion[1]
                        else:
                            for value in position_2.values():
                                if value == emotion[1]:
                                    position_2[emotion[0]] = emotion[1]
                                    b_use = True
                                else:
                                    break
                            if len(position_3.keys()) >= 0 and not b_use:
                                if len(position_3.keys()) == 0:
                                    position_3[emotion[0]] = emotion[1]
                                else:
                                    for value in position_3.values():
                                        if value == emotion[1]:
                                            position_3[emotion[0]] = emotion[1]
                                            b_use = True
                                        else:
                                            break
                                    if len(position_4.keys()) >= 0 and not b_use:
                                        if len(position_4.keys()) == 0:
                                            position_4[emotion[0]] = emotion[1]
                                        else:
                                            for value in position_4.values():
                                                if value == emotion[1]:
                                                    position_4[emotion[0]] = emotion[1]
                                                    b_use = True
                                                else:
                                                    break
                                            if len(position_5.keys()) >= 0 and not b_use:
                                                if len(position_5.keys()) == 0:
                                                    position_5[emotion[0]] = emotion[1]
                                                else:
                                                    for value in position_5.values():
                                                        if value == emotion[1]:
                                                            position_5[emotion[0]] = emotion[1]
                                                            b_use = True
                                                        else:
                                                            break
                                                    if len(position_6.keys()) >= 0 and not b_use:
                                                        if len(position_6.keys()) == 0:
                                                            position_6[emotion[0]] = emotion[1]
                                                        else:
                                                            for value in position_6.values():
                                                                if value == emotion[1]:
                                                                    position_6[emotion[0]] = emotion[1]
                                                                else:
                                                                    break
        else:
            break

    return position_1, position_2, position_3, position_4, position_5, position_6


def emotionscount(dictemotion):
    """
    Cette fonction permet de retourner le nombre d'emotion detecte
    :param dictemotion: Liste des emotions
    """
    emotion_count = 0
    for emotion in dictemotion:
        emotion_count += emotion[1]
    if emotion_count == 0:
        emotion_count = 1
    return emotion_count


def drawrectangle(sourceimage, coordinatesface, sourcefilepath):
    """
    Cette fonction dessine un rectangle sur un visage.
    :param sourceimage: Source de l'image.
    :param coordinatesface: Coordonnees du visage.
    :param sourcefilepath: chemin du fichier
    """
    x_coord, y_coord, w_coord, h_coord = coordinatesface
    cv2.rectangle(sourceimage, (x_coord, y_coord),
                  (x_coord + w_coord, y_coord + h_coord), 255, 2)
    cv2.imwrite(sourcefilepath, sourceimage)
