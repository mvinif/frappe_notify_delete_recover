# Recover deleted documents in Frappe/ERPNext

This method keep monitoring deleted documents and once trigged a recover page will be sent to team email with a notification

## Usage
To ideal usage of this method, firstly we need :

 - Setup a default outgoing email account in Frappe configuration
 - Configure hook.py file
 - Insert main.py in frappe app
 - Copy the WWW folder to frappe app
 
After the configuration the method runs automatically once someone made a change
 
 ## Functionality
 Each deleted trigger the function, which verify if the doctype is in monitored list, once validated, the method send the e-mail notification

## Pending
 - Document filter list
 - Multiples deletes at once
 - Multiples recovers at once
