=========
Extensions
=========

A CKAN extension is a Python package that modifies or extends CKAN. Each extension contains one or more plugins that must be added to your CKAN config file to activate the extension’s features.

---------------------
Creating a new extension
---------------------
You can etiher use a ``cookiecutter`` command or CLI command ``ckan generate extension`` to create an “empty” extension from a template. For whichever method is chosen, the first step is to activate the CKAN virtual environment::

    . /usr/lib/ckan/default/bin/activate

Create a new extension from the template:

* Cookiecutter::

    cookiecutter ckan/contrib/cookiecutter/ckan_extension/

* CLI command::

    ckan generate extension

After running the command, a new CKAN extension's project directory will be created::

    ckanext-iauthfunctions/
      ckanext/
          __init__.py
          iauthfunctions/
              __init__.py
      ckanext_iauthfunctions.egg-info/
      setup.py

* ``setup.py``:  the setup script for the project. Used to install the project into CKAN's virutal environment. Edit this file, once you've created the extension:

.. code-block:: python

    entry_points='''
        [ckan.plugins]
        example_iauthfunctions=ckanext.iauthfunctions.plugin:ExampleIAuthFunctionsPlugin
    ''',

And install it after::

    . /usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/ckanext-iauthfunctions
    python setup.py develop


Custom extension example:
******
Here's an example of a custom ``ExampleIAuthFunctionsPlugin`` extension, that allows users only in a ``curator`` group to be able to create new groups:

.. code-block:: python

    # ckanext-iauthfunctions/ckanext/iauthfunctions/plugin.py. 
    # encoding: utf-8
    from ckan.types import AuthResult, Context, ContextValidator, DataDict
    from typing import Optional, cast
    import ckan.plugins as plugins
    import ckan.plugins.toolkit as toolkit

    def group_create(context: Context, data_dict: Optional[DataDict] = None) -> AuthResult:
      # Get the user name of the logged-in user.
      user_name: str = context['user']

      # Get a list of the members of the 'curators' group.
      try:
          members = toolkit.get_action('member_list')(
              {},
              {'id': 'curators', 'object_type': 'user'})
      except toolkit.ObjectNotFound:
          # The curators group doesn't exist.
            return {'success': False, 'msg': "The curators groups doesn't exist, so only sysadmins are authorized to create groups."}

      # 'members' is a list of (user_id, object_type, capacity) tuples, we're only interested in the user_ids.
      member_ids = [member_tuple[0] for member_tuple in members]

      # We have the logged-in user's user name, get their user id.
      convert_user_name_or_id_to_id = cast(
        ContextValidator,
        toolkit.get_converter('convert_user_name_or_id_to_id'))

      try:
          user_id = convert_user_name_or_id_to_id(user_name, context)
        except toolkit.Invalid:
          # The user doesn't exist (e.g. they're not logged-in).
          return {'success': False,
              'msg': 'You must be logged-in as a member of the curators group to create new groups.'}

      # Finally, we can test whether the user is a member of the curators group.
      if user_id in member_ids:
        return {'success': True}
      else:
        return {'success': False, 'msg': 'Only curators are allowed to create groups'}

    class ExampleIAuthFunctionsPlugin(plugins.SingletonPlugin):
        plugins.implements(plugins.IAuthFunctions)

      def get_auth_functions(self) -> dict[str, AuthFunction]:
        return {'group_create': group_create}

Code explanation:
*****
* ``context``: the context parameter of the ``group_create()`` function is a dictionary that CKAN passes to all authorization and action functions containing some computed variables. This is where the function gets the logged-in user from.
* ``data_dict``: this parameter contains any data posted by the user to CKAN (any fields they’ve completed in a web form they’re submitting or any JSON fields they’ve posted to the API).

The toolkit’s ``get_action()`` function returns a CKAN action function. The action functions available to extensions are the same functions that CKAN uses internally to carry out actions when users make requests to the web interface
or API. Calling ``member_list()`` in this way is equivalent to posting the same data dict to the ``/api/3/action/member_list`` API endpoint.

.. code-block:: python

    members = toolkit.get_action('member_list')(
        {},
        {'id': 'curators', 'object_type': 'user'})

The toolkit’s get_converter() function returns validator and converter functions from ``ckan.logic.converters`` for plugins to use. This is the same set of converter functions that CKAN’s action functions use to convert user-provided
data.

.. code-block:: python

    convert_user_name_or_id_to_id = cast(
        ContextValidator,
        toolkit.get_converter('convert_user_name_or_id_to_id'))
    user_id = convert_user_name_or_id_to_id(user_name, context)

Best practice to use exception handling in cases where a function could fail, like the site not having **curator** group to check members for.

.. code-block:: python

    try:
      members = toolkit.get_action('member_list')(
          {},
          {'id': 'curators', 'object_type': 'user'})
    except toolkit.ObjectNotFound:
      # The curators group doesn't exist.
      return {'success': False, 'msg': "The curators groups doesn't exist, so only sysadmins are authorized to create groups."}

Troubleshooting:
*****
**PluginNotFoundException**

* Check the extension name in the CKAN confi file - should match the extension name in the ``plugin.ini`` file.
• Check that ``python setup.py develop`` is run in the extension’s directory, with the CKAN virtual environment activated. The command needs to be run after every extension creation.

**ImportError**

* Check the path to the plugin class in the ``setup.py`` file.

