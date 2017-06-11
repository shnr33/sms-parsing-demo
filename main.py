import logging
import json
import re
import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from collections import defaultdict

# A random secret used by Flask to encrypt session data cookies
SECRET_KEY = "z\xac\x8e?\xe2g\x8fX\xfb\x18\xf2\xcd$i\x12\n\x9a\x93\xb0\x1a\x91\xc3\xbbU"

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

MSG_TYPE_TRANSACTIONAL = 'TRANSACTIONAL'
MSG_TYPE_PROMOTIONAL = 'PROMOTIONAL'
MSG_TYPE_PERSONAL = 'PERSONAL'
MSG_TYPE_MISC = 'MISC.'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard', methods=['POST'])
def dashboard():
    """Shows the dashboard once the file data is parsed."""
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    # if user does not select file, browser 
    # submits an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file:
        try:
            file.read(19)  # TO skip 19 characters which make up the JS var declaration
            file_data = json.load(file)
        except Exception:
            flash('Error reading file. Check for a valid JSON file or try another file')
            return redirect(url_for('index'))

        parsed_sms_data = parse_sms_data(file_data)

        return render_template("dashboard.html", parsed_sms_data=parsed_sms_data)


def get_msg_type(sender):
    if re.match(r'[a-zA-Z]{2}-\d{6}$', sender):
        # Promotional SMS will be of type - LM-010201 (ends with 6 numeric characters)
        return MSG_TYPE_PROMOTIONAL
    elif re.match(r'[a-zA-Z]{2}-[a-zA-Z]{6}$', sender):
        # Transactional SMS will be of type - LM-HDFCBK (ends with 6 alpha characters)
        return MSG_TYPE_TRANSACTIONAL
    elif re.match(r'^\+\d*$', sender):
        # Messages recieved from proper 10 digit numbers - +919888800999
        return MSG_TYPE_PERSONAL
    else:
        # Categorising the rest as Misc.
        return MSG_TYPE_MISC


def get_sender_service_type(sender):
    sender = sender.upper()
    sender_type = get_msg_type(sender)

    if (sender.find('HDFC') > 0 or sender.find('ICICI') > 0 or 
            sender.find('AXIS') > 0 or sender.find('SBI') > 0 or 
            sender.find('UTI') > 0 or sender.find('CITI') > 0 or 
            sender.find('KOTAK') > 0 or sender.find('CANBNK') > 0 or sender.find('PAYTM') > 0):
        return 'BANK/FINANCIAL'
    elif sender.find('OLA') > 0 or sender.find('UBER') > 0:
        return 'CAB'
    elif sender.find('BGRKNG') > 0 or sender.find('FRZMNU') > 0 or sender.find('BOX') > 0:
        return 'FOOD'
    elif sender.find('AMAZON') > 0 or sender.find('FLPKRT') > 0 or sender.find('SNAPDL') > 0:
        return 'E-COMMERCE'
    elif sender.find('DTH') > 0 or sender.find('TSKY') > 0 or sender.find('DISHTV') > 0:
        return 'DTH SERVICES'
    elif sender.find('INDIGO') > 0:
        return 'AIRLINES'
    elif sender_type == MSG_TYPE_PERSONAL:
        return 'PERSONAL'
    else:
        return 'MISC.'


def parse_sms_data(messages_data):
    message_list = messages_data.get('messages')
    sender_dict = defaultdict(dict)
    collated_sms_data = []
    # Parse individual SMS data
    for message in message_list:
        if message['sender']:
            # Ignore messages sent from self
            continue
        if message['mms']:
            # Ignore MMS messages
            continue
        sender = message['number']
        msg_type = get_msg_type(sender)
        text = message['text']
        timestamp_in_millis = message['timestamp']
        timestamp_in_seconds = timestamp_in_millis / 1000.0
        sms_datetime = datetime.datetime.fromtimestamp(timestamp_in_seconds).strftime('%Y-%m-%d %H:%M:%S')

        # Collating the messages according to type for a given sender
        if msg_type == MSG_TYPE_TRANSACTIONAL:
            sender_dict[sender].update({'tx': sender_dict[sender].get('tx') + 1 if sender_dict[sender].get('tx') else 1})
        elif msg_type == MSG_TYPE_PROMOTIONAL:
            sender_dict[sender].update({'promo': sender_dict[sender].get('promo') + 1 if sender_dict[sender].get('promo') else 1})
        sender_dict[sender].update({'total': sender_dict[sender].get('total') + 1 if sender_dict[sender].get('total') else 1})

        message_info = {'msg_type': msg_type,
                        'sms_text': text,
                        'sms_datetime': sms_datetime
                        }
        if sender_dict[sender].get('messages'):
            message_info.update(sms_id=len(sender_dict[sender]['messages']) + 1)
            sender_dict[sender]['messages'].append(message_info)
        else:
            message_info.update(sms_id=1)
            sender_dict[sender]['messages'] = [message_info]

    i = 1  # A sequential id to act as serial number
    # Going through collated data to prepare data for the dashboard
    for sender, info in sender_dict.items():
        collated_data = {}
        collated_data['id'] = i
        collated_data['sender'] = sender
        collated_data['sender_service_type'] = get_sender_service_type(sender)
        collated_data['total_sms'] = info.get('total')
        collated_data['total_tx_sms'] = info.get('tx')
        collated_data['total_promo_sms'] = info.get('promo')
        collated_data['messages'] = info.get('messages')

        collated_sms_data.append(collated_data)

        i += 1

    return collated_sms_data


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'Sorry for the inconvenience. An server error occurred.', 500
# [END app]
