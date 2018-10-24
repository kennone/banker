#!/usr/bin/env python
####################################
# Bank Statement Parser
# Author: Ken O'Neill
# Date: 24th Oct 2018
# Last Revision: 10th May 2018
# Version: v1.01
####################################

import logging
import argparse
import time
import os
import sys
import csv
from argparse import RawDescriptionHelpFormatter


# Class for storing transaction information
class Transaction:
    def __init__(self):
        self.date = 0
        self.type = ""
        self.description = ""
        self.value = 0.0
        self.balance = 0.0
        self.account_name = ""
        self.account_number = ""

    def __repr__(self):
        return repr((self.date, self.type, self.description, self.value,
                     self.balance, self.account_name, self.account_number))
            
    def __str__(self):
        output_string = (
            "Date: {0}\n"
            "Type: {1}\n"
            "Description: {2}\n"
            "Value: {3}\n"
            "Balance: {4}\n"
            "Account Name: {5}\n"
            "Account Number: {6}\n").format(
                self.date, self.type, self.description, self.value,
                self.balance, self.account_name, self.account_number)
        
        return str(output_string)


def main():
    startup_message()
    load_transactions()


def startup_message():
    # startup_message message
    logger.info("")
    logger.info('------------------------------------------------------------')
    logger.info('#                                                       ')
    logger.info('#       Banker v1.00                                    ')
    logger.info('#                                                       ')
    logger.info('#       Script for parsing bank statements and updating ')
    logger.info('#       account spreadsheet                             ')
    logger.info('#                                                       ')
    logger.info('------------------------------------------------------------')
    logger.info("")
    time.sleep(3)


def load_transactions():

    if("csv" not in args.transactions):
        logger.error("You must specify a transaction CSV file.")
        logger.error("Exiting script. Goodbye")
        sys.exit(0)
    else:

        logger.info("Loading transactions from {0}".format(args.transactions))

        try:
            with open(args.transactions, 'rb') as f:
                reader = csv.reader(f)
                raw_transaction_list = list(reader)

                transaction_list = []

                # Load the transaction list lines into Transaction
                # class variables
                for csv_line in raw_transaction_list:
                    
                    logger.debug("CSV Line: {0}".format(csv_line))

                    if "Date" not in csv_line and len(csv_line) > 5:
                        new_transaction = Transaction()

                        logger.debug("CSV Line: {0} {1} {2} {3} {4} {5} {6}"
                                        .format(csv_line[0], csv_line[1],
                                                csv_line[2], csv_line[3],
                                                csv_line[4], csv_line[5],
                                                csv_line[6]))

                        new_transaction.date = csv_line[0]
                        new_transaction.type = csv_line[1]
                        new_transaction.description = csv_line[2]
                        new_transaction.value = csv_line[3]
                        new_transaction.balance = csv_line[4]
                        new_transaction.account_name = csv_line[5]
                        new_transaction.account_number = csv_line[6]
                        transaction_list.append(new_transaction)

                        print new_transaction                   
                
        except Exception as err:
            logger.error("Unable to load transaction list. Please check path "
                         "again. Error: {0}".format(err))
            logger.error("Exiting...")
            sys.exit(0)
    
if __name__ == '__main__':

    # Argument options
       
    example_text = ("Usage Examples:\n\n"
                    "python banker.py --transactions example.csv")   
    
    parser = argparse.ArgumentParser(
        description=example_text,
        formatter_class=RawDescriptionHelpFormatter)
    
    parser.add_argument("-debug", "--debug",
                        help="Enable the debug level logging",
                        action='store_true')
    parser.add_argument("-t", "--transactions", help="Camera IP address")
    args = parser.parse_args()

    # Logger Environment setup
    logger = logging.getLogger('Banker')

    if(args.debug):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    log_dir = 'logs/'
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    date = time.strftime("%d-%m-%Y_%H_%M_%S")

    # Write the log out to the screen

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    
    # Log file writing        
    log_name = 'banker_' + date + '.log'   
    ch = logging.FileHandler(log_dir + log_name)
    ch.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter('%(asctime)s - ' 
                                     '%(name)s - ' 
                                     '%(levelname)s - ' 
                                     '%(message)s')

    streamFormatter = logging.Formatter('%(asctime)s - '
                                        '%(name)s - ' 
                                        '%(levelname)s - ' 
                                        '%(message)s')

    ch.setFormatter(logFormatter)
    sh.setFormatter(streamFormatter)
    logger.addHandler(ch)
    logger.addHandler(sh)

    main()
