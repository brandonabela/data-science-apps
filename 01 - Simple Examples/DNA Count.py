####################
# Import Libraries
####################

import pandas as pd
import streamlit as st
import altair as alt

####################
# Page Title
####################

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA

***
""")

####################
# Input Text Box
####################

# Storing DNA sequence input
sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

# Split lines and display sequence
sequence = st.text_area("Sequence input", sequence_input, height=150)
sequence = sequence.splitlines()

# Merge Line and ignore first line
sequence = sequence[1:]
sequence = ''.join(sequence)

# Print Line
st.write("""
***
""")

# Print Heading
st.header('Output (DNA Nucleotide Count)')

# Show as Dictionary

st.subheader('1. Show as dictionary')

def DNA_nucleotide_count(seq):
    return dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C'))
    ])

X = DNA_nucleotide_count(sequence)
X

# Show as Text

st.subheader('2. Show as Text')
st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['T']) + ' thymine (T)')
st.write('There are ' + str(X['G']) + ' guanine (G)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')

# Show as DataFrame

st.subheader('3. Show as DataFrame')

df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)

df = df.rename(columns = {'index': 'nucleotide'})
st.write(df)

# Show as Bar Chart using Altair

st.subheader('4. Show as Bar Chart')

p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)

p = p.properties(
    width=alt.Step(80) # Control bar width
)

st.write(p)
