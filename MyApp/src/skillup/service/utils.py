import re


def clean(txt: str) -> str:
    '''
    This function cleans the text and makes it less aggressive.
    :param txt: The text to clean
    :return: The cleaned text
    '''
    txt = txt.replace("addict", "person with a substance use disorder")
    txt = txt.replace("handicapped parking", "accessible parking")
    txt = txt.replace("crazy", "surprising/wild")
    return txt