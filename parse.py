import os
import json
import pprint

class Token:
    def __init__(self, word, i, sen_index):
        self.word_index = i
        self.sen_index =  sen_index
        self.word_text = word[0]
        self.pos_info = word[1]
        self.lemma = self.get_lemma()
        self.pos = self.get_pos()
        self.character_offset_begin = self.get_character_offset_begin()
        self.character_offset_end = self.get_character_offset_end()
        
    def get_lemma(self):
        return self.pos_info["Lemma"]

    def get_pos(self):
        return self.pos_info["PartOfSpeech"]

    def get_character_offset_begin(self):
        return self.pos_info["CharacterOffsetBegin"]

    def get_character_offset_end(self):
        return self.pos_info["CharacterOffsetEnd"]


class Sentence:
    def __init__(self, sentence_info, i, parse_id):
        self.sen_index = i
        self.parse_id = parse_id
        self.sen_info = sentence_info
        self.parsetree = sentence_info['parsetree']
        self.sentence_text = sentence_info['text']
        self.dependencies = sentence_info['dependencies']
        self.tokens = self.get_tokens_from_sen(sentence_info['words'])
        
    def get_tokens_from_sen(self, words):
        token_list = []
        self.tokens_len = len(words)
        for i in range(self.tokens_len):
            token_list.append(Token(words[i], i, self.sen_index))
        return token_list
         

class Parsing:
    def __init__(self, parse_info, i):
        self.parse_id = i
        self.parse_info = parse_info
        self.sentences = self.get_sentences_from_parse() 
        self.word_problem_text = self.get_word_problem_text()
  
    def get_sentences_from_parse(self):
        sen_list = []
        sentences = self.parse_info['sentences']
        self.sen_len = len(sentences);
        for i in range(self.sen_len):
            sen_list.append(Sentence(sentences[i], i, self.parse_id))
        return sen_list 

    def get_word_problem_text(self):
        text = ""
        for sen in self.sentences:
            text += sen.sentence_text
        return text

    def print_test(self):
        print "********"
        print "wp_id:", self.parse_id
        print "parse information:\n"
        print self.parse_info
        print "wp_text:", self.word_problem_text 
        for i in range(self.sen_len):
            print "--sen--sen_id:", self.sentences[i].sen_index
            print "--sen--parse_id:", self.sentences[i].parse_id 
            print "--sen--sen_info:\n" 
            print "--sen--parsetree:", self.sentences[i].parsetree 
            print "--sen--sen_text:", self.sentences[i].sentence_text 
            print "--sen--depend..:", self.sentences[i].dependencies 
            for j in range(self.sentences[i].tokens_len):
                print "----tokens--sen_index:", self.sentences[i].tokens[j].sen_index
                print "----tokens--word_text::", self.sentences[i].tokens[j].word_text
                print "----tokens--pos_info:", self.sentences[i].tokens[j].pos_info
                print "----tokens--lemma:", self.sentences[i].tokens[j].lemma
                print "----tokens--pos:", self.sentences[i].tokens[j].pos
                print "----tokens--self.character_offset_begin:", self.sentences[i].tokens[j].character_offset_begin
        print 
        print  




