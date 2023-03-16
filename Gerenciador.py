import PySimpleGUI as sg

def salvar_tarefas(tarefas):
    with open('tarefas.txt', 'w') as arquivo:
        for tarefa in tarefas:
            arquivo.write(f"{tarefa[0]}, {tarefa[1]}, {tarefa[2]}\n")
            
def carregar_tarefas():
    tarefas = []
    
    try:
        with open('tarefas.txt', 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    tarefa = linha.split(',')
                    tarefas.append((tarefa[0], tarefa[1], tarefa[2].lower() == 'true'))
    except FileNotFoundError:
        pass
    return  tarefas

# Criando o layout
def criar_janela_inicial():
    sg.theme('DarkBlue4')
    tarefas = carregar_tarefas()
    lista_tarefas = [
        [sg.Checkbox(tarefa[0], default=tarefa[2]), sg.Text(tarefa[1])]
        for tarefa in tarefas
    ]

    linha_nova_tarefa = [sg.Checkbox('', default=False), sg.Input('')]
    linha_botoes = [sg.Button('Nova Tarefa'), sg.Button('Resetar'), sg.Button('Salvar')]

    layout = [
        [sg.Frame('Tarefas', layout=lista_tarefas, key='container')],
        [sg.Frame('Nova Tarefa', layout=[linha_nova_tarefa])],
        linha_botoes
    ]

    return sg.Window('To Do List', layout=layout, finalize=True), tarefas


# Criar a janela
janela, tarefas = criar_janela_inicial()

# Criar as regras da janela
while True:
    eventos, valores = janela.read()
    if eventos == sg.WIN_CLOSED:
        break
    elif eventos == 'Salvar':
        salvar_tarefas(tarefas)
    elif eventos == 'Nova Tarefa':
        nova_tarefa = (valores[0], valores[1], False)
        tarefas.append(nova_tarefa)
        janela.extend_layout(janela['container'], [[sg.Checkbox(nova_tarefa[0], default=False), sg.Text(nova_tarefa[1])]])
    elif eventos == 'Resetar':
        janela.close()
        janela, tarefas = criar_janela_inicial()