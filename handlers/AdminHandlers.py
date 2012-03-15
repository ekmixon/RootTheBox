'''
Created on Mar 13, 2012

@author: moloch
'''

#import logging

from uuid import uuid1
from tornado.web import RequestHandler #@UnresolvedImport
from libs.SecurityDecorators import * #@UnusedWildImport
from models import Team, Box, CrackMe

class AdminCreateHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
        self.get_functions = {
            'team': self.get_team, 
            'box': self.get_box, 
            'crackme': self.get_crackme, 
            'se': self.get_se
        }
        self.post_functions = {
            'team': self.post_team, 
            'box': self.post_box, 
            'crackme': self.post_crackme, 
            'se': self.post_se
        }
    
    @authorized('admin')
    @restrict_ip_address
    def get(self, *args, **kwargs):
        if args[0] in self.get_functions.keys():
            self.get_functions[args[0]]()
        else:
            self.render("admin/unkown_object.html", error=args[0])
    
    @authorized('admin')
    @restrict_ip_address
    def post(self, *args, **kwargs):
        if args[0] in self.post_functions.keys():
            self.post_functions[args[0]](*args, **kwargs)
        else:
            self.render("admin/unkown_object.html", error=args[0])

    def get_team(self):
        self.render("admin/create_team.html")
        
    def post_team(self, *args, **kwargs):
        try:
            team_name = self.get_argument('team_name')
            motto = self.get_argument('motto')
        except:
            self.reander("admin/error.html", errors = "Failed to create team")
        team = Team(
            team_name = unicode(team_name),
            motto = unicode(motto)
        )
        self.dbsession.add(team)
        self.dbsession.flush()
        self.render("admin/created.html", game_object='team')

    def get_box(self):
        self.render("admin/create_box.html")
    
    def post_box(self, *args, **kwargs):
        try:
            box_name = self.get_argument("box_name")
            ip_address = self.get_argument("ip_address")
            description = self.get_argument("description")
            root_key = self.get_argument("root_key")
            root_value = int(self.get_argument("root_value"))
            user_key = self.get_argument("user_key")
            user_value = int(self.get_argument("user_value"))
        except:
            self.render("admin/error.html", errors = "Failed to create box")
        box = Box(
            box_name = unicode(box_name),
            ip_address = unicode(ip_address),
            description = unicode(description),
            root_key = unicode(root_key),
            root_value = root_value,
            user_key = unicode(user_key),
            user_value = user_value
        )
        self.dbsession.add(box)
        self.dbsession.flush()
        self.render("created.html", game_object = "box")
        
    def get_crackme(self):
        self.render("admin/create_crackme.html")
    
    def post_crackme(self, *args, **kwargs):
        try:
            crack_me_name = self.get_argument('crack_me_name')
            description = self.get_argument('description')
            value = int(self.get_argument('value'))
            file_name = self.get_argument('file_name')
            file_uuid = uuid1()
            token = self.get_argument('token')
        except:
            self.render("admin/error.html", errors = "Failed to create crack me")
        crack_me = CrackMe(
            crack_me_name = unicode(crack_me_name),
            description = unicode(description),
            value = value,
            file_name = unicode(file_name),
            file_uuid = unicode(file_uuid),
            token = unicode(token)
        )
        self.dbsession.add(crack_me)
        self.dbsession.flush()
        self.render('admin/created.html', game_object = "crack me")
    
    def get_se(self):
        pass
        
    def post_se(self, *args, **kwargs):
        self.render("admin/create_se.html")

class AdminEditHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
    
    @authorized('admin')
    @restrict_ip_address
    def get(self, *args, **kwargs):
        print 'got', args
        print 'kw got', kwargs
    
    @authorized('admin')
    @restrict_ip_address
    def post(self, *args, **kwargs):
        pass