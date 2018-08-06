## Mautic

#### Installation

This application requires [Frappe](https://github.com/frappe/frappe) and [ERPNext](https://github.com/frappe/erpnext) v10.0.0 or higher.

1. `bench get-app mautic https://github.com/DOKOS-IO/mautic/`
2. `bench install-app mautic`
3. `bench restart && bench migrate`

In Mautic, create new API credentials for OAuth2.  
In the redirect URI section add the following URI:
`{Your Site}?cmd=mautic.mautic.doctype.mautic_settings.mautic_settings.mautic_callback`

In ERPNext, add your API credentials, the link to your Mautic instance, save and click on "Allow Mautic Access"  

The application is scheduled to run hourly by default.
Verify that your scheduler is enabled (`bench enable-scheduler`).

Your ERPNext and Mautic sites need to have SSL certificates.

#### Features

##### Mautic Segment to ERPNext "Mautic Segment"

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|Name| --> |Segment Name|
|Description| --> |Segment Description|

##### Mautic Company to ERPNext Customer

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|Company Name| --> |Customer Name|
|Company Website| --> |Customer Website|

*Post Processing*  

If no address called "*CustomerName*-Mautic" exists, a new one is created.  
Else the existing one is updated.

##### Mautic Contact to ERPNext Contact

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|Contact First Name| --> |Contact First Name|
|Contact Last Name| --> |Contact Last Name|
|Contact Email| --> |Contact Email ID|
|Contact Segment| --> |Contact Segment| (Only one segment is synchronized for now)

*Post Processing*  

If the contact in Mautic is linked to an organization, the contact in ERPNext is linked to the corresponding Customer or Lead (*company_name* field).  
Else a new Lead is created and linked to the contact.

##### ERPNext Customer to Mautic Companies

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|Customer Name| --> |Company Name|
|Customer Website| --> |Company Website|

##### ERPNext Contact to Mautic Contact

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|Contact Salutation| --> |Contact Title|
|Contact First Name| --> |Contact First Name|
|Contact Last Name| --> |Contact Last Name|
|Contact Email ID| --> |Contact Email|
|Contact Phone| --> |Contact Phone|
|Contact Mobile No| --> |Contact Mobile|
|Contact Linked Customer| --> |Contact Company|

*Pre Processing*

If the contact is not linked to a customer or a lead, it is not sent to Mautic.
If the contact's email address is "Guest", it is not sent to Mautic.

#### License
GPLv3
