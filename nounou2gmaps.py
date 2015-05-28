import bottle
from bottle import view
from bottle import get
from bottle import app


def enum(**enums):
    return type('Enum', (), enums)


def nounoufile2json(filename):
    import re
    with open(filename) as f:
        content = f.readlines()
        titles = len(content)*[None]
        addresses = len(content)*[None]
        extras = len(content)*[None]
        phones = len(content)*[None]

        State = enum(NONE=0, TITLE=1, CITY=2, ADDRESS=3, EXTRA=4)
        state = State.NONE
        index = -1
        for i, line in enumerate(content):
            if re.match('^Madame', line):
                state = State.TITLE
                index=index+1
            elif re.match('^Journ', line):
                state = State.EXTRA

            regtel = r'([0-9][0-9](\.| )?[0-9][0-9](\.| )?[0-9][0-9](\.| )?[0-9][0-9](\.| )?[0-9][0-9])'
            tel = re.search(regtel, line)
            if tel:
                phones[index] = tel.group(1)
                line = re.sub(regtel, '', line)

            if state == State.TITLE:
                titles[index] = line
                state=state+1
            elif state == State.CITY:
                addresses[index] = line
                state=state+1
            elif state == State.ADDRESS:
                addresses[index] = "{0}, {1}".format(line, addresses[index] if addresses[index] else "")
                state=state+1
            elif state == State.EXTRA:
                extras[index] = "{0} {1}".format(line, extras[index] if extras[index] else "")

    return {
        'titles': titles,
        'phones': phones,
        'addresses': addresses,
        'extras': extras
    }


@bottle.get("/")
def home():
    from bottle import redirect
    redirect("/nounous")


@bottle.get("/nounous")
def index():
    from bottle import template
    return template("nounou2gmaps.html")


@bottle.get("/nounous/marker.json")
def marker():
    return nounoufile2json(path.join(path.dirname(path.realpath(__file__)), "ListeAssMat-2015-05-13.txt"))


from bottle import TEMPLATE_PATH
from os import path
TEMPLATE_PATH.append(path.join(path.dirname(path.realpath(__file__)), "."))
from bottle import run
run(port=8787)
