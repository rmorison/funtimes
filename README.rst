funtimes
========

prog03
******

It comes with a sqlitedb, but you can inject your own data. 

.. code-block:: bash
    
    $ mkvirtualenv funtimes
    $ pip install -r requirments.txt
    $ cd small
    $ ./manage.py inject_data --randomize
    $ ./manage.py runserver


    Now You'll want to navigate to /tinyFeed.json
    Login at /admin/
    Find login information at /tinyFeed.json
    
