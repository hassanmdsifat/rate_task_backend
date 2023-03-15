#!/bin/sh
coverage run manage.py test
coverage html --omit="admin.py"