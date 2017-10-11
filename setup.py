#!/usr/bin/python3
# -*- coding: utf-8 -*-

from distutils.core import setup

datas=[('share/applications', ['data/sdj.desktop']),
('share/sdj/glades', ['src/glades/about.glade']),     
('share/sdj/glades', ['src/glades/domain_err1.glade']),
('share/sdj/glades', ['src/glades/domain.glade']),             
('share/sdj/glades', ['src/glades/domain_success.glade']),
('share/sdj/glades', ['src/glades/domain_add.glade']),   
('share/sdj/glades', ['src/glades/domain_invalid_ip.glade']),  
('share/sdj/glades', ['src/glades/domain_update_host.glade']) ]

setup(
    name='SimpleDomainJoiner',
    version='0.70',
    url = 'https://github.com/PardusGenc/Simple-Domain-Joiner',
    license = 'GPL',
    author = 'Ali Orhun Akkirman',
    author_email = 'aoakkirman@gmail.com',
    description = 'Simple Domain Joiner offers a very simple graphical user interface to change the domain of the system.',
    packages = ['src'],
    keywords = ['sdj'],
    scripts=['script/sdj'],
    data_files = datas
)


