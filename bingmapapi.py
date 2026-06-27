import streamlit as st
from streamlit.components.v1 import html

def embed_bing_maps():
    # Replace 'your_bing_maps_api_key' with your actual Bing Maps API key
    bing_maps_api_key = 'yJFOAm3PDQfXfy2p4P0y~V3aNyUzg97AnqLONJMP_uQ~AqTtHFaYzvL01z82WcXwXha9JiGq9JNtS1DYPxBw3AwI0y9O_9_yxiasMWFRyAm0'

    html_code = f"""
    <iframe width="800" height="600" src="https://www.bing.com/maps/embed/viewer.aspx?v=3&cp=latitude~longitude&lvl=zoom&sty=b&typ=d&pp=latitude~longitude&ps=30&dir=0&mkt=en-us&form=BMEMJS" frameborder="0" scrolling="no"></iframe>
    """.replace('yJFOAm3PDQfXfy2p4P0y~V3aNyUzg97AnqLONJMP_uQ~AqTtHFaYzvL01z82WcXwXha9JiGq9JNtS1DYPxBw3AwI0y9O_9_yxiasMWFRyAm0', bing_maps_api_key)

    st.components.v1.html(html_code, height=600)

#    html(html_code, height=600)
