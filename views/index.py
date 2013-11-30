from flask import Blueprint,render_template
from lolipop.models import Notice,Topic

bp = Blueprint('index',__name__)

@bp.route("/")
@bp.route("/index")
def index():
    notices = Notice.query.order_by(Notice.id.desc())
    topics = Topic.query.order_by(Topic.last_post_id.desc()).limit(15)
    return render_template('index.html',topics=topics,notices=notices)
    #return 'hello world'