import mat73
import csv

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from bokeh.plotting import figure
import altair as alt


global Description, NewData, data

def FindLongestList(Data):
    templength = 0
    for list in Data:
        length = len(list)
        if  length >=  templength:
            templength = length
    return templength

def CreateTimeAxisList(Data):
    i = 0.01
    timeList = []
    while len(timeList) <= FindLongestList(Data):
        timeList.append(i)
        i = i + 0.01
    return timeList

def ListTimeCorecction(DataList, DataFactor):
    list_multiplied = [entry for entry in DataList for _ in range(DataFactor)]
    return list_multiplied

def GetDataFromMat(FileName):
    data_dict = mat73.loadmat('C:\\Users\\oze\\Desktop\\' + FileName)  ## Write the path of the dSPACE data File.
    global Description
    Description = []
    word = 0

    data = []
    item = 0

    listRow = []
    i = 0

    list_origen = []
    fac = 0
    ind = 0
    Loading = 1
    global  NewData
    NewData = []

    while word != 72:
        Description.append(data_dict['rec']['Y'][word]['Description'])
        word = word + 1
    Description.append('timeList')

    while item != 72:  # need to be changed to number of virables recorded
        data.append(data_dict['rec']['Y'][item]['Data'])
        item = item + 1
    timeList = CreateTimeAxisList(data)
    data.append(timeList)

    for AnyList in data:
        # TEST
        print(Loading, len(AnyList), FindLongestList(data))
        # TEST

        if len(AnyList) < FindLongestList(data):
            if ((FindLongestList(data) / len(AnyList)) > 10.4 and (FindLongestList(data) / len(AnyList) < 11.6)):
                DataFactor = 10.5
            else:
                DataFactor = round(FindLongestList(data) / len(AnyList))
            NewList = ListTimeCorecction(AnyList, DataFactor)
        NewData.append(NewList)

        ##TEST
        print('After:', len(NewList))
        Loading = Loading + 1

    return Description, data, NewData, FileName


def WriteToCSV(TargetName, Description, data, NewData):
    with open(TargetName, 'w', newline='') as file:  ## Write the name of the new converted csv file.
        writer = csv.writer(file)
        writer.writerow(Description)
        i = 0
        listRow = []

        while i < FindLongestList(data):  ## Set the data Quntity as the time of the meshurment
            for list_origen in NewData:
                if i < len(list_origen):
                    listRow.append(list_origen[i])
                else:
                    listRow.append('')
            writer.writerow(listRow)
            i = i + 1
            listRow = []


def StreamlitGUI(TargetName, FileName):

    left_column, right_column = st.columns(2)

    StData = pd.read_csv(TargetName)


    #st.sidebar.write('This graphs are ganerted from .mat file.')
    #st.sidebar.write('Name of File: ', FileName)
    #Tax = st.sidebar.radio(label='Time as X axis?', options=['Yes', 'No'])

    X = left_column.selectbox('', Description)
    Xnum = Description.index(X)
    left_column.line_chart(data=NewData[Xnum])

    Y = right_column.selectbox(' ', Description)
    Ynum = Description.index(Y)
    right_column.line_chart(data=NewData[Ynum])\

    st.write("""# **The selected graphes combined** """)

    stdf = pd.DataFrame(StData, columns=[X, Y])
    st.line_chart(stdf)

    if X != Y:
        c = alt.Chart(stdf).mark_circle(size=60).encode(x=X, y=Y).interactive()
        st.altair_chart(c, use_container_width=True)

    # To run, open cmd at the right path and type: streamlit run main.py


def main():
    st.set_page_config(layout="wide")
    st.write("""## **dSpace Data analysis From .mat File** """)
    my_expander = st.sidebar.expander(label='Files selection')
    with my_expander:
        FileName = st.file_uploader('Choose a .mat file: ')
        TargetF = st.text_input('Choose The name of the target creation file: ', 'Type Here')

    if (FileName != None) and (TargetF != 'Type Here'):
        Description, data, NewData, FileName = GetDataFromMat(FileName.name)
        WriteToCSV(TargetF, Description, data, NewData)
        StreamlitGUI(TargetF, FileName)

if __name__ == "__main__":
    main()