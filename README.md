delicious_import
================

#### This script allow to import your bookmarks from html files to [Delicios.com](https://delicious.com)

    delicious_import.py

It's very slowly import! Alternative method was import by hand. Script use delicious.py client for make api requests. It doesnt work with json (interesting export from Firefox with tags) it, maybe, in future. If you know another solution to import links with tags to delicios or parse export file from Delicios and add in Firefox with tags, please, tell me about.

I found this repo ([chromalicious](https://github.com/mpenkov/chromalicious)) when already wrote my own.

Required:

    sudo pip install pydelicios
    sudo pip install lxml

Usage:

    $ ./delicios_import file1.html file2.html ...

Big output in console for faster go through the link, if have any problem with import link. Look likes:

[...]

    0541 -> this already added to Delicios: https://bugs.etersoft.ru/show_bug.cgi?id=6843 | Задача 6843 – Освоить
    сборку пакетов и написать документацию 0540 -> this already added to Delicios: http://toolserver.org/
    ~diberri/cgi-bin/html2wiki/index.cgi | html2wiki - Convert HTML text to wiki markup 0539 ->
    this already added to Delicios: http://wordmediawikiaddin.codeplex.com/ | Microsoft 
    Office Word Add-in For MediaWiki

[...]

You can write output in file standart methods (if have more than 1000 links to import).

    $ ./delicious_import.py >console_log

It also generate html-report file (not good realization, but pretty and useful).

    report+file1.html

    Structure of *report+file1.html* is:
    
        Total links found in file:
        Already added to Delicios:
        Add at this time:
        Not correct link:
        Unnamed link:

Needs some refactoring, i know.

UPD:

If you see an error that looks like:

    xml.etree.ElementTree.ParseError: no element found: line 1, column 38

It will skip any links that have already been imported. This seems to be an intermittent error in pydelicious.
