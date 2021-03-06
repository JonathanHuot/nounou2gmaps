# -*- coding: utf-8 -*-
import bottle
import os
from os import path
import re


bottle.TEMPLATE_PATH.append(path.join(path.dirname(path.realpath(__file__)), "."))
app = bottle.Bottle()


def enum(**enums):
    return type('Enum', (), enums)


State = enum(NONE=0, TITLE=1, ADDRESS=2, EXTRA=3)


patterns = [
    {
        "pattern": r'(0[0-9](\.| )?[0-9][0-9](\.| )?[0-9][0-9](\.| )?[0-9][0-9](\.| )?[0-9][0-9])',
        "attribute": "phone",
        "clean": "[. -]"
    },
    {
        "pattern": r'(13600 LA CIOTAT)',
        "attribute": "city",
        "state": State.ADDRESS
    },
    {
        "pattern": r'(13600)',
        "attribute": "city",
        "state": State.ADDRESS
    },
    {
        "pattern": r'( ([0-9]+|CHE|AV|RUE|IMP|CLOS|VILLA) .*)',
        "attribute": "address",
        "state": State.ADDRESS
    },
    {
        "pattern": r'((Journée|Périscolaire).*)',
        "attribute": "extra",
        "state": State.EXTRA
    }
]


def nounoupattern(nounou, line):
    for p in patterns:
        found = re.search(p["pattern"], line)
        if found:
            if "clean" in p:
                nounou[p["attribute"]] += " " + re.sub(p["clean"], "", found.group(1))
            else:
                nounou[p["attribute"]] += " " + found.group(1)
            if "state" in p:
                nounou["state"] = p["state"]
            return re.sub(p["pattern"], '', line)
    return None


def nounou2json(nounou, line):
    if nounou["state"] != State.EXTRA:
        newline = nounoupattern(nounou, line)
        if newline is not None:
            line = newline

    if not line.strip(" ,\r\n"):
        return

    if nounou["state"] == State.TITLE:
        nounou["title"] += " " + line
    elif nounou["state"] == State.ADDRESS:
        nounou["address"] += ", " + line
    elif nounou["state"] == State.EXTRA:
        nounou["extra"] += " " + line


def cleanup(nounou):
    if nounou:
        del nounou["state"]
        if "city" in nounou:
            nounou["address"] += ", " + nounou["city"]
            del nounou["city"]

        nounou["title"] = nounou["title"].strip(" ,\r\n")
        nounou["extra"] = nounou["extra"].strip(" ,\r\n")
        nounou["phone"] = nounou["phone"].strip(" ,\r\n")
        nounou["address"] = re.sub(", ,", ",", re.sub("[\r\n]", "", re.sub(", ,", ",", nounou["address"].strip(" ,\r\n"))))


def nounoufile2json(filename):
    nounous = []
    nounou = {
        "state": State.TITLE,
        "title": "",
        "city": "",
        "phone": "",
        "address": "",
        "extra": ""
    }

    with open(filename) as f:
        content = f.readlines()

        for line in content:
            line = line.strip(" ,\r\n")
            if not line:
                continue

            if re.search('Madame', line):
                # cleanup nounou
                cleanup(nounou)

                # create nounou
                nounou = {
                    "state": State.TITLE,
                    "title": "",
                    "city": "",
                    "phone": "",
                    "address": "",
                    "extra": ""
                }
                nounous.append(nounou)

            nounou2json(nounou, line)
    cleanup(nounou)
    return {
        'nounous': nounous
    }


@app.get("/")
def home():
    from bottle import redirect
    redirect("/nounous")


@app.get("/nounous")
def index():
    from bottle import template
    return template(
        "nounou2gmaps.html",
        geo_key=os.environ.get(
            "GOOGLE_GEOCODING_APIKEY",
            "Set your Google Geocoding API key"
        )
    )


@app.get("/nounous/marker.json")
def marker():
    nounoudict = nounoufile2json(path.join(path.dirname(path.realpath(__file__)), "ListeAssMat-2015-05-13.txt"))

    # for testing API, enable DEBUG and it returns only first 2 records
    if os.environ.get("DEBUG", None) == "true":
        nounoudict["nounous"] = nounoudict["nounous"][:2]
    return nounoudict


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 8787))
