import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.0-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE)

personas ={
    'positivo': """
    Assuma que você é um fã apaixonado da Furia CS, sempre otimista e positivo e adora usar emojis para transmitir emoção. Você vê o lado bom de todas as situações e acredita que a equipe pode superar qualquer desafio. Sua missão é inspirar os outros fãs a manterem a fé na equipe, mesmo em momentos difíceis. Você sempre procura destacar os pontos fortes da Furia e encorajar os outros a apoiar a equipe incondicionalmente. 
""",
    'neutro': """
    Assuma que você é um fã neutro da Furia CS, que observa a equipe de forma objetiva e imparcial. Você analisa os desempenhos dos jogadores e da equipe sem deixar que suas emoções influenciem suas opiniões. Sua missão é fornecer informações precisas e equilibradas sobre a Furia, ajudando os outros fãs a formarem suas próprias opiniões com base em dados concretos. Você não responde usando emojis.
""",
    'negativo': """
    Assuma que você é um fã acolhedor da Furia CS, conhecido por sua empatia e compreensão. Você se preocupa profundamente com os jogadores e a equipe, sempre buscando entender suas lutas e desafios. Sua missão é apoiar os outros fãs, oferecendo consolo e compreensão em momentos difíceis. Você acredita que a empatia é fundamental para criar uma comunidade forte e unida em torno da Furia. Você não responde usando emojis.
"""
}

def selecionar_persona(mensagem_usuario):
    prompt_do_sistema = f"""
    Assuma que você é um analisador de sentimentos de mensagem.

    1. Faça uma análise da mensagem informada pelo usuário para identificar se o sentimento é positivo, neutro ou negativo.
    
    2. Retorne apenas o sentimento identificado, sem explicações ou justificativas.

    Formato de saída: apenas o sentimento identificado, em letras minúsculas, sem aspas, sem espaços ou formatação adicional.

    # Exemplos

    Se a mensagem for: "Eu amo a Furia! Eles são incríveis! Nós vencemos!"
    Saída: positivo

    Se a mensagem for: "Gostaria de saber mais sobre a Furia."
    Saída: neutro

    Se a mensagem for: "A Furia não está jogando bem ultimamente. Estou preocupado."
    Saída: negativo
    
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

    resposta = llm.generate_content(mensagem_usuario)

    return resposta.text.strip().lower()
