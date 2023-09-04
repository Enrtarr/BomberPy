
# with open('./saves/test1.txt', 'r') as reader:
#     # lit chaque ligne du fichier un par un
#     # for ligne in reader:
#     #     print(ligne, end='')
#     amogus = reader.readlines()

# with open('./saves/test1.txt', 'w') as writer:
#     # inverse l'ordre des lignes du fichier
#     # writer.writelines(reversed(amogus))
    
#     # inverse l'ordre des lignes du fichier
#     for ligne in reversed(amogus):
#         writer.write(ligne)


class LecteurDeFichier():
    def __init__(self, file_path:str):
        self.__path = file_path
        self.__file_object = None
        if not file_path.endswith('.txt'):
            raise NameError("File must be a '.txt' extension")

    def __enter__(self):
        self.__file_object = open(self.__path, 'r')
        return self

    def __exit__(self, type, val, tb):
        self.__file_object.close()
    
    def lireFichier(self):
        return self.__file_object.readlines()

    def lireLigne(self, num:int):
        # on prend la ligne n°num, et on enlève le dernier charactère (EOL)
        ligne = self.__file_object.readlines()[num-1][:-1]
        return ligne
        

class EcriveurDeFichier():
    def __init__(self, file_path:str):
        self.__path = file_path
        self.__file_object = None
        if not file_path.endswith('.txt'):
            raise NameError("File must be a '.txt' extension")

    def __enter__(self):
        self.__file_object = open(self.__path, 'w')
        return self

    def __exit__(self, type, val, tb):
        self.__file_object.close()
    
    def ecrireLigne(self, fichier:list, ligne:int, cont:str):
        # print('started writing...')
        i=1
        for line in fichier:
            # print(f'{i}?{ligne}')
            print(f'{i}={fichier[i-1][:-1]}')
            if i == ligne:
                self.__file_object.write(cont + '\n')
                print(f'{i}>{cont}')
            else:
                self.__file_object.write(line)
            i+=1
        


# with LecteurDeFichier('./datas/settings.txt') as liseur:
    # Perform custom class operations
    # fichier_1 = liseur.lireFichier()
    # print(fichier_1)
    # ligne_2 = liseur.lireLigne(2)
    # print(ligne_2)

# with EcriveurDeFichier('./datas/settings.txt') as ecriveur:
#     ecriveur.ecrireLigne(fichier_1, 3, 'sussy')
