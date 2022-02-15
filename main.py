import sys, copy
from comando import *

##########################
# Trabalho realizado por Nicolas Demantova Ribeiro
# UDESC CCT - Joinville/SC
# Semestre 2021/2
# TEC0001 - Professora Karina Girardi Roggia
##########################


#########PSEUDOALGORITMO#########
# Descobrir alfabeto da máquina
# CRIAR MAQUINAAUX1.TXT
#    Máquina essencialmente separa cada símbolo por espaço e insere um # no começo
# Para cada estado da máquina original
    # Criar 3 outros estados: Um inverso, um de pulo duplo e um pulo duplo inverso
    # O estado inverso será igual ao estado normal, exceto que seu movimento será invertido
    # Cada estado de pulo duplo seguirá o mesmo comando dado, exceto que não realizará nenhuma escrita ou leitura
    # Criar um estado auxiliar que inverte a polaridade da máquina, assim alternando entre normal e inverso
##################################

# ESTRUTURA #
# O arquivo principal se chama comandos, é um objeto com arrays. O cabeçalho de cada objeto corresponde
# ao estado atual em que o comando se encontra. Dentro dele um array contendo a classe Comando, que contem a tupla
# respectiva ao comando, em nenhuma ordem particular
# EX:
# {
#     'Estado0': [COMANDO1, COMANDO2, COMANDO3...],
#     'Estado1': [COMANDO1, COMANDO2, COMANDO3...],
#     'Estado2': [COMANDO1, COMANDO2, COMANDO3...],
#     ...
# }
permitidas = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*_!~|&"


def main(args):
    global permitidas
    comandos = dict()
    estados_tot = 0
    if len(args) > 1:  # File used as parameter
        try:
            comandos = carregar_arquivo(args[1])
            printar_comandos(comandos)
        except IOError:
            print("Erro em carregar arquivo!")
            return
        # COMEÇAR
        # Descobrir alfabeto
        alfabeto = []
        for comando in comandos:
            for j in range(len(comandos[comando])):
                if comandos[comando][j].current_symbol not in alfabeto:
                    alfabeto.append(comandos[comando][j].current_symbol)
        for i in alfabeto:
            if i not in permitidas:
                print("ERRO! ENTRADA CONTÉM CARACTERES NÃO PERMITIDOS!")
                return
        # Criar estado init (0)
        if '*' in alfabeto:
            alfabeto.remove('*')
        if '_' in alfabeto:
            alfabeto.remove('_')
        init = dict()
        init["0"] = []
        for i in alfabeto:
            init["0"].append(Comando("0", i, "#", "R", "escreve_{}_init".format(i)))
        # Criar estados escreve_x_init
        escreve_x_init = dict()
        for i in alfabeto:
            if not "escreve_{}_init".format(i) in escreve_x_init:
                escreve_x_init["escreve_{}_init".format(i)] = []
            for j in alfabeto:
                escreve_x_init["escreve_{}_init".format(i)].append(
                    Comando("escreve_{}_init".format(i), j, i, "R", "escreve_{}_init".format(j))
                    )
            escreve_x_init["escreve_{}_init".format(i)].append(
                Comando("escreve_{}_init".format(i), "_", i, "R", "escreve_@")
                )
        # Criar estado escreve_@
        escreve_arroba = dict()
        escreve_arroba["escreve_@"] = []
        for i in alfabeto:
            escreve_arroba["escreve_@"].append(Comando("escreve_@", i, "@", "L", "rebobinar"))
        escreve_arroba["escreve_@"].append(Comando("escreve_@", "_", "@", "L", "rebobinar"))
        # Criar estados escreve_x
        escreve_x = dict()
        escreve_x["escreve_branco"] = []
        for i in alfabeto:
            if not "escreve_{}".format(i) in escreve_x:
                escreve_x["escreve_{}".format(i)] = []
            for j in alfabeto:
                escreve_x["escreve_{}".format(i)].append(
                    Comando("escreve_{}".format(i), j, i, "R", "escreve_{}".format(j))
                    )
            escreve_x["escreve_branco"].append(
                Comando("escreve_branco", i, "_", "R", "escreve_{}".format(i))
                )
            escreve_x["escreve_{}".format(i)].append(
                Comando("escreve_{}".format(i), "_", i, "R", "escreve_branco")
                )
            escreve_x["escreve_{}".format(i)].append(
                Comando("escreve_{}".format(i), "@", i, "R", "escreve_@")
                )
        escreve_x["escreve_branco"].append(Comando("escreve_branco", "@", "_", "R", "escreve_@"))
        escreve_x["escreve_branco"].append(Comando("escreve_branco", "_", "_", "L", "rebobinar"))

        # Criar estados fixos (rebobinar + rebobinar_start e start)
        fixos = dict()
        fixos["start"] = []
        fixos["start"].append(Comando("start", "@", "_", "L", "rebobinar_start"))
        fixos["start"].append(Comando("start", "*", "*", "R", "escreve_branco"))
        fixos["rebobinar_start"] = []
        fixos["rebobinar_start"].append(Comando("rebobinar_start", "*", "*", "L", "rebobinar_start"))
        fixos["rebobinar_start"].append(Comando("rebobinar_start", "#", "*", "R", "1"))
        fixos["rebobinar"] = []
        fixos["rebobinar"].append(Comando("rebobinar", "#", "#", "R", "start"))
        fixos["rebobinar"].append(Comando("rebobinar", "_", "_", "R", "start"))
        fixos["rebobinar"].append(Comando("rebobinar", "*", "*", "L", "rebobinar"))


        # COMEÇAR INVERSÕES

        # Criar estados clones inversos
        # Escritos da forma (estado_atual)_inverso_(nro_comando)

        inversos = dict()
        """
        for i in comandos:
            for j in range(len(comandos[i])):
                tmp = copy.copy(comandos[i][j])
                inversos["{}_inverso_{}".format(i, j)] = []
                tmp.current_state = "{}_inverso_{}".format(i, j)
                if tmp.direction.upper() == "L":
                    tmp.direction = "R"
                else:
                    tmp.direction = "L"
                inversos["{}_inverso_{}".format(i, str(j))].append(
                    Comando("{}_inverso_{}".format(i, str(j)), "#", "#", "R", tmp.new_state)
                    )
                if tmp.new_state != 'halt-accept':
                    tmp.new_state = "{}_duplo_inverso_{}".format(i, str(j))
                inversos["{}_inverso_{}".format(i, str(j))].append(tmp)
        """
        for i in comandos:
            inversos["{}_inverso".format(i)] = []
            for j in range(len(comandos[i])):
                tmp = copy.copy(comandos[i][j])
                if tmp.direction.upper() == 'L':
                    tmp.direction = "R"
                else:
                    tmp.direction = "L"
                tmp.current_state = "{}_inverso".format(i)
                tmp.new_state = "{}_duplo_inverso_{}".format(i, str(j))
                inversos["{}_inverso".format(i)].append(tmp)
            inversos["{}_inverso".format(i)].append(
                Comando("{}_inverso".format(i), "#", "#", "R", i)
                )


        # Criar estados de pulo duplo normais
        # Escritos da forma (estado_atual)_duplo_(nro_comando)

        pulo_duplo = dict()
        # 0 0 0 R 1
        # {}_duplo_{} * * R 1
        for i in comandos:
            for j in range(len(comandos[i])):
                cmd = copy.copy(comandos[i][j])
                pulo_duplo["{}_duplo_{}".format(i, str(j))] = []
                pulo_duplo["{}_duplo_{}".format(i, str(j))].append(
                    Comando("{}_duplo_{}".format(i, str(j)), "*", "*", cmd.direction, cmd.new_state)
                    )
                pulo_duplo["{}_duplo_{}".format(i, str(j))].append(
                    Comando("{}_duplo_{}".format(i, str(j)), "#", "*", "R",
                            "{}_duplo_inverso_{}".format(i, str(j)))
                    )

        # Criar estados de pulo duplo invertidos
        # Escritos da forma (estado_atual)_duplo_inverso_(nro_comando)

        pulo_duplo_inverso = dict()

        for i in comandos:
            for j in range(len(comandos[i])):
                print(i + " " + str(j))
                cmd = copy.copy(comandos[i][j])
                if cmd.direction.upper() == "L":
                    cmd.direction = "R"
                else:
                    cmd.direction = "L"
                pulo_duplo_inverso["{}_duplo_inverso_{}".format(i, str(j))] = []
                pulo_duplo_inverso["{}_duplo_inverso_{}".format(i, str(j))].append(
                    Comando("{}_duplo_inverso_{}".format(i, str(j)),
                            "*", "*", cmd.direction, "{}_inverso".format(cmd.new_state))
                    )

        # Criar estados de inversão de polaridade
        # Escritos da forma (estado_original)_inversao_(estado_destino)

        polaridade = dict()

        # 0_duplo_3 * * R 3
        # 0_duplo_3 # * L 0_duplo_inverso_3
        """
        for i in comandos:
            for j in range(len(comandos[i])):
                cmd = copy.copy(comandos[i][j])
                polaridade["{}_polaridade_{}".format(i, j)] = []
                polaridade["{}_polaridade_{}".format(i, j)].append(
                    Comando("{}_polaridade_{}".format(i, j),
                            "*", "*", "R", "{}_inverso_{}".format(cmd.new_state, str(j)))
                    )
        """
        # Corrigir caminho na Máquina original

        for i in comandos:
            for j in range(len(comandos[i])):
                if not comandos[i][j].new_state.startswith("halt"):
                    comandos[i][j].new_state = "{}_duplo_{}".format(i, str(j))

        # PRINTS
        # print(alfabeto)
        # printar_comandos(escreve_x)
        # printar_comandos(fixos)
        # printar_comandos(escreve_x_init)
        # printar_comandos(init)
        # printar_comandos(escreve_arroba)
        # printar_comandos(comandos)
        # printar_comandos(inversos)
        # printar_comandos(pulo_duplo)
        # printar_comandos(pulo_duplo_inverso)
        # printar_comandos(polaridade)
        # printar_comandos(comandos)

        merge = copy.copy(comandos)
        merge.update(escreve_x)
        merge.update(fixos)
        merge.update(escreve_x_init)
        merge.update(init)
        merge.update(escreve_arroba)
        merge.update(inversos)
        merge.update(pulo_duplo)
        merge.update(pulo_duplo_inverso)
        # merge.update(polaridade)
        #printar_comandos(merge)

        exportar_arquivo(merge)





        """
        # Criar estados de Pulo Duplo inversos
        # Para cada comando, de cada estado, criar um estado com um único comando que só redireciona
        pulo_duplo_inverso = dict()  # Escrito da forma {}_duplo_inverso_{}
        for i in inversos:
            for j in inversos[i]:
                cmd = inversos[i][j]
                pulo_duplo_inverso["{}_duplo_inverso_{}".format(i, str(j))] = []
                pulo_duplo_inverso["{}_duplo_inverso_{}".format(i, str(j))].append(
                    Comando("{}_duplo_inverso_{}".format(
                        i, str(j)), "*", "*", cmd.direction, cmd.next_state
                        )
                    )
"""
        return

    else:
        print("Erro! Passe um arquivo como parâmetro")
        return


# Carrega o arquivo com as variáveis
def carregar_arquivo(name):
    file = open(name, "r+")
    lines = file.readlines()
    comandos = {}
    for line in lines:
        temp = line.replace("\n", "")
        temp = temp.split(" ")
        if temp[4].isnumeric():
            temp[4] = str(int(temp[4])+1)
        if temp[0].isnumeric():
            temp[0] = str(int(temp[0]) + 1)
        C = Comando(temp[0], temp[1], temp[2], temp[3], temp[4])
        if not C.current_state in comandos:
            comandos[C.current_state] = []
        comandos[C.current_state].append(C)
    return comandos

def exportar_arquivo(comandos):
    try:
        file = open("resultado.out", "w")
        for i in comandos:
            for j in comandos[i]:
                file.write(j.formatar())
    except IOError:
        print("Erro ao exportar arquivo!")




def printar_comandos(comandos):
    for comando in comandos:
        for j in range(len(comandos[comando])):
            comandos[comando][j].printar()




main(sys.argv)