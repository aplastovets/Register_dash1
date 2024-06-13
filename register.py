import streamlit as st
import pandas as pd
import plotly.express as px

# Заголовок приложения
st.title("Аналитика судебного реестра")

# Данные
uploaded_registry = st.file_uploader("Выберите файл реестра в формате csv", type="csv")


if uploaded_registry is not None:
    # Чтение CSV файла в DataFrame
    df = pd.read_csv(uploaded_registry)
    pivot_status = df.groupby(['Юрист', 'Статус']).size().unstack(fill_value=0)
    st.write(pivot_status)

    df_reset = pivot_status.reset_index()
    df_melted = df_reset.melt(id_vars=['Юрист'], var_name='Статус', value_name='Количество дел')

    # Определяем цвета для статусов
    color_map = {
        'Выиграли': '#B6E880',
        'Исполнено': '#EF553B',
        'Мировое': '#EF553B',
        'Проиграли': '#EF553B',
        'On hold': '#19D3F3',
        'В работе': '#FECB52',
        'Обжалуем': '#FECB52'
    }

    # Добавляем столбец с цветами
    df_melted['Цвет'] = df_melted['Статус'].map(color_map)

    # Создаем гистограмму
    fig = px.bar(df_melted, x='Юрист', y='Количество дел', color='Статус',
                 color_discrete_map=color_map, width=800, height=600,
                 title='Количество дел для каждого юриста по статусам')
    st.plotly_chart(fig)


    # Добавляем столбец с цветами
    df_melted['Цвет'] = df_melted['Статус'].map(color_map)

    # Создаем и отображаем отдельные гистограммы для каждого юриста
    for юрист in df_melted['Юрист'].unique():
        df_filtered = df_melted[df_melted['Юрист'] == юрист]
        fig = px.bar(df_filtered, x='Статус', y='Количество дел', color='Статус', width=800, height=600,
                     color_discrete_map=color_map, title=f'Количество дел для юриста {юрист}')
        st.plotly_chart(fig)

     

    st.title('Введите стоимость Юристов')
    price = False
    price = st.number_input('Введите стоимость', min_value=0.0, step=0.01)
    
    if price is not False:

        df['Сумма в иске'] = pd.to_numeric(df['Сумма в иске'], errors='coerce')
        df['Итоговые потери'] = df['Сумма в решении'] + df['Расходы юристов']
        pivot_df = df[['Юрист', 'Сумма в иске', 'Итоговые потери']].groupby(['Юрист']).sum()
        pivot_df['Стоимоть юриста'] = 2000000
        pivot_df['Доходность юриста'] = pivot_df['Сумма в иске'] - pivot_df['Итоговые потери']
        pivot_df['Окупаемость юриста'] = pivot_df['Доходность юриста'] - pivot_df['Стоимоть юриста']


        st.write("Если будет совсем плохо:")
        st.write(pivot_df)

        df['Текущие потери'] = df['Списали со счета'] - df['Расходы юристов']
        current_losses = df[['Юрист', 'Сумма в иске', 'Текущие потери']].groupby(['Юрист']).sum()
        current_losses['Стоимоть юриста'] = 2000000
        current_losses['Доходность юриста'] = current_losses['Сумма в иске'] - current_losses['Текущие потери']
        current_losses['Окупаемость юриста'] = current_losses['Доходность юриста'] - current_losses['Стоимоть юриста']

        st.write("Наилучшие стечения обстоятельств")
        st.write(current_losses)
