import streamlit as st

def app():
    text = '''
    # Roosevelt Racers Race Time Calculator V2

    Race Time Calculator for the STEM Racing competition.
    Built with: Python 🐍, Streamlit

    ![image](https://raw.githubusercontent.com/ELROSTEM/Race-Time-Calculator-V2/refs/heads/main/.github/images/RTC%20cover.jpg)

    # Who are the Roosevelt Racers (RR)?

    We are a dedicated team of Eleanor Roosevelt High School students participating in this year's National Finals competition. After our team went through a brief hiatus during the height of the COVID-19 pandemic, the Roosevelt Racers reentered the competitive sphere in 2024 and placed 1st in all categories during the 2024 Eastern Regionals. If we win or place at least above 3rd place nationally, we’ll advance to the World Finals.

    This is what the competition looks like IRL:

    ![Alt Text](https://media.giphy.com/media/SCuZ1vPVJXdi2e95Hc/giphy.gif)

    # What is the Race Time Calculator?

    The Race Time Calculator, built by our engineering team, was designed to complement our design process by creating a virtual testing environment for car models. The original Race Time Calculator was built by the R&D division of the 2020-2021 Roosevelt Racers Team to serve as an indicator of whether or not a dragster should be manufactured. This season, we aimed to incorporate the Calculator into a design process by developing an approximate, if not fully accurate, model of car motion capable of comparing car models based on physical parameters. Our ultimate vision is to create software that accelerates the engineering process for our dragsters as well as to create a product polished enough for other teams to utilize in their engineering endeavors.

    ![image](https://raw.githubusercontent.com/ELROSTEM/Race-Time-Calculator-V2/refs/heads/main/.github/images/screenshot.png)

    '''
    st.markdown(text)