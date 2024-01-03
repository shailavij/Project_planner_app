import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
#from  PIL import ImageChops
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 

#st.set_page_config(page_title="Sharone's Streamlit App Gallery", page_icon="", layout="wide")

# sysmenu = '''
# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# '''
#st.markdown(sysmenu,unsafe_allow_html=True)

#Add a logo (optional) in the sidebar
logo = Image.open(r'logo1.png')
profile = Image.open(r'logo2.png')

with st.sidebar:
    choose = option_menu("App Gallery", ["Project Planning","Contact"],
                         icons=['house', 'camera fill', 'kanban', 'book','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


#logo = Image.open(r'C:\Users\13525\Desktop\Insights_Bees_logo.png')
#profile = Image.open(r'C:\Users\13525\Desktop\medium_profile.png')

if choose == "Project Planning":
#Add a file uploader to allow users to upload their project plan file
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your project plan</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Fill out the project plan template and upload your file here. After you upload the file, you can edit your project plan within the app.", type=['csv'], key="2")
    if uploaded_file is not None:
        Tasks=pd.read_csv(uploaded_file)
        Tasks['Start'] = Tasks['Start'].astype('datetime64[ns]')
        Tasks['Finish'] = Tasks['Finish'].astype('datetime64[ns]')
        
        grid_response = AgGrid(
            Tasks,
            editable=True, 
            height=300, 
            width='100%',
            )

        updated = grid_response['data']
        df = pd.DataFrame(updated) 
        
        if st.button('Generate Gantt Chart'): 
            fig = px.timeline(
                            df, 
                            x_start="Start", 
                            x_end="Finish", 
                            y="Task",
                            color='Team',
                            hover_name="Task Description"
                            )

            fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       
            
            fig.update_layout(
                            title='Project Plan Gantt Chart',
                            hoverlabel_bgcolor='rgb(252,141,89)',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                            bargap=0.2,
                            height=600,              
                            xaxis_title="", 
                            yaxis_title="",                   
                            title_x=0.5,                    #Make title centered                     
                            xaxis=dict(
                                    tickfont_size=15,
                                    tickangle = 0,
                                    rangeslider_visible=True,
                                    side ="top",            #Place the tick labels on the top of the chart
                                    showgrid = True,
                                    zeroline = True,
                                    showline = True,
                                    showticklabels = True,
                                    tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                    )
                        )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('---') 
   



elif choose == "Contact":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
        Email=st.text_input(label='Please Enter Your Email') #Collect user feedback
        Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')

