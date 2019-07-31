# install accountsservice files

    accountsservice/io.elementary.pantheon.AccountsService.xml /usr/share/dbus-1/interfaces/
    accountsservice/io.elementary.pantheon.AccountsService.policy /usr/share/polkit-1/actions/

# create symbolic link
    /usr/share/dbus-1/interfaces/io.elementary.pantheon.AccountsService.xml
    →
    /usr/share/accountsservice/interfaces/io.elementary.pantheon.AccountsService.xml

