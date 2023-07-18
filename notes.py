# Por Eduardo G.

import PySimpleGUI as sg
from datetime import date
from screeninfo import get_monitors
import os

sg.theme('SystemDefault1')

lista = []          # Todas as tarefas a serem realizadas
checkeds = []       # Tarefas realizadas
uncheckeds = []     # Tarefas não realizadas

current_directory = os.getcwd()

if 'Histórico' and 'Tarefas' in os.listdir(current_directory):
    pass
else:
    os.mkdir('Histórico')
    os.mkdir('Tarefas')
    os.mknod('{}/Tarefas/tarefas'.format(current_directory))
    os.mknod('{}/Tarefas/checkeds'.format(current_directory))
    os.mknod('{}/Tarefas/uncheckeds'.format(current_directory))

history_exists = os.path.exists('{}/Histórico/{}'.format(current_directory, date.today()))

with open(r'{}/Tarefas/tarefas'.format(current_directory), 'r+') as fp:
    if history_exists == False:
        fp.truncate(0)

    for line in fp:
        x = line[:-1]
        lista.append(x)
        
with open(r'{}/Tarefas/checkeds'.format(current_directory), 'r+') as fp:
    if history_exists == False:
        fp.truncate(0)

    for line in fp:
        x = line[:-1]
        checkeds.append(x)

with open(r'{}/Tarefas/uncheckeds'.format(current_directory), 'r+') as fp:
    if history_exists == False:
        fp.truncate(0)

    for line in fp:
        x = line[:-1]
        uncheckeds.append(x)

treedata = sg.TreeData()
history_path = ('{}/Histórico/'.format(current_directory))
history = os.listdir(history_path)

for i in history:
    file = open('{}/Histórico/{}'.format(current_directory, i))
    lines = file.readlines()
    treedata.Insert("", i, i, lines[0][11:])
    for line in lines:
        treedata.Insert(i, 'a', line, "")

class MyWindow(sg.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_default_screen_dimensions(self):
        default_monitor = [monitor for monitor in get_monitors() if monitor.is_primary][0]
        screen_width, screen_height = default_monitor.width, default_monitor.height
        return screen_width, screen_height

    def my_move_to_center(self):
        if not self._is_window_created('tried Window.move_to_center'):
            return
        screen_width, screen_height = self.get_default_screen_dimensions()
        win_width, win_height = self.size
        x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
        self.move(x, y)

   
# Função para adicionar checkbox às tarefas.
    # item - Nome da tarefa
    # index - Localização da tarefa
    # checked - Se a checkbox da arefa esará marcada ou não
    # is_deleted - Se a tarefa será deletada

def checkbox(item, index, checked, is_deleted):
    icon_uncheck = '[ ]'
    icon_check = '[X]'

    if checked == True and is_deleted == False:
        if item not in checkeds and item not in uncheckeds:
            checkeds.append(item)
            lista.insert(index, '{} {}'.format(icon_check, item))

        elif item in checkeds and item not in uncheckeds:
            checkeds.remove(item)
            uncheckeds.append(item)
            lista.insert(index, '{} {}'.format(icon_uncheck, item))

        elif item not in checkeds and item in uncheckeds:
            uncheckeds.remove(item)
            checkeds.append(item)
            lista.insert(index, '{} {}'.format(icon_check, item))


    if checked == False and is_deleted == False:
            if item not in uncheckeds and item not in checkeds:
                uncheckeds.append(item)
                lista.insert(index, '{} {}'.format(icon_uncheck, item))

    if is_deleted == True and item[4:] in uncheckeds:
        lista.remove(item)
        uncheckeds.remove(item[4:])

    if is_deleted == True and item[4:] in checkeds:
        lista.remove(item)
        checkeds.remove(item[4:])


def _percent():
    if len(checkeds) == 0 or len(lista) == 0:
        return 0
    else:
        percent = (len(checkeds) / len(lista)) * 100
        return float(f'{percent:.2f}')

def _save():
    tarefas_file = '{}/Tarefas/tarefas'.format(current_directory)    
    checkeds_file = '{}/Tarefas/checkeds'.format(current_directory)    
    uncheckeds_file = '{}/Tarefas/uncheckeds'.format(current_directory)    

    with open(r'{}'.format(tarefas_file), 'w') as fp:
        for i in lista:
            fp.write("{}\n".format(i))

    with open(r'{}'.format(checkeds_file), 'w') as fp:
        for i in checkeds:
            fp.write("{}\n".format(i))

    with open(r'{}'.format(uncheckeds_file), 'w') as fp:
        for i in uncheckeds:
            fp.write("{}\n".format(i))

    with open(r'{}/Histórico/{}'.format(current_directory, date.today()), 'w') as fp:
        fp.write("Concluído: {}%".format(_percent()))
        if _percent() == 100.0:
            fp.write(" - PARABÉNS!!\n\n")
        else:
            fp.write("\n\n")
        for i in lista:
            fp.write("{}\n".format(i))


layout_l = [ [sg.InputText(do_not_clear = False, font='Iosevka 14', s=(45), expand_x=True),
            sg.Push(),
            sg.Button('Adicionar', bind_return_key=True)],
           [sg.Listbox(values=lista, s=(10,15), expand_x=True, expand_y=True, font='Iosevka 16', key = '-tarefas-')],
           [sg.T("Concluído: {}{}".format(_percent(), '%'), key="-percent-")],
           [sg.Button('Histórico'),
            sg.Push(),
            sg.Button('Sair', key="-SAIR1-")] ]

layout_r = [ [sg.Button('Con')],
             [sg.Button('▲')],
             [sg.Button('▼')],
             [sg.Button('🗑')]]

layout_historic = [ [sg.Tree(treedata, ['Concluído'], expand_x=True, expand_y=True, font='Iosevka 12', col0_width=(53), key='-TREE-')],
                    [sg.Button("<"),
                    sg.Push(),
                    sg.Button("Sair", key="-SAIR2-")] ]

layout = [ [sg.T('Tarefas', font='_ 14', justification='c', expand_x=True, s=(52,0))],
           [sg.Col(layout_l, p=0, expand_x=True, expand_y=True, key='-COL1_L-'), 
            sg.Col(layout_r, p=0, key='-COL1_R-'),
            sg.Col(layout_historic, key='-COL2-', visible=False, expand_x=True, expand_y=True)] ]

window = MyWindow('Lista de Tarefas', layout, font='Iosveka 10', finalize=True, location=(0,0))
#window = sg.window('Lista de Tarefas', layout, font='Iosveka 10', finalize=True, location=(0,0))
window.my_move_to_center()

while True:
    tarefa = ()
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-SAIR1-' or event == '-SAIR2-':
        break

    elif event == 'Adicionar':
        if values[0] == '':
            pass
        else:
            checkbox(values[0], 9999999, False, False)
            window['-tarefas-'].update(values=lista, set_to_index=[lista.index("[ ] {}".format(values[0]))], scroll_to_index=(lista.index("[ ] {}".format(values[0]))))   
            _percent()
            window['-percent-'].update('Concluído: {}{}'.format(_percent(), '%'))
            _save()
            window['-TREE-'].update(treedata)
                
    elif event == '🗑':
        tarefa = window['-tarefas-'].get_indexes()
        #lista.pop(tarefa[0])
        checkbox(values['-tarefas-'][0], tarefa[0], False, True)
        window['-tarefas-'].update(values=lista, set_to_index=[tarefa[0]], scroll_to_index=(tarefa[0]))
        _percent()
        window['-percent-'].update('Concluído: {}{}'.format(_percent(), '%'))
        _save()
        window['-TREE-'].update(treedata)

    elif event == '▲':
        temp = {}
        tarefa = window['-tarefas-'].get_indexes()
        temp["item"] = values['-tarefas-'][0][4:]
        temp["index"] = tarefa[0]
       # checkbox(temp["item"], (temp["index"] - 1), False, False)
        if temp["item"] in checkeds:
            if temp["index"] > 0:
                lista.pop(tarefa[0])
                lista.insert((temp["index"] - 1), "[X] {}".format(temp["item"]))
                window['-tarefas-'].update(values=lista, set_to_index=[temp["index"] - 1], scroll_to_index=(temp["index"] - 1))
                window['-TREE-'].update(treedata)
            else:
                pass
        else:
            if temp["index"] > 0:
                lista.pop(tarefa[0])
                lista.insert((temp["index"] - 1), "[ ] {}".format(temp["item"]))
                window['-tarefas-'].update(values=lista, set_to_index=[temp["index"] - 1], scroll_to_index=(temp["index"] - 1))
                window['-TREE-'].update(treedata)
            else:
                pass
        _save()

    elif event == '▼':
        temp = {}
        tarefa = window['-tarefas-'].get_indexes()
        temp["item"] = values['-tarefas-'][0][4:]
        temp["index"] = tarefa[0]
       # checkbox(temp["item"], (temp["index"] - 1), False, False)
        if temp["item"] in checkeds:
            if temp["index"] < (len(lista) - 1):
                lista.pop(tarefa[0])
                lista.insert((temp["index"] + 1), "[X] {}".format(temp["item"]))
                window['-tarefas-'].update(values=lista, set_to_index=[temp["index"] + 1], scroll_to_index=(temp["index"] + 1))
                window['-TREE-'].update(treedata)
            else:
                pass
        else:
            if temp["index"] < (len(lista) - 1):
                lista.pop(tarefa[0])
                lista.insert((temp["index"] + 1), "[ ] {}".format(temp["item"]))
                window['-tarefas-'].update(values=lista, set_to_index=[temp["index"] + 1], scroll_to_index=(temp["index"] + 1))
                window['-TREE-'].update(treedata)
            else:
                pass
        _save()
        
    elif event == 'Con':
        temp = {}
        tarefa = window['-tarefas-'].get_indexes()
        temp["item"] = values['-tarefas-'][0][4:]
        temp["index"] = tarefa[0]
        lista.pop(tarefa[0])
        checkbox(temp["item"], temp["index"], True, False)
        window['-tarefas-'].update(values=lista, set_to_index=[temp["index"]], scroll_to_index=(temp["index"]))
        _percent()
        window['-percent-'].update('Concluído: {}{}'.format(_percent(), '%'))
        _save()
        window['-TREE-'].update(treedata)

    elif event == 'Histórico':
        window['-COL2-'].update(visible=True)
        window['-COL1_L-'].update(visible=False)
        window['-COL1_R-'].update(visible=False)

    elif event == '<':
        window['-COL2-'].update(visible=False)
        window['-COL1_L-'].update(visible=True)
        window['-COL1_R-'].update(visible=True)

window.close()