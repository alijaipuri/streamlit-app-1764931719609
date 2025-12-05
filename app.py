import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='Currency Converter', page_icon='📈')

st.title('💸 Currency Converter')
st.markdown('Convert between USD, EUR, GBP, and INR with real-time exchange rates')

# API endpoint to get real-time exchange rates
def get_exchange_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        rates = data['rates']
        return rates
    except requests.exceptions.RequestException as e:
        st.error(f'Error fetching exchange rates: {e}')
        return None

# Get real-time exchange rates
exchange_rates = get_exchange_rates()

# Check if exchange rates are available
if exchange_rates:
    # Define currencies and their corresponding exchange rates
    currencies = {
        'USD': 1,
        'EUR': exchange_rates['EUR'],
        'GBP': exchange_rates['GBP'],
        'INR': exchange_rates['INR']
    }

    # Sidebar inputs
    with st.sidebar:
        st.header('Settings')
        base_currency = st.selectbox('Base Currency', list(currencies.keys()))
        target_currency = st.selectbox('Target Currency', list(currencies.keys()))
        amount = st.number_input('Amount', min_value=0.0, value=100.0, step=0.01)

    # Main content
    if st.button('Convert', type='primary'):
        try:
            # Calculate converted amount
            converted_amount = (amount / currencies[base_currency]) * currencies[target_currency]
            st.success(f'{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}')
        except ZeroDivisionError:
            st.error('Cannot divide by zero')
        except Exception as e:
            st.error(f'Error converting currency: {e}')

    # Show exchange rates
    with st.expander('View Exchange Rates'):
        exchange_rates_df = pd.DataFrame(list(currencies.items()), columns=['Currency', 'Exchange Rate'])
        st.write(exchange_rates_df)

    # Show example
    with st.expander('See example'):
        example_amount = 100.0
        example_base_currency = 'USD'
        example_target_currency = 'EUR'
        example_converted_amount = (example_amount / currencies[example_base_currency]) * currencies[example_target_currency]
        st.write(f'Example: {example_amount} {example_base_currency} is equal to {example_converted_amount:.2f} {example_target_currency}')
else:
    st.error('Error fetching exchange rates')