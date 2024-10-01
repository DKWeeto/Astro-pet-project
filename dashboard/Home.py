import streamlit as st


def theming():
    selected = st.session_state['themebutton']
    if selected == 'light':
        st._config.set_option(f'theme.base', "dark")
        st._config.set_option(f'theme.backgroundColor', "#000000")
        st._config.set_option(f'theme.primaryColor', "#8B0000")
        st._config.set_option(f'theme.secondaryBackgroundColor', "#000000")
        st._config.set_option(f'theme.textColor', "#8B0000")
        st.session_state['themebutton'] = 'dark'
    else:
        st._config.set_option(f'theme.base', "light")
        st._config.set_option(f'theme.backgroundColor', "#FFFFFF")
        st._config.set_option(f'theme.primaryColor', "#000000")
        st._config.set_option(f'theme.secondaryBackgroundColor', "#AE74E0")
        st._config.set_option(f'theme.textColor', "#000000")
        st.session_state['themebutton'] = 'light'


def init_themes():
    if 'themebutton' not in st.session_state:
        st.session_state.themebutton = 'dark'

    with st.sidebar:
        st.button("Change theme", on_click=theming)


if __name__ == "__main__":
    init_themes()

    
    title = '<p style="font-family: Futura;font-size: 75px;">Welcome to the <em>Night Sky Forecast!</em></p>'
    st.markdown(title, unsafe_allow_html=True)
