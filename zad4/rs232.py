# -*- coding: ascii -*-

FRAME = 11


def start_bit(char, add):
    if add:
        char = '0' + char
        return char
    else:
        return char[1:]


def stop_bits(char, add):
    if add:
        char += '11'
        return char
    else:
        return char[:-2]


def delete_frame(char):
    char = start_bit(char, False)
    char = stop_bits(char, False)
    return char


def send(sentence):
    frame = 'f'
    for char in sentence:
        char = bin(ord(char))[2:]
        if len(char) < 8:
            for i in range(0, 8 - len(char)):
                char = '0' + char
        char = char[::-1]
        char = start_bit(char, True)
        char = stop_bits(char, True)
        for c in char:
            frame += c
    return frame[1:]


def divideString(string):
    chars = []
    for i in range(0, int(len(string) / FRAME)):
        char = 'f'
        for j in range(i * FRAME, i * FRAME + FRAME):
            char += str(string[j])
        chars.append(char[1:])
    return chars


def decode(string):
    chars = divideString(string)
    charsWithoutStartAndStopBits = []
    for c in chars:
        charsWithoutStartAndStopBits.append(delete_frame(c))
    ints = []
    for c in charsWithoutStartAndStopBits:
        c = c[::-1]
        ints.append(int(c, 2))
    encodedMessage = 's'
    for i in ints:
        encodedMessage += chr(i)
    return encodedMessage[1:]


def censor(sentence):
    forbidden = ['bad', 'something']
    for word in forbidden:
        if word in sentence:
            sentence = sentence.replace(word, len(word) * '*')
    return sentence

while True:
    message = input('Message to send: \n')
    out_data = send(message)
    in_data = []
    for bit in out_data:
        in_data.append(int(bit))

    i = 0
    data = ""
    for c in out_data:
        if i == 11:
            i = 0
            data += " "
        data += c
        i += 1
    print("DATA:", data)

    decoded_message = decode(in_data)
    decoded_message = censor(decoded_message)
    print("Received message: ", decoded_message)
    print("--------------------------------------------------------------------------------")
