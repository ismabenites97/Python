import mysql.connector
import tkinter as tk
from tkinter import messagebox
import logging

# Configuração do sistema logs
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s" #Formato das mensagens do log (data, nivel e mensagem)
)

# Variavel que ativa ou desativa o debug no terminal
DEBUG_MODE = True

#Valida se o debug está ativo e registra a mensagem no arquivo
def log_debug(msg):
    if DEBUG_MODE:
        print(f"[DEBUG] {msg}")
    logging.debug(msg)

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3307",
        user="god",
        password="270797",
        database="baiosys"
    )

def create_table():
    try:
        with create_connection() as connect: # Garante que a conexão será fechada corretamente
            with connect.cursor() as commands_sql:
                commands_sql.execute("""
                    CREATE TABLE IF NOT EXISTS CADASTRO (
                        NUMERO_EXAME INT AUTO_INCREMENT PRIMARY KEY,
                        NOME_PACIENTE VARCHAR(255),
                        IDADE VARCHAR(10),
                        CONVENIO VARCHAR(100),
                        PROCEDIMENTO VARCHAR(255),
                        DATA DATE,
                        HORA_INICIO TIME,
                        HORA_TERMINO TIME,
                        MEDICO_SOLICITANTE VARCHAR(255),
                        MEDICO_EXECUTANTE VARCHAR(255),
                        TECNICO_AUXILIAR VARCHAR(255),
                        QRCODE MEDIUMBLOB
                    )
                """)
                connect.commit()
                logging.info("Tabela CADASTRO criada/verificada com sucesso.")
                log_debug("Tabela criada/verificada.")
    except mysql.connector.ProgrammingError as e:
        messagebox.showerror("Erro", "Usuário ou senha incorretos no MySQL.")
        logging.error(f"Erro de autenticação: {e}")
    except mysql.connector.DatabaseError as e:
        messagebox.showerror("Erro", "Banco de dados não encontrado.")
        logging.error(f"Erro de banco: {e}")
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", "Não foi possível conectar ao MySQL. Verifique se o Docker está ativo.")
        logging.error(f"Erro de conexão ao MySQL: {e}")

def register_patient(data):
    try:
        with create_connection() as connect:
            with connect.cursor() as commands_sql:
                commands_sql.execute("""
                    INSERT INTO CADASTRO (
                        NOME_PACIENTE, 
                        IDADE, 
                        CONVENIO, 
                        PROCEDIMENTO,
                        DATA,
                        HORA_INICIO, 
                        HORA_TERMINO,
                        MEDICO_SOLICITANTE, 
                        MEDICO_EXECUTANTE,
                        TECNICO_AUXILIAR,
                        QRCODE
                    ) VALUES (
                        %(PACIENTE)s, %(IDADE)s, %(CONVENIO)s, %(PROCEDIMENTO)s,
                        %(DATA_EXAME)s, %(HORA_INICIO)s, %(HORA_TERMINO)s,
                        %(MEDICO_SOLICITANTE)s, %(MEDICO_EXECUTANTE)s,
                        %(TECNICO_AUXILIAR)s, %(QRCODE)s
                    )
                """, data)
                connect.commit()
                logging.info(f"Paciente {data['PACIENTE']} cadastrado com sucesso.")
                log_debug(f"Paciente {data['PACIENTE']} cadastrado.")
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Não foi possível cadastrar o paciente:\n{str(e)}")
        logging.error(f"Erro no insert: {e}")
        log_debug(f"Erro no insert: {e}")
