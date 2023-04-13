#!/bin/sh

startme() {
    pushd flask-sp/sp-wsgi > /dev/null
    if [ ! -f sp_conf.py ] ; then
        cp sp_conf.py.example sp_conf.py
    fi
    if [ ! -f service_conf.py ] ; then
        cp service_conf.py.example service_conf.py
    fi
    ../../tools/make_metadata.py sp_conf > sp.xml
    ./sp.py sp_conf &
    popd > /dev/null

    pushd flask-idp/idp2 > /dev/null
    if [ ! -f idp_conf.py ] ; then
        cp idp_conf.py.example idp_conf.py
    fi
    ../../tools/make_metadata.py idp_conf > idp.xml
    ./idp.py idp_conf &
    popd > /dev/null
}

stopme() {
    pkill -f "sp.py"
    pkill -f "idp.py"
}

case "$1" in
    start)   startme ;;
    stop)    stopme ;;
    restart) stopme; startme ;;
    *) echo "usage: $0 start|stop|restart" >&2
       exit 1
       ;;
esac
