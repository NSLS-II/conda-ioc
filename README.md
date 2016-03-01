conda-ioc
=========

template for an isolated conda environment IOC
* with procServ/conserver config options
* with an example of hosting some EPICS PVs using pypvserver

Usage
=====

1. Edit `config`

    ```bash
    NAME=conda-ioc
    PORT=4001
    HOST=xf03id-srv1
    USER=softioc

    # conda-related options:
    CONDA_ENV=conda_ioc
    # CONDA_ROOT=$PWD/mc
    CONDA_ROOT=/tmp/ramdisk/condaioc
    PACKAGES=ophyd
    ```

    NAME should be set to the IOC name.
    PORT should be what `manage-iocs nextport` gives
    HOST should be updated depending on the machine it's being run on
    CONDA_ENV can be left as-is
    PACKAGES should be set to the conda packages required

2. Tweak `custom_install.sh` if any non-conda packages should be installed.
    This example installs both pcaspy and pypvserver from their respective git repositories.

3. Install/enable the IOC to automatically start on reboot
    ```bash
    sudo manage-iocs install conda-ioc
    sudo manage-iocs enable conda-ioc
    ```

4. Update conserver
    ```bash
    sudo update-iocs-cf
    sudo service conserver reload
    ```

5. Start the IOC
    ```bash
    sudo service softioc-conda-ioc start
    ```

6. Check its status
    ```bash
    manage-iocs status
    console conda-ioc
    ```
