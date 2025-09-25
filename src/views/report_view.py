"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from queries.read_order import get_highest_sold_items_redis, get_highest_spending_users
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """ Show report of highest spending users """
    highest_spenders = get_highest_spending_users()
    rows = "".join(
        f"<tr><td>{user_id}</td><td>${total:.2f}</td></tr>"
        for user_id, total in highest_spenders
    )
    return get_template(
        f"""
        <h2>Les plus gros acheteurs</h2>
        <p>Voici les utilisateurs ayant dépensé le plus d'argent (tous temps confondus) :</p>
        <table class="table">
            <tr>
                <th>ID Utilisateur</th>
                <th>Total Dépensé</th>
            </tr>
            {rows}
        </table>
        """
    )

def show_best_sellers():
    """ Show report of best selling products """
    best_sellers = get_highest_sold_items_redis()
    rows = "".join(
        f"<li>Produit {product_id} : {quantity} vendus</li>"
        for product_id, quantity in best_sellers
    )
    return get_template(
        f"<h2>Les articles les plus vendus</h2><ul>{rows}</ul>"
    )