#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:52:59 2022

@author: apirodd
"""

from flask import Flask

flask_test = Flask(__name__)


@flask_test.route("/")
def main():
    return "Benvenuti in Flask!"

if __name__ == "__main__":
    flask_test.run()