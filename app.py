from flask import Flask, render_template, request, redirect, url_for
import redis
import datetime

# O parâmetro decode_responses=True faz com que o Redis retorne strings em vez de bytes
red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)

@app.route("/")
def index():
    tarefas = []
    return render_template('index.html')

@app.route("/criar-tarefa")
def criar_tarefa():
    return render_template('add-tarefa.html')

@app.route("/salvar-tarefa", methods=["POST"])
def salvar_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")

        # verificar se o titulo obrigatório foi preenchido
        if titulo:
            # gerar um id único pela bilioteca do redis
            id_tarefa = red.incr("tarefa:id_counter")

            # obter a data e hora atual
            data_criacao = datetime.datetime.now().isoformat()

            status_inicial = "Pendente"

            chave_tarefa = f"tarefa:{id_tarefa}"

            # criando o hash para salvar no redis
            red.hset(chave_tarefa, mapping={
                'id': id_tarefa,
                'titulo': titulo,
                'descricao': descricao,
                'data_criacao': data_criacao,
                'status': status_inicial
            })

            # salvando ids em um conjunto pra acessar mais facilmente depois
            red.sadd('tarefas_ids', id_tarefa)

            print(f"Tarefa {titulo} salva com sucesso no Redis! ID: {id_tarefa}")

            return redirect(url_for('index'))
        else:
            return "Erro: O título da tarefa não pode ser vazio.", 400 # Retorna um erro HTTP 400

    else: 
        # Se a requisição não for POST (o que não deve acontecer se o formulário for enviado corretamente),
        # redireciona de volta para a página de criação.
        return redirect(url_for('criar_tarefa'))