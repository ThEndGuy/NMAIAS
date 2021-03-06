from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import pathlib
import webbrowser
import os


__VERSION__ = 1.6

dir_path = pathlib.Path().absolute()
absolute_path = os.path.join(dir_path, "NMAIAS.pyw")

try:
    import requests
except:
    os.system("pip install -r requirements.txt")
    try:
        import requests
    except:
        messagebox.showwarning(
            "Erro de pip",
            'Há algo de errado com o teu pip (provavelmente não está adicionado ao "PATH"). \n'
            "Por favor ler o README e ver o tutorial que se encontra lá.",
        )
        os.startfile(dir_path + "\README.md")


GH = "https://github.com/ThEndGuy/NMAIAS"
gh_file_nmaias = "https://raw.githubusercontent.com/ThEndGuy/NMAIAS/main/NMAIAS.pyw"
r = requests.get(gh_file_nmaias)
program_in_list = r.text.split("\n")


root = Tk()
root.title("NMAIAS - V" + str(__VERSION__))
icon = PhotoImage(file=os.path.join(dir_path, "icon.png"))
root.iconphoto(False, icon)

filename = os.path.join(dir_path, "Cadeiras.txt")
frame0 = Frame(root)
frame0.grid(row=0, column=0, columnspan=2)
root.option_add("*font", "Times 15")

br_frame = Frame(root)
br_frame.grid(row=2, column=1, sticky=E)

frame_options = Frame(root)
frame_options.grid(row=3, column=1, sticky=E)

frame_main = Frame(root)
frame_main.grid(row=1, column=0)

frame_bottom = Frame(root)
frame_bottom.grid(row=4, column=0, columnspan=2)

has_custom_browser = "False"

line_repeat_number = 7


def update_check(startup=False):
    try:
        file = open(filename, "r")
        lines = file.readlines()
        if lines[3] == "auto_updates = False\n" and startup == True:
            return
    except:
        pass
    global r
    r = requests.get(gh_file_nmaias)
    cloud_version = float(program_in_list[9][13:])

    if __VERSION__ < cloud_version:
        want_update = messagebox.askyesno(
            "Atualização disponível!",
            "Uma nova atualização foi detetada. \n"
            "Versão local: V" + str(__VERSION__) + "\n"
            "Versão atual: V" + str(cloud_version) + "\n"
            "Deseja atualizar?",
        )
        if want_update:
            do_update()
    elif not startup:
        messagebox.showinfo(
            "Informação", "Já tem a versão mais atualizada, V" + str(__VERSION__)
        )


def do_update():
    self_file = open("NMAIAS.pyw", "w", encoding="utf-8")
    self_file.writelines(r.text)
    os.startfile(absolute_path)
    quit()


def open_link(link):
    read_file = open(filename, "r")
    cb = read_file.readline()[21:]
    browser = read_file.readline()[17:]
    if cb == "True":
        webbrowser.get(browser + " %s").open_new_tab(link)
    else:
        webbrowser.open_new_tab(link)


def new_subject():
    popup = Toplevel()
    popup.wm_title("Adicionar nova cadeira")
    entry_width = 60
    spancolumn = 10

    def write_new_subject(file, name, moodle_id, t_link, tp_link, l_link, password):
        read_file = open(file, "r")
        lines = read_file.readlines()
        name_lines = []
        # if has_custom_browser == "True":
        lines = lines[line_repeat_number:]
        for entry in lines:
            if lines.index(entry) % line_repeat_number == 0:
                name_lines.append(entry)
        if "name = " + insert_cadeira_name.get() + " \n" in name_lines:
            messagebox.showerror("Erro", "Já existe uma cadeira com este nome")
        else:
            write_file = open(file, "a")
            read_file = open(file, "r")
            lines = read_file.readlines()
            if not lines:
                for _ in range(line_repeat_number):
                    write_file.write("\n")

            write_file.write("name = " + name + " \n")
            write_file.write("moodle_id = " + moodle_id + " \n")

            if t_link == "":
                write_file.write("t_link = None" + " \n")
            else:
                write_file.write("t_link = " + t_link + " \n")

            if tp_link == "":
                write_file.write("tp_link = None" + " \n")
            else:
                write_file.write("tp_link = " + tp_link + " \n")

            if l_link == "":
                write_file.write("l_link = None" + " \n")
            else:
                write_file.write("l_link = " + l_link + " \n")

            if password == "":
                write_file.write("password = None" + " \n")
            else:
                write_file.write("password = " + password + " \n")

            write_file.write("\n")
            write_file.close()

    def add_new_subject():
        if (
            insert_cadeira_name.get() != ""
            and insert_cadeira_id.get() != ""
            and (
                insert_cadeira_zoom_T.get() != ""
                or insert_cadeira_zoom_TP.get() != ""
                or insert_cadeira_zoom_L != ""
            )
        ):
            try:
                open(filename)
            except FileNotFoundError:
                messagebox.showinfo(
                    "Informação",
                    'Não foi encontrado nenhum ficheiro chamado " ' + filename + '" '
                    'pelo que vai ser criado um novo. Se já tem um ficheiro " '
                    + filename
                    + '",'
                    "verifique se ele esta na mesma pasta que este programa",
                )
                open(filename, "x")

            write_new_subject(
                filename,
                insert_cadeira_name.get(),
                insert_cadeira_id.get(),
                insert_cadeira_zoom_T.get(),
                insert_cadeira_zoom_TP.get(),
                insert_cadeira_zoom_L.get(),
                insert_password.get(),
            )
        else:
            messagebox.showwarning(
                "Aviso", "Por favor preencha todos necessários os campos em branco"
            )
        refresh_all_cadeiras()

    def limpar():
        insert_cadeira_name.delete(0, END)
        insert_cadeira_id.delete(0, END)
        insert_cadeira_zoom_T.delete(0, END)
        insert_cadeira_zoom_TP.delete(0, END)
        insert_cadeira_zoom_L.delete(0, END)
        insert_password.delete(0, END)

    sticky_setting = "W"
    cadeira_name = Label(popup, text="Nome da cadeira:")
    cadeira_name.grid(row=0, column=0, columnspan=spancolumn, sticky=sticky_setting)

    insert_cadeira_name = Entry(popup, width=entry_width)
    insert_cadeira_name.grid(
        row=1, column=0, columnspan=spancolumn, sticky=sticky_setting
    )

    cadeira_id = Label(popup, text="Link do moodle")
    cadeira_id.grid(row=2, column=0, columnspan=spancolumn, sticky=sticky_setting)

    insert_cadeira_id = Entry(popup, width=entry_width)
    insert_cadeira_id.grid(
        row=3, column=0, columnspan=spancolumn, sticky=sticky_setting
    )

    cadeira_zoom_T = Label(popup, text="Link do zoom das T")
    cadeira_zoom_T.grid(row=4, column=0, columnspan=spancolumn, sticky=sticky_setting)

    insert_cadeira_zoom_T = Entry(popup, width=entry_width)
    insert_cadeira_zoom_T.grid(
        row=5, column=0, columnspan=spancolumn, sticky=sticky_setting
    )

    cadeira_zoom_TP = Label(popup, text="Link do zoom das TP")
    cadeira_zoom_TP.grid(row=6, column=0, columnspan=spancolumn, sticky=sticky_setting)

    insert_cadeira_zoom_TP = Entry(popup, width=entry_width)
    insert_cadeira_zoom_TP.grid(
        row=7, column=0, columnspan=spancolumn, sticky=sticky_setting
    )

    cadeira_zoom_L = Label(popup, text="Link do zoom das PL")
    cadeira_zoom_L.grid(row=8, column=0, columnspan=spancolumn, sticky=sticky_setting)

    insert_cadeira_zoom_L = Entry(popup, width=entry_width)
    insert_cadeira_zoom_L.grid(
        row=9, column=0, columnspan=spancolumn, sticky=sticky_setting
    )

    password = Label(popup, text="Password(Opcional): ")
    password.grid(row=10, column=0, columnspan=spancolumn, sticky=sticky_setting)

    insert_password = Entry(popup, width=entry_width)
    insert_password.grid(row=11, column=0, columnspan=spancolumn, sticky=sticky_setting)

    aviso = Label(
        popup, text="Basta preencher pelo menos um dos campos da T, TP ou PL "
    )
    aviso.grid(
        row=13, rowspan=3, column=0, columnspan=spancolumn, sticky=sticky_setting
    )

    atencao = Label(
        popup,
        text='ATENÇÃO: Manter sempre o ficheiro " '
        + filename
        + '" na mesma pasta deste programa ',
    )
    atencao.grid(row=16, column=0, columnspan=spancolumn, sticky=sticky_setting)

    confirm = Button(popup, text="Confirmar", command=add_new_subject)
    confirm.grid(row=100, column=0)

    clean = Button(popup, text="Limpar", command=limpar)
    clean.grid(row=100, column=5)

    cancel = Button(popup, text="Cancelar", command=popup.destroy)
    cancel.grid(row=100, column=9)


class disciplina:
    def __init__(self, name, y, x=0, rowspan=1, columnspan=1, sticky=None):
        self.name = name
        self.frame = LabelFrame(frame_main, text=name)
        self.frame.grid(
            row=y, column=x, rowspan=rowspan, columnspan=columnspan, sticky=sticky
        )

    def create_zoom_button(self, link, mode=0):
        if mode == 0:
            self.zoom_button_name_T = Button(
                self.frame, text="Teórica", command=lambda: open_link(link)
            )
        elif mode == 1:
            self.zoom_button_name_TP = Button(
                self.frame, text="Prática", command=lambda: open_link(link)
            )
        else:
            self.zoom_button_name_L = Button(
                self.frame, text="Laboratorial", command=lambda: open_link(link)
            )

    def place_zoom_button(
        self, row, column, mode=0, rowspan=1, columnspan=1, sticky=None
    ):
        if mode == 0:
            self.zoom_button_name_T.grid(
                row=row,
                column=column,
                rowspan=rowspan,
                columnspan=columnspan,
                sticky=sticky,
            )
        elif mode == 1:
            self.zoom_button_name_TP.grid(
                row=row,
                column=column,
                rowspan=rowspan,
                columnspan=columnspan,
                sticky=sticky,
            )
        else:
            self.zoom_button_name_L.grid(
                row=row,
                column=column,
                rowspan=rowspan,
                columnspan=columnspan,
                sticky=sticky,
            )

    def create_moodle_button(self, link):
        self.moodle_button_name = Button(
            self.frame, text="Moodle", command=lambda: open_link(link)
        )

    def place_moodle_button(self, row, column, rowspan=1, columnspan=1, sticky=None):
        self.moodle_button_name.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
        )

    def delete_cadeira_button(self):
        self.delete_cadeira = Button(
            self.frame,
            text="APAGAR",
            command=lambda: apagar_e_refresh(self.name, filename),
        )

    def place_delete_cadeira_button(
        self, row, column, rowspan=1, columnspan=1, sticky=None
    ):
        self.delete_cadeira.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
        )

    def password_button(self):
        self.password_button_create = Button(
            self.frame,
            text="Copiar Password",
            command=lambda: copy_password(self.name, filename),
        )

    def place_password_button(self, row, column, rowspan=1, columnspan=1, sticky=None):
        self.password_button_create.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
        )


def copy_password(name, files):
    file = open(files)
    file_read = file.readlines()
    for line in file_read:
        if line == "name = " + name + " \n":
            password = file_read[file_read.index(line) + 5][11:-1]
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()


def custom_browser():
    global has_custom_browser
    has_custom_browser = messagebox.askyesnocancel(
        "Aviso",
        "Se o link abre no browser "
        "errado é porque está a usar um browser não conhecido."
        " Pretende alterar o browser selecionado? (Selecionar"
        " SEUBROWSER.exe)",
    )

    if has_custom_browser is not None:
        read_file = open(filename, "r")
        lines = read_file.readlines()
        if lines[0][:3] == "has":
            for _ in range(line_repeat_number):
                lines.pop(0)
        read_file.close()
        write_file = open(filename, "w")
        if has_custom_browser is False:
            write_file.write("has_custom_browser = " + str(has_custom_browser) + " \n")
            for _ in range(line_repeat_number - 1):
                write_file.write("\n")
        else:
            path = filedialog.askopenfilename(
                title="Escolhe um browser",
                initialdir=".",
                filetype=(("exe files", "*.exe"), ("all files", "*.")),
            )
            write_file.write("has_custom_browser = " + str(has_custom_browser) + " \n")
            write_file.write("custom_browser = " + path + " \n")
            for i in range(line_repeat_number - 2):
                write_file.write("\n")
        write_file.close()
        append_file = open(filename, "a")
        append_file.writelines(lines)


def apagar_e_refresh(name, file):
    delete_cadeira(name, file)
    refresh_all_cadeiras()


def delete_cadeira(name, file):
    apagar = messagebox.askyesno(
        "Aviso",
        "Todos os dados de " + name + " vão ser perdidos "
        "\nDeseja mesmo apagar esta cadeira?",
    )
    if apagar:
        read_file = open(file, "r")
        lines = read_file.readlines()
        for line in lines:
            if "name = " + name + " \n" == line:
                x = lines.index(line)
                for i in range(line_repeat_number):
                    lines.pop(x)
        write_file = open(file, "w")
        write_file.writelines(lines)
        write_file.close()
    else:
        pass


def refresh_all_cadeiras():
    file = open(filename, "r")
    lines = file.readlines()
    global frame_main
    frame_main.destroy()
    frame_main = Frame(root)
    frame_main.grid(row=1, column=0)
    if lines:
        i = line_repeat_number
        while i < len(lines):

            if i % line_repeat_number == 0:  # Nome
                cadeira_name = lines[i][7:-2]
                disc = disciplina(
                    str(cadeira_name), i // line_repeat_number, columnspan=2, sticky=W
                )
            if i % line_repeat_number == line_repeat_number - 6:  # Moodle
                disc.create_moodle_button(lines[i][12:-2])
                disc.place_moodle_button(i // line_repeat_number, 0)

            if i % line_repeat_number == line_repeat_number - 5:  # Teorica
                if lines[i][-10:-2] == "#success":
                    new_string1 = lines[i][9:-10] + lines[i][-2:]
                else:
                    new_string1 = lines[i][9:-2]
                if lines[i][9:-2] != "None":
                    disc.create_zoom_button(new_string1)
                    disc.place_zoom_button(i // line_repeat_number, 1)

            if i % line_repeat_number == line_repeat_number - 4:  # Teorica pratica
                if lines[i][10:-1] != "None ":
                    if lines[i][-10:-1] == "#success":
                        new_string2 = lines[i][10:-10] + lines[i][-2:]
                    else:
                        new_string2 = lines[i][10:-2]
                    disc.create_zoom_button(new_string2, 1)
                    disc.place_zoom_button(i // line_repeat_number, 2, 1)

            if i % line_repeat_number == line_repeat_number - 3:  # Laboratorial
                if lines[i][9:-1] != "None ":
                    if lines[i][-10:-2] == "#success":
                        new_string3 = lines[i][9:-10] + lines[i][-2:]
                    else:
                        new_string3 = lines[i][9:-2]
                    disc.create_zoom_button(new_string3, 2)
                    disc.place_zoom_button(i // line_repeat_number, 3, 2)

            if i % line_repeat_number == line_repeat_number - 2:  # Password
                if lines[i][11:-2] != "None":
                    disc.password_button()
                    disc.place_password_button(i // line_repeat_number, 4)

            if i % line_repeat_number == line_repeat_number - 1:  # Apagar
                disc.delete_cadeira_button()
                disc.place_delete_cadeira_button(i // line_repeat_number, 5)

            i += 1


def options():
    def auto_update():
        global updates_on
        updates_on = True
        file = open(filename, "r")
        liness = file.readlines()
        file = open(filename, "w")
        liness[3] = "auto_updates = True\n"
        file.writelines(liness)
        file.close()
        auto_updates()

    def not_auto_update():
        global updates_on
        updates_on = False
        file = open(filename, "r")
        liness = file.readlines()
        file = open(filename, "w")
        liness[3] = "auto_updates = False\n"

        file.writelines(liness)
        file.close()
        auto_updates()

    class Option:
        def __init__(self, name, frame_name, row, col):
            self.name = name
            self.frame_name = frame_name
            self.row = row
            self.col = col
            self.frame_name = LabelFrame(options_popup, text=self.name)
            self.frame_name.grid(row=self.row, column=self.col)

        def button(self, t1, t2, cmd1, cmd2, on="False"):
            if on == "True":
                self.b1 = Button(self.frame_name, text=t1, state=DISABLED, bg="CYAN")
                self.b2 = Button(self.frame_name, text=t2, command=cmd2)
            else:
                self.b1 = Button(self.frame_name, text=t1, command=cmd1)
                self.b2 = Button(self.frame_name, text=t2, state=DISABLED, bg="RED")
            self.b1.grid(row=0, column=0)
            self.b2.grid(row=0, column=1)

        def reset(self):
            self.frame_name.destroy()
            self.frame_name = LabelFrame(options_popup, text=self.name)
            self.frame_name.grid(row=self.row, column=self.col)

    def auto_updates():
        updates: Option
        file = open(filename, "r")
        lines = file.readlines()
        if lines[3] != "\n":
            enable = lines[3][15:-1]
        else:
            file = open(filename, "w")
            lines[3] = "auto_updates = False\n"
            file.writelines(lines)
            enable = "False"
        try:
            updates.reset()
        except:
            pass
        updates = Option("Auto atualizações", "AutoUpdate", 0, 0)
        updates.button("ON", "OFF", auto_update, not_auto_update, enable)

    options_popup = Toplevel()
    options_popup.wm_title("Opções")
    auto_updates()


try:
    open(filename)
    refresh_all_cadeiras()
except FileNotFoundError:
    pass


update_check(startup=True)


nmaias = Label(frame0, text="NMAIAS - Não Me Apetece Ir Ao Site")
nmaias.grid(row=1, column=0, columnspan=10, sticky=W)

github_button = Button(
    br_frame,
    text="GitHub",
    command=lambda: webbrowser.open_new_tab(GH),
    bd=0,
    fg="BLUE",
    activeforeground="RED",
)
underline_font = font.Font(github_button, github_button.cget("font"))
underline_font.configure(underline=True)
github_button.configure(font=underline_font)
github_button.grid(row=1, column=1, columnspan=10, sticky=E)


options_button = Button(frame_options, text="Opções", command=options)
options_button.grid(row=0, column=0, sticky=E)

different_browser = Button(
    frame_bottom, text="Links abrem no browser errado?", command=custom_browser
)
different_browser.grid(row=1000, column=3)

new_subject_button = Button(
    frame_bottom, text="Adicionar nova cadeira", command=new_subject
)
new_subject_button.grid(row=1000)

refresh = Button(frame_bottom, text="Refresh", command=refresh_all_cadeiras)
refresh.grid(row=1000, column=1)

update = Button(frame_bottom, text="Atualizar", command=update_check)
update.grid(row=1000, column=2)

root.mainloop()

