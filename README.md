# MTGBot

MTGBot is a little [Slack][]bot that watches for mentions of [Magic the
Gathering (TM)][MTG] card names and responds with links to images of the cards.

MTGBot runs on [AppEngine][], and it's super small, so it will probably run
fine within Google's free tier (it certainly does for me).

MTGBot uses card data from [MTGJson][] to look up cards, and it links directly
to official Magic card images.

![MTGBot demo image](mtgbot.png)

[Slack]: https://slack.com/
[MTG]: http://magic.wizards.com/
[AppEngine]: https://mtgjson.com://cloud.google.com/appengine/
[MTGJson]: https://mtgjson.com/

# Setup

1. [Tell Slack about your bot](https://api.slack.com/apps/).
2. Put the secret keys you got from Slack into `secrets.yaml.EDIT_ME` (and
   rename it to `secrets.yaml`).
3. Run `setup.sh`. (Use `pip` to install Python dependencies if needed.)
4. [Set up a Google Cloud Services account](https://cloud.google.com/).
5. [Install Google Cloud Services command-line tool](https://cloud.google.com/sdk/gcloud/).
6. Run `gcloud app deploy app.yaml --project $YOUR_PROJECT_NAME_HERE`.

# License

<a rel="license"
    href="http://creativecommons.org/publicdomain/zero/1.0/">
  <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
</a>
<br />
To the extent possible under law,
<a rel="dct:publisher"
    href="https://github.com/leonbarrett/">
  <span property="dct:title">Leon Barrett</span></a>
has waived all copyright and related or neighboring rights to
<span property="dct:title">MTGBot</span>.
This work is published from:
<span property="vcard:Country" datatype="dct:ISO3166"
    content="US" about="https://github.com/leonbarrett/mtgbot">
United States</span>.
