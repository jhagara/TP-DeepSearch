import math
import re
from elasticsearch import Elasticsearch
from textblob import TextBlob as tB
import config
KEYWORDS_LIMIT = 10
PHRASE_MAX_LENGTH = 3

stops = ["a", "aby", "aj", "ak", "aká", "akáže", "aké", "akéže", "akého", "akéhože", "akej", "akejže", "akému", "akémuže", "ako", "akože", "akom", "akomže", "akou", "akouže", "akú", "akúže", "akých", "akýchže", "akým", "akýmže", "akými", "akýmiže", "ale", "alebo", "ani", "áno", "asi", "až", "ba", "bez", "bezo", "bol", "bola", "boli", "bolo", "bude", "budem", "budeme", "budeš", "budete", "budú", "by", "byť", "cez", "cezo", "čej", "či", "čí", "čia", "čie", "čieho", "čiemu", "čím", "čími", "čiu", "čo", "čoho", "čom", "čomu", "čou", "ďalšia", "ďalšie", "ďalšieho", "ďalšiemu", "ďalšiu", "ďalší", "ďalších", "ďalším", "ďalšími", "ďalšou", "dnes", "do", "ho", "ešte", "i", "iba", "ich", "im", "iná", "inej", "iné", "iného", "inému", "iní", "inom", "inú", "iný", "iných", "inými", "ja", "je", "jeho", "jej", "jemu", "ju", "k", "ká", "káže", "kam", "kamže", "každá", "každé", "každému", "každí", "každou", "každom", "každú", "každý", "každých", "každým", "každými", "kde", "keď", "kej", "kejže", "ké", "kéže", "kie", "kieho", "kiehože", "kiemu", "kiemuže", "kieže", "koho", "kom", "komu", "kou", "kouže", "kto", "ktorá", "ktorej", "ktoré", "ktorí", "ktorou", "ktorú", "ktorý", "ktorých", "ktorým", "ktorými", "ku", "kú", "kúže", "ký", "kýho", "kýhože", "kým", "kýmu", "kýmuže", "kýže", "lebo", "leda", "ledaže", "len", "ma", "má", "majú", "mám", "máme", "máš", "máte", "mať", "medzi", "mi", "mne", "mnou", "mňa", "moj", "moje", "mojej", "mojich", "mojim", "mojimi", "mojou", "moju", "môcť", "môj", "môjho", "môže", "môžem", "môžeme", "môžeš", "môžete", "môžu", "mu", "musieť", "musí", "musia", "musím", "musíme", "musíte", "musíš", "my", "na", "nad", "nado", "nám", "nami", "nás", "náš", "naša", "naše", "našej", "nášho", "naši", "našich", "našim", "našimi", "našou", "ne", "neho", "nech", "nej", "nejaká", "nejaké", "nejakého", "nejakej", "nejakému", "nejakom", "nejakou", "nejakú", "nejakých", "nejakým", "nejakými", "nemu", "než", "nich", "nič", "ničím", "ničoho", "ničom", "ničomu", "nie", "niektorá", "niektoré", "niektorého", "niektorej", "niektorému", "niektorom", "niektorou", "niektorú", "niektorý", "niektorých", "niektorým", "niektorými", "nim", "nimi", "ním", "ňom", "ňou", "ňu", "o", "od", "odo", "on", "ona", "oni", "ono", "ony", "oň", "oňho", "po", "pod", "podo", "podľa", "pokiaľ", "potom", "popod", "popri", "poza", "práve", "pre", "prečo", "preto", "pretože", "pred", "predo", "pri", "s", "sa", "si", "sme", "so", "som", "ste", "sú", "svoj", "svoja", "svoje", "svojho", "svojich", "svojim", "svojím", "svojimi", "svojou", "svoju", "ta", "tá", "tam", "tak", "takže", "táto", "teda", "tej", "tejto", "ten", "tento", "tiež", "tí", "tie", "tieto", "títo", "to", "toho", "tohto", "tom", "tomto", "tomu", "tomuto", "toto", "tou", "touto", "tu", "tú", "túto", "tvoj", "tvoja", "tvoje", "tvojej", "tvojho", "tvoji", "tvojich", "tvojím", "tvojimi", "ty", "tých", "tým", "tými", "týmto", "už", "v", "vám", "vami", "vás", "váš", "vaša", "vaše", "vašej", "vášho", "vaši", "vašich", "vašim", "vaším", "viac", "vo", "však", "všetci", "všetka", "všetko", "všetky", "všetok", "vy", "z", "za", "začo", "začože", "zo", "že"]


class Analyzer(object):
    def __tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def __n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)

    def __idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.__n_containing(word, bloblist)))

    def __tfidf(self, word, blob, bloblist):
        return self.__tf(word, blob) * self.__idf(word, bloblist)

    # generate key words from bloblist
    def key_words(self, bloblist, list_of_starts):

        key_words_art = []

        for i, blob in enumerate(bloblist):
            scores = {word: self.__tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            start = list_of_starts[i]
            key_words = []
            position_index = {}

            # find positions of keywords
            for word, score in sorted_words[:KEYWORDS_LIMIT]:
                pos = 0
                pos_list = []
                for key in blob.words:
                    pos = pos + 1
                    if key == word:
                        pos_list.append(pos)
                position_index[word] = pos_list

            connected_words = []
            nonconnected_words = []
            duplicate_index = position_index.copy()

            # find keywords which can be connected together
            for word in position_index:
                duplicate_index.pop(word)
                for pos in position_index[word]:
                    distance1 = 1
                    distance2 = 1
                    new = word
                    ctrl = 0
                    number_of_words = 1
                    while ctrl != 1:
                        ctrl = 1
                        for word2 in duplicate_index:
                            for pos2 in duplicate_index[word2]:
                                if pos - pos2 == distance1 and word not in start:
                                    new = word2 + " " + new
                                    distance1 = distance1 + 1
                                    ctrl = 2
                                    number_of_words = number_of_words + 1
                                    break
                                if pos2 - pos == distance2 and word2 not in start:
                                    new = new + " " + word2
                                    distance2 = distance2 + 1
                                    ctrl = 2
                                    number_of_words = number_of_words + 1
                                    break
                            if ctrl == 2:
                                break
                        if number_of_words == PHRASE_MAX_LENGTH:
                            break
                if number_of_words > 1:
                    connected_words.append(new)
                else:
                    nonconnected_words.append(new)

        # filter out keywords which are substrings of other keyword connections
            count = 0
            all_keywords = ""
            for conn in connected_words:
                all_keywords = all_keywords + " " + conn
                count = count + 1
                test = " " + conn + " "
                if test not in all_keywords:
                    key_words.append(conn)
            for word in nonconnected_words:
                count = count + 1
                test = " " + word + " "
                if test not in all_keywords:
                    key_words.append(word)
                if count == KEYWORDS_LIMIT:
                    break

            key_words_art.append(key_words)

        return key_words_art

    # generate key words from json
    def key_words_from_json(self, jlist):

        bloblist = []
        list_of_starts = []

        for article in jlist:
            all_text = ''
            for group in article['groups']:
                all_text += group['text']

            # remove stop words and get list of sentence starters
            all_text = ' '.join([word for word in all_text.split() if word not in stops and word.lower() not in stops])
            starts = re.findall('(?:^|(?:[.!?]\s))(\w+)', all_text)
            list_of_starts.append(starts)
            bloblist.append(tB(all_text))

        return self.key_words(bloblist, list_of_starts)

    # generate key words and insert then in to elastic
    def insert_key_words(self, issue_id):

        elastic_index = config.elastic_index()

        # establishment of connection
        es = Elasticsearch()

        articles = es.search(index=elastic_index, doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                                 'size': 1000})['hits']['hits']

        article_ids = []
        article_bodies = []

        for hit in articles:
            if hit['_source']['is_ignored'] is False:
                article_bodies.append(hit['_source'])
                article_ids.append(hit['_id'])

        art_key_words = self.key_words_from_json(article_bodies)


        for i, article_id in enumerate(article_ids):
            updated = es.update(index=elastic_index,
                                doc_type='article',
                                id=article_id,
                                body={
                                    "script": {
                                        "inline": "ctx._source.keywords = params.keywords",
                                        "lang": "painless",
                                        "params": {
                                            "keywords": art_key_words[i]
                                            }
                                        }
                                    })

        es.indices.refresh(index=elastic_index)
