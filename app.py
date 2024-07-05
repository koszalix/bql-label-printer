#!/usr/bin/env python

"""
Simple Web Interface to create labels on a Brother Printer
"""

import sys
from glob import glob
from os.path import basename

from PIL import Image
import yaml
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend
from brother_ql.devicedependent import models, label_type_specs, label_sizes
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

DEBUG = False
MODEL = None
BACKEND_CLASS = None
BACKEND_STRING_DESCR = None
LABEL_SIZES = [(name, label_type_specs[name]["name"]) for name in label_sizes]


@app.route("/")
def do_editor():
    """
    The main editor view
    :return:
    """
    return render_template(
        "index.html", categories=get_categories(), labels=get_labels("generic")
    )


@app.route("/expiry")
def do_expiry():
    """
    The expiry label view
    :return:
    """
    return render_template("expiry.html")


@app.route("/print", methods=["POST"])
def do_print():
    """
    Receive the image from the frontend and print it
    :return: string a simple 'ok' when no exception was thrown
    """
    im = Image.open(request.files["data"])
    qlr = BrotherQLRaster(MODEL)
    print(request.form)
    try:
        create_label(
                qlr,
                im,
                request.form["size"],
                threshold=70,
                cut=bool(request.form["cut"]),
                rotate=int(request.form["rotate"]),
         )
    except ValueError:
        return "Bad image"

    # noinspection PyCallingNonCallable
    be = BACKEND_CLASS(BACKEND_STRING_DESCR)
    be.write(qlr.data)
    be.dispose()
    del be

    return "ok"


@app.route("/reload", methods=["GET"])
def reload_labels():
    """
    Reload labels from selected category
    :return
    """
    categories = get_categories()
    categories.remove(request.args.get("category"))
    categories = [request.args.get("category")] + categories
    return render_template(
        "index.html",
        categories=categories,
        labels=get_labels(request.args.get("category")),
    )


def get_labels(category: str):
    """
    List the available label templates
    :return:
    """
    filenames = glob(sys.path[0] + f"/static/labels/{category}/*.html")
    filenames.sort()

    return [basename(x[:-5]) for x in filenames]


def get_categories():
    """
    List all categories
    return:
    """
    filenames = glob(sys.path[0] + "/static/labels/*")
    filenames.sort()

    return [basename(x) for x in filenames if x[0] != "."]


def main():
    """
    Initializes the webserver
    :return:
    """
    global DEBUG, MODEL, BACKEND_CLASS, BACKEND_STRING_DESCR
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="The IP the webserver should bind to. Use 0.0.0.0 for all",
    )
    parser.add_argument(
        "--port", default=8013, help="The port the webserver should start on"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Activate flask debugging support",
    )
    parser.add_argument(
        "--model",
        default="QL-500",
        choices=models,
        help="The model of your printer (default: QL-500)",
    )
    parser.add_argument("--config-file", default="", help="path to config file")
    parser.add_argument(
        "printer",
        help="String descriptor for the printer to use (like tcp://192.168.0.23:9100 or "
        "file:///dev/usb/lp0)",
        nargs="*",
    )

    args = parser.parse_args()

    if args.config_file:
        with open(args.config_file, "r") as file:
            config = yaml.safe_load(file)
            try:
                args.host = config["server"]["host"]
                args.port = config["server"]["port"]
                args.debug = config["server"]["debug"]
                args.model = config["backend"]["model"]
                args.printer = config["backend"]["printer"]
            except KeyError:
                print("Config error")
                exit(-3)
    DEBUG = args.debug
    MODEL = args.model

    try:
        selected_backend = guess_backend(args.printer)
        BACKEND_CLASS = backend_factory(selected_backend)["backend_class"]
        BACKEND_STRING_DESCR = args.printer
    except:
        parser.error(
            "Couldn't guess the backend to use from the printer string descriptor"
        )

    app.run(host=args.host, port=args.port, debug=DEBUG)


if __name__ == "__main__":
    main()
