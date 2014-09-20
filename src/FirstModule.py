'''
Created on Jul 11, 2014

@author: Andre
'''
#Define a function
def add(a,b):
    return a+b

#Define a quick function
add = lambda x, y: x + y

#Function that returns several value (use along multiple affectation defined below)
def decomposer(entier, divise_par):
    p_e = entier // divise_par
    reste = entier % divise_par
    return p_e, reste

# !!!!! a function CANNOT modify, by affectation,
#the value of a variable exterior to the space of the function
#Except if we call the variable as global
i = 4 # Une variable, nommée i, contenant un entier
def inc_i():
    """Fonction chargée d'incrémenter i de 1"""
    global i # Python recherche i en dehors de l'espace local de la fonction

# BUT you can append a value to an exterior list for example. Calling a method on an exterior object works

#Import a module and use a function from that module. A function sqrt defined by
#ourselves wouldn't create a conflict with this one. Modules are groups of functions.
import math
math.sqrt(16)
#search for help on given module
help("math")

#Change space of names where module is imported
import math as mathematiques
mathematiques.sqrt(25)

#Import functions from module into our own space (here import all functions from math)
from math import *

#Pause the system while in execution
import os
os.system("pause")

#Import our own module: save code in multipli.py in the same folder as current script
#first and then
from multipli import *

#Insert the following if we want to execute the following ONLY when launching the module itself.
#If we import it, the if condition will be false (__name__ is a variable created at the launch
#of the file
if __name__ == "__main__":
    add(4,5)
    os.system("pause")
    
#Packages are like directories containing modules. Packages can also include packages
#(like a subdirectory). To import all modules within a subpackage for example:
import package1.subpackage3

#To create your own packages, just create the corresponding folders
######################################################################
######################################################################

#try/except to catch errors
#we can catch different errors by specifying its name after except. If we to catch
#all errors, just don't put anything after except

numerator=3
denominator=0
try: #here only put the sensitive part prone to errors
    result = numerator / denominator
except NameError:
    print("La variable numerator ou denominator n'a pas été définie.")
except TypeError:
    print("La variable numerator ou denominator possède un type incompatible avec la division.")
except ZeroDivisionError as renaming_exception:
    print("La variable denominator est égale à 0.")
else: #is executed if no exception is caught. We don't put it in try because nothing sensitive here
    print("Le résultat obtenu est", result)
finally:
    # Instruction(s) exécutée(s) qu'il y ait eu des erreurs ou non
    # Par exemple même s'il y a un return dans un des except, cela sera exécuté

#Assertions: raise an error only if condition is False
var = 5
assert var == 5 #nothing will happen
assert var == 8 #AssertError will be raised

#To raise our own errors: raise and put the name we want. We usually put the exception directly after
annee = input() # L'utilisateur saisit l'année
try:
    annee = int(annee) # On tente de convertir l'année
    if annee<=0:
        raise ValueError("l'année saisie est négative ou nulle")
except ValueError:
    print("La valeur saisie est invalide (l'année est peut-être négative).")
    
#Strings are objects. We can use methods on them. In the following example if we don't 
#put anythin in {} then the order is simply the one in format()
prenom = "Paul"
nom = "Dupont"
age = 21
print( "Je m'appelle {0} {1} ({3} {0} pour l'administration) et j'ai {2} " \
"ans.".format(prenom, nom, age, nom.upper()))

#Concatenate strings:
age = 21
message = "J'ai " + age + " ans."

#Go through strings:
chaine = "Salut les ZER0S !"
chaine[0] # Première lettre de la chaîne
chaine[:2] # Du début jusqu'à la troisième lettre non comprise
chaine[2:] # De la troisième lettre (comprise) à la fin



#############################################################
################# LISTS #####################################
#############################################################


#Define lists (can contain all sorts of types):
ma_liste = [1, 3.5, "une chaine", []]
ma_liste.append(56) # On ajoute 56 à la fin de la liste
ma_liste.insert(2, 'c') # On insère 'c' à l'indice 2
ma_liste2=[1,5]
ma_liste.extend(ma_liste2) # On insère ma_liste2 à la fin de ma_liste
del ma_liste[2] # On supprime le troisième élément de la liste
ma_liste.remove(32) # 
for elt in ma_liste: # elt va prendre les valeurs successives des éléments de ma_liste
    print(elt)
for i, elt in enumerate(ma_liste):
    print("À l'indice {} se trouve {}.".format(i, elt))

#VERY IMPORTANT. Using a method on a list acts directly on the list and DOESN'T RETURN
#ANYTHING. As opposite to strings for example where the modification is in the returned
#value.

#Define a tuple (like a list but non-modifiable)
tuple_non_vide = (1, 3, 5)

#Multiple affectation
a, b = 3, 4

#Convert a string to a list
ma_chaine = "Bonjour à tous"
ma_chaine.split(" ")

#Convet a list to a string
ma_liste = ['Bonjour', 'à', 'tous']
" ".join(ma_liste)

#Define function with unknown number of parameters
def fonction_inconnue(nom, prenom,*parametres): #Here nom and prenom are necessary
...     """Test d'une fonction pouvant être appelée avec un nombre variable de paramètres"""
...     
...     print("J'ai reçu : {}.".format(parametres))

#Use a list a function input
liste_des_parametres = [1, 4, 9, 16, 25, 36]
print(*liste_des_parametres)

#List comprehensions
liste_origine = [0, 1, 2, 3, 4, 5]
[nb * nb for nb in liste_origine] # returns [0, 1, 4, 9, 16, 25]

liste_origine = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[nb for nb in liste_origine if nb % 2 == 0] #returns [2, 4, 6, 8, 10]


#####################################################################
################# DICTIONNARIES #####################################
#####################################################################

#Dictionnaries: like lists but no order and KEYS involved
mon_dictionnaire = {}
mon_dictionnaire["key"] = "value"
mon_dictionnaire = {'mot de passe': '*', 'pseudo': 'Prolixe'}
mon_dictionnaire[5] = "y"
mon_dictionnaire['c', 1] = "fou blanc" #we can use tuples as keys
mon_dictionnaire = {'pseudo', 'mot de passe'} #this is NOT a dictionnaty, but a SET. Like a list, but can't contain the same object twice
del mon_dictionnaire["chemise"] #removes the given key
mon_dictionnaire.pop("chemise") #same as del but returns the deleted value

#We can stock functions in a dictionnary and re-use it!
def fete():
    print("C'est la fête.")
fonctions = {}
fonctions["fete"] = fete
fonctions["fete"]() #returns C'est la fete

#We can go trough the keys or values of a dictionnary:
for key in mon_dictionnaire.keys():
    print(key)
for value in mon_dictionnaire.values():
    print(value)
for key, value in mon_dictionnaire.items():
    print("La clé {} contient la valeur {}.".format(key, value))

#To be able to catch NAMED unknown parameters:
def fonction_inconnue(**parametres_nommes):
    print("J'ai reçu en paramètres nommés : {}.".format(parametres_nommes))

fonction_inconnue(p=4, j=8)
#Returns: J'ai reçu en paramètres nommés : {'p': 4, 'j': 8}

#UNNAMED parameters are in a liste, NAMED parameters are in a dictionnary
def fonction_inconnue(*en_liste, **en_dictionnaire):

#Use a dictionnary a function input
parametres = {"sep":" >> ", "end":" -\n"}
print("Voici", "un", "exemple", "d'appel", **parametres)
#here sep=">>' and end="-\n" for the function print

#############################################################
################# FILES #####################################
#############################################################

#change working directory
import os
os.chdir("C:/tests python/") #set wd
os.getcwd() #get wd

#Read a file
mon_fichier = open("fichier.txt", "r")
contenu = mon_fichier.read()
mon_fichier.close()

#Write in a file
mon_fichier = open("fichier.txt", "w") # Argh j'ai tout écrasé !
mon_fichier.write("Premier test d'écriture dans un fichier via Python") #Returns number of characters written
mon_fichier.close()

#The file is closed at the end EVEN IF IF AN EXCEPTION IS RAISED
with open('fichier.txt', 'r') as mon_fichier:
    texte = mon_fichier.read()
#To use working directory, just indicate relative paths going from 

#To save your OBJECTS:
import pickle
score = {} #let's put a dictionnary for example
with open('donnees', 'wb') as fichier: #open a file as binary
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)

#To read saved objects
with open('donnees', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    score_recupere = mon_depickler.load()
    
ma_liste1 = [1, 2, 3]
ma_liste2 = ma_liste1 #ma_liste2 points to the SAME OBJECT as ma_liste1. Meaning if you modify one, the other one will also be modified
#If you want to create a DISTINCT copy:
ma_liste2 = list(ma_liste1)

ma_liste1 == ma_liste2 # On compare le contenu des listes
ma_liste1 is ma_liste2 # On compare leur référence

###############################################################
################# OBJECTS #####################################
###############################################################

class Personne:
    """Classe définissant une personne caractérisée par :
    - son nom
    - son prénom
    - son âge
    - son lieu de résidence"""

    def __init__(self, nom, prenom): 
    # Constructor for the object
    # Self is always there, even if no other parameters
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
        self.lieu_residence = "Paris"
        
tab=Personne("Lucas","Saloumi")

class TableauNoir:
    """Classe définissant une surface sur laquelle on peut écrire,
    que l'on peut lire et effacer, par jeu de méthodes. L'attribut modifié
    est 'surface'"""

    
    def __init__(self):
        """Par défaut, notre surface est vide"""
        self.surface = ""
    def ecrire(self, message_a_ecrire):
    #An object method (with self parameter)
        """Méthode permettant d'écrire sur la surface du tableau.
        Si la surface n'est pas vide, on saute une ligne avant de rajouter
        le message à écrire"""
    #quand vous tapez tab.ecrire(…), cela revient au même que si vous écrivez TableauNoir.ecrire(tab, …).
        
        if self.surface != "":
            self.surface += "\n"
        self.surface += message_a_ecrire


#Self means we are referring to the instanciated object attribute, not the general class
#Pour résumer, quand vous devez travailler dans une méthode de l'objet sur l'objet lui-même, vous allez passer par self.


# !!!!!!!!!!!!!!! Class attributes (not self) are unique per class
class Compteur:
    """Cette classe possède un attribut de classe qui s'incrémente à chaque
    fois que l'on crée un objet de ce type"""

    
    objets_crees = 0 # Le compteur vaut 0 au départ
    def __init__(self):
        """À chaque fois qu'on crée un objet, on incrémente le compteur"""
        Compteur.objets_crees += 1
    #The following is CLASS METHOD.
    def combien(cls):
        """Méthode de classe affichant combien d'objets ont été créés"""
        print("Jusqu'à présent, {} objets ont été créés.".format(
                cls.objets_crees))
    combien = classmethod(combien)

Compteur.combien() #returns Jusqu'à présent, 0 objets ont été créés.

a = Compteur() # On crée un premier objet
Compteur.objets_crees #Returns 1
Compteur.combien() # returns Jusqu'à présent, 1 objets ont été créés.

b = Compteur()
Compteur.objets_crees #Returns 2
Compteur.combien() # returns Jusqu'à présent, 2 objets ont été créés.

######### STATIC METHODS ###################
# Similar to class methods but don't take any parameters
class Test:
    """Une classe de test tout simplement"""
    def __init__(self):
        """On définit dans le constructeur un unique attribut"""
        self.mon_attribut = "ok"
        
    def afficher():
        """Fonction chargée d'afficher quelque chose"""
        print("On affiche la même chose.")
        print("peu importe les données de l'objet ou de la classe.")
    afficher = staticmethod(afficher)
    
un_test=Test()
dir(un_test) # returns a list of all attributes and methods in  the 
un_test.__dict__ #returns a dictionnary with all atribute names as keys and attribute values as values

#################################################################
################# PROPERTIES#####################################
#################################################################

#Special attributes where we ourselves define what happens when we try to read them or modify them
#Also possible to define what heppens when we delete the attribute (del) or call for help on the attribute (less often used)

#The whole point is to make it appear seamless to the user. He's accessing an attribute as usual 
#but we want special stuff to happen when he does so we define it as a property.

class Personne:
    """Classe définissant une personne caractérisée par :
    - son nom ;
    - son prénom ;
    - son âge ;
    - son lieu de résidence"""

    
    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
        self._lieu_residence = "Paris" # Notez le souligné _ devant le nom: convention pour les proprietes !!!
    def _get_lieu_residence(self):
    """Méthode qui sera appelée quand on souhaitera accéder en lecture
        à l'attribut 'lieu_residence'"""
        
        
        print("On accède à l'attribut lieu_residence !")
        return self._lieu_residence
    def _set_lieu_residence(self, nouvelle_residence):
        """Méthode appelée quand on souhaite modifier le lieu de résidence"""
        print("Attention, il semble que {} déménage à {}.".format( \
                self.prenom, nouvelle_residence))
        self._lieu_residence = nouvelle_residence
    # On va dire à Python que notre attribut lieu_residence pointe vers une
    # propriété
    lieu_residence = property(_get_lieu_residence, _set_lieu_residence) # note that no underscore is in front

jean = Personne("Micado", "Jean")
jean.lieu_residence
#returns On accède à l'attribut lieu_residence !
#'Paris'
jean.lieu_residence = "Berlin"
#returns :Attention, il semble que Jean déménage à Berlin.
jean.lieu_residence
#returns On accède à l'attribut lieu_residence !
#'Berlin'

######################################################################
################# SPECIAL METHODS#####################################
######################################################################

# A special method is surrounded by 2 underscores on each side, just like the constructor !
#Very often it is to personalize already existing functions (we don't even have to write a constructor in theory)

# Special methods for objects and attributes:

#For example, to modify what happens when we just enter an object
class Personne:
    """Classe représentant une personne"""
    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur"""
        return "Personne: nom({}), prénom({}), âge({})".format(
                self.nom, self.prenom, self.age)

p1 = Personne("Micado", "Jean")
p1 # we could also write: repr(p1)
#Instead of <__main__.XXX object at 0x00B46A70> we get:
#Personne: nom(Micado), prénom(Jean), âge(33)

#To modify what happens when we call print(object) (by default uses __repr__):
class Personne:
    """Classe représentant une personne"""
    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
    def __str__(self):
        """Méthode permettant d'afficher plus joliment notre objet"""
        return "{} {}, âgé de {} ans".format(
                self.prenom, self.nom, self.age)
        

print(p1) #or str(p1)

# When we access an attribute : object.attribute, if the attribute is not there then __getattr__ is called. We can redefine it:
def __getattr__(self, nom):
    """Si Python ne trouve pas l'attribut nommé nom, il appelle
    cette méthode. On affiche une alerte"""
    
    print("Alerte ! Il n'y a pas d'attribut {} ici !".format(nom))

# When we modify an attribute : object.attribute=value, then __setattr__ is called. We can redefine it:
def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée quand on fait objet.nom_attr = val_attr.
        On se charge d'enregistrer l'objet"""
        
        object.__setattr__(self, nom_attr, val_attr) # use the __setattr__ method from the parent. If we put self.nom_attr=val_attr, the method is going to call itself infinitely
        self.enregistrer()

# When we delete an attribute : del object.attribute, then __delattr__ is called. We can redefine it (here we forbid the deletion)
def __delattr__(self, nom_attr):
        """On ne peut supprimer d'attribut, on lève l'exception
        AttributeError"""
        
        raise AttributeError("Vous ne pouvez supprimer aucun attribut de cette classe")

# Special methods for containers (lists, dictionnaries, etc.)

#We can define an envelop class for dictionnaries. Zdict will behave like a dictionnary.

class ZDict:
    """Classe enveloppe d'un dictionnaire"""
    def __init__(self):
        """Notre classe n'accepte aucun paramètre"""
        self._dictionnaire = {}
    def __getitem__(self, index):
        """Cette méthode spéciale est appelée quand on fait objet[index]
        Elle redirige vers self._dictionnaire[index]"""
        
        return self._dictionnaire[index]
    def __setitem__(self, index, valeur):
        """Cette méthode est appelée quand on écrit objet[index] = valeur
        On redirige vers self._dictionnaire[index] = valeur"""
        
        self._dictionnaire[index] = valeur

#"in" keyword
8 in ma_liste # is the same as...
ma_liste.__contains__(8)

d1.__add__(4) #is equivalent to d1 + 4. If you want this to work (d1 is an object), you can define __add__ in the class
# same for __sub__ __mul__ etc.
#if we want to define 4 + d1, we can modify __radd__ (pas necessairement commutatif !)
#+= : __iadd__
#== : __eq__
#!= : __ne__
#> : __gt__ etc.

# When saving object (with pickle), __getstate__ is called (if not defined than __dict__ is saved)
# When opening object, the object's dictionnary of attributes (__dict__ or what __getstate__ returned) goes through __setstate__
class Temp:
    """Classe contenant plusieurs attributs, dont un temporaire"""
    
    def __init__(self):
        """Constructeur de notre objet"""
        self.attribut_1 = "une valeur"
        self.attribut_2 = "une autre valeur"
        self.attribut_temporaire = 5
   
    def __getstate__(self):
        """Renvoie le dictionnaire d'attributs à sérialiser"""
        dict_attr = dict(self.__dict__)
        dict_attr["attribut_temporaire"] = 0
        return dict_attr
    
    def __setstate__(self, dict_attr):
        """Méthode appelée lors de la désérialisation de l'objet"""
        dict_attr["attribut_temporaire"] = 0
        self.__dict__ = dict_attr

##############################################################
################# SORTING#####################################
##############################################################

#sort() : class methods for lists only. Doesn't return anything and modifies the list directly
prenoms = ["Jacques", "Laure", "André", "Victoire", "Albert", "Sophie"]
prenoms.sort()
#sorted(): general function for lists, tuples, dictionnaries. Returns the sorted object but doesn't modify the original one
sorted(prenoms)

#python automatically chooses the sorting method based on the type of onjects within the list.
#if all numbers, than number orders. If strings,then alphabetical. If mix, then error is given.






















