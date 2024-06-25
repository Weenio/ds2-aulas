from PyQt5 import uic, QtWidgets
from reportlab.pdfgen import canvas
from database import banco

app = QtWidgets.QApplication([])

agenda = uic.loadUi('Agenda.ui')
listarContatos = uic.loadUi("ListaCadastro.ui")
alterar = uic.loadUi("Alterar.ui")
def Cadastro():
    name = agenda.textNome.text()
    email = agenda.textEmail.text()
    telefone = agenda.textTelefone.text()
    
    isChecked = ""
    
    if agenda.checkedResidencial.isChecked():
        isChecked = "residencial"
    elif agenda.checkedCasa.isChecked():
        isChecked = "celular"
    else:
        isChecked = 'comi o do meu lado esquerdo'
        isChecked = "não informado"
    
    try:
        cursor =  banco.cursor()
        cursor.execute(f"Insert into tbl_contatos(nome, email, telefone, tipo_telefone)values('{name}','{email}','{telefone}','{isChecked}')")    
        banco.commit()
        print("O cadastro da sua agenda foi feito!")
    except Exception as e:
        print(f"Sua requisição nao deu certo veja: {e}")    

def Consultar ():
    print("Entramos no cu do guilherme dnv")
    listarContatos.show()
    if(agenda):
        agenda.hide()
    else:
        alterar.hide()
    cursor = banco.cursor()
    
    cursor.execute('select * from tbl_contatos')
    dados = cursor.fetchall()
    listarContatos.tabelaContatos.setRowCount(len(dados))
    listarContatos.tabelaContatos.setColumnCount(5)
    
    for i in range(0, len(dados)):
        for f in range (0,5):
            listarContatos.tabelaContatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(dados[i][f])))

def Excluir():
    linhaContato = listarContatos.tabelaContatos.currentRow()
    listarContatos.tabelaContatos.removeRow(linhaContato)
    
    cursor = banco.cursor()
    cursor.execute(f"select id from tbl_contatos")
    contatos_lidos = cursor.fetchall()
    valorId= contatos_lidos[linhaContato][0]
    cursor.execute(f"Delete from tbl_contatos where id = {str(valorId)}")
    banco.commit()
    
    
    
def GerarPDF():
    cursor = banco.cursor()
    cursor.execute("Select * from tbl_contatos")
    contatosLidos = cursor.fetchall()
    
    y = 0
    pdf = canvas.Canvas("Lista_contatos.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200,800, "Lista de contatos")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "NOME")
    pdf.drawString(210,750, "EMAIL")
    pdf.drawString(410,750, "TELEFONE")
    pdf.drawString(490,750, "TIPO DE CONTATO")
    
    for i in range (0, len(contatosLidos)):
        y = y+50
        pdf.drawString(10,750 - y, str(contatosLidos[i][0]))
        pdf.drawString(110,750 - y, str(contatosLidos[i][1]))
        pdf.drawString(210,750 - y, str(contatosLidos[i][2]))
        pdf.drawString(410,750 - y, str(contatosLidos[i][3]))
        pdf.drawString(490,750 - y, str(contatosLidos[i][4]))
    pdf.save()
    print('PDF gerado com sucesso!')
    
def EsconderJanela():
    listarContatos.hide()
    agenda.show()
    
def CatarID():
    linhaContato = listarContatos.tabelaContatos.currentRow()
    cursor = banco.cursor()
    cursor.execute(f"select * from tbl_contatos")
    contatos_lidos = cursor.fetchall()
    valorId = contatos_lidos[linhaContato][0]
    nome = contatos_lidos[linhaContato][1]
    email = contatos_lidos[linhaContato][2]
    telefone = contatos_lidos[linhaContato][3]
    dados = [valorId, nome, email, telefone]
    
    print(valorId)
    ExibirAlterar(dados)
    
    
def ExibirAlterar(dados):
    listarContatos.hide()
    alterar.show()
    alterar.textID.setText(str(dados[0]))
    alterar.textNome.setText(dados[1])
    alterar.textEmail.setText(dados[2])
    alterar.textTelefone.setText(dados[3])
    
    
def Alteracao():
    id = alterar.textID.text()
    name = alterar.textNome.text()
    email = alterar.textEmail.text()
    telefone = alterar.textTelefone.text()
    
    isChecked = ""
    
    if alterar.checkedResidencial.isChecked():
        isChecked = "residencial"
    elif alterar.checkedCasa.isChecked():
        isChecked = "celular"
    else:
        isChecked = 'comi o do meu lado esquerdo'
        isChecked = "não informado"
    try:
        cursor=banco.cursor()
        cursor.execute(f"Update tbl_contatos a set a.nome = '{name}', a.email = '{email}', a.telefone = '{telefone}', a.tipo_telefone = '{isChecked}' where a.id = {int(id)}")
        print(f"Update tbl_contatos a set a.nome = '{name}', a.email = '{email}', a.telefone = '{telefone}', a.tipo_telefone = '{isChecked}' where a.id = {int(id)}")
        banco.commit()
        print("Registro alterado com sucesso!")
    except Exception as e:
        print(f"Deu erro: {e}")
    
        
listarContatos.voltarButton.clicked.connect(EsconderJanela)
listarContatos.deleteButton.clicked.connect(Excluir)
listarContatos.pdfButton.clicked.connect(GerarPDF)
listarContatos.AltButton.clicked.connect(CatarID)
agenda.cadButton.clicked.connect(Cadastro)
agenda.consButton.clicked.connect(Consultar)
alterar.cadButton.clicked.connect(Alteracao)
alterar.consButton.clicked.connect(Consultar)
agenda.show()
app.exec()