# CKAN
As a data management system designed to help organizations and communities publish, share, and discover datasets, CKAN acts as a platform to manage large-scale data repositories, making it easier for users to find and access structured data. CKAN allows a creation of data portals, mainly used by government agencies to allow public access to various data (open data concept).

CKAN itself is pretty robust, with dataset publishing, discovering and interactive cabalities, with additional extensions allowing for an increase in its functionality based on specific needs.

CKAN code architecture

![download](https://github.com/user-attachments/assets/d0629712-5279-4847-9e64-f720361000f1)

CKAN's architecture is devided into components that interact with eachother. Each component's functionality can be expanded with plugins without changing the core CKAN.

CKAN itself is written in Pylons (Python's web framework - now turned into Pyramid). It relies on ``PyUtilib Component Architecture`` to declare a series of interfaces and extension points that then are used by plug-ins to hook in. It also implements a series of `Jinja2` extension (notably ``CKAN_EXTENDS``) that allows easily template inheritance between CKAN and connected plug-ins.

## Models

CKAN primarly stores data in relational databases (most commonly used is PostgreSQL) as CKAN focuses on structured, interrelated data management.

### 1. Metadata Storage in Databases

CKAN stores metadata related to datasets, users, organizations, recources, etc. as tables in relational database. Each of these tables has relationship between them, like ``resource`` table being related to ``package`` table (representing datasets) by foreign key (``package_id``).

![resource-package-relation](https://github.com/user-attachments/assets/141b8b48-5714-439c-bfb0-7d559335b485)

### 2. Storing files and Resources

CKAN can either store files directly or it can link to external files or data sources.

* **File-Based Storage**: When a file (e.g., a CSV or JSON file) is uploaded, CKAN can store the file locally on the server's filesystem or in a cloud storage. The file’s metadata (such as filename, format, and size) is stored in the resource table in the database. 
* **External URLs**: If the resource is a link to an external file (e.g., a dataset hosted on a different server or in the cloud), CKAN stores the URL in the database rather than the file itself.

### 3. DataStore Plugin

By default CKAN stores tabular data (like CSV) as raw files without the ability to query through them, meaning that users would have to download the files and analyse them offline. With additional plugins, like **DataStore**, it becomes possible to store the actual structured, queryable data from these files, alongside the metadata.

DataStore plugin is usually complimented by an additional **Datapusher** plugin. The Datapusher automatically downloads any tabular data files like CSV or Excel from a CKAN site's resources when they are added to the CKAN site, parses them to pull out the actual data, then uses the DataStore API to push the data into the CKAN site's DataStore.

While it's still possible to use DataStore plugin without Datapusher, the data extraction would have to be manual with ``ckan datastore push`` command each time a file uploaded.

Data flow with DataStore plugin

![ckan-datastore-flow](https://github.com/user-attachments/assets/e79aa22c-6968-4e81-8eff-b20ffc540e4d)

### 4. Search Index (Solr)

CKAN integrates with a search engine (usually Solr) to expand its search capabilities across datasets.

Solr is built on top of Apache Lucene, a full-text search library. Solr's indexing makes searches much faster by converting raw data into a format optimized for quick searching. With Solr's multithreading, batch processing capabilities the dataset searches become faster.

![ckan-solr-flow](https://github.com/user-attachments/assets/f0ef99d0-cde5-43db-8c59-3c466412e5e6)

## Logic

### 1. Actions

In CKAN, actions are the core operations or tasks that can be performed through its API and user interface. They correspond to the various operations related to datasets, groups, organizations, users, and other entities managed within the CKAN system. An action request is validated, executed and a response is returned everytime it is called.

Every CKAN's plugin is called through the CKAN's Action API endpoint ``.../api/3/action/{action_name}``. Some actions examples using CKAN API:

1. Create Dataset (``package_create``)
2. Add Resources (``resource_create``)
3. Apply Tags (``tag_create`` and ``tag_show``)
4. Allow Access (``user_role_create``)

CKAN's [API reference](https://docs.ckan.org/en/2.9/api/#action-api-reference)

### 2. Authorization

CKAN uses a **role-based access control** model, where users are assigned roles within organizations or datasets, and these roles determine what actions they can perform.

CKAN primarly uses **Flask-Auth**, **Flask-Login**, and **Pylons** (older CKAN version) authorization mechanisms for authentication or authorization.

**Flask-Login** - a Flask extension used in CKAN to manage user sessions and authorization within CKAN's web interface. This extensions itself does not handle permissions beyond ``logged in or not``, and account registration and recovery.

It can also integrate with third-party authentication providers through plugins. For enterprise deployments, CKAN supports LDAP, SAML2, OAuth2, and OpenID Connect through plugins. These allow log in using corporate credentials instead of CKAN's internal user database:

* ``ckanext-ldap``: allows authentication via LDAP (e.g., Active Directory).
* ``ckanext-saml2``: integrates CKAN with SAML2-based identity providers (e.g., Okta, Azure AD).
* ``ckanext-oauth2``: supports OAuth2 authentication (Google, GitHub, etc.).
* ``ckanext-oidc``: supports OpenID Connect for authentication.

In addition to Flask-Login, CKAN has its own **IAuthFunctions** interface that controls who can perform specific actions. With this it's possible to override CKAN's default permission rules:

```python
import ckan.plugins as p
import ckan.plugins.toolkit as tk

class CustomAuthPlugin(p.SingletonPlugin):
    # Tell CKAN that this plugin implements IAuthFunctions
    p.implements(p.IAuthFunctions)

    # Define custom authorization functions
    def get_auth_functions(self):
        return {
            'package_create': custom_package_create
        }
```

When using CKAN's API, authentication is done through API tokens (API keys are **not** recommended).

## API

CKAN utilizes RESTful API that allows interaction with CKAN programmatically. Usually CKAN's API will consists of three parts:

* Action API – The main API for managing datasets, users, and organizations.
* Datastore API (plugin) – Used for querying structured data in CKAN's Datastore.
* Search API (plugin) – Used for searching datasets, organizations, and resources.

Additional CKAN's API explanation and examples: [api-guide](https://github.com/KlauMack/ckan/blob/main/doc/api/api-guide.rst)

### Extensions

CKAN extensions are used to extend or enhance CKAN's core functionality. They allow you to add new features or modify existing behavior without changing the core CKAN code.

Custom extensions are created by hooking into CKAN's Interface. CKAN provides several interfaces and hooks that allow developers to interact with its core functions:

1. `IDatasetForm` - used to modify or extend the dataset form fields.
2. `IDatasetView` - allows to customize the way datasets are viewed on the CKAN site.
3. `IPlugin` - allows you to define your own CKAN plugin and hook into the system to add new features or extend existing ones.
4. `IConfigurer` - allows updating CKAN's configurations.
5. `IValidator` - used to modify default data validation.


Structure of an Extension:

* A Python package with custom logic.
* Template files for changing the front-end.
* Configuration to integrate the extension with CKAN.
* Static files like CSS/JS for custom UI components.

## Views

CKAN views are created form resources, were raw data (CSV or JSON) is turned into charts, tables, maps, etc.

Types of CKAN views:
* **Data Table**: Displays tabular data from CSV/Excel.	Viewing structured data without downloading.
* **Graph** (Chart): Generates bar, line, or pie charts from numeric data.	Visualizing trends in dataset values.
* **Map** (GeoView): Displays geographic data from GeoJSON/KML.	Showing locations, boundaries, or geospatial data.
* **Image View**: Displays image files (JPEG, PNG, GIF).	Viewing satellite images or scanned documents.
* **Text View**: Renders plain text or JSON content.	Displaying logs, reports, or API responses.
* **PDF View**: Shows PDF files directly in the browser.	Viewing research papers or government reports.

### Viewability detection

When a resource is uploaded, CKAN automatically detects if view is possible. In addition, a manual view creation is also possible through web interface.

CKAN determines whether a view is possible from a resource based on a combination of file format detection, metadata, and available plugins:

1. CKAN checks resource's file extension (``.csv``, ``.json``, ``.geojson``, ``.pdf``) and MIME type (``text/csv``, ``application/json``, ``image/png``) to create the view. For example, **data.csv** file with MIME type **text/csv** is recognized as a tabular dataset, so a Data Table view can be created.
2. Additional plugins expand the view creation process:
   * ``ckanext-geoview`` → Enables GeoJSON & KML views.
   * ``ckanext-d3charts`` → Enables graph views (charts).
  
Available views based on file type:
| File Type  | View |
| ------------- | ------------- |
| CSV / Excel | Data Table |
| JSON / JSONL | Text View |
| GeoJSON / KML | Map View |
| PNG / JPG / GIF | Image Viewer |
| PDF | PDF Viewer |

## Plugins

Alongside DataStore plugin, here are additional most commonly or natively used plugins:

* ``ckanext-harvest``: Enables the harvesting of datasets from external sources. Allows access to data in other CKAN servers.
* ``ckanext-spatial``: Adds support for spatial (geospatial) data and metadata standards. Enables CKAN to handle and serve geographic datasets (such as shapefiles, GeoJSON, KML, etc.).
* ``ckanext-saml``: Integrates SAML-based Single Sign-On (SSO) - allows authentication with external credentials. 
* ``ckanext-google-analytics``: Provides integration with Google Analytics for tracking usage statistics on the CKAN portal.
* ``ckanext-validation``: Provides ability to validate tabular data and integrate validation reports to the CKAN interface.
* ``ckanext-multilingual``: Allows CKAN to handle content in multiple languages by enabling translations of dataset metadata. Works together with Solr for searching as well.

