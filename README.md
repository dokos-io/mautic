## Mautic Integration
Version: 1.0.0 beta

#### Installation

This application requires (Frappe)[https://github.com/frappe/frappe] and (ERPNext)[https://github.com/frappe/erpnext] v10.0.0 or higher.

1. `bench get-app mautic_integration https://github.com/DOKOS-IO/mautic_integration/`
2. `bench install-app mautic_integration`
3. `bench restart && bench migrate`

The application is scheduled to run once a day by default.
Verify that your scheduler is enabled (`bench enable-scheduler`).

Your ERPNext and Mautic sites need to have SSL certificates.

#### Features

##### Mautic Company to ERPNext Customer

*Basic Mapping*  
|Source|Flow|Target|
|--|--|--|
|Company Name| --> |Customer Name|
|Company Website| --> |Customer Website|

*Post Processing*  
If no address called "*CustomerName*-Mautic" exists, a new one is created.
Else the existing one is updated.

##### Mautic Contact to ERPNext Contact

*Basic Mapping*  
|Source|Flow|Target|
|--|--|--|
|Contact First Name| --> |Contact First Name|
|Contact Last Name| --> |Contact Last Name|
|Contact Email| --> |Contact Email ID|

*Post Processing*  
If the contact in Mautic is linked to an organization, the contact in ERPNext is linked to the corresponding Customer or Lead (*company_name* field).
Else a new Lead is created and linked to the contact.

##### ERPNext Customer to Mautic Companies

*Basic Mapping*  
|Source|Flow|Target|
|--|--|--|
|Customer Name| --> |Company Name|
|Customer Website| --> |Company Website|

##### ERPNext Contact to Mautic Contact

*Basic Mapping*  
|Source|Flow|Target|
|--|--|--|
|Contact First Name| --> |Contact First Name|
|Contact Last Name| --> |Contact Last Name|
|Contact Email ID| --> |Contact Email|

#### License
GPLv3
