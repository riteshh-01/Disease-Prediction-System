import pickle
import streamlit as st
import warnings 
warnings.filterwarnings("ignore")

st.title("Disease Prediction System!!")
age=st.number_input("Enter Age : ")
hrb=st.number_input("Enter Heart Rate bpm : ")
bt=st.number_input("Enter Body Temperature : ")
os=st.number_input("Enter Oxygen Saturation : ")
btn=st.button("Predict!!")
if btn:
    dp=pickle.load(open("dp.pkl","rb"))
    res=dp.predict([[age,hrb,bt,os]])[0]
    st.warning(f"Expected Disease : {res}")