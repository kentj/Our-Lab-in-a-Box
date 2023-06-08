# Our-Lab-in-a-Box

The purpose of this project is to create a standardized access control platform for our labs based around Apache Guacamole and Keycloak.

Instructions for building a working environment can be found under "documentation" in the file Lab-in-a-Box Identity Management and Remote Access.adoc.  This is an AsciiDoc file which like Markdown, can be converted to various formats.

To download the script, use:

`curl -LO  https://raw.githubusercontent.com/kentj/Our-Lab-in-a-Box/main/scripts/configure_lab.py`

You can download the example config.ini file for the script using:

`curl -LO  https://raw.githubusercontent.com/kentj/Our-Lab-in-a-Box/main/scripts/lab_config.ini`

Make sure you check each entry in `lab_config.ini` to make sure it is sensible for your lab.

To build a PDF of the documentation, assuming you have docker installed, you can run:

`docker run -it -v <your directory where you've downloaded the *.adoc and image files>:/documents/ asciidoctor/docker-asciidoctor`

This will give you a command prompt inside the docker container running the ascii-doctor software.  Type:

`asciidoctor-pdf <name of file.adoc>`

and a file `<name of file.pdf>` will be generated.


