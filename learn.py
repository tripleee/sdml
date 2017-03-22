#!/usr/bin/env python3

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extaction.text import TfidfVectorizer
import json


def learn (instance, category, text):
    """
    Update the classifier instance with data for category from markdown text.
    """
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0,
                         stop_words = 'english')
    tfidf_matrix = tf.fit_transform(instance
    instance.fit_transform(


def main (output='learned.json'):
    """
    Read command-line arguments as JSON from Metasmoke; try to learn
    from the samples in the input.  Save updated model to JSON file
    (default "learned.json").
    """
    from fileinput import input as fileinput
    import logging

    logging.basicConfig(level=logging.WARNING,
        format='%(module)s [%(asctime)s]: %(message)s')

    mnb = MultinomialNB()
    
    for line in fileinput():
        entries = json.loads(line)
        for entry in entries:
            flags = [x for x in ['is_tp', 'is_fp', 'is_naa'] if entry[x]]
            if len(flags) != 1:
                logging.warn('id: {0} flags: {1}'.format(entry['id'], flags))
                continue
            text = '\n'.join(entry['title'], entry['body'])
            if flags == 'is_fp':
                mnb
            print('id: {0} site: {1} is_fp: {2} is_tp: {3} is_naa: {4}'.format(
                entry['id'], entry['link'].split('/')[2], entry['is_fp'],
                    entry['is_tp'], entry['is_naa']))

    ######## TODO: write to json (or pickle?)


if __name__ == '__main__':
    main()
