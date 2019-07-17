import textwrap


def wrapTextByWidth(drawer, text, font, maxWidth):
    splitCount = 0
    splitText = text
    needSplit = True

    while needSplit:
        textWidth = drawer.textsize(splitText, font)[0]
        if textWidth > maxWidth:
            splitCount += 1
            textLength = len(splitText)
            splitText = splitText[:round(textLength/2)]
        else:
            needSplit = False

    fullTextLength = len(text)
    splitTextArr = textwrap.wrap(text, fullTextLength/(splitCount**2))
    newLineTextArr = ['{0}\n'.format(el) for el in splitTextArr]
    splitText = ''.join(newLineTextArr)
    return splitText
