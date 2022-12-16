import streamlit as st #importing streamlit for making Web App
from streamlit.proto.RootContainer_pb2 import SIDEBAR
import plotly.express as px; #importing plotly for making Graph
import pandas as pd #importing pandas for doing operations on DataFrame

#importing and selecting Attributes for doing analysis on DataFrame
df = pd.read_csv("C:\\Users\\Prerna kamboj\\Documents\\Python\\heart.csv")
df = df.drop(['ExerciseAngina','FastingBS','Oldpeak','ST_Slope','ChestPainType'],axis=1)

st.set_page_config(page_title="Heart Disease Analysis",
  layout="wide"
)

st.header("Heart csv Dashboard...")
 
# SIDEBAR CONFIGURATION
#Header of SideBar
st.sidebar.header("Filter")

#SideBar Slider for selecting age
age = st.sidebar.slider("Age: ", int(df["Age"].min()), int(df["Age"].max()), value=(50,60))

#SideBar MultiSelect for selecting Gender 
gender = st.sidebar.multiselect(
  "Gender: ",
  options=df["Sex"].unique(), #Setting Options available for user for selecting Gender using Gender Column
  default=df["Sex"].unique() #Options which would be selected already on launch of Web App
)

#SideBar MultiSelect for selecting ECG
resting_ecg = st.sidebar.multiselect(
  "Resting Ecg: ",
  options=df["RestingECG"].unique(),
  default=df["RestingECG"].unique()
)

#SideBar MultiSelect for selecting MaxHR
maxhr = st.sidebar.slider("Max HeartRate: ", int(df["MaxHR"].min()), int(df["MaxHR"].max()), (100,160))

# Here We are filtering data on the basis of options selected by the user provided on SIDEBAR
df_selection = df.query(
  "Sex == @gender & RestingECG== @resting_ecg & (Age>=@age[0] and Age<=@age[1]) & (MaxHR>=@maxhr[0] and MaxHR<=@maxhr[1])"
)

# Making Bar Graph b/w Age & Heart Disease on the basis of Gender
Gender_Plot = px.bar(df_selection, 
  x="Age", 
  y="HeartDisease",
  color="Sex",
  color_discrete_map= {'M' : 'royalblue', 'F' : 'orangered'}, # Setting Color for 'M' & 'F' Curve
  title="<b>Frequency of Heart Patients on the basis of Gender b/w"+ str(age[0]) + "-" + str(age[1]) + "Yr</b>", # Setting title for the Graph
)

# Making Line Chart b/w Age and Heart Disease
Age = px.line(df_selection.groupby("Age")["HeartDisease"].sum(), # Here We are using Groupby to get count of Heart Patients of respective age
  title="<b>Frequency of Heart Patients b/w "+ str(age[0]) + "-" + str(age[1]) + "Yr</b>",
)

# Plotting Line Chart on Web App
st.plotly_chart(Age)

#Setting Line b/w two Charts
st.markdown("------")

# Plotting Line Chart on Gender App
st.plotly_chart(Gender_Plot)

st.markdown("------")


# Setting Pie Chart b/w Heart Disease and Resting ECG
ECG_Plot = px.pie(df_selection, 
  values="HeartDisease", 
  names="RestingECG",
  title="<b>Percentage Distribution of Heart Patients on the basis of ECG</b>",
)


# Plotting Given Pie Chart
st.plotly_chart(ECG_Plot)

# Making Line Chart b/w MaxHR and Heart Disease
MaxHR = px.line(df_selection.groupby("MaxHR")["HeartDisease"].sum(), # Here We are using Groupby to get count of Heart Patients of respective MaxHR
  title="<b>Frequency of Heart Disease b/w "+ str(maxhr[0]) + "-" + str(maxhr[1]) + " Max HRate</b>",
)

st.markdown("------")

# Plotting
st.plotly_chart(MaxHR)

