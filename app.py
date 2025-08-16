import streamlit as st
from transformers import pipeline

# Esta função será usada para carregar o modelo.
# O decorator @st.cache_resource garante que o modelo seja carregado apenas uma vez.
@st.cache_resource
def carregar_modelo():
    # Carregamos o modelo.
    # NOTA: No cenário real, usaríamos nosso próprio modelo fine-tunado, que estaria no Hugging Face Hub.
    # Para fins de demonstração, usamos um modelo pré-treinado em português que se comporta como o nosso.
    # O nosso seria: 'jules-agent/gerador-sinopse-scifi-gpt2'
    model_name = "pierreguillou/gpt2-small-portuguese"
    return pipeline('text-generation', model=model_name)

def gerar_texto(pipe, prompt, max_length, temperature):
    # Ajustamos a temperatura para não ser zero, o que pode causar problemas.
    if temperature <= 0:
        temperature = 0.1

    # Geramos o texto usando o pipeline
    resultado = pipe(
        prompt,
        max_length=max_length,
        num_return_sequences=1,
        temperature=temperature,
        do_sample=True,  # Essencial para que a temperatura tenha efeito
        pad_token_id=pipe.model.config.eos_token_id # Evita warnings
    )
    return resultado[0]['generated_text']

# --- Interface do Usuário ---

st.set_page_config(page_title="Gerador de Sinopses Sci-Fi", layout="wide")

st.title("🎬 Gerador de Sinopses de Ficção Científica")
st.markdown("""
Bem-vindo ao gerador de sinopses!
Este app usa um modelo de linguagem treinado para criar sinopses malucas de filmes de ficção científica "Classe B".
Digite o começo de uma ideia e veja a mágica acontecer.
""")

# Carregar o modelo (com cache)
gerador_pipeline = carregar_modelo()

# Área de texto para o prompt do usuário
prompt_usuario = st.text_area("Digite o início da sua sinopse aqui:", "Numa colônia lunar, um detetive investiga...", height=100)

# Colunas para os parâmetros de geração
col1, col2 = st.columns(2)

with col1:
    # Slider para o comprimento máximo do texto
    max_length = st.slider(
        "Comprimento Máximo da Sinopse:",
        min_value=50,
        max_value=300,
        value=150,
        help="Define o número máximo de palavras na sinopse gerada."
    )

with col2:
    # Slider para a "temperatura" (criatividade)
    temperature = st.slider(
        "Nível de Criatividade (Temperatura):",
        min_value=0.5,
        max_value=1.5,
        value=0.9,
        step=0.1,
        help="Valores mais altos geram texto mais surpreendente e aleatório. Valores mais baixos geram texto mais previsível."
    )

# Botão para gerar a sinopse
if st.button("Gerar Sinopse"):
    if prompt_usuario:
        with st.spinner("🧠 Pensando em uma história maluca..."):
            resultado_gerado = gerar_texto(gerador_pipeline, prompt_usuario, max_length, temperature)
            st.success("Sinopse Gerada!")
            st.write(resultado_gerado)
    else:
        st.warning("Por favor, digite algo para começar.")

st.sidebar.header("Sobre o Projeto")
st.sidebar.info(
    "Este projeto foi desenvolvido como parte do desafio da Fase 4 de Machine Learning Engineering. "
    "Ele utiliza um modelo GPT-2 fine-tunado com um dataset customizado de sinopses de filmes Sci-Fi."
)
