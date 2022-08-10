import inspect
from importlib import import_module
from pathlib import Path
from typing import Callable, List

import streamlit_patches as st


def home():
    st.title("🌍 Streamlit Hub!")
    st.write(
        """
Welcome to the Streamlit Hub.

Here, you will find fun Streamlit re-usable pieces of code to customize your apps. Have fun!
"""
    )


def contribute():
    st.title("🙋 Contribute")


st.page(home, "Home", "🌎")
st.page(contribute, "Contribute", "🙋")


def empty():
    pass


st.page(empty, "―――――――――――――――――", " ")

component_names = [folder.name for folder in Path("components").glob("*")]

settings = dict()

for component in component_names:
    mod = import_module(f"components.{component}")
    title = mod.__title__
    icon = mod.__icon__
    func = mod.__func__
    examples = mod.__examples__

    def get_page_content(icon: str, title: str, examples: List[Callable]) -> Callable:
        def page_content():
            st.title(icon + " " + title)
            st.write("## Example")

            for example in examples:
                st.code(inspect.getsource(example))
                example()

            st.write("## Docstring")
            st.help(func)

            st.write("## Source code")
            st.code(inspect.getsource(func))

        page_content.__name__ = title

        return page_content

    settings[component] = dict(
        path=get_page_content(icon, title, examples),
        name=title,
        icon=icon,
    )

    st.page(**settings[component])