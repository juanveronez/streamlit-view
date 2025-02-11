import streamlit as st
import pandas as pd
from plotly import graph_objects as go
from typing import Literal

from database import engine

def create_plot(df: pd.DataFrame, 
                plot_type: Literal['bar', 'line', 'scatter', 'pie']):
    
    if plot_type == 'bar':
        return go.Figure(data=[go.Bar(x=df['name'], y=df['price'])])
    elif plot_type == 'line':
        return go.Figure(data=[go.Scatter(x=df["name"], y=df['price'], mode='lines+markers')])
    elif plot_type == 'scatter':
        return go.Figure(data=[go.Scatter(x=df['name'], y=df['price'], mode='markers')])
    elif plot_type == 'pie':
        return go.Figure(data=[go.Pie(labels=df['name'], values=df['price'])])
    
    raise ValueError(f"Unsupported plot type: {plot_type}")

def get_products():
    q = "SELECT DISTINCT name, price FROM products ORDER BY price DESC"

    with engine.connect() as con:
        return pd.read_sql(q, con)

def main():
    df = get_products()

    st.title('Dashboard de Preços')

    st.write("Produtos:")
    st.dataframe(df)

    uploaded_file = st.file_uploader("Carregar arquivo Excel", type="xlsx")
    if uploaded_file is not None:
        excel_data = pd.read_excel(uploaded_file)
        df = pd.concat([df, excel_data])  # Combinar com dados do banco
        df = df.nlargest(
            5, "price"
        )  # Atualizar o DataFrame para o top 5 após concatenação

    st.write("Top 5 Produtos (Atualizado):")
    st.dataframe(df[:5])

    plot_types = ["bar", "line", "scatter", "pie"]
    plot_type = st.selectbox("Selecione o tipo de gráfico", plot_types)
    plot = create_plot(df, plot_type)
    st.plotly_chart(plot)

    # Adicionar uma imagem
    # st.image("caminho_para_sua_imagem.jpg", caption="Imagem de Exemplo")

    # Função adicional 1: Seleção de data
    st.date_input("Escolha uma data")

    # Função adicional 2: Caixa de texto
    texto = st.text_input("Digite algo")

    # Função adicional 3: Slider
    numero = st.slider("Escolha um número", 0, 100)

    # Função adicional 4: Botão de rádio
    opcao = st.radio("Escolha uma opção", ["Opção 1", "Opção 2", "Opção 3"])

    # Função adicional 5: Checkbox
    check = st.checkbox("Marque a opção")

    # Função adicional 6: Seletor de cor
    cor = st.color_picker("Escolha uma cor")

    # Mostrar as escolhas do usuário
    st.write("Texto digitado:", texto)
    st.write("Número escolhido:", numero)
    st.write("Opção selecionada:", opcao)
    st.write("Checkbox marcado:", check)
    st.write("Cor escolhida:", cor)


if __name__ == "__main__":
    main()