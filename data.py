import cPickle as pickle
from datetime import datetime
from google.appengine.ext import ndb
import json
import re
import yaml


ALL_SETS_FILENAME = "AllSets.json"
CARDS_FILENAME = "cards.pickle"
REGEX_FILENAME = "regex.pickle"
SECRETS_FILENAME = "secrets.yaml"


def preprocess_cards(all_sets_filename, cards_filename):
    with open(all_sets_filename) as f:
        allsets = json.load(f)
    # Pick the card IDs from the oldest available sets
    cards = {}
    for s in sorted(allsets.values(),
                    key=lambda x: x['releaseDate'], reverse=True):
        for card in s['cards']:
            for name in card.get('names', [card['name']]):
                if 'multiverseid' in card:
                    cards[name.lower()] = {'multiverseid': card['multiverseid']}
    with open(cards_filename, 'w') as f:
        pickle.dump(cards, f, pickle.HIGHEST_PROTOCOL)
    return cards


def preprocess_regex(cards, regex_filename):
    names = cards.keys()
    # Sort the names to preferentially match longer cards
    re_names = map(re.escape, sorted(names, key=len, reverse=True))
    regex = re.compile(r"\b(" +
                       r"|".join(re_names) +
                       r")\b", re.IGNORECASE)
    with open(regex_filename, 'w') as f:
        pickle.dump(regex, f, pickle.HIGHEST_PROTOCOL)
    return regex


def load_secrets():
    with open(SECRETS_FILENAME) as f:
        return yaml.load(f)


def validate_secrets():
    """Make sure you've supplied your Slack secrets in secrets.yaml."""
    secrets = load_secrets()
    assert len(secrets['verification_token']) == 24
    assert len(secrets['bot_user_oauth_access_token']) == 42


def preprocess():
    """Precompute stuff so loading in appengine is fast."""
    cards = preprocess_cards(ALL_SETS_FILENAME, CARDS_FILENAME)
    preprocess_regex(cards, REGEX_FILENAME)
    validate_secrets()


def load_cards():
    with open(CARDS_FILENAME) as f:
        return pickle.load(f)


def load_regex():
    with open(REGEX_FILENAME) as f:
        return pickle.load(f)


class CardUsage(ndb.Model):
    name = ndb.StringProperty()
    last_usage = ndb.DateTimeProperty()


def get_card_usage(card_names):
    return ndb.get_multi([ndb.Key(name) for name in card_names])


def note_card_usage(card_name):
    card_usage = CardUsage(name=card_name, last_usage=datetime.now(),
                           id=card_name)
    card_usage.put()


if __name__ == '__main__':
    preprocess()
