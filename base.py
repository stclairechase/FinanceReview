import click
import setuptools
import os
from pandas import DataFrame, read_csv

verifier_options = ['yes', 'y', 'true', 'no', 'n', 'false']
yes_option = verifier_options[:4]
no_option = verifier_options[4:]

directory_path = os.path.dirname(os.path.realpath(__file__))

bill_file_name = f'fr_data/fr_bill_data.csv'
bill_file_path = os.path.join(directory_path, bill_file_name)

def format_input(val: str) -> str:
    val = val.replace(' ', '').lower()
    if ',' in val: 
        return val.split(',')
    return val

def exception_catch(input_val: str, options: list):

    proper_input = False
    while proper_input == False: 
        
        user_input = input(input_val)
        cleaned_input = format_input(user_input)
        if cleaned_input not in verifier_options:
            print('Please select from this list: %s' % verifier_options)
        else: 
            break
    return cleaned_input

def update_bill_value(bill_list: list):

    if os.path.exists(bill_file_path):
        dataframe: DataFrame = read_csv(bill_file_path)
        data: dict = dataframe.to_dict(orient='records')
    else: 
        data = {}

    for bill in bill_list: 

        new_value = input(f'How much is {bill} monthly? ')
        formatted_new_value = format_input(new_value)
        data[bill] = formatted_new_value

    bill_val_str = [f'- {bill_name}: {bill_value}$' for bill_name, bill_value in data.items()]
    bill_val_str = '\n'.join(bill_val_str)

    verifier = f'All current bills: \n{bill_val_str}\n Would you like to update? (y/n) '
    filtered_verifier = exception_catch(verifier, verifier_options)
    
    if filtered_verifier in no_option:
        return 
    for bill, value in data.items():
        update_verify = f'Would you like to update {bill} from {value}$? (y/n)'
        cleaned_update_verify = exception_catch(update_verify, verifier_options)
        if cleaned_update_verify in yes_option: 
            new_value = input(f'What is the new total of {bill}? ')
            cleaned_new_value = format_input(new_value)
            data[bill] = cleaned_new_value
    df_data = [data]
    new_dataframe = DataFrame(df_data)
    new_dataframe.to_csv(bill_file_path, index=False)

def update_bill_info():

    current_bills = input('List all bills, seperate each value by a comma: ')
    formatted_bills = format_input(current_bills)

    bill_check_str = f'- {formatted_bills}' 
    if type(formatted_bills) == list:
        bill_check_str = '- ' + '\n- '.join(formatted_bills)

    verifier = input(f'Are these all your current bills (y/n): \n{bill_check_str}\n')
    formatted_verifier = format_input(verifier)

    if formatted_verifier in yes_option:
        pass
    if formatted_verifier in no_option:
        removal_list = input('Please list all bills you want to remove. Seperate by commas.')

    update_bill_value(formatted_bills)

@click.command()
@click.option('--update', default='World', help='Updates exisiting data.')
def update_initial_data():

    """
    -- current income 
        -- estimated monthly, hourly, or yearly
    -- current debts
        -- interest on debts 
    -- bills
        -- all bills, seperated by comma? 
    
    """
    return 


if __name__ == '__main__':

    saved_user_data_file_path = directory_path + '/fr_data/'
    os.makedirs(saved_user_data_file_path, exist_ok=True)

    update_bill_info()
