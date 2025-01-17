import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st
import matplotlib.pyplot as plt

# Definindo as variáveis fuzzy e seus termos
matematica = ctrl.Antecedent(np.arange(0, 11, 1), 'matematica')
logico = ctrl.Antecedent(np.arange(0, 11, 1), 'logico')
estatistica = ctrl.Antecedent(np.arange(0, 11, 1), 'estatistica')
programacao = ctrl.Antecedent(np.arange(0, 11, 1), 'programacao')
preferencia = ctrl.Consequent(np.arange(0, 11, 1), 'preferencia')

# Definindo os termos fuzzy para cada variável
matematica['baixo'] = fuzz.trimf(matematica.universe, [0, 0, 5])
matematica['medio'] = fuzz.trimf(matematica.universe, [0, 5, 10])
matematica['alto'] = fuzz.trimf(matematica.universe, [5, 10, 10])

logico['baixo'] = fuzz.trimf(logico.universe, [0, 0, 5])
logico['medio'] = fuzz.trimf(logico.universe, [0, 5, 10])
logico['alto'] = fuzz.trimf(logico.universe, [5, 10, 10])

estatistica['baixo'] = fuzz.trimf(estatistica.universe, [0, 0, 5])
estatistica['medio'] = fuzz.trimf(estatistica.universe, [0, 5, 10])
estatistica['alto'] = fuzz.trimf(estatistica.universe, [5, 10, 10])

programacao['baixo'] = fuzz.trimf(programacao.universe, [0, 0, 5])
programacao['medio'] = fuzz.trimf(programacao.universe, [0, 5, 10])
programacao['alto'] = fuzz.trimf(programacao.universe, [5, 10, 10])

# Ajustando as funções de pertinência para preferencia
preferencia['baixa'] = fuzz.trimf(preferencia.universe, [0, 0, 6])
preferencia['media'] = fuzz.trimf(preferencia.universe, [4, 6, 8])  # Ajuste para [5, 7, 9] para [4, 6, 8]
preferencia['alta'] = fuzz.trimf(preferencia.universe, [7, 10, 10])  # Reduzindo para [7, 10, 10]

# Definindo as regras fuzzy
regra1 = ctrl.Rule(matematica['alto'] & logico['alto'] & estatistica['alto'] & programacao['alto'], preferencia['alta'])
regra2 = ctrl.Rule((matematica['alto'] | logico['alto'] | estatistica['alto'] | programacao['alto']), preferencia['alta'])
regra3 = ctrl.Rule((matematica['medio'] & logico['medio'] & estatistica['medio'] & programacao['medio']), preferencia['media'])
regra4 = ctrl.Rule(matematica['baixo'] & logico['baixo'] & estatistica['baixo'] & programacao['baixo'], preferencia['baixa'])

# Criando o sistema de controle
controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4])
sistema = ctrl.ControlSystemSimulation(controle)

# Interface gráfica com Streamlit
st.markdown(
        """
        <div style='text-align: center;'>
            <h1>Sistema Fuzzy para o curso de Ciência de Dados da Fatec</h1>
        </div>
        """, unsafe_allow_html=True
    )
# Centralizando a imagem usando colunas
col1, col2, col3 = st.columns([1, 2, 1])  # Definindo uma estrutura de colunas com proporções 1:2:1

with col2:
    st.image('/Users/ronnieshida/PycharmProjects/novoprojeto/img.png', width=350)
#st.title('Sistema Fuzzy para o curso de Ciência de Dados da Fatec Adamantina')

# Slider para entrada de valores
st.sidebar.title('Valores de Entrada')
matematica_value = st.sidebar.slider('Matemática', 0, 10, 5)
logico_value = st.sidebar.slider('Lógico', 0, 10, 5)
estatistica_value = st.sidebar.slider('Estatística', 0, 10, 5)
programacao_value = st.sidebar.slider('Programação', 0, 10, 5)

# Atualizando os valores de entrada no sistema fuzzy
sistema.input['matematica'] = matematica_value
sistema.input['logico'] = logico_value
sistema.input['estatistica'] = estatistica_value
sistema.input['programacao'] = programacao_value

# Computando o resultado
sistema.compute()

# Obtendo o valor de saída nítido
preferencia_value = sistema.output['preferencia']

# Exibindo o resultado
#st.write(f'Preferência de Curso: {preferencia_value:.2f}')
st.markdown(f'<p style="font-size:24px;">Afinidade do aluno para o curso em uma escala de 0 a 10 é: <strong>{preferencia_value:.2f}</strong></p>', unsafe_allow_html=True)


# Visualização dos universos e funções de pertinência
st.subheader('Visualização das Funções de Pertinência')

# Plotando as funções de pertinência
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 10))

# Matemática
ax1.plot(matematica.universe, fuzz.trimf(matematica.universe, [0, 0, 5]), 'b', linewidth=1.5, label='Baixo')
ax1.plot(matematica.universe, fuzz.trimf(matematica.universe, [0, 5, 10]), 'g', linewidth=1.5, label='Médio')
ax1.plot(matematica.universe, fuzz.trimf(matematica.universe, [5, 10, 10]), 'r', linewidth=1.5, label='Alto')
ax1.title.set_text('Matemática')
ax1.legend()

# Lógico
ax2.plot(logico.universe, fuzz.trimf(logico.universe, [0, 0, 5]), 'b', linewidth=1.5, label='Baixo')
ax2.plot(logico.universe, fuzz.trimf(logico.universe, [0, 5, 10]), 'g', linewidth=1.5, label='Médio')
ax2.plot(logico.universe, fuzz.trimf(logico.universe, [5, 10, 10]), 'r', linewidth=1.5, label='Alto')
ax2.title.set_text('Lógico')
ax2.legend()

# Estatística
ax3.plot(estatistica.universe, fuzz.trimf(estatistica.universe, [0, 0, 5]), 'b', linewidth=1.5, label='Baixo')
ax3.plot(estatistica.universe, fuzz.trimf(estatistica.universe, [0, 5, 10]), 'g', linewidth=1.5, label='Médio')
ax3.plot(estatistica.universe, fuzz.trimf(estatistica.universe, [5, 10, 10]), 'r', linewidth=1.5, label='Alto')
ax3.title.set_text('Estatística')
ax3.legend()

# Programação
ax4.plot(programacao.universe, fuzz.trimf(programacao.universe, [0, 0, 5]), 'b', linewidth=1.5, label='Baixo')
ax4.plot(programacao.universe, fuzz.trimf(programacao.universe, [0, 5, 10]), 'g', linewidth=1.5, label='Médio')
ax4.plot(programacao.universe, fuzz.trimf(programacao.universe, [5, 10, 10]), 'r', linewidth=1.5, label='Alto')
ax4.title.set_text('Programação')
ax4.legend()

# Ajustes finais de layout
plt.tight_layout()

# Mostrando os gráficos no Streamlit
st.pyplot(fig)
