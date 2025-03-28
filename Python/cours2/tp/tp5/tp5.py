import heapq
from collections import Counter, namedtuple

class Noeud:
    def __init__(self, caractere, frequence, gauche=None, droite=None):
        self.caractere = caractere
        self.frequence = frequence
        self.gauche = gauche
        self.droite = droite
    
    def __lt__(self, autre):
        return self.frequence < autre.frequence

def construire_arbre_huffman(texte):
    frequence = Counter(texte)
    heap = [Noeud(c, f) for c, f in frequence.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        gauche = heapq.heappop(heap)
        droite = heapq.heappop(heap)
        noeud_parent = Noeud(None, gauche.frequence + droite.frequence, gauche, droite)
        heapq.heappush(heap, noeud_parent)
    
    return heap[0]

def generer_codes_huffman(arbre, prefixe="", code_huffman={}):
    if arbre:
        if arbre.caractere is not None:
            code_huffman[arbre.caractere] = prefixe
        generer_codes_huffman(arbre.gauche, prefixe + "0", code_huffman)
        generer_codes_huffman(arbre.droite, prefixe + "1", code_huffman)
    return code_huffman

def compresser(texte):
    arbre = construire_arbre_huffman(texte)
    dictionnaire = generer_codes_huffman(arbre)
    code_binaire = "".join(dictionnaire[c] for c in texte)
    return code_binaire, dictionnaire, arbre

def decomprimer(code_binaire, arbre):
    texte = ""
    noeud = arbre
    for bit in code_binaire:
        noeud = noeud.gauche if bit == "0" else noeud.droite
        if noeud.caractere is not None:
            texte += noeud.caractere
            noeud = arbre
    return texte

if __name__ == "__main__":
    texte = "huffman coding is fun"
    code_binaire, dictionnaire, arbre = compresser(texte)
    texte_decompresse = decomprimer(code_binaire, arbre)
    
    assert texte == texte_decompresse
    print("Texte compressé:", code_binaire)
    print("Texte décompressé:", texte_decompresse)