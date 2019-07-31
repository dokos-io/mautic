## Mautic

#### Installation

This application requires [Frappe](https://github.com/frappe/frappe) and [ERPNext](https://github.com/frappe/erpnext) v10.0.0 or higher.

1. `bench get-app mautic https://github.com/DOKOS-IO/mautic/`
2. `bench install-app mautic`
3. `bench restart && bench migrate`

#### Mautic configuration

In Mautic:
* in the Configuration > API Settings, enable API and HTTP Basic Auth then _Save & Close_
* in the API Credentials, create new API credentials for OAuth2:
  * enter a name to identify your ERPNext instance
  * enter the redirect URI like this `{https://your.erpnext.site}?cmd=mautic.mautic.doctype.mautic_settings.mautic_settings.mautic_callback&grant_type=authorization_code&response_type=code,`:
    * make sure to use the correct protocol (`http` or `https`) given your frappe hostname and SSL configuration
    * (of course) adapt the domain name
    * do not leave any trailing `/` at the end of your domain name
    * you can add more URI by separating them by a `,`
    * make sure to always have a `,` at the end or Mautic will not use the URI :warning:
* _Save & Close_


#### ERPNext Mautic configuration

In ERPNext:
* enable Mautic
* add your API credentials:
  * enter the link to your Mautic instance, **without any trailing slash**: `https://your.mautic.site`
  * copy the "_Public Key_" from Mautic to the _Client ID_
  * copy the "_Secret Key_" from Mautic to the _Client Secret_
* save
* click on "Allow Mautic Access" (you should be redirected to your Mautic instance)
  * login as administrator
  * when prompted, accept the application to connect to Mautic

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
