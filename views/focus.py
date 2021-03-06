from flask import Blueprint,redirect,url_for,abort
from flask.ext.login import current_user
from lolipop.models import Node
from _helpers import redis,cache

bp = Blueprint("focus",__name__)

def nodes_id():
    if current_user is not None and current_user.is_authenticated():
        user_key = 'user-nodes/%d' % current_user.id
        return redis.smembers(user_key)

def getNodes():
    nodes = None
    uids = nodes_id()
    if uids:
        nodes = Node.query.filter(Node.id.in_(uids))
    return nodes

@bp.route('/add/<int:node_id>')
def add(node_id):
    if current_user is not None and current_user.is_authenticated():
        user_key = 'user-nodes/%d' % current_user.id
        p = redis.pipeline()
        p.sadd(user_key,node_id)
        p.execute()
    cache.clear()
    return redirect(url_for('node.nodes'))

@bp.route('/remove/<int:node_id>')
def remove(node_id):
    if current_user is not None and current_user.is_autheneticated():
        user_key = 'user-nodes/%d' % current_user.id
        p = redis.pipeline()
        p.srem(user_key,node_id)
        p.execute()
    cache.clear()
    return redirect(url_for('node.nodes'))

