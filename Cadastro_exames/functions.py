from tkinter import Label, Entry, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import re

#Função para padronizar mensagens de erro
def show_error(msg, title="Erro"):
    messagebox.showerror(title, msg)

# Funções principais
def create_box(window, nome, y_position, bg_color):
    label = Label(window, text=nome, anchor="w", font=("Arial", 12, "bold"), bg=bg_color)# Cria o rótulo do campo
    label.place(x=20, y=y_position)# Posiciona o rótulo na tela

    box = Entry(window, width=38, relief='solid')# Cria o campo de texto
    box.place(x=200, y=y_position + 3) # Posiciona o campo na tela

    return box, y_position + 40

def create_calendar_box(window, nome, y_position, bg_color):
    label = Label(window, text=nome, anchor="w", font=("Arial", 12, "bold"), bg=bg_color)
    label.place(x=20, y=y_position)

    calendar_box = DateEntry(window, width=15, date_pattern='dd/mm/yyyy', bg=bg_color)
    calendar_box.place(x=200, y=y_position + 3)

    return calendar_box, y_position + 40

def create_age_box(window, nome, y_position, bg_color):
    label = Label(window, text=nome, anchor="w", font=("Arial", 12, "bold"), bg=bg_color)
    label.place(x=20, y=y_position)

    age_box = Entry(window, width=10, relief='solid')
    age_box.place(x=200, y=y_position + 3)

    """Valida idade ao sair do campo"""
    def valid_out_age(event):
        value = age_box.get().strip()# Pega o valor digitado
        if value == "":
            return
        if not value.isdigit():
            show_error("Digite apenas números no campo de idade.")
            age_box.delete(0, 'end')
        else:
            idade = int(value)
            if not (0 <= idade <= 120):
                show_error("Idade inválida. Digite um valor entre 0 e 120.")
                age_box.delete(0, 'end')

    age_box.bind("<FocusOut>", valid_out_age)# Clicar fora do campo
    return age_box, y_position + 40

def create_time_box(window, nome, y_position, bg_color, other_time_box=None, is_start=True):
    label = Label(window, text=nome, anchor="w", font=("Arial", 12, "bold"), bg=bg_color)
    label.place(x=20, y=y_position)

    time_box = Entry(window, width=10, relief='solid')
    time_box.place(x=200, y=y_position + 3)

    def valid_out_time(event):
        value = time_box.get().strip()

        # Preenche automaticamente minutos caso não sejam informados
        if value and ':' not in value:
            value += ":00"

        try:
            hour, minute = map(int, value.split(":")) # Divide o valor em hora e minutos e converte para int
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
            
            time_box.delete(0, 'end') # Atualiza campo formatado
            time_box.insert(0, f"{hour:02d}:{minute:02d}")
        except:
            if value:  # Só mostra erro se usuário digitou algo
                show_error("Digite um horário válido no formato HH:MM (00:00 a 23:59).")
            time_box.delete(0, 'end')
            return

        # Valida intervalo com outro campo, se fornecido
        if other_time_box and other_time_box.get().strip():
            start_str = time_box.get() if is_start else other_time_box.get().strip() #Define a hora inicial e de termino
            end_str = other_time_box.get().strip() if is_start else time_box.get()
            if not valid_time_interval(start_str, end_str):
                time_box.delete(0, 'end')# Se o intervalo for incorreto, ele limpa o campo

    time_box.bind("<FocusOut>", valid_out_time)
    return time_box, y_position + 40

def create_qrcode_box(window, nome, y_position, bg_color):
    label = Label(window, text=nome, anchor="w", font=("Arial", 12, "bold"), bg=bg_color)
    label.place(x=20, y=y_position)

    qrcode_box = Entry(window, width=30, relief='solid')
    qrcode_box.place(x=135, y=y_position + 2)

    return qrcode_box, y_position + 40

# Funções de validação
def valid_time_interval(start, end): #Verifica se o horario de termino é maior que o de inicio
    try:
        if ':' not in start:
            start += ":00"
        if ':' not in end:
            end += ":00" #Adiciona "00" se o user digitou apenas um a hora (ex: 6)

        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()

        if end_time <= start_time:
            show_error("A hora de término não pode ser menor que a hora de início.")
            return False
        return True
    except ValueError:
        show_error("Formato de hora inválido. Use HH:MM.")
        return False

def valid_form(form): #Ignora o campo QRCODE, pois ele não é obrigatório o preenchimento
    for field, value in form.items():
        if field == "QRCODE":
            continue
        if not value or not str(value).strip():#Caso o campo esteja vazio ou com espaços
            return False
    return True

def valid_time(text):
    if text == "":
        return True
    if len(text) > 5: # Caracteres do horário
        return False
    return bool(re.match(r"^(?:[01]?\d|2[0-3]):?[0-5]?\d?$", text)) #Valida formatos (Hora: entre 0 e 23 e minutos: 0 e 59)

#Converte para o formato do Mysql
def format_datetime(date_str, time_str):
    try:
        datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Data ou horário inválido. Use os formatos DD/MM/AAAA e HH:MM.")