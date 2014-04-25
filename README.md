delicious_import
================

#### This script allow to import your bookmarks from html files to [Delicios.com](https://delicious.com)

    delicious_import.py

<a href="https://www.flickr.com/photos/dmgl/14005344475" title="delicious_import.py by Dmitry Milovidov, on Flickr"><img src="https://farm3.staticflickr.com/2933/14005344475_a7fd527890_o.png" width="762" height="327" alt="delicious_import.py"></a>

It's a very slowly importer! Alternative method is to import by hand. Script use delicious.py client to make api requests. It doesn't work with json (interesting export from Firefox with tags) yet. Maybe, in future. If you know another solution to import links with tags to delicios or parse export file from Delicios and add into Firefox with tags, please, let me know.

I found this repo ([chromalicious](https://github.com/mpenkov/chromalicious)) when already wrote my own.

Required:

    sudo pip install pydelicios
    sudo pip install lxml

Usage:

    $ ./delicios_import file1.html file2.html ...

It makes a huge output to console. If there's any problem while importing a link, it would be colored red, just like the one on screenshot.

You can write output to file using standart methods (for example if have more than 1000 links to import).

    $ ./delicious_import.py >console_log

It also generate html-report file (not good realization, but pretty and useful).

    report-file1.html

    Structure of *report-file1.html* is:
    
        Total links found in file:
        Already added to Delicios:
        Add at this time:
        Not correct link:
        Unnamed link:

Needs some refactoring, I know.

UPD:

If you see an error that looks like:

    xml.etree.ElementTree.ParseError: no element found: line 1, column 38

It will skip any links that have already been imported. This seems to be an intermittent error in pydelicious.
