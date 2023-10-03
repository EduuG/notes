# By Eduardo G.

import PySimpleGUI as sg
from datetime import date
from screeninfo import get_monitors
import os


# When the current day is over, it will detect that there's no history with
# the current date, so another one will be create, along side with a new
# "checkeds" and "uncheckeds" files. The current list of checkeds and
# uncheckeds will fill these new files.
def Daily_Check():
    history_exists = os.path.exists("Daily Tasks/History/{}".format(date.today()))

    with open(r"Daily Tasks/tasks", 'r+') as fp:
        if history_exists is False:
            fp.truncate(0)

        for line in fp:
            x = line[:-1]
            tasks.append(x)

    with open(r"Daily Tasks/checkeds", 'r+') as fp:
        if history_exists is False:
            fp.truncate(0)

        for line in fp:
            x = line[:-1]
            checkeds.append(x)

    with open(r"Daily Tasks/uncheckeds", 'r+') as fp:
        if history_exists is False:
            fp.truncate(0)

        for line in fp:
            x = line[:-1]
            uncheckeds.append(x)


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


# Function to add checkbox to the tasks.
    # item - Task's name
    # index - Task's index
    # checked - If the task's checkbox will be checked or not
    # is_deleted - If the task will be deleted
def checkbox(item, index, checked, is_deleted):
    icon_uncheck = '[ ]'
    icon_check = '[X]'

    if checked is True and is_deleted is False:
        if item not in checkeds and item not in uncheckeds:
            checkeds.append(item)
            tasks.insert(index, '{} {}'.format(icon_check, item))
            confirm_icon = '☑'

        elif item in checkeds and item not in uncheckeds:
            checkeds.remove(item)
            uncheckeds.append(item)
            tasks.insert(index, '{} {}'.format(icon_uncheck, item))
            confirm_icon = '☑'

        elif item not in checkeds and item in uncheckeds:
            uncheckeds.remove(item)
            checkeds.append(item)
            tasks.insert(index, '{} {}'.format(icon_check, item))
            confirm_icon = '☐'

        return confirm_icon

    if checked is False and is_deleted is False:
        if item not in uncheckeds and item not in checkeds:
            uncheckeds.append(item)
            tasks.insert(index, '{} {}'.format(icon_uncheck, item))

    if is_deleted is True and item[4:] in uncheckeds:
        tasks.remove(item)
        uncheckeds.remove(item[4:])

    if is_deleted is True and item[4:] in checkeds:
        tasks.remove(item)
        checkeds.remove(item[4:])


def _percent():
    if len(checkeds) == 0 or len(tasks) == 0:
        return 0
    else:
        percent = (len(checkeds) / len(tasks)) * 100
        return float(f'{percent:.2f}')


def _save():
    tasks_file = 'Daily Tasks/tasks'
    checkeds_file = 'Daily Tasks/checkeds'
    uncheckeds_file = 'Daily Tasks/uncheckeds'

    with open(r'{}'.format(tasks_file), 'w') as fp:
        for i in tasks:
            fp.write("{}\n".format(i))

    with open(r'{}'.format(checkeds_file), 'w') as fp:
        for i in checkeds:
            fp.write("{}\n".format(i))

    with open(r'{}'.format(uncheckeds_file), 'w') as fp:
        for i in uncheckeds:
            fp.write("{}\n".format(i))

    with open(r'Daily Tasks/History/{}'.format(date.today()), 'w') as fp:
        fp.write("Concluído: {}%".format(_percent()))
        if _percent() == 100.0:
            fp.write(" - PARABÉNS!!\n\n")
        else:
            fp.write("\n\n")
        for i in tasks:
            fp.write("{}\n".format(i))


sg.theme('SystemDefault1')

tasks = []          # All the tasks to be completed
checkeds = []       # Completed tasks
uncheckeds = []     # Uncompleted tasks

current_directory = os.getcwd()

if 'Daily Tasks' and 'Long Tasks' in os.listdir(current_directory):
    pass
else:
    os.mkdir("Daily Tasks")
    os.mkdir("Long Tasks")
    os.mkdir("Daily Tasks/History")
    os.mknod("Daily Tasks/tasks")
    os.mknod("Daily Tasks/checkeds")
    os.mknod("Daily Tasks/uncheckeds")

treedata = sg.TreeData()
history_path = ("Daily Tasks/History/")
history = os.listdir(history_path)

for i in history:
    file = open('Daily Tasks/History/{}'.format(i))
    lines = file.readlines()
    treedata.Insert("", i, i, lines[0][11:])
    for line in lines:
        treedata.Insert(i, 'a', line, "")


def layout_start():
    layout = [[sg.Button("Daily Tasks", s=(20, 10), key="-DAILY-"),
               sg.Push(),
               sg.Button("Long Tasks", s=(20, 10), key="-LONG-")]]

    window = MyWindow('Tasks', layout, font='Iosveka 10',
                      finalize=True, location=(0, 0))

    return window


layout_history = [[sg.Tree(treedata, ['Concluído'], expand_x=True,
                           expand_y=True, font='Iosevka 12', col0_width=(53),
                           key='-TREE-')],
                  [sg.Button("<"),
                  sg.Push(),
                  sg.Button("Sair", key="-SAIR2-")]]


def layout_daily():
    layout_l = [[sg.InputText(do_not_clear=False, font='Iosevka 14', s=(45),
                              expand_x=True),
                sg.Push(),
                sg.Button('Adicionar', bind_return_key=True)],
                [sg.Listbox(values=tasks, s=(10, 15), expand_x=True,
                            expand_y=True, font='Iosevka 16',
                            enable_events=True, key='-tasks-')],
                [sg.T("Concluído: {}{}".format(_percent(), '%'),
                      key="-percent-")],
                [sg.Button('Histórico'),
                sg.Push(),
                sg.Button('Sair', key="-SAIR1-")]]

    layout_r = [[sg.Button('☑', font='_ 16', key='-confirm-')],
                [sg.Button('▲', font='_ 14')],
                [sg.Button('▼', font='_ 14')],
                [sg.Button('🗑', font='_ 16')]]

    layout = [[sg.T('ー Tarefas ー', font='_ 14', justification='c',
                    expand_x=True, s=(52, 0))],
              [sg.Col(layout_l, p=0, expand_x=True, expand_y=True,
                      key='-COL1_L-'),
               sg.Col(layout_r, p=0, key='-COL1_R-'),
               sg.Col(layout_history, key='-COL2-', visible=False,
                      expand_x=True, expand_y=True)]]

    window = MyWindow('Tasks', layout, font='Iosveka 10', finalize=True,
                      location=(0, 0))
    window.move_to_center()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-SAIR1-':
            break

        elif event == 'Adicionar':
            if values[0] == '':
                pass
            else:
                checkbox(values[0], 9999999, False, False)
                window['-tasks-'].update(values=tasks, set_to_index=[tasks.index("[ ] {}".format(values[0]))], scroll_to_index=(tasks.index("[ ] {}".format(values[0]))))   
                _percent()
                window['-percent-'].update('Concluído: {}{}'.format(_percent(), '%'))
                _save()
                window['-TREE-'].update(treedata)

        elif event == '🗑':
            if values['-tasks-']:
                tarefa = window['-tasks-'].get_indexes()
                checkbox(values['-tasks-'][0], tarefa[0], False, True)
                window['-tasks-'].update(values=tasks, set_to_index=[tarefa[0]], scroll_to_index=(tarefa[0]))
                _percent()
                window['-percent-'].update('Concluído: {}{}'.format(_percent(), '%'))
                _save()
                window['-TREE-'].update(treedata)

        elif event == '▲':
            if values['-tasks-']:
                temp = {}
                tarefa = window['-tasks-'].get_indexes()
                temp["item"] = values['-tasks-'][0][4:]
                temp["index"] = tarefa[0]
                if temp["item"] in checkeds:
                    if temp["index"] > 0:
                        tasks.pop(tarefa[0])
                        tasks.insert((temp["index"] - 1), "[X] {}".format(temp["item"]))
                        window['-tasks-'].update(values=tasks, set_to_index=[temp["index"] - 1], scroll_to_index=(temp["index"] - 1))
                        window['-TREE-'].update(treedata)
                    else:
                        pass
                else:
                    if temp["index"] > 0:
                        tasks.pop(tarefa[0])
                        tasks.insert((temp["index"] - 1), "[ ] {}".format(temp["item"]))
                        window['-tasks-'].update(values=tasks, set_to_index=[temp["index"] - 1], scroll_to_index=(temp["index"] - 1))
                        window['-TREE-'].update(treedata)
                    else:
                        pass
                _save()

        elif event == '▼':
            if values['-tasks-']:
                temp = {}
                tarefa = window['-tasks-'].get_indexes()
                temp["item"] = values['-tasks-'][0][4:]
                temp["index"] = tarefa[0]
                if temp["item"] in checkeds:
                    if temp["index"] < (len(tasks) - 1):
                        tasks.pop(tarefa[0])
                        tasks.insert((temp["index"] + 1), "[X] {}".format(temp["item"]))
                        window['-tasks-'].update(values=tasks, set_to_index=[temp["index"] + 1], scroll_to_index=(temp["index"] + 1))
                        window['-TREE-'].update(treedata)
                    else:
                        pass
                else:
                    if temp["index"] < (len(tasks) - 1):
                        tasks.pop(tarefa[0])
                        tasks.insert((temp["index"] + 1), "[ ] {}".format(temp["item"]))
                        window['-tasks-'].update(values=tasks, set_to_index=[temp["index"] + 1], scroll_to_index=(temp["index"] + 1))
                        window['-TREE-'].update(treedata)
                    else:
                        pass
                _save()

        elif event == '-confirm-':
            if values['-tasks-']:
                temp = {}
                tarefa = window['-tasks-'].get_indexes()
                temp["item"] = values['-tasks-'][0][4:]
                temp["index"] = tarefa[0]
                tasks.pop(tarefa[0])
                confirm_icon = checkbox(temp["item"], temp["index"], True, False)
                window['-confirm-'].update(confirm_icon)
                window['-tasks-'].update(values=tasks, set_to_index=[temp["index"]], scroll_to_index=(temp["index"]))
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

        elif event == '-tasks-':
            if values['-tasks-'][0][4:] in checkeds:
                window['-confirm-'].update('☐')
            elif values['-tasks-'][0][4:] in uncheckeds:
                window['-confirm-'].update('☑')


# def layout_long():
#     layout = [[sg.T('ー Tarefas ー', font='_ 14', justification='c', expand_x=True, s=(52, 0))], 
#               [sg.Col(layout_l, p=0, expand_x=True, expand_y=True, key='-COL1_L-'),
#                sg.Col(layout_r, p=0, key='-COL1_R-'),
#                sg.Col(layout_history, key='-COL2-', visible=False, expand_x=True, expand_y=True)]]

#     window = MyWindow('Tasks', layout, font='Iosveka 10', finalize=True, location=(0, 0))


window = layout_start()
window.my_move_to_center()

while True:
    tarefa = ()

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-SAIR1-' or event == '-SAIR2-':
        break

    elif event == "-DAILY-":
        window.close()
        Daily_Check()
        layout_daily()

    window.close()
