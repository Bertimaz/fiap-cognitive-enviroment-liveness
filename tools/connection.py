import boto3
# import config
import streamlit as st

def connect_aws():
  
  aws_access_key_id=st.secrets['aws_access_key_id']
  aws_secret_access_key=st.secrets['aws_secret_access_key']
  session=boto3.Session(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
  return session