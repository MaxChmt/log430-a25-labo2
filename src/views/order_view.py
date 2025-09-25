"""
Order view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import numbers
from views.template_view import get_template, get_param
from controllers.order_controller import create_order, delete_order, get_report_highest_sold_items, get_report_highest_sold_items_redis, get_report_highest_spending_users,list_orders_from_redis, list_orders_from_mysql
from controllers.product_controller import list_products
from controllers.user_controller import list_users

def show_order_form():
    """ Show order form and list """
    highest_spending_users = get_report_highest_spending_users()
    print(f"[DEBUG] Highest spending users: {highest_spending_users}", flush=True)
    highest_sold_items = get_report_highest_sold_items()
    print(f"[DEBUG] Highest sold items: {highest_sold_items}", flush=True)
    highest_sold_items_redis = get_report_highest_sold_items_redis()
    print(f"[DEBUG] Highest sold items redis: {highest_sold_items_redis}", flush=True)
    orders = list_orders_from_redis(10)
    products = list_products(99)
    users = list_users(99)
    highest_sold_items_redis_rows = [f"""
        <tr>
            <td>{product_id}</td>
            <td>{count}</td>
        </tr>""" for product_id, count in highest_sold_items_redis]
    highest_sold_items_rows = [f"""
        <tr>
            <td>${float(total_amount):.2f}</td>
            <td>{int(count)}</td>
        </tr>""" for total_amount, count in highest_sold_items]
    highest_spending_users_rows = [f"""
            <tr>
                <td>{user_id}</td>
                <td>${total:.2f}</td>
            </tr> """ for user_id, total in highest_spending_users]
    order_rows = [f"""
            <tr>
                <td>{order['id']}</td>
                <td>${order['total_amount']}</td>
                <td><a href="/orders/remove/{order['id']}">Supprimer</a></td>
            </tr> """ for order in orders]
    user_rows = [f"""<option key={user.id} value={user.id}>{user.name}</option>""" for user in users]
    product_rows = [f"""<option key={product.id} value={product.id}>{product.name} (${product.price})</option>""" for product in products]
    return get_template(f"""
        <h2>Utilisateurs ayant dépensé le plus</h2>
        <p>Voici les utilisateurs ayant dépensé le plus d'argent (tous temps confondus) :</p>
        <table class="table">
            <tr>
                <th>ID Utilisateur</th> 
                <th>Total Dépensé</th> 
            </tr>  
            {" ".join(highest_spending_users_rows)}
        </table>
        <h2>Produits les plus vendus</h2>
        <p>Voici les produits ayant le plus de succès (tous temps confondus) :</p>
        <table class="table">
            <tr>
                <th>Prix éléments</th> 
                <th>Total vendus</th> 
            </tr>  
            {" ".join(highest_sold_items_rows)}
        </table>
        <h2>Produits les plus vendus via Redis</h2>
        <p>Voici les produits ayant le plus de succès (tous temps confondus) :</p>
        <table class="table">
            <tr>
                <th>Id produit</th> 
                <th>Total vendus</th> 
            </tr>  
            {" ".join(highest_sold_items_redis_rows)}
        </table>
        <h2>Commandes</h2>
        <p>Voici les 10 derniers enregistrements :</p>
        <table class="table">
            <tr>
                <th>ID</th> 
                <th>Total</th> 
                <th>Actions</th> 
            </tr>  
            {" ".join(order_rows)}
        </table>
        <h2>Enregistrement</h2>
        <form method="POST" action="/orders/add">
            <div class="mb-3">
                <label class="form-label">Utilisateur</label>
                <select class="form-control" name="user_id" required>
                    {" ".join(user_rows)}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Article</label>
                <select class="form-control" name="product_id" required>
                    {" ".join(product_rows)}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Quantité</label>
                <input class="form-control" type="number" name="quantity" step="1" value="1" min="1" max="999" required>
            </div>
            <button type="submit" class="btn btn-primary">Enregistrer</button>
        </form>
    """)

def register_order(params):
    """ Add an order based on given params """
    if len(params.keys()):
        user_id = get_param(params, "user_id")
        product_id = get_param(params, "product_id")
        quantity = get_param(params, "quantity")
        items = [
            {'product_id': product_id, 'quantity': quantity}
        ]
        result = create_order(user_id, items)
    else: 
        return get_template(f"""
                <h2>Erreur</h2>
                <code>La requête est vide</code>
            """)

    if isinstance(result, numbers.Number):
        return get_template(f"""
                <h2>Information: la commande {result} a été ajoutée.</h2>
                <a href="/orders">← Retourner à la page des commandes</a>
            """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)
    
def remove_order(order_id):
    """ Remove an order with the given ID """
    result = delete_order(order_id)
    if result:
        return get_template(f"""
            <h2>Information: la commande {order_id} a été supprimée.</h2>
            <a href="/orders">← Retourner à la page des commandes</a>
        """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)