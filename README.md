Odoo on OpenShift
===================

This git repository helps you get up and running quickly an Odoo
installation on OpenShift.

Running on OpenShift
--------------------

Create an account at https://www.openshift.com

Install the RHC client tools if you have not already done so:
    
    sudo gem install rhc
    rhc setup

Create a python application

    rhc app create myodoo python-2.7 posgresql-9.2

Add this upstream repo

    cd myodoo
    git remote add upstream -m master https://github.com/dreispt/openshift-odoo-quickstart.git
    git pull -s recursive -X theirs upstream master

Then push the repo upstream

    git push

The database admin password will generated and displayed during the app deployment.

That's it. You can now check your application at:

    http://myodoo-$yournamespace.rhcloud.com

Database admin password
-----------------------

The database management admin password is randomly generated 
during the deployment. Look for a “Admin password” line of the
`git push` output. It is stored in the environment variable
`ODOO_ADMIN_PASSWD`.

Odoo Cron jobs
--------------

An Odoo cron worker will also be launched, 

Longpolling
-----------

Since gears can only expose a single port to the outside, 
this app won’t be able to also expose the longpolling port.

Attachment storage
------------------

By default Odoo saves attached files to disk. They will be saved 
inside the gear data directory, but since the space available is
limited, you would be better by configuring Odoo to save attachments
to the PostgreSQL database.

Odoo configuration
------------------

The app uses the `odoo.conf` configuration file at the root directory,
Feel free to tune it’s parameters, 

