import speech_recognition as sr
from astral import LocationInfo
from astral.sun import sun
import datetime
import pyttsx3

class Identification:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 195)
        self.engine.setProperty('volume', 2.0)
        self.engine.setProperty('voice', 'brazil')

    def verificar_horario(self):
        latitude = -23.5505
        longitude = -46.6333
        local = LocationInfo("São Paulo", "Brazil", "America/Sao_Paulo", latitude, longitude)

        solar_info = sun(local.observer, date=datetime.date.today(), tzinfo=local.timezone)

        hora_atual = datetime.datetime.now().time()

        if solar_info['sunrise'].time() <= hora_atual <= solar_info['sunset'].time():
            return "bom dia"
        else:
            return "boa noite"

    def falar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

class RecognizeSpeech:
    @staticmethod
    def reconhece_fala():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Aguardando o comando 'Harry'...")
            audio = recognizer.listen(source)

        try:
            texto = recognizer.recognize_google(audio, language='pt-BR')
            print("Você disse: " + texto)
            return texto.lower()
        except sr.UnknownValueError:
            print("Não entendi o que foi dito")
            return None
        except sr.RequestError as e:
            print("Erro ao solicitar resultados; {0}".format(e))
            return None

    @staticmethod
    def responde_em_voz(texto):
        engine = pyttsx3.init()
        engine.say(texto)
        engine.runAndWait()

    @staticmethod
    def responde(texto):
        if texto is None:
            return
        
        if "harry oi" in texto:
            RecognizeSpeech.responde_em_voz("Oi! Como posso ajudar?")
        elif "harry tudo bem" in texto or "harry como vai" in texto:
            RecognizeSpeech.responde_em_voz("Estou bem, obrigado por perguntar!")
        elif "harry o que você é" in texto:
            RecognizeSpeech.responde_em_voz("Eu me chamo Harry, sou um assistente virtual em fase de estudos. Sendo assim, esta é a minha versão beta. Ainda vou passar por muitas melhorias e espero poder te ajudar sempre no futuro. Precisa de mais alguma coisa?")
        elif "harry quem o criou" in texto:
            RecognizeSpeech.responde_em_voz("Eu fui criado por um jovem desenvolvedor chamado Thiago, mas também conhecido como Marteex.")
        else:
            RecognizeSpeech.responde_em_voz("Desculpe, não entendi o que você disse. Pode repetir?")

if __name__ == "__main__":
    while True:
        texto_reconhecido = RecognizeSpeech.reconhece_fala()
        if texto_reconhecido and "harry" in texto_reconhecido:
            RecognizeSpeech.responde_em_voz("Sim, estou ouvindo...")
            while True:
                comando = RecognizeSpeech.reconhece_fala()
                if comando == "harry sair":
                    RecognizeSpeech.responde_em_voz("Encerrando o assistente. Até logo! Espero te ver mais vezes.")
                    break
                RecognizeSpeech.responde(comando)
            break
