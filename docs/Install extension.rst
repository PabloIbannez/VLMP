Install Extension
=================

There are two main ways to install and work with new extensions: **Development Mode** and **Production Mode**.

1. **Development Mode**:
   
   During the development phase, to avoid reinstalling VLMP after each change, it is recommended to work on a local copy of VLMP that contains the modules being developed. This allows you to continuously edit the modules until they are fully implemented. To work in this mode, when initializing VLMP, you should use the following command:

   .. code-block:: python

      vlmp = VLMP.VLMP("localFolder")

   In this way, VLMP will be initialized using the version located in `"localFolder"` instead of the installed version. As a result, any changes made to the modules in this folder will be effective immediately without the need to reinstall VLMP. Additionally, if the folder `"localFolder"` does not already exist, this command will create a local copy of VLMP in that folder.

2. **Production Mode**:

   Once the extension has been fully developed and tested, it can be included in the installed version of VLMP on your computer. To do this, navigate to the VLMP folder and execute the following command:

   .. code-block:: bash

      python -m pip install .

   This command will install the current version of VLMP along with your extension into your system’s environment, making it ready for production use.
