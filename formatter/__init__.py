#!/usr/bin/env python3

import re

from flask import Flask, render_template, flash, request
from wtforms import Form, TextAreaField, validators, RadioField


#from loguru import logger
import iocextract

sha256_filename_finder = re.compile(r"(?im)(?:[^a-fA-F\d]|\b)(?P<hash>[a-fA-F\d]{64})(?:[^a-fA-F\d]|\b)(?P<filename>\S+)\b")

type_finder = re.compile("(?im)^\s*type:\s*(?P<report_type>\w+)")
tlp_finder = re.compile("(?im)^\s*(?:tag:\s*|)tlp:\s*(?P<tlp>\w+)")

subject_finder = re.compile("(?im)^\s*subject:\s(?!tlp)\S+.*")
tag_finder = re.compile("(?im)^\s*tag:\s(?!tlp)\S+.*")
# tag: tlp:red    nomatch
#  tag: TLp:red   nomatch
# tag: foo        match
#    tag: bar     match
# tag: bartlp     match

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

REPORT_TYPES = [
'phish',
'malware',
'bec/scam',
'dump',
'apt',
]

TLP_LEVELS = {
    'red' : "#B40404",
    'amber' : "#FF8000",
    'green' : "#21610B",
    'white' : 'black',
}

class ReusableForm(Form):
    userinput = TextAreaField('Input data:', validators=[validators.DataRequired()])
    report_type = RadioField('Report Type:',
                             choices=REPORT_TYPES,
                             validators=[validators.DataRequired()],
                             default='phish',
                             )
    tlp_level = RadioField("TLP Level",
                           choices=TLP_LEVELS.keys(),
                           validators=[validators.DataRequired()],
                           default='red',
                           )

@app.route("/<path:path>", methods=['GET', 'POST'])
def hello(path):
    form = ReusableForm(request.form)

    if request.method == 'POST':
        userinput=request.form['userinput']
        report_type=request.form['report_type']
        tlp_level=request.form['tlp_level']

    if form.validate():
        if type_finder.findall(userinput):
            report_type = type_finder.findall(userinput)[0]
            flash(f"User included report type ({report_type}) with input data",category='warning')
        if tlp_finder.findall(userinput):
            tlp_level = tlp_finder.findall(userinput)[0]
            flash(f"User included tlp level ({tlp_level}) with input data",category='warning')

        flash("")
        flash(f"type: {report_type}", category='info')
        flash(f"tag: tlp:{tlp_level.upper()}", category='info')
        # Save the comment here.

        seen_iocs = []
        datatypes = {
            'url' : iocextract.extract_urls,
            'ip' : iocextract.extract_ips,
            'from' : iocextract.extract_emails,
            'md5' : iocextract.extract_md5_hashes,
            'sha1' : iocextract.extract_sha1_hashes,
            'sha256' : iocextract.extract_sha256_hashes,
            'sha512' : iocextract.extract_sha512_hashes,
        }
        for datatype in datatypes:
            for extracted_value in datatypes[datatype](userinput):
                if str(extracted_value) not in seen_iocs:
                    seen_iocs.append(str(extracted_value))
                    flash(f"{datatype}: {iocextract._refang_common(extracted_value)}", category='info')

        if sha256_filename_finder.findall(userinput):
            for result in sha256_filename_finder.findall(userinput):
                flash(f"hash|filename: {'|'.join(result)}", category='info')

        if subject_finder.findall(userinput):
            for result in subject_finder.findall(userinput):
                flash(f"subject: {result}", category='info')
    else:
        flash('Please enter some data')

    return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')