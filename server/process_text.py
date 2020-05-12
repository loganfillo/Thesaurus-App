import os
import random
import enum
import math
import string
import time
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import spacy
from spacy.symbols import VERB, NOUN, ADJ, ADV
import requests
from pattern.en import conjugate, pluralize, singularize, PAST, PRESENT, PARTICIPLE


class InputTextProcessor:
    """
    A class for processing input text into output text with synonyms 
    that still retains the same meaning
    """
    

    """
    Loads the spaCy English NLP model
    """
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")


    """
    Processes the input text by replacing all meaningful words in the text with 
    synonyms but still retaining the meaning of the original text

    @param input_text: The text to be processed
    @retruns: The procesed output text
    """
    def process(self, input_text):
        try:
            output_text = input_text
            doc = self.retokenize_apostrophes(self.nlp(input_text))
            output_sents = []
            for sent in doc.sents:            
                words = [Word(self.nlp, token, sent) for token in sent]
                new_words = [self.get_synonym(word) if self.has_synonym(word) 
                            else word.text for word in words]
                output_sents.append(self.form_new_sentence(new_words))
            output_text = ' '.join(output_sents)
            return output_text
        except RuntimeError as err:
            # Terrible hack to stop the StopIteration RuntimeError problem in py37
            # https://www.python.org/dev/peps/pep-0479/
            if 'StopIteration' in str(err): 
                print(repr(err))
                return self.process(input_text)
            else:
                raise Exception


    """
    Retokonizes the doc so that words with apostrophes are not broken apart
    https://stackoverflow.com/questions/59579049/how-to-tell-spacy-not-to-split-any-words-with-apostrophs-using-retokenizer

    @param doc: The result of the NLP on the input text
    @returns: A doc object where any tokens with apostrophes are merged back to their original words
    """
    def retokenize_apostrophes(self, doc):
        position = [token.i for token in doc if token.i!=0 and "'" in token.text]
        with doc.retokenize() as retokenizer:
            for pos in position:
                retokenizer.merge(doc[pos-1:pos+1])
        return doc


    """
    Forms a list of words into a punctual sentance

    @param words: list of strings
    @returns: A string of the given words formed into a sentence
    """
    def form_new_sentence(self, words): 
        #TODO: finish this method for all types of punctuation
        puncuation = string.punctuation
        for i, word in enumerate(words):
            if word in puncuation:
                if word in '!%,.:;?':
                    words[i-1:i+1] = [''.join(words[i-1] + words[i])]
                elif word in '$@':
                    words[i:i+2] = [''.join(words[i] + words[i+1])] 
        return ' '.join(words)

    """
    Returns True if the given word has a meaningful synonym

    @param word: The word object
    @returns: True if the word has a meaningful synonym 
    """
    def has_synonym(self, word):
        return ((word.is_stop == False) and 
                (word.is_alpha == True) and
                ((word.pos == VERB) or
                 (word.pos == NOUN) or
                 (word.pos == ADJ)  or
                 (word.pos == ADV)))


    """
    Gets a new synonym for the given word

    @param word: The given word object
    @returns: A synonym of the word, with correct tense and plurality 
    """
    def get_synonym(self, word):
        start = time.time()
        lemma = word.lemma
        url = os.environ['THESAURUS_API_URL']  + lemma
        params = {'key':  os.environ['THESAURUS_API_KEY']}
        print(url)
        syn = word.text
        req = requests.get(url, params=params)
        if req.status_code == 200:
            entries = req.json()
            if isinstance(entries[0], dict): # Different formats should mean no synonyms
                if word.pos == VERB:
                    pos = 'verb'
                elif word.pos == NOUN:
                    pos = 'noun'
                elif word.pos == ADJ:
                    pos = 'adjective'
                elif word.pos == ADV:
                    pos = 'adverb'
                entries = [entry for entry in entries if pos in entry['fl'] and entry['hwi']['hw'] == lemma]
                if len(entries) > 0: 
                    entry = entries[0] # Assuming there is only one entry with identical headword to lemma
                    all_syns = [syn for syns in entry['meta']['syns'] for syn in syns]
                    syn =  self.pick_close_synonym(word, all_syns)
        end = time.time()
        print("Time for :" , lemma, end-start)  
        return syn


    """
    Picks a close synonym to the given word from the list of synonyms

    @param word: The given word
    @param syns: The list of synonyms to the word
    """
    def pick_close_synonym(self, word, syns):
        orig_sent = word.sent
        syns_with_sim = []
        for syn in syns:
            syn_with_morph = self.match_morphology(word, syn)
            new_sent = self.nlp(orig_sent.text.replace(word.text, syn_with_morph))[:]       
            sim = orig_sent.similarity(new_sent)
            syn_with_sim = {'sim': sim, 'syn': syn_with_morph}
            syns_with_sim.append(syn_with_sim)
        np_sims = np.array([s['sim'] for s in syns_with_sim])
        thresh= np.percentile(np_sims, 75)
        rand_syn = random.choice([s['syn'] for s in syns_with_sim if s['sim'] >= thresh])
        return rand_syn


    """
    Modifies the given synonym so that it matches the morphology of the given word

    @param word: The given word object
    @param syn: The given synonym 
    @returns: The modified (if needed) synonym 
    """
    def match_morphology(self, word, syn):
        person = 1
        if word.morph.is_third_person is not None:
            person = 3
        if word.morph.tense is not None:
            syn = conjugate(syn, tense=word.morph.tense, person=person)
        if word.morph.is_plural is not None and word.pos == NOUN:
            syn = pluralize(syn)
        if word.morph.is_singular is not None and word.pos == NOUN:
            syn = singularize(syn)
        return syn
            

class Word:
    """
    A class for representing a word in a sentance
    """


    """
    Creates a word

    @param nlp: The NLP model used to creates the word token
    @param token: The word token
    @param sent: The sentence the word is a part of
    """
    def __init__(self, nlp, token, sent):
        self._nlp = nlp
        self.sent = sent
        self.token = token
        self.lemma = token.lemma_
        self.text = token.text
        self.pos = token.pos
        self.is_alpha = token.is_alpha
        self.is_stop = token.is_stop
        self.morph = self.get_morphology(token)


    """
    Gets the rule based morphology of the word from the token

    @param token: The word token
    @returns: The Morphology object of the token, where each relevant field is
              is not None and all other fields are None 
    """
    def get_morphology(self, token):
        morph = Morphology()
        morph_dict = self._nlp.vocab.morphology.tag_map[token.tag_]
        if not token.is_stop and token.is_alpha:
            if 'Tense_past' in morph_dict.keys():
                if 'VerbForm_part' in morph_dict.keys():
                    morph.tense = PAST+PARTICIPLE
                else:
                    morph.tense = PAST
                morph.tense = PAST
            if 'Tense_pres' in morph_dict.keys():
                if 'VerbForm_part' in morph_dict.keys():
                    morph.tense = PRESENT+PARTICIPLE
                else:
                    morph.tense = PRESENT
            if 'Person_three' in morph_dict.keys():
                morph.is_third_person = True
            if 'Number_plur' in morph_dict.keys():
                morph.is_plural= True
            if 'Number_sing' in morph_dict.keys():
                morph.is_singular= True
            print(token.text, spacy.explain(token.tag_), morph_dict)
        return morph


class Morphology:
    """
    A class for representing word morphology
    """

    def __init__(self):
        self.is_singular = None
        self.is_plural = None
        self.is_third_person = None
        self.tense = None
        

