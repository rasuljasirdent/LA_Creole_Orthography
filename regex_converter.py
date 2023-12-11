from os import listdir
import csv
import regex as re

consonant = "b|ç|c|ch|d|f|g|j|k|l|m|n|p|q|r|s|t|v|w|x|z|ʒ"

front_vowel = "e|é|è|ê|ë|i|î|ï|y|E|É|È|Ê|Ë|I|Î|Ï|Y|ɛ|œ|Œ|æ|Æ"
back_vowel = "a|á|â|o|v|u|ù|û|ü|A|Á|Â|O|Ô|U|Ù|Û|Ü"
special_vowel = "ã|ā|ẽ|ē|õ|ō"
vowel = f"{front_vowel}|{back_vowel}|{special_vowel}"

before_front_vowel = f"(?={front_vowel})"
before_back_vowel = f"(?={back_vowel})"
before_vowel = f"(?={vowel})"

after_vowel = f"(?<={vowel})"

#start and end of word
punc = r"\.|,|:|;|\'|\"|«|»|\u00BB|\?|\!|\(|\)\[|\]"
boundary = r"\s|^|$"
boundary = f"{boundary}|{punc}"
sow = f"(?<={boundary})"
eow = f"(?={boundary})"

#A consonant or non alpha character if it's there, or eow
not_vowel= f"[^{vowel}]??".replace("|", "")



def intervocalic(s):
    return f"{before_vowel}{s}{after_vowel}"

def as_word(s):
    return f"{sow}{s}{eow}"

def handle_q(s):
    s = re.sub(r"qu", "k", s)
    s = re.sub(r"q", "k", s)
    return s

def handle_j(s):
    je = f"je{before_vowel}"
    s = re.sub(je, "ʒ", s)
    s = re.sub("j", "ʒ", s)
    return s

def handle_g (s):
    ge = f"ge{before_back_vowel}"
    soft_g = f"g{before_front_vowel}"
    #make an exception
    s = re.sub("gué", "ghé", s)

    s = re.sub(ge, "ʒ", s)
    s = re.sub(soft_g, "ʒ", s)
    return s

def pronoun_circumflex(s):
    o_possesive = f"(?<=[mts])o{eow}"
    s = re.sub(o_possesive, "ô", s)
    return s

def handle_short_e(s):
    short_e = f"{sow}e[ht]?{eow}"
    s = re.sub(short_e, "é", s)
    return s

def plural_determiners(s):
    det = f"{sow}([cdlmts])(es){eow}"
    s = re.sub(det, r"\1é8", s)
    s = re.sub("c(?=é8)", "7", s)
    return s

def handle_l(s):
    #or ville
    s = re.sub(as_word("([mv])illes?"), r"\1il", s)
    s = re.sub(f"illes?{eow}", "ij", s)
    s = re.sub(f"{after_vowel}il+e*", "j", s)
    s = re.sub("ll", "l", s)
    return s

def handle_xcs(s):
    s = re.sub(r"x(?=p|t|k|f|s|ch)", "ks", s)
    s = re.sub(f"x{before_vowel}", "ks", s)
    s=  re.sub("xc", "ks", s)

    s= re.sub(intervocalic("cc"), "ks", s)
    s= re.sub(intervocalic("s"), "z", s)

    s = re.sub("’|'", "", s)

    s = re.sub(intervocalic("c"), "s", s)

    cest = f"cest{eow}"
    s = re.sub(cest, "7é8", s)

    sc_front = f"s?c{before_front_vowel}"
    s = re.sub(sc_front, "s", s)
    cei = f"{vowel}c(?=[ei])"
    s = re.sub(cei, "s", s)
    return s



def handle_vowels(s):
    s = re.sub(as_word("un"), "œ̃", s)
    s = re.sub(f"mmant{eow}", "mẫ1", s)
    s = re.sub(f"mment{eow}", "mẫ2", s)
    s = re.sub(f"ement{eow}", "emẫ2", s)
    s = re.sub(as_word("(femme)|(fame)"), "fã2m", s)
    s = re.sub(f"{after_vowel}mme{eow}", "me", s)


    s = re.sub(f"am(?={not_vowel})", "ẫ3", s)
    s = re.sub(f"an(?={not_vowel})", "ẫ1", s)


    # Difference in pronunciation
    s = re.sub(f"ai[ts(ent)]{eow}", "é", s)

    s = re.sub(f"aim(?={not_vowel})", "ễ1", s)
    s = re.sub(f"ain(?={not_vowel})", "ễ2", s)
    s = re.sub(f"en(?={not_vowel})", "ã2", s)
    s = re.sub(f"em(?={not_vowel})", "ã4", s)
    s = re.sub(f"(?<={consonant})en(?={vowel})", "ã2", s)
    s = re.sub(f"(?<=(acc)|(cid))ents?{eow}", "ã2", s)
    s = re.sub(f"rent{eow}", "re", s)
    s = re.sub(f"ent{eow}", "ã2", s)

    s = re.sub(f"(eun)|(un)(?={not_vowel})", "œ̃", s)
    s = re.sub(f"ien(?={not_vowel})", "iẽ2", s)
    s = re.sub(f"ieu", "jeu", s)
    s = re.sub(f"onp*(?={not_vowel})", "õ1", s)
    s = re.sub(f"onp*(?={not_vowel})", "õ2", s)
    s = re.sub("ù", "u", s)

    s = re.sub(f"uin(?={not_vowel})", "uẽ", s)
    s = re.sub(f"oin(?={not_vowel})", "ouẽ", s)
    s = re.sub(f"[iy]m(?={not_vowel})", "aî̃1", s)
    s = re.sub(f"e?[iy]n(?={not_vowel})", "aî̃2", s)
    s = re.sub(f"e[uû]t?(?={not_vowel})", "u", s)


    s = re.sub("(œu)|(oeu)", "eu", s)
    s = re.sub(f"(?<=({consonant})+)er{eow}", "èr", s)
    s = re.sub(f"e[rz]{eow}", "é", s)
    return s


def handle_glides(s):
    s = re.sub(intervocalic("y"), "j", s)
    # High vowels become glides before vowels
    s = re.sub(f"ou{before_vowel}", "w", s)
    s = re.sub("gua", "gwa", s)
    s = re.sub(f"(?<=[^g])u(?=y|{vowel})", "ɥ", s)
    #don't delete this g
    s = re.sub(f"(?<=g)ues*{eow}", "g", s)
    s = re.sub(f"(?<=g)u(?=y|{vowel})", "ou", s)
    s = re.sub(r"long(?=\W|$|t)", "lõ1", s)
    s = re.sub(f"y{before_vowel}", "j", s)
    s = re.sub(f"y", "j", s)
    return s

def handle_misc(s):
    #more vowel stuff
    s = re.sub(r"ct(?=(am|an|aen|aim|ain|aon|em|en|ein|eun|ien|im|in|oin|om|on|uin|uin|um|un|ym|yn))", "", s)
    s = re.sub(f"eing{eow}", "ein", s)
    s = re.sub(f"e(?=({consonant}){{2,}})", "ɛ", s)
    s = re.sub(f"(?={vowel}.+)e(?={consonant})", "ɛ", s)

    #some silent consonants
    s = re.sub(f"(s|nt){eow}", "", s)
    s = re.sub(f"(?<={vowel}|r)[dp]{eow}", "", s)
    s = re.sub(f"(?<=[1-4])[td]{eow}", "", s)
    s = re.sub(f"(?<=ã4)ps{eow}", "", s)
    s = re.sub(f"{after_vowel}dd|pp{eow}", "", s)
    s = re.sub(f"{after_vowel}g{eow}", "", s)
    s = re.sub(f"{after_vowel}gg{eow}", "g", s)
    s = re.sub(f"ot{eow}", "o6", s)

    #revisit
    s = re.sub(f"(?<={back_vowel}|{consonant}{{1}})t{eow}", "", s)
    s =  re.sub(f"t{eow}", "", s)
    s =  re.sub(f"o6{eow}", "ot", s)

    s =  re.sub(f"ice(?=\W)", "ss", s)
    return s

def fra_pre(s):
    s = handle_q(s)
    s = handle_j(s)
    s = handle_g(s)
    s = pronoun_circumflex(s)
    s = handle_short_e(s)
    s = plural_determiners(s)
    #second s will get dropped but keeps the rest from being deleted
    s = re.sub(r"[Ee]st-ce", "esss", s)
    s = handle_l(s)
    #s = handle_xcs(s)
    s = handle_vowels(s)
    s = handle_glides(s)
    s = handle_misc(s)
    return s
    
def post_fra(s):
    #Post-processing for French-orthography KV
    vowel= "i|y|ɨ|ʉ|ɯ|u|ɪ|ʏ|ʊ|e|ø|ɘ|ɵ|ɤ|o|ə|ɛ|œ|ɜ|ɞ|ʌ|ɔ|æ|ɐ|a|ɶ|ɑ|ɒ|ã|ɑ̃|ɑ̃|ɛ̃|ɔ̃|œ̃"
    consonant = "b|ʃ|d|f|g|j|k|l|m|n|p|r|s|t|v|w|z|ʒ"
    s = re.sub(f"{sow}[lnd(tr)]ɔ{eow}", "\1o", s)
    s = re.sub(f"(?<={consonant})ɔ(?=({consonant})+{vowel})", "o", s)
    s = re.sub(f"ɔœ̃", "un", s)
    s = re.sub(f"tte{eow}", "t", s)
    s = re.sub(f"(?={consonant}[rl]{eow})", "", s)
    s = re.sub(f"rr", "r", s)

    #determiners
    s = re.sub(f"é8", "ê", s)
    s = re.sub(f"7(?=ê|e)", "ç", s)

    # remove silent H
    # pronounced h -revisit
    #h -> 77 / \W|#|[aɑe]_[aɑe]
    h =re.sub("h", "", s)
    #77 -> h / \W|#|[aɑe]_[aɑe]


    #remove schwa before initial vowel or at end of line (verse)
    s =re.sub(f"ə(?={vowel}|{boundary})", "", s)

    #eliminate <e> which should not be pronounced before future, conditional endings
    s =re.sub(f"(?<=({vowel})({consonant}))[əɛ]rie{eow}","rie", s)
    s =re.sub(f"(?<=({vowel})({consonant}))[əɛ]rɛ{eow}", "rɛ", s)
    s =re.sub(f"(?<=({vowel})({consonant}))[əɛ]ra{eow}", "ra", s)
    s =re.sub(f"(?<=({vowel})({consonant}))[əɛ]re{eow}", "re", s)
    s =re.sub(f"(?<=({vowel})({consonant}))[əɛ]riɔ̃{eow}", "riɔ̃", s)


    # restore <y> between <g> and <s>
    s =re.sub("gs", "gys", s)
    s =re.sub(r"pœ\-ɛtr", "pœtɛt", s)


    # remove hyphens
    s =re.sub(r"\-", "", s)

    s =re.sub(f"j(?={vowel})", "i", s)
    s =re.sub(f"tj", "sj", s)
    # replace <j> with <i> between consonants
    s =re.sub(f"(?<={consonant})j(?={consonant})", "i", s)
    s =re.sub(f"(?<=[nt])ə", "", s)
    s =re.sub(f"(?<=mou|b|arj)ɑ̃[0-4]{eow}", "ɛ̃", s)
    s =re.sub(f"[ɔo]tɛ{eow}", "ɔt", s)

    #drop the r for -ir, -re verbs
    s =re.sub(f"ir{eow}", "i", s)
    return s

def pre_ipa_kv(s):
    consonant = "b|h|d|f|g|j|k|l|m|n|p|r|s|t|v|w|z"
    s = re.sub("ã", "ɑ̃", s)
    s = re.sub("ə̃", "ɛ̃", s)
    s = re.sub("ã", "ɑ̃", s)
    s = re.sub("e", "é", s)
    s = re.sub(f"(?<={boundary})s(?=a|é{boundary})", "ç", s)
    s = re.sub(f"(?<={boundary})s(?=’a(l|p)é?{boundary})", "ç", s)
    s = re.sub(f"(?<={boundary})s(?=’(a|i)(la)*{boundary})", "ç", s)

    s  =re.sub(f"(?<=a|i|ɛ|ò)([nm])(?={boundary})", r"\1\1", s)
    s  = re.sub(f"nj", "ñ", s)

    #mid
    s  = re.sub(r"ɛ̃[1-2]?(?=n)", "èn", s)
    s  = re.sub(r"ɛ̃1", "im", s)
    s  = re.sub(r"ɛ̃2", "in", s)
    #s  = re.sub(r"fɛ̃", "fim", s)
    s  = re.sub(r"ɛ̃", "in", s)
    s  = re.sub(r"ɔœ̃", "œ̃", s)
    s  = re.sub(f"mœ̃{eow}", "myn", s)
    s  = re.sub(f"œ̃", "ym", s)

    s  = re.sub(f"ɔ̃1", "on", s)
    #special override
    s  = re.sub(f"ɔ̃2m", "onm", s)
    s  = re.sub(r"ɔ̃2", "om", s)
    s  = re.sub(r"ɔ̃(?=[bp])", "om", s)
    s  = re.sub(f"kɔ̃{eow}", "kom", s)
    s  = re.sub(r"nɔ̃\-", r"nom\-", s)
    s  = re.sub(r"\-nɔ̃", r"\-nom", s)
    s  = re.sub(r"ɔ̃", r"on", s)

    #low
    s  = re.sub(r"ɑ̃(1|3)n", r"ònn", s)
    s  = re.sub(r"ɑ̃1m", r"anm", s)
    s  = re.sub(r"ɑ̃1", r"an", s)
    s  = re.sub(r"ɑ̃2", r"en", s)
    s  = re.sub(r"ɑ̃3", r"am", s)
    s  = re.sub(r"ɑ̃4([mn])", r"en\1", s)
    s  = re.sub(r"ɑ̃4", r"em", s)

    s  = re.sub(r"ɑ̃(?<=ɲ|ŋ)", r"a", s)
    s  = re.sub(r"avɑ̃", r"avan", s)
    s  = re.sub(f"tɑ̃t{eow}", r"tant", s)
    s  = re.sub(f"(?<=z|n)ɑ̃{eow}", r"an", s)
    s  = re.sub(r"ésɑ̃s", r"ésɑns", s)

    s  = re.sub(r"ɑ", r"a", s)
    return s

def post_ipa_kv(s):
    oral = "a|e|é|è|i|o|ò|ou|u"
    nasalized = "ɑ̃|ɛ̃|ɔ̃|œ̃"
    vowel = f"{oral}|{nasalized}"

    s = re.sub(r"(?<=m|l|t|s|d|c)é̂|(e8)", "ê", s)
    s = re.sub(r"ò̀", "ò", s)
    s = re.sub(f"ou(?={vowel})", "w", s)
    s = re.sub(f"ii", "iy", s)
    s = re.sub(f"i(?={vowel})", "y", s)
    s = re.sub(f"ɥ", "w", s)
    s = re.sub(f"(?<={vowel})i", "ï", s)
    s = re.sub(f"(?<=e|é)ï", "yi", s)

    s = re.sub(f"òlé{eow}", "olé", s)
    s = re.sub(f"{sow}([kds]){eow}", "r\1e", s)
    return s


def pre_kv_ipa(s):
    oral = "a|e|é|è|i|o|ò|ou|u"
    nasalized = "ɑ̃|ɛ̃|ɔ̃|œ̃"
    vowel = f"{oral}|{nasalized}"
    nasalizer ="n|m"

    s = re.sub("ñ", "ɲ", s)
    s = re.sub(f"ng{eow}", "ŋ", s)

    #The order of these rules is very important.
    #First break up nasalizer in these contexts
    s = re.sub(f"(?<={oral})n({oral})", "1", s)
    s = re.sub(f"(?<={oral})m({oral})", "2", s)
    s = re.sub(f"oun", "ou1", s)
    s = re.sub(f"oum", "ou2", s)
    s = re.sub(f"nɲ", "1ɲ", s)
    s = re.sub(f"(?<=a|i)nn", "qn", s)
    s = re.sub(f"(?<=a|i)mm", "qm", s)



    #Then do the main rules

    s = re.sub(f"(?<=u){nasalizer}", "œ̃", s)
    s = re.sub(f"(?<=o){nasalizer}", "ɔ̃", s)
    s = re.sub(f"(?<=i){nasalizer}", "ɛ̃", s)
    s = re.sub(f"(?<=a|e){nasalizer}", "ɑ̃", s)

    #Handle the special cases
    s = re.sub(f"a(?=a_ɲ|ŋ)", "ɑ̃", s)
    s = re.sub(f"ònn", "òɑ̃n", s)
    s = re.sub(f"ènn", "èɛ̃n", s)

    #Get rid of the original vowel and nasalization breaks
    s = re.sub(f"{oral}(?={nasalized})", "", s)
    s = re.sub(f"u1", "un", s)
    s = re.sub(f"u2", "um", s)
    s = re.sub(f"1ɲ", "nɲ", s)
    s = re.sub(f"1(?={vowel})", "n", s)
    s = re.sub(f"2(?={vowel})", "m", s)
    s = re.sub(f"q(?={nasalizer})", "", s)

    #May or may not want to get rid of apostrophes
    s = re.sub(f"'|’", "", s)
    return s

def post_kv_ipa(s):
    #This one is last because ou will not be nasalized
    s = re.sub(f"u(m|n)", "œ̃", s)
    return s

def pre_dlc_kv(s):
    oral = "a|e|è|i|o|ò|(ou)"
    nasalized = "ɑ̃|ɛ̃|ɔ̃"
    vowel = f"{oral}|{nasalized}"
    nasalizer: = "n|m"

    #semivowel
    s = re.sub("ui", "wi", s)

    #The order of these rules is very important.
    #First break up nasalizer in these contexts
    s = re.sub(f"(?<={oral})n({oral})", "1", s)
    s = re.sub(f"(?<={oral})m({oral})", "2", s)

    #Then do the main rules
    s = re.sub(f"(?<=o|ò){nasalizer}", "ɔ̃", s)
    s = re.sub(f"(?<=e){nasalizer}", "ɛ̃", s)
    s = re.sub(f"(?<=a){nasalizer}", "ɑ̃", s)

    #Get rid of the original vowel and nasalization breaker
    s = re.sub(f"{oral}(?={nasalized})", "", s)
    s = re.sub(f"1(?={vowel})", "n", s)
    s = re.sub(f"2(?={vowel})", "m", s)
    return s

def post_ipa_dlc(s):
    s = re.sub(f"u(?=[aeèioòu])", "w", s)
    s = re.sub(f"i(?=[aeèioòu])", "y", s)
    return s
    
def create_map_dict(map_file):
    reader = csv.reader(open(map_file, "r"))
    mapping = dict(reader)
    #The column labels are an epitran artifact
    mapping.pop("Orth", None)
    return mapping

#Make direct swaps in order
def apply_mapping(s, mapping):
    for k, v in mapping.items():
        s = s.replace(k, v)
    return s

def fra_kv(s, fra_map):
    s = fra_pre(s)
    s = apply_mapping(s, fra_map)
    s = post_fra(s)
    s = pre_ipa_kv(s)
    s = apply_mapping(s, ipa_kv_map)
    s = post_ipa_kv(s)
    return s
"""
some more pre ipa-kv rules to revisit later
ɑ̃ -> en / ko(m|n(t|m))_
ɑ̃ -> òn / (k|j)_n
ɑ̃ -> an / it_::boundary:
ɑ̃ -> em / t_::boundary::
ɑ̃ -> an / k_::boundary::
ɑ̃ -> an / (vaj|mom|(dj*))_
ɑ̃ -> an / ʃ_(m|s)::boundary::
ɑ̃ -> an / _g
ɑ̃ -> an / [ʒ]m_
ɑ̃ -> en / _n|(d|s)::boundary::
ɑ̃ -> em / _b
ɑ̃ -> an / _(ʃ|ʒ|mb)
ɑ̃ -> an / (p|j)_s
ɑ̃ -> en / tr_t
ɑ̃ -> an / (pl)|r_t
ɑ̃ -> an / v_t
ɑ̃ -> an / (l|m)_(k|d)
ɑ̃ -> an / _dal
ɑ̃ -> an / _::boundary::
ɑ̃ -> en / _

o-> ô / ::boundary::s_::boundary::
    #a ->á / ::boundary::l_\?
    #a ->á / ::boundary::ç_la
"""



project_folder = f"{drive_home}/creole_transliteration"
listdir(project_folder)
map_folder = f"{project_folder}/map"
map_files = [f"{map_folder}/{f}" for f in listdir(map_folder)]

fra_map = create_map_dict('/content/drive/My Drive/creole_transliteration/map/lou-Latn-fra.csv')
ipa_kv_map = create_map_dict('/content/drive/My Drive/creole_transliteration/map/lou-IPA-kv.csv')

test = fra_kv("mo frère di mò to va dansé tout lanouitte", fra_map)

