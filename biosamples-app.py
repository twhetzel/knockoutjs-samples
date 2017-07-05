from flask import Flask, request, redirect, render_template, session, jsonify
import json, requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("biosamples.html")


@app.route("/search_input")
def search_input():
    """ 
    Take in a search term and return a list of Sample IDs and other metadata. 
    """
    bs_search = request.args.get('sample_ids', type=str)
    BIOSAMPLES_SEARCH = "http://www.ebi.ac.uk/biosamples/api/samples/search/findByText?text="+bs_search
    # print "** BSS: ", BIOSAMPLES_SEARCH
    all_sample_accessions = _get_samples(BIOSAMPLES_SEARCH)
    return jsonify(all_sample_accessions)


def _get_samples(url):
    """ 
    Use search term and BioSamples 'findByText' API (https://www.ebi.ac.uk/biosamples/help/api).
    """
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
                all_sample_accessions.append(all_sample_data.copy())
            return all_sample_accessions + _get_samples(data['_links']['next']['href'])
        else:
            sample_list = data['_embedded']['samples']
            for sample in sample_list:
                accession = sample['accession']
                name = sample['name']
                description = sample['description']
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
    """
    Takes in IDs of selected samples. In the BioSamples to Galaxy app this method will 
    call export() to send the data back to Galaxy to continue the process to load
    BioSamples data into Galaxy.
    """
   
    if request.method == 'GET':
        print "GET called..."
        pass
    if request.method == 'POST':
        sample_values = request.form.getlist('check')
        # jsdata = request.form['javascript_data']
        print "CB: ", sample_values
        return "Hello Galaxy!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

