#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:51:21 2023

@author: fbi
"""

### Importering av moduler

import streamlit as st
import tin100 as tin
import pandas as pd
import numpy as np

## title

st.title("""
          Lånesøknad for boliglån
    """)

## Bilde

st.markdown("![Alt Text]("
            "https://blogg.paretobank.no/hs-fs/hubfs/Driftsfinansiering%20Slik%20skriver%20du%\
20en%20lånesøknad.png?width=1000&name=Driftsfinansiering%20Slik%20skriver%20du%20en%20lånesøknad.png)")

alder = st.number_input("**Alder**", min_value=0, max_value=100, value=30, step=1, key=1)

gender = st.radio("**Kjønn**", ("Mann", "Dame"), key=2)

Gift = st.selectbox("**Gift**", ["Ja", "Nei"], key=3)

Selvstendig = st.selectbox("**Selvsendig drivende**", ["Ja", "Nei"], key=4,
                           help="Hvordan driver, henter du inntekt?")

Utdanning = st.selectbox("**Utdanning**", ["Ja", "Nei"], key=5,
                         help="Utdanning høgre enn vidergåande.")

Barn = st.number_input("**Barn under 18 år**", min_value=0, max_value=100, value=0, step=1, key=6)

if Barn >= 3:
    Barn = 3
else:
    Barn = Barn

Eigendom = st.selectbox("**Eiendomsområde**", ["Storby", "By", "Distrikt Norge"], key=7,
                        help="Hvilken eigendomsområder er du fra?")
if Eigendom == 'Storby':
    Eigendom = 0
elif Eigendom == 'By':
    Eigendom = 1
else:
    Eigendom = 2

Kredit_hist = st.slider("**Kredit historie**", 0, 1, 1)

Inntekt = st.number_input("**Inntekt (Antall 1000)**", min_value=0.0, max_value=10000000.0, step=5.0, value=50.0, key=8,
                          help="Her snakker vi om bruttoinntekt (inntekt før skatt)")

Medsokerinntekt = st.number_input("**Medsøkerinntekt (Antall 1000)**", min_value=0.0, max_value=10000000.0,
                                  step=5.0, value=50.0, key=9,
                                  help="Medsøkerinntekt er inntekten til en person som søker sammen med deg om å få et "
                                       "lån eller annen form for finansiering. Dette kan være en ektefelle, samboer "
                                       "eller "
                                       " noen annen form for partner.")

tid_laan = st.number_input("**Tidligere lån? (antall 1000)**", min_value=0.0, max_value=10000000.0, step=5.0,
                           value=50.0,
                           key=10, help="Hvor mye tidligere lån har du?")

onsk_laan = st.number_input("**Lån (antall 1000)**", min_value=0.0, max_value=10000000.0, step=5.0, value=50.0,
                            key=11, help="Hvor mye vil du låne?")

egenkapital = st.number_input("**Egenkapital (antall 1000)**", min_value=0.0, max_value=10000000.0, step=1.0,
                              value=5.0, key=12, help="Hvor mye egenkapital har du?")

mnd = st.slider("**Låne lengde (antall måned)**", 0, 360, 1, help="Hvor lang tid vil du låne?", key=13)

rente = st.slider("**Rente**", min_value=0.0, max_value=10.0, step=0.1, key=14,
                  help='Sjekk ut nebetaligsplan for ulike renter.')

Laan = tid_laan + onsk_laan  # totalt lån, tidligere + ønsket lån

if rente < 1.04:
    rente = 1.07
else:
    rente += 0.03

Laan_med_rente = Laan * (1 + rente / 100) ** (mnd / 12)  # lån med hensyn til rente og måneder

### Legger dataen inn i en dictionary

data_dic = {'Gender': [np.where(gender == 'Male', 1, 0)],
            'Married': [np.where(Gift == 'Ja', 1, 0)],
            'Dependents': [Barn],
            'Education': [np.where(Utdanning == 'Ja', 1, 0)],
            'Self_Employed': [np.where(Selvstendig == 'Ja', 1, 0)],
            'ApplicantIncome': [Inntekt * 1000],
            'CoapplicantIncome': [Medsokerinntekt * 1000],
            'LoanAmount': [Laan * 1000],
            'Loan_Amount_Term': [tid_laan * 1000],
            'Credit_History': [Kredit_hist],
            'Property_Area': [Eigendom]}

## Konverterer fra dictionary til dataframe
data = pd.DataFrame.from_dict(data_dic)

## Tekst med info om nettsiden
with st.sidebar:
    st.subheader('Om siden')
    st.markdown('En lånesøknad er en formell anmodning om å få låne penger fra en bank eller annen kredittinstitusjon.'
                ' Søknaden skal inneholde informasjon om den personen som søker lån, for eksempel inntekt, formue,'
                ' gjeld og personlig informasjon. Søknaden skal også inneholde informasjon om hva lånet skal brukes'
                ' til, samt den ønskede lånebeløpet og løpetiden.')

    st.markdown('Det er viktig at all informasjonen som gis i en lånesøknad er korrekt og oppdatert, siden bankene'
                ' eller kredittinstitusjonene vil bruke denne informasjonen for å vurdere søkerens kredittverdighet'
                ' og avgjøre om lånesøknaden skal godkjennes eller ikke.')

    st.markdown('Det er også viktig å sjekke og sammenligne ulike tilbud og lånebetingelser fra forskjellige'
                ' institusjoner før en avgjørelse tas. Så i korte trekk så er en lånesøknad en formell anmodning'
                ' om lån fra en institusjon som skal inneholde informasjonen om deg som person, dine økonomiske'
                ' forhold og hva lånet skal brukes til.')
    st.markdown('Denne nettsiden er lagd av **Joel**, **Dino** and **Trish** ved hjelp av modulen Streamlit')


### Nedbetalings graph

## Total lån med rente, nedbetalig av lån, fast betaling til toalat lån med rente (totalt kostnad)

def Laan_graph(graph=None):
    G = Laan * 1000
    terminrente = ((rente / 100) / (1 - (1 + (rente / 100)) ** (-mnd)))
    y = G * terminrente  # Måndelig terminbeløp

    tot = G * (1 + rente / 100) ** (mnd / 12)
    terminbelop = tot / mnd

    nedbetaling = []
    avdrag = []
    laanekost = []

    for j in range(mnd + 1):
        G = G * (1 + rente / 100) - y
        nedbetaling.append(G)
        avdrag.append(Laan * 1000 - G)
        laanekost.append(terminbelop * j)

    chart_data = pd.DataFrame(
        [[i, k, t] for i, k, t in zip(nedbetaling, avdrag, laanekost)],
        columns=['Nedbetalingsplan', 'Avdrag på lånesum', 'Total terminbeløp'])

    if graph == 1:
        st.line_chart(chart_data)
    else:
        return np.around(y, 2)


Laan_graph(graph=1)

### Informasjon under grafen om lånesøknaden

var = [Laan, Laan, Laan_graph(graph=2), egenkapital]

var_str = ['Totalt lån',
           'Totalt lån med rente', 'Månedlig terminbeløp', 'Egenkapital krav for lån']

for i, k in zip(var, var_str):
    if k == 'Låne mengde' or k == 'Totalt lån':
        i = i * 1000
    elif k == 'Totalt lån med rente':
        i = np.around(Laan_med_rente * 1000, 1)
    elif k == 'Egenkapital krav for lån':
        i = np.around((onsk_laan * 1000) * 0.15, 1)
    st.write('**' + k + '**', ': ', i)


### knapp som sender lånesøknaden til testing/predikering

def knapp():
    if st.button('Send søknad'):
        if onsk_laan * 0.15 >= egenkapital:
            return st.write('Takk for søknaden, din søknad er dessverre ikke akseptert.'
                            ' \
        For å få det ønsket lånet må du ha en egenekapital større eller lik {2} Du kan ikke låne: \
        {0} USD i {1} måneder'.format(Laan * 1000, mnd, (onsk_laan * 1000) * 0.15))

        elif (Inntekt + Medsokerinntekt) <= (onsk_laan / 5):
            return st.write('Takk for søknaden, din søknad er dessverre ikke akseptert.'
                            ' \
For å få det ønsket lånet må du ha en total inntekt (medsøkerinntekt + inntekt) større eller lik {2} Du kan ikke låne: \
{0} USD i {1} måneder'.format(Laan * 1000, mnd, (onsk_laan * 1000) / 5))

        prediction = tin.predic(data, tin.RanForClf())

        if prediction == 0:
            return st.write('Takk for søknaden, din søknad er dessverre ikke akseptert. '
                            ' \
                          Du kan ikke låne: {0} USD i {1} måneder'.format(Laan * 1000, mnd))
        else:
            return st.write('Takk for søknaden, din søknad er akseptert.'
                            '\
         Totalkostnad på {0} år: {1} '
                            '\
         , Lånekostnad {2} pr. md.'.format(int(mnd / 12), np.around(Laan_med_rente * 1000, 1),
                                           np.around(Laan_graph(), 1)))


knapp()