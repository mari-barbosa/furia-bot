from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from helper import carrega, salva
from selecionar_persona import personas, selecionar_persona

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-pro-exp-03-25"   
genai.configure(api_key=CHAVE_API_GOOGLE)

app = Flask(__name__)
app.secret_key = 'furia'

contexto = carrega("dados/furia.txt")

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            personalidade = personas[selecionar_persona(prompt)]

            prompt_do_sistema = f"""
            # PERSONA
            Você é um assistente virtual que ajuda os fãs da Furia CS a encontrar informações sobre a equipe, jogadores, torneios e estatísticas.
            Você não deve responder perguntas que não sejam informações sobre a Furia CS!
            Você deve utilizar apenas dados que estejam dentro do 'contexto' para responder as perguntas.

            # CONTEXTO
            {contexto}

            # PERSONALIDADE
            {personalidade}
            """

            configuracao_modelo = {
                "temperature" : 0.1,
                "max_output_tokens" : 8192
            }

            llm = genai.GenerativeModel(
                model_name=MODELO_ESCOLHIDO,
                system_instruction=prompt_do_sistema,
                generation_config=configuracao_modelo
            )

            resposta = llm.generate_content(prompt)
            return resposta.text
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no Gemini: %s" % erro
            
            sleep(50)


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    return resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
