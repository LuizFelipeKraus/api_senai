from resource.users import UserRegister, UserLogin, UserLogout, AllUsers
from resource.products import ProductResource, AllProducts
from resource.categories import CategoryResource, Allcategory
from resource.address import AddressResource, AllAddress
from resource.orders import OrderResource, AllOrder
from resource.products_category import ProductCategoryResource
from resource.order_itens import OrderItemResource, AllOrderItem, AllOrderItemDate
from app import api, app


api.add_resource(AllUsers, '/users')
api.add_resource(UserRegister, '/users/register/')
api.add_resource(UserLogin, '/users/login')
api.add_resource(UserLogout, '/users/logout')

api.add_resource(AllProducts, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')

api.add_resource(Allcategory, '/categories')
api.add_resource(CategoryResource, '/categories/<int:category_id>')

api.add_resource(AllAddress, '/users/address')
api.add_resource(AddressResource, '/address/<int:address_id>')

api.add_resource(AllOrder, '/orders')
api.add_resource(OrderResource, '/orders/<int:orders_id>')

api.add_resource(OrderItemResource, '/orders/items/<int:order_item_id>')
api.add_resource(AllOrderItem, '/orders/items/users')
api.add_resource(AllOrderItemDate, '/orders/items/<string:start_date>/<string:end_date>')
if __name__ == '__main__':
    app.run(debug=True)