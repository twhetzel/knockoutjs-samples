from flask import Flask, request, redirect, render_template, session, jsonify
import urllib
import urlparse
import json, requests
import pandas as pd
from xml.etree import ElementTree as ET
import io

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("task-list.html")

@app.route("/tasks")
def tasks():
    allData = [{"title": "wash cat", "isDone": False}, {"title": "do something", "isDone": True}]
    return jsonify(allData)


@app.route("/search_input")
def search_input():
    bs_search = request.args.get('sample_ids', type=str)
    print "BS-Input: ", bs_search
    # bs_search = "\"E-MTAB-3173\""
    BIOSAMPLES_SEARCH = "http://www.ebi.ac.uk/biosamples/api/samples/search/findByText?text="+bs_search
    print "** BSS: ", BIOSAMPLES_SEARCH
    all_sample_accessions = _get_samples(BIOSAMPLES_SEARCH)
    # print "\n** SAMPLE-IDS: ", all_sample_accessions
    # return jsonify(items = all_sample_accessions)
    #TODO: Format data for use with this getJSON
    return jsonify(all_sample_accessions)
    # allData = [{"title": "wash the cat", "isDone": False}, {"title": "do something", "isDone": True}]
    # return jsonify(allData)


def _get_samples(url):
    all_sample_accessions = []
    all_sample_data = {}

    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code == 200:
        response = r.text
        data = json.loads(response)

        if 'next' in data['_links']:
            sample_list = data['_embedded']['samples']
            for sample in sample_list:
                accession = sample['accession']
                name = sample['name']
                description = sample['description']
                all_sample_data['accession'] = accession
                # all_sample_accessions.append(accession)
                all_sample_accessions.append(all_sample_data.copy())
                # print len(all_sample_accessions)
            return all_sample_accessions + _get_samples(data['_links']['next']['href'])
        else:
            sample_list = data['_embedded']['samples']
            for sample in sample_list:
                accession = sample['accession']
                name = sample['name']
                description = sample['description']
                # all_sample_accessions.append(accession)
                all_sample_data['accession'] = accession
                all_sample_data['name'] = name
                if description:
                    all_sample_data['description'] = description
                else:
                    all_sample_data['description'] = 'None'
                all_sample_accessions.append(all_sample_data.copy())
            return all_sample_accessions
    else:
        r.raise_for_status()


@app.route("/process_samples", methods=['GET', 'POST'])
def process_samples():
    print "Samples being processed...."
    print "Method called: ", request.method

    if request.method == 'GET':
        print "GET called..."
        return "Hello World!!!"
    if request.method == 'POST':
        # sample_values = request.form.getlist('check')
        jsdata = request.form['javascript_data']
        print "CB: ", jsdata
        return "Hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)