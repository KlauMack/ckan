=========
Sysadmin guide
=========

Sysadmins have full access to user, organization and dataset information. They can edit, delete or move users or datasets through organizations.

---------------------
Managing organizations and datasets
---------------------
Some Sysadmim operations include:

* deleting or adding users to an organization
* changing user’s role in the organization
* deleting the organization editing its description
* editing, updating or deleting a dataset
* move dataset to another organization

Sysadmins can use these operations either by visiting organization's home page or the datasets page.

---------------------
Permanently deleting datasets, organizations and groups
---------------------
A dataset, organization or group which has been deleted is not permanently removed from CKAN; it is simply marked
as ‘deleted’ and will no longer show up in search. The assigned URL cannot be re-used for a new entity.

To permanently delete (``purge``) an entity:

* Navigate to the dataset’s “Edit” page, and delete it.
* Visit ``http://<my-ckan-url>/ckan-admin/trash/``.
This page shows all deleted datasets, organizations and groups and allows you to delete them permanently.

---------------------
Managing users
---------------------
To find a user’s profile, go to ``http://<my-ckan-url>/user/``.

You can search by any part of the user profile, including their e-mail address. For non-sysadmin users, the search on this page will only match public parts of the profile, so
they cannot search by e-mail address.

On their user profile, you will see a ``Manage`` button. You can delete the user
or change any of its settings, including their name and password.

---------------------
Site customization
---------------------
Some simple customizations for the CKAN site are available at ``http://<my-ckan-url>/ckan-admin/config/``.

Here it's possible edit:

  {
    **Site title** - This title is used in the HTML <title> of pages served by CKAN (which may be displayed on your browser’s title bar).
    **Style**
    **Site tag line**
    **Site tag logo** - a URL for the site logo, used at the head of every page of CKAN.
    **About** - text that appears on the “about” page, ``http://<my-ckan-url>/about``. Can use **Markdown** here. If it is left empty, a standard text describing CKAN will appear.
    **Intro text** - this text appears on the home page of your site.
    **Custom CSS** - For simple style changes, can add CSS code here which will be added to the <head> of every page.
  }
