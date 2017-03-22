# sdml - Smoke Detector (Machine Learning)

This is an experimental multinomial naive bayesian classifier to
identify potential spam posts on the Stack Exchange network.
It uses `scikit-learn` for the classification stuff.

This is a retake from an earlier effort by
[Art of Code](https://github.com/ArtOfCode-)


## Requirements

You can use `pip` to install all the required packages for this thing:

    python2 -m pip install -r requirements.txt

You will also need a working implementation of `cPickle`.
You've *probably* got one, but not *all* Py2 installs came with it.

## Using it

Once you've `git clone`d the repo, you can do one of two things:

- update the data set, or
- just run the thing already

To update the data set, you need to run a few scripts.
The first gets new data,
the second analyzes it for specific attributes,
and the third converts the analyzed data to a format that the classifier can load.

To successfully run the first script, you need a valid
[API key](https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation)
for [metasmoke](https://github.com/Charcoal-SE/metasmoke).
Read the
[API docs](https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation)
to learn how to get one.

    python2 getmsdata.py INSERT_MS_API_KEY_HERE
    python2 analyze.py
    python2 prepare.py

When those scripts complete,
you have the data set up that the classifier needs to run from.
You can run the live classifier now
(which takes data from the Stack Exchange websocket, like Smokey does):

    python2 ws.py

## Classification Principles

Because the Stack Exchange network
hosts a number of sites
which cover vastly different sets of topics,
we want to identify what
the normal posts on every member site look like,
and train a simple classifier for each.
Spam posts tend to be identical across the network,
but similarly come in different categories
(pills, IT training, lottery scams, etc).
<!--
The classifier attempts to group them into subsets
and postulate categories for those, too.
-->

