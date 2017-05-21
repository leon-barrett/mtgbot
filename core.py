import data
import flask
from google.appengine.ext.deferred import defer
import logging
import requests


class Delay(object):
    """A delayed function. Get the value with deref. (Yes, inspired by
    Clojure.)"""

    def __init__(self, f):
        self.f = f
        self.val = None

    def deref(self):
        if self.val == None:
            self.val = self.f()
        return self.val


cards = Delay(data.load_cards)
regex = Delay(data.load_regex)
secrets = Delay(data.load_secrets)


def card_image_url(card):
    return ("http://gatherer.wizards.com/Handlers/Image.ashx"
            "?multiverseid=%s&type=card") % card['multiverseid']


def find_card(text):
    matches = regex.deref().findall(text)
    if matches:
        card_name = max(matches, key=len).lower()
        return card_name, card_image_url(cards.deref()[card_name])


def post_to_slack(channel, card_name, url):
    return requests.post("https://slack.com/api/chat.postMessage",
                         {'channel': channel,
                          'text': '<%s|%s>' % (url, card_name),
                          'token': secrets.deref()[
                              'bot_user_oauth_access_token']})


def handle_message(event):
    text = event.get('text', None)
    if not text:
        return
    card_name, card_url = find_card(text)
    channel = event.get('channel', None)
    if card_name and channel:
        logging.info('channel "%s" card_name "%s" card_url "%s"',
                     channel, card_name, card_url)
        post_to_slack(channel, card_name, card_url)


app = flask.Flask(__name__)


@app.route('/slack', methods=['POST'])
def slack():
    content = flask.request.get_json()
    logging.info('content %s', content)
    if content.get('token', '') != secrets.deref()['verification_token']:
        return "denied", 403
    if 'challenge' in content:
        return flask.jsonify({'challenge': content['challenge']})
    event = content.get('event', {})
    type_ = event.get('type', None)
    subtype = event.get('subtype', None)
    # Don't talk to bots
    if type_ == 'message' and subtype != "bot_message":
        # Defer the work so we can respond to Slack quickly
        defer(handle_message, event)
    return 'ok', 200


@app.errorhandler(404)
def page_not_found(e):
    return 'Not found', 404


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
