=============================
QiitaNote
=============================

Description
-----------------------------

* Tech note for me by Sphinx.
* Available To search by `Alfred <http://www.alfredapp.com/>`_ + `Dash <http://kapeli.com/dash>`_.
* Available To associate with `Kobito <http://kobito.qiita.com/en>`_.

Requirement
-----------------------------

* Python
* pip
* virtualenv
* Pandoc
* Kobito.app
* Dash.app
* Alfred.app

::

 You have to integrate Dash with Alfred.

 http://www.alfredforum.com/topic/1919-dash-documentation-for-80-apis/?p=10275


Setup
-----------------------------

1. Clone repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

 $ git clone git@github.com:tell-k/qiitanote.git

2. Create virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

 $ cd qiitanote
 $ virtualenv venv
 $ source venv/bin/activate

3. Install python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

 (venv)$ pip install -r requirements.txt

4. Build sphinx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

 (venv)$ make html

 # You can check _build/html and Kobito.app and Dash.app.

License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* libs/sphinxcontrib_markdown.py Licensed under the `BSD License<https://gist.github.com/tk0miya/4336929>`_. 

Thanks to original author Takeshi Komiya.

