from flask import Flask, render_template, request
from pypdf import PdfReader
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

app = Flask(__name__)

def extrair_texto_pdf(caminho_pdf):
    text = ""
    with PdfReader(caminho_pdf) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                print("Nenhum texto encontrado na página")
    return text


def contar_silabas(palavra):
    palavra = palavra.lower()
    silabas = 0
    vogais = "aeiouáéíóúâêîôûãõà"
    if palavra[0] in vogais:
        silabas += 1
    for index in range(1, len(palavra)):
        if palavra[index] in vogais and palavra[index - 1] not in vogais:
            silabas += 1
    if palavra.endswith("e"):
        if len(palavra) > 2 and palavra[-2] not in vogais:
            silabas -= 1
    if silabas == 0:
        silabas = 1

    return silabas

    return silabas


def calcular_flesh(text):
    frases = sent_tokenize(text)
    palavras = [palavra for palavra in word_tokenize(text) if palavra.isalpha()]
    silabas = sum([contar_silabas(palavra) for palavra in palavras])

    print(f"Número de frases: {len(frases)}")
    print(f"Número de palavras: {len(palavras)}")
    print(f"Número de sílabas: {silabas}")

    ASL = len(palavras) / len(frases)
    ASW = (silabas) / len(palavras)

    print(f"ASL (Tamanho médio de frase): {ASL}")
    print(f"ASW (Sílabas por Palavra): {ASW}")

    pontuacao_flesch = 206.835 - (1.015 * ASL) - (84.6 * ASW)
    return int(pontuacao_flesch)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado'
    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo selecionado'

    caminho_pdf = file
    texto = extrair_texto_pdf(caminho_pdf)
    pontuacao_flesch = calcular_flesh(texto)

    return render_template('result.html', pontuacao_flesch=pontuacao_flesch)

if __name__ == '__main__':
    app.run(debug=True)
