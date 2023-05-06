from flask import Blueprint, abort, escape
from flask import flash, render_template, redirect, url_for, request
import os
from . import db, limiter, q
from .models import Order
from .bot import visit
import codecs
import ipaddress




main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('homepage.html')


@main.route('/order/create', methods=['POST'])
@limiter.limit("40/minute")
def create_order():
  try:
    article = escape(request.form.get('article'))
    quantity = escape(request.form.get('quantity'))
    username = escape(request.form.get('username'))
    if username == "pilvar":
      if not ipaddress.ip_address(request.remote_addr).is_private:
        abort(403)
    address = escape(request.form.get('address'))
    email = escape(request.form.get('email'))
    order_id = codecs.encode((article+quantity+username+address).encode('ascii'), 'base64').decode('utf-8')
    order_id = order_id.replace("\n","") #I have no ideas where it happens, but I think there's a new line appended somewhere. Putting this line here and there fixed it.
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
      iteration = 0
      order_id = order.order_id
      og_order_id = order_id
      while order:
          order_id = og_order_id+"-"+str(iteration)
          order = Order.query.filter_by(order_id=order_id).first()
          iteration += 1
    status = "Under review"
    new_order = Order(order_id=order_id,
                    email=email,
                    username=username,
                    address=address,
                    article=article,
                    quantity=quantity,
                    status=status)
    db.session.add(new_order)
    db.session.commit()
    q.enqueue(visit, order_id)
    return redirect("/orders/"+order_id+"/preview")
  except Exception as e:
    return(str(e))

@main.route('/orders/<order_id>/preview')
def order(order_id):
    if order_id:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            abort(404)
        if ipaddress.ip_address(request.remote_addr).is_private:
            article_infos = order.article.split(":")
            article_name = article_infos[0]
            article_link = article_infos[1]
            return render_template('inspect_order.html', order_id=order.order_id, article_name=article_name, article_link=article_link, quantity=order.quantity)
        else:
            return render_template('order_status.html', status=order.status)
    else:
        return redirect("/")

@main.route('/orders/<order_id>/get_user_infos')
def userinfos(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    return {'username': order.username, 'address': order.address, 'email': order.email}

@main.route('/order/update', methods=['POST'])
def update():
    if ipaddress.ip_address(request.remote_addr).is_private:
        order_id = request.form.get('order_id')
        order_status = request.form.get('order_status')
        if order_status == "accepted":
            order_status = os.getenv('FLAG')
        Order.query.filter_by(order_id=order_id).update({
            'status': order_status
            })
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")