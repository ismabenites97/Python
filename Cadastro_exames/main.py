from tkinter import *
from tkinter import messagebox, filedialog
from datetime import datetime
from db_mysql import create_table, register_patient

from functions import (
    create_box, 
    create_calendar_box, 
    create_age_box, 
    create_time_box, 
    create_qrcode_box, 
    valid_form,
    valid_time_interval,
    format_datetime
)

#Cores
co1 = "#000000"  # Preto
co2 = "#feffff"  # Branco
co3 = "#4fa882"  # Verde
co4 = "#d9f3fc" # Azul claro

#Janela
window = Tk()
window.title("System")
window.geometry('450x750')
window.configure(background=co4)
window.resizable(width=False, height=False) #Bloqueia maximização de janela

#Titulo
Label(window, text="Cadastro de Exames", font=("Arial", 14, "bold"), bg=co4).pack(pady=30)

y_position = 80

#Campos do formulário
patient_input, y_position = create_box(window, "Paciente:", y_position, co4)
age_input, y_position = create_age_box(window, "Idade:", y_position, co4)
insurance_input, y_position = create_box(window, "Convênio:", y_position, co4)
procedure_input, y_position = create_box(window, "Procedimento:", y_position, co4)
date_input, y_position = create_calendar_box(window, "Data do Exame:", y_position, co4)
start_time_input, y_position = create_time_box(window, "Hora de Início:", y_position, co4, is_start=True)
end_time_input, y_position = create_time_box(window, "Hora de Término:", y_position, co4, other_time_box=start_time_input, is_start=False)
requesting_doctor_input, y_position = create_box(window, "Médico Solicitante:", y_position, co4)
executing_doctor_input, y_position = create_box(window, "Médico Executante:", y_position, co4)
technician_input, y_position = create_box(window, "Técnico Auxiliar:", y_position, co4)
qrcode_input, y_position = create_qrcode_box(window, "QRCode:", y_position, co4)

#Cria tabela caso ela não exista
create_table() 


#Funções auxiliares
def read_qrcode(path):
    #Lê o QR Code e retorna os bytes do arquivo
    if not path:
        return None
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        messagebox.showerror("Erro de Arquivo", "Arquivo de QR Code não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro de Leitura", f"Erro ao ler o QR Code: {str(e)}")
    return None

#Monta o dicionário com os dados do formulário
def build_form():
    
    date_mysql = format_datetime(date_input.get(), start_time_input.get())
    qrcode_bytes = read_qrcode(qrcode_input.get())
    
    form = {
        "PACIENTE": patient_input.get(),
        "IDADE": age_input.get(),
        "CONVENIO": insurance_input.get(),
        "PROCEDIMENTO": procedure_input.get(),
        "DATA_EXAME": date_mysql,
        "HORA_INICIO": start_time_input.get(),
        "HORA_TERMINO": end_time_input.get(),
        "MEDICO_SOLICITANTE": requesting_doctor_input.get(),
        "MEDICO_EXECUTANTE": executing_doctor_input.get(),
        "TECNICO_AUXILIAR": technician_input.get(),
        "QRCODE": qrcode_bytes,
        "QRCODE_PATH": qrcode_input.get()
    }
    return form

def clear_fields():
        patient_input.delete(0, END)
        age_input.delete(0, END)
        insurance_input.delete(0, END)
        procedure_input.delete(0, END)
        date_input.set_date(datetime.today())
        start_time_input.delete(0, END)
        end_time_input.delete(0, END)
        requesting_doctor_input.delete(0, END)
        executing_doctor_input.delete(0, END)
        technician_input.delete(0, END)
        qrcode_input.delete(0, END)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
    if file_path:
        qrcode_input.delete(0, END)
        qrcode_input.insert(0, file_path)

#Funções do botões
def insert_button():
    #Registra paciente no banco
    form = build_form()

    # Validação dos campos
    if not valid_form(form):
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos")
        return
    
    # Valida horário de início e término
    if not valid_time_interval(start_time_input.get(), end_time_input.get()):
        return

    # Salva no banco
    try:
        register_patient(form)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível cadastrar no banco.\n{str(e)}")
        return

    messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
    clear_fields()

#Botões
button_insert = Button(window, text="Cadastrar", anchor='center', font=("Arial", 14, "bold"), bg=co3, fg=co2, command=insert_button)
button_insert.place(x=30, y=550)

button_clean = Button(window, text="Limpar", anchor='center', font=("Arial", 14, "bold"), bg=co3, fg=co2, command=clear_fields)
button_clean.place(x=334, y=550)

button_choice = Button(window, text="Selecionar", font=("Arial", 10, "bold"), bg=co3, fg=co2, command=open_file)
button_choice.place(x=350, y=475)

window.mainloop()