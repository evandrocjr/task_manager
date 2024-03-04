import tkinter as tk                     # Importar biblioteca de interface gráfica
from tkinter import messagebox, ttk          # Importar biblioteca de mensagens
from tkcalendar import DateEntry        # Importar biblioteca de calendário
from datetime import date, timedelta, datetime    # Importar biblioteca de datas
import mysql.connector                  # Importar biblioteca de conexão com banco de dados

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="eva",
    password="zxcasdqwe123",
    database="gerenciador_tarefas"
)

# cursor
cursor = db.cursor()

# Checar se o banco de dados existe e criar se não
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()
for database in databases:
    if database[0] == "gerenciador_tarefas":
        break
else:
    cursor.execute("CREATE DATABASE gerenciador_tarefas")

# Criar tabela de tarefas
cursor.execute("CREATE TABLE IF NOT EXISTS tarefas (id INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255), data_inicio DATE, data_conclusao DATE, status VARCHAR(255) DEFAULT 'pendente')")


# GUI ********************************************************************************************************************

# Criar interface gráfica

# Janela principal
root = tk.Tk()
# Titulo da janela
root.title("Stark Industries - Gerenciador de Tarefas")
# Tamanho da janela
root.geometry('800x600')  # Largura x Altura
# Evita maximizar a janela
root.resizable(False, False)
# Cor de fundo
root.attributes('-alpha', 0.0) 

# Criar frame com cor de fundo
frame = tk.Frame(root, bg='grey', bd=5)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Criar canvas para desenhar um retangulo com bordas arredondadas
canvas = tk.Canvas(frame, width=780, height=580, bg='darkgrey', highlightthickness=0)
canvas.pack()

# Desenhar retangulo com bordas arredondadas
x0, y0, x1, y1, radius = 10, 10, 770, 570, 10
points = [x0+radius, y0,
          x1-radius, y0,
          x1, y0, x1, y0+radius,
          x1, y1-radius,
          x1, y1, x1-radius, y1,
          x0+radius, y1,
          x0, y1, x0, y1-radius,
          x0, y0+radius,
          x0, y0, x0+radius, y0]
canvas.create_polygon(points, outline='', fill='grey15')

# Frame para exibir tarefas
tarefas_frame = tk.Frame(root, bg='gold2')
tarefas_frame.pack()

# Função para exibir tarefas
def display_tarefas():
    # Limpar frame, evitando duplicação
    global tarefas_frame
    tarefas_frame.destroy()
    tarefas_frame = tk.Frame(root, bg='black')
    tarefas_frame.pack()

    # Criar visializacao utilizando Treeview
    tree = ttk.Treeview(tarefas_frame, columns=('Descricao', 'Inicio', 'Conclusao', 'Status'), show='headings')
    tree.heading('Descricao', text='Tarefa')
    tree.heading('Inicio', text='Início')
    tree.heading('Conclusao', text='Conclusão')
    tree.heading('Status', text='Status')
    tree.pack()

    # Exibir tarefas
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        # Format the dates
        inicio_str = tarefa[2].strftime('%d/%m/%Y')
        conclusao_str = tarefa[3].strftime('%d/%m/%Y')

        tree.insert('', 'end', values=(tarefa[1], inicio_str, conclusao_str, tarefa[4]))

# Função para adicionar tarefa
def add_tarefa():
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Adicionar Tarefa")
    nova_janela.configure(bg='dim gray')
    nova_janela.geometry('400x300')  # Set the window size to 400x300

    # Labels e inputs
    descricao_label = tk.Label(nova_janela, text="Descrição:", bg='black', fg='white')
    descricao_label.pack(padx=10, pady=10)  # Add padding
    descricao_entry = tk.Entry(nova_janela)
    descricao_entry.pack(padx=10, pady=10)  # Add padding

    # Data de início
    inicio_label = tk.Label(nova_janela, text="Data Início: ", bg='black', fg='white')
    inicio_label.pack(padx=10, pady=10)  # Add padding
    inicio_entry = DateEntry(nova_janela, mindate=date.today())
    inicio_entry.pack(padx=10, pady=10)  # Add padding

    # Data de Conclusao
    conclusao_label = tk.Label(nova_janela, text="Data Conclusão: ", bg='black', fg='white')
    conclusao_label.pack(padx=10, pady=10)  # Add padding
    conclusao_entry = DateEntry(nova_janela, mindate=date.today() + timedelta(days=1))
    conclusao_entry.set_date(date.today() + timedelta(days=1))
    conclusao_entry.pack(padx=10, pady=10)  # Add padding
    # Atualizada data minima da conclusao sempre que a data de inicio é atualizada
    def update_conclusao_entry_mindate(event):
        conclusao_entry.config(mindate=inicio_entry.get_date() + timedelta(days=1))
    inicio_entry.bind("<<DateEntrySelected>>", update_conclusao_entry_mindate)

    # Botão de envio
    envio_button = tk.Button(nova_janela, text="Enviar", command=lambda: enviar_tarefa(descricao_entry.get(), inicio_entry.get(), conclusao_entry.get()))
    envio_button.pack(padx=10, pady=10)  # Add padding

# Função para enviar tarefa
def enviar_tarefa(descricao, inicio, conclusao):
    sql = "INSERT INTO tarefas (descricao, data_inicio, data_conclusao) VALUES (%s, %s, %s)"
    val = (descricao, inicio, conclusao)
    cursor.execute(sql, val)
    db.commit()
    messagebox.showinfo("Tarefa adicionada", "Tarefa adicionada com sucesso!")
    display_tarefas()
    
# Função para marcar tarefa como completa
def marcar_completa(id):
    sql = "UPDATE tarefas SET status = 'completa' WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    messagebox.showinfo("Tarefa atualizada", "Tarefa marcada como completa!")
    display_tarefas()
    
# Função para remover tarefas completas
def remover_completa():
    sql = "DELETE FROM tarefas WHERE status = 'completa'"
    cursor.execute(sql)
    db.commit()
    messagebox.showinfo("Tarefa removida", "Tarefas completas removidas com sucesso!")
    display_tarefas()

# Display tarefas
display_tarefas()

# Botão de adicionar tarefa
add_button = tk.Button(root, text="Adicionar Tarefa", command=add_tarefa, bg='firebrick2', fg='white', font=('Helvetica', 14), width=20, height=2, relief=tk.RAISED, bd=5)
add_button.pack(side='left', padx=60, pady=40)

# Botão de remover tarefas completas
remove_button = tk.Button(root, text="Remover Tarefas Completas", command=remover_completa, bg='firebrick2', fg='white', font=('Helvetica', 14), width=20, height=2, relief=tk.RAISED, bd=5)
remove_button.pack(side='right', padx=60, pady=40)

# Rodar interface gráfica
root.mainloop()