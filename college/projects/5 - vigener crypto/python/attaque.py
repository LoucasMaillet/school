#! /usr/bin/python3.10
# -*- coding: utf-8 -*-
"""
Mini-projet Vigénère : attaque du cryptosystème
@author: Lucas Maillet
"""

from unicodedata import normalize
from collections import defaultdict
from typing import Iterable, Iterator
from vigenere import dechiffrer, ascii_uppercase, TKey

# Type alias

TTree = dict[str, dict | set]
TNode = dict[str, dict | set] | set

# Functions & attack procedure


def to_ascii_upper(words: Iterable[str]) -> Iterator[str]:
    return map(lambda word: normalize('NFKD', word).encode('ascii', 'ignore').upper().decode("ascii"), words)


def to_tree(words: Iterable[str]) -> TTree:
    tree = {}

    def __set_node(i: int, j: int, parent: TNode):
        char = words[i][j]
        j += 1
        if not char in parent:  # If node or pre-leaf node
            parent[char] = {} if j+1 < len(words[i]) else set()
        if j+1 == len(words[i]):  # If leaf
            parent[char].add(words[i][-1])
        else:
            __set_node(i, j, parent[char])

    for i in range(len(words)):
        __set_node(i, 0, tree)
    return tree


def inter_tree(tree_base: TTree, tree_dif: TTree) -> TTree:
    tree = {}

    def __set_node(dest: TTree, parent0: TNode, parent1: TNode) -> TNode:
        for k, v in parent0.items():
            if k in parent1:
                v_ = v.copy()
                dest[k] = v_
                if isinstance(v_, dict):
                    __set_node(v_, v, parent1[k])

    __set_node(tree, tree_base, tree_dif)
    return tree


def pkeys_word(pword: TTree, word: str) -> Iterator[TKey]:
    top = len(word) - 1

    def __find_k(pword_: TNode, key: TKey, i: int):
        for j in range(len(ascii_uppercase)):
            char = dechiffrer(word[i], (j,))
            if char in pword_:
                if i == top:
                    # print(dechiffrer(word, key + (j,)), key + (j,))
                    yield key + (j,)
                else:
                    yield from __find_k(pword_[char], key + (j,), i + 1)

    yield from __find_k(pword, tuple(), 0)


def pkey_diff(key_from: str, key_to: str) -> int:
    return (ascii_uppercase.index(key_to) - ascii_uppercase.index(key_from)) % 26


def correct_index(string: str, word: str) -> int:
    j = string.find(word)
    return (j - string.count(' ', 0, j))


if __name__ == "__main__":  # By probability
    msg = "DL ZHGIVUEL OD UL LQK TYDVL OIL XEU DLC YEIOSASOI KVXJ KBBI WA PYWYC TWBH QDVBI IBO BWZ QUFZ SDLLVBANODLZ CEFA OCHSSI VL NEMAOI"
    keys_occ = tuple(defaultdict(int) for _ in range(4))
    j = 0
    for i, c in enumerate(msg):
        if c not in ascii_uppercase:
            j += 1
            continue
        keys_occ[(i-j) % 4][c] += 1
    keys = tuple(pkey_diff('E', max(occ, key=occ.get)) for occ in keys_occ)
    print(keys)

if __name__ == "__mains__":  # By almost brute force
    msg = "DL ZHGIVUEL OD UL LQK TYDVL OIL XEU DLC YEIOSASOI KVXJ KBBI WA PYWYC TWBH QDVBI IBO BWZ QUFZ SDLLVBANODLZ CEFA OCHSSI VL NEMAOI"
    # From https://www.listesdemots.com/motsde2lettres.htm
    words_2char = "aa", "ah", "ai", "aï", "an", "as", "au", "ay", "ba", "bê", "bi", "bu", "çà", "ça", "ce", "ci", "da", "de", "dé", "do", "du", "dû", "dû", "eh", "en", "es", "ès", "et", "eu", "ex", "fa", "fi", "go", "ha", "hé", "hi", "ho", "if", "il", "in", "je", "ka", "la", "là", "la", "le", "lé", "li", "lu", "ma", "me", "mi", "mu", "mû", "na", "ne", "né", "né", "ni", "nô", "nu", "oc", "oh", "om", "on", "or", "os", "ou", "où", "pi", "pu", "qi", "ra", "ré", "ri", "ru", "sa", "se", "si", "su", "ta", "te", "té", "to", "tô", "tu", "ud", "un", "us", "ut", "va", "vé", "vs", "vu", "wu", "xi"
    # Turn to uppercase and normalize non-ascii word (can generate duplicate)
    words_2char = (*to_ascii_upper(words_2char),)
    # From https://www.listesdemots.com/motsde3lettres.htm
    words_3char = "aas", "ace", "ada", "ado", "aga", "age", "âge", "âgé", "agi", "aïd", "aie", "aïe", "ail", "air", "ais", "aïs", "ait", "ale", "alu", "âme", "ami", "ana", "âne", "ani", "ans", "api", "app", "ara", "arc", "are", "arf", "ars", "art", "asa", "ase", "aux", "avé", "axa", "axe", "axé", "ays", "bac", "bah", "bai", "bal", "ban", "bar", "bas", "bat", "bât", "bau", "béa", "bec", "bée", "béé", "bel", "ben", "ber", "beu", "bey", "bic", "bim", "bio", "bip", "bis", "bit", "blé", "boa", "bob", "bof", "bog", "bol", "bon", "bop", "bot", "box", "boy", "bru", "bue", "bug", "bun", "bus", "but", "bût", "bye", "cab", "caf", "cal", "cap", "car", "cas", "cep", "ces", "cet", "chu", "cif", "cil", "cis", "clé", "cob", "coi", "col", "com", "con", "coq", "cor", "côt", "cou", "cox", "cré", "cri", "cru", "crû", "cul", "cut", "dab", "dah", "dal", "dam", "dan", "dao", "daw", "deb", "déj", "del", "dém", "déo", "der", "des", "dés", "des", "dès", "dey", "dia", "din", "dip", "dis", "dit", "dît", "dix", "doc", "dol", "dom", "don", "dop", "dos", "dot", "dru", "dry", "dub", "duc", "due", "duo", "dur", "dus", "dûs", "dut", "dût", "dzo", "eau", "éco", "écu", "égo", "élu", "ému", "éon", "épi", "ère", "erg", "ers", "est", "êta", "été", "eue", "euh", "eus", "eut", "eût", "eux", "ève", "éwé", "exo", "fac", "faf", "fan", "faq", "far", "fat", "fax", "fée", "fer", "feu", "fez", "fia", "fic", "fie", "fié", "fil", "fin", "fis", "fit", "fît", "fiu", "fix", "fla", "fob", "foc", "fog", "foi", "fol", "fon", "for", "fou", "fox", "fui", "fun", "fur", "fus", "fut", "fût", "gag", "gai", "gal", "gan", "gap", "gay", "gaz", "gel", "géo", "gex", "ghi", "gif", "gin", "gis", "gît", "glu", "goï", "gon", "gos", "goy", "gré", "gué", "gui", "gur", "gus", "gym", "haï", "han", "hem", "hep", "heu", "hia", "hic", "hie", "hié", "hip", "hit", "hop", "hot", "hou", "hua", "hub", "hue", "hué", "hui", "hum", "hun", "ibn", "ibo", "ici", "ide", "ifs", "île", "ils", "ion", "ipé", "ira", "ire", "iso", "ive", "ixa", "ixe", "ixé", "jab", "jam", "jan", "jar", "jas", "jet", "jeu", "job", "jus", "kan", "kas", "kat", "kéa", "ken", "ket", "khi", "kid", "kif", "kil", "kip", "kir", "kit", "kob", "koï", "kop", "kot", "kru", "ksi", "kwa", "kyu", "lac", "lad", "lai", "lao", "las", "led", "lei", "lek", "lem", "les", "lés", "lès", "let", "leu", "lev", "lez", "lia", "lie", "lié", "lin", "lis", "lit", "loa", "lob", "lof", "log", "loi", "lol", "los", "lot", "lue", "lui", "luo", "lus", "lut", "lût", "lux", "lys", "mac", "mag", "mai", "mal", "man", "mao", "mas", "mat", "mât", "max", "mec", "mél", "méo", "mer", "mes", "met", "mie", "mil", "min", "mir", "mis", "mit", "mît", "mix", "mmm", "moa", "mob", "moi", "mol", "mon", "môn", "mor", "mos", "mot", "mou", "mox", "mua", "mue", "mué", "mug", "mur", "mûr", "mus", "mut", "mût", "mye", "nac", "nan", "nay", "née", "nef", "nem", "néo", "nés", "net", "ney", "nez", "nia", "nib", "nid", "nie", "nié", "nif", "nim", "nit", "nom", "non", "nos", "nôs", "nua", "nue", "nué", "nui", "nul", "nus", "oba", "obi", "ode", "off", "ohé", "ohm", "oie", "oïl", "ois", "oit", "oka", "ola", "olé", "onc", "ont", "ope", "öre", "ors", "osa", "ose", "osé", "ost", "ôta", "ôte", "ôté", "oud", "ouf", "ouh", "oui", "ouï", "out", "ove", "ové", "oxo", "oye", "paf", "pal", "pan", "pap", "par", "pas", "pat", "pec", "pep", "pet", "peu", "pff", "phi", "phô", "pic", "pie", "pif", "pin", "pis", "piu", "pli", "plu", "pop", "pot", "pou", "pré", "pro", "psi", "pst", "psy", "pua", "pub", "pue", "pué", "pur", "pus", "put", "pût", "puy", "qat", "qin", "qis", "que", "qui", "rab", "rac", "rad", "rai", "raï", "ram", "rap", "ras", "rat", "ray", "raz", "réa", "rée", "réé", "reg", "rem", "rez", "rhé", "rhô", "ria", "rib", "rie", "rif", "rio", "ris", "rit", "rît", "riz", "rob", "roc", "roi", "rom", "ros", "rot", "rôt", "rua", "rue", "rué", "rus", "rut", "ruz", "rye", "sac", "saï", "sal", "sar", "sas", "sax", "sec", "sel", "sen", "sep", "ses", "set", "sic", "sil", "sir", "sis", "six", "ska", "ski", "soc", "soi", "sol", "som", "son", "sot", "sou", "spa", "spi", "sua", "suc", "sud", "sue", "sué", "sup", "sur", "sûr", "sus", "sut", "sût", "tac", "taf", "tag", "tan", "tao", "tar", "târ", "tas", "tat", "tau", "tec", "tee", "tef", "tek", "tel", "tep", "ter", "tes", "tés", "tes", "têt", "tex", "thé", "tic", "tif", "tin", "tip", "tir", "toc", "tof", "toi", "tom", "ton", "top", "tos", "tôs", "tôt", "tri", "tua", "tub", "tue", "tué", "tuf", "tus", "tut", "tût", "uds", "une", "uni", "uns", "ure", "usa", "use", "usé", "ute", "val", "van", "var", "vas", "vau", "ver", "vés", "vêt", "via", "vie", "vif", "vil", "vin", "vis", "vit", "vît", "voc", "vol", "vos", "vue", "vus", "wad", "wap", "wax", "web", "woh", "wok", "won", "wus", "yak", "yam", "yen", "yet", "yin", "yod", "yue", "zec", "zée", "zef", "zek", "zen", "zig", "zip", "zob", "zoé", "zoo", "zou", "zup", "zut"
    # Turn to uppercase and normalize non-ascii word (can generate duplicate)
    words_3char = (*to_ascii_upper(words_3char),)
    # Tree of possible 2 & 3 words
    # Tree structure is for sort of dicotomic research -> avoid search time
    tree_2char = to_tree(words_2char)
    tree_3char = to_tree(words_3char)
    # small optimization in our case
    tree_2and3char = inter_tree(tree_3char, tree_2char)

    pkeys = [*pkeys_word(tree_2and3char, "DLC")]  # Get base keys
    msg_split = msg.split()

    # Sort know keys by interpolation with subkey of 2
    for i, w in enumerate(filter(lambda w: len(w) == 2, msg_split)):
        i = correct_index(msg, w) % 4
        wkeys = (*pkeys_word(tree_2char, w),)
        pkeys = tuple(key for key in pkeys if any(
            wkey[:3-i] == key[i:i+2] for wkey in wkeys))

    # Sort know keys by interpolation with subkey of 3
    for w in filter(lambda w: len(w) == 3, msg.split()):
        i = correct_index(msg, w) % 4
        wkeys = (*pkeys_word(tree_3char, w), msg_split)
        pkeys = tuple(key for key in pkeys if any(
            wkey[:3-i] == key[i:i+3] for wkey in wkeys))

    for key in pkeys:
        for i in range(len(ascii_uppercase)):
            key_ = (*key, i)
            print(
                f"Decryption with {key_} as key:\n{dechiffrer(msg, key_)}`\n")

    final_key = (18, 7, 10, 16)  # Founded key
    decrypt_key = "LE PROBLEME EN CE BAS MONDE EST QUE LES IMBECILES SONT SURS ET FIERS DEUX ALORS QUE LES GENS INTELLIGENTS SONT EMPLIS DE DOUTES"
    print(f"Found key: {final_key}\nDecrypted msg:\n{decrypt_key}")
