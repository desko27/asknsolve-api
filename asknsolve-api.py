#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   ALPHA
#  - Created:   2015/02/21
# ----------------------------------------------------------------------------
# Ask&Solve API Server.

from flask import Flask, request, jsonify
from flask.views import MethodView
from hashids import Hashids
from sqlsoup import SQLSoup

# custom classes
from class_Config import Config, conf_exists

# ---------------------------------------------------------------------------
# globals
# ---------------------------------------------------------------------------
conf = Config('conf.ini')
app = Flask(__name__)
hashids = Hashids(conf.hash.salt)
db = SQLSoup('mysql://%s:%s@%s/%s?charset=utf8'
    % ( conf.db.user, conf.db.password, conf.db.host, conf.db.database ))

# ---------------------------------------------------------------------------
# functions
# ---------------------------------------------------------------------------
def row2dict(row, hash = True):
    d = row.__dict__
    d.pop('_sa_instance_state')
    if hash and d.has_key('id'): d['hash'] = id2hash(d['id'])
    return d
    
def db2json(rows, hash = True):
    json_results = []
    if type(rows) is not list: rows = [rows]
    for row in rows: json_results.append(row2dict(row, hash))
    return jsonify(items = json_results)

# hash id converters
id2hash = lambda id: hashids.encode(id, int(conf.hash.expander))
hash2id = lambda hash: hashids.decode(hash)[0]

# ---------------------------------------------------------------------------
# custom exceptions
# ---------------------------------------------------------------------------
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code = None, payload = None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# ---------------------------------------------------------------------------
# error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(Exception)
def restful_exception_handler(e):
    db.rollback()
    return jsonify(message = e.message), 500

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify(message = 'Not Found'), 404

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# ---------------------------------------------------------------------------
# views
# ---------------------------------------------------------------------------
class TicketAPI(MethodView):

    def get(self, hash):
    
        if hash is None:
            # return a list of tickets
            return db2json(db.tickets.all())
        else:
            # expose a single ticket
            return db2json(db.tickets.filter_by(id = hash2id(hash)).one())
            
    def post(self):
        
        # create a new ticket
        db.tickets.insert(
            owner_id =      request.json.get('owner_id'),
            title =         request.json.get('title'),
            description =   request.json.get('description'),
            priority =      request.json.get('priority')
        )   
        db.commit()
        return jsonify(request.json), 201

    def delete(self, hash):
    
        # delete a single ticket
        db.delete(db.tickets.filter_by(id = hash2id(hash)).one())
        db.commit()
        return jsonify(result = True)

    def put(self, hash):
    
        # update a single ticket
        query = db.tickets.filter_by(id = hash2id(hash))
        ticket = query.one()
        
        query.update({
            'owner_id':     request.json.get('owner_id', ticket.id),
            'title':        request.json.get('title', ticket.title),
            'description':  request.json.get('description', ticket.description),
            'priority':     request.json.get('priority', ticket.priority)
        })
        db.commit()
        return jsonify(result = True)

# ---------------------------------------------------------------------------
# routing rules
# ---------------------------------------------------------------------------
ticket_view = TicketAPI.as_view('ticket_api')
app.add_url_rule('/tickets', defaults = {'hash': None}, view_func = ticket_view, methods = ['GET'])
app.add_url_rule('/tickets', view_func = ticket_view, methods = ['POST'])
app.add_url_rule('/tickets/<hash>', view_func = ticket_view, methods = ['GET', 'PUT', 'DELETE'])

# ---------------------------------------------------------------------------
# program
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    
    # run server
    app.run(debug = True)
    # app.run()
