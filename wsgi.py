from flask import *
from flask_mysqldb import MySQL
<<<<<<< HEAD
=======

>>>>>>> 17af074312bf8e44b9ca596683c28ee0f3ec3716
application = Flask(__name__)

application.config['MYSQL_HOST'] = 'custom-mysql.gamification.svc.cluster.local'
application.config['MYSQL_USER'] = 'xxuser'
application.config['MYSQL_PASSWORD'] = 'welcome1'
application.config['MYSQL_DB'] = 'sampledb'
mysql = MySQL(application)
listitem = []

@application.route("/")
def home():
    return render_template("home.html")


@application.route("/about")
def about():
    no_of_item = request.args.get('noofitem')
    cart_product_id = request.args.getlist('productId')
    page_name= request.args.get('pagename')
    if page_name == 'Cart':
        ls = cart_product_id
        newls = ls[0].rstrip(')').lstrip('(').split(',')
        item = []
        listitem = []
        for a in newls:
            item.append(a.strip("'"))
        if len(item) == 2 and item[1] == '':
            listitem.append(item[0].strip("'"))
        else:
            for val in item:
                listitem.append(val.lstrip(' ').strip("'"))
        cart_product_id=listitem
    print("about",cart_product_id)
    if no_of_item == None:
        no_of_item = 0
    else:
        no_of_item = no_of_item
    try:
        cur = mysql.connection.cursor()
        res = cur.execute(
            "SELECT DISTINCT CASE WHEN A.ITEM_NUMBER='1000' THEN 'Reflex Women' WHEN A.ITEM_NUMBER='2000' THEN 'Reflex Men' ELSE A.BRAND END AS BRAND, A.ITEM_NUMBER FROM sampledb.XXIBM_PRODUCT_STYLE A ")
        if res > 0:
            categoryData = cur.fetchall()
        res2 = cur.execute(
            "SELECT DISTINCT  FAMILY,FAMILY_NAME from sampledb.XXIBM_PRODUCT_CATALOGUE ")
        if res2 > 0:
            BrandData = cur.fetchall()
            return render_template('about.html', categoryData=categoryData, brandData=BrandData,
                                   noOfItems=no_of_item, cartprid=cart_product_id)
    except Exception as e:
        return str(e)
    cur.close()


@application.route("/displayCategory", methods=['GET', 'POST'])
def displayCategory():
    if request.method == "POST":
        ColorId = request.form.getlist('Color')
        SizeId = request.form.getlist('Size')
        product = []
        try:
            cur = mysql.connection.cursor()
            if len(ColorId)==0:
                SizeIds=tuple(SizeId)
                res = cur.execute(
                "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and A.SKU_ATTRIBUTE_VALUE1 in %s ",
                    (SizeIds,))
            elif len(SizeId)==0:
                ColorIds = tuple(ColorId)
                res = cur.execute(
                    "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and  A.SKU_ATTRIBUTE_VALUE2 in %s",
                    (ColorIds,))
            else:
                valueId = tuple(ColorId + SizeId)
                res = cur.execute(
                    "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and (A.SKU_ATTRIBUTE_VALUE1 in %s and A.SKU_ATTRIBUTE_VALUE2 in %s)",
                    (valueId,valueId))
            if res > 0:
                data = cur.fetchall()
                product.append(data)
                return render_template("displayCategory.html", data=product)
            else:
                error = "Sorry No data available"
                return render_template("error.html", error=error)
        except Exception as e:
            return str(e)
        return render_template('displayCategory.html')
    else:
        categoryId = request.args.get('categoryId')
        product = []
        try:
            cur = mysql.connection.cursor()
            res = cur.execute(
                "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1  from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B,sampledb.XXIBM_PRODUCT_STYLE C where A.ITEM_NUMBER=B.ITEM_NUMBER and A.STYLE_ITEM=C.ITEM_NUMBER and A.STYLE_ITEM=%s",
                (categoryId,))
            if res > 0:
                productData = cur.fetchall()
                product.append(productData)
                return render_template("displayCategory.html", data=product)
            else:
                error = "Sorry No data available"
                return render_template("error.html", error=error)
        except Exception as e:
            return str(e)
        cur.close()


@application.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        categoryId = request.form.get('search')
        data = request.form.get('search')
        words = categoryId.split()
        if len(words) > 0:
            categoryId = '%'
            for i in words:
                if i == 'Men':
                    categoryId = categoryId + ' ' + i + '%'
                else:
                    categoryId = categoryId + i + '%'
        elif categoryId == 'Men':
            categoryId = '%' + ' ' + categoryId + '%'
        else:
            categoryId = '%' + categoryId + '%'
        product = []
        print(categoryId)
        try:
            cur = mysql.connection.cursor()
            res = cur.execute(
                "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and (A.LONG_DESCRIPTION like %s or A.SKU_ATTRIBUTE_VALUE1 like %s or A.SKU_ATTRIBUTE_VALUE2 like %s or concat(A.LONG_DESCRIPTION,A.SKU_ATTRIBUTE_VALUE2) like %s or concat(A.SKU_ATTRIBUTE_VALUE2,A.LONG_DESCRIPTION) like %s or concat(A.LONG_DESCRIPTION,A.SKU_ATTRIBUTE_VALUE1) like %s or concat(A.SKU_ATTRIBUTE_VALUE1,A.LONG_DESCRIPTION) like %s"
                "or concat(A.SKU_ATTRIBUTE_VALUE1,A.SKU_ATTRIBUTE_VALUE2) like %s or concat(A.SKU_ATTRIBUTE_VALUE2,A.SKU_ATTRIBUTE_VALUE1) like %s or concat(A.LONG_DESCRIPTION ,concat(A.SKU_ATTRIBUTE_VALUE1,A.SKU_ATTRIBUTE_VALUE2)) like %s or concat(A.LONG_DESCRIPTION ,concat(A.SKU_ATTRIBUTE_VALUE2,A.SKU_ATTRIBUTE_VALUE1)) like %s)",
                (categoryId, categoryId, categoryId,categoryId,categoryId,categoryId,categoryId,categoryId,categoryId,categoryId,categoryId))
            if res > 0:
                data = cur.fetchall()
                product.append(data)
                return render_template("search.html", data=product)
            else:
                error = "Sorry No data available"
                return render_template("error.html", error=error)
        except Exception as e:
            return str(e)
        cur.close()
    return render_template('search.html')


@application.route("/brandCategory", methods=['GET', 'POST'])
def brandCategory():
    if request.method == "POST":
        ColorId = request.form.getlist('Color')
        SizeId = request.form.getlist('Size')
        product = []
        try:
            cur = mysql.connection.cursor()
            if len(ColorId) == 0:
                SizeIds = tuple(SizeId)
                res = cur.execute(
                    "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and A.SKU_ATTRIBUTE_VALUE1 in %s ",
                    (SizeIds,))
            elif len(SizeId) == 0:
                ColorIds = tuple(ColorId)
                res = cur.execute(
                    "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and  A.SKU_ATTRIBUTE_VALUE2 in %s",
                    (ColorIds,))
            else:
                valueId = tuple(ColorId + SizeId)
                res = cur.execute(
                    "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and (A.SKU_ATTRIBUTE_VALUE1 in %s and A.SKU_ATTRIBUTE_VALUE2 in %s)",
                    (valueId, valueId))
            if res > 0:
                data = cur.fetchall()
                product.append(data)
                return render_template("BrandDescription.html", data=product)
            else:
                error = "Sorry No data available"
                return render_template("error.html", error=error)
        except Exception as e:
            return str(e)
        return render_template('BrandDescription.html')
    else:
        categoryId = request.args.get('categoryId')
        product = []
        try:
            cur = mysql.connection.cursor()
            res = cur.execute(
                "Select  DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A,sampledb.XXIBM_PRODUCT_PRICING B ,sampledb.XXIBM_PRODUCT_CATALOGUE C where C.COMMODITY=A.catalogue_category and A.ITEM_NUMBER=B.ITEM_NUMBER and C.FAMILY=%s",
                (categoryId,))
            if res > 0:
                productData = cur.fetchall()
                product.append(productData)
                return render_template("BrandDescription.html", data=product)
            else:
                error = "Sorry No data available"
                return render_template("error.html", error=error)
        except Exception as e:
            return str(e)
        cur.close()


@application.route("/productDescription")
def productDescription():
    productId = request.args.get('productId')
    product = []
    try:
        cur = mysql.connection.cursor()
        res = cur.execute(
            "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,(B.LIST_PRICE-B.LIST_PRICE*B.DISCOUNT) AS DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN_STOCK' ELSE 'OUT_OF_STOCK' END AS STOCK, A.LONG_DESCRIPTION from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and A.ITEM_NUMBER=%s",
            (productId,))
        if res > 0:
            productData = cur.fetchone()
            product.append(productData)
            return render_template("productDescription.html", Itemdata=product)
        else:
            error = "Sorry No data available"
            return render_template("error.html", error=error)
    except Exception as e:
        return str(e)
    cur.close()


@application.route("/addToCart")
def addToCart():
    productId = request.args.get('productId')
    print("add",productId)
    listitem.append(productId)
    print(listitem)
    noofitems = len(listitem)
    return redirect(url_for('about', noofitem=noofitems, productId=listitem,pagename='addcart'))


@application.route("/Cart")
def cart():
    productId = request.args.get('productId')
    print("Cart",productId)
    ls = list(productId.rstrip(']').lstrip('[').split(","))
    listitem = []
    if len(ls) == 2 and ls[1] == '':
        listitem.append(ls[0].strip("'"))
    else:
        for val in ls:
            listitem.append(val.lstrip(' ').strip("'"))
    try:
        totalproduct = tuple(listitem)
        print("cart",totalproduct)
        cur = mysql.connection.cursor()
        res = cur.execute(
            "Select A.DESCRIPTION ,B.ITEM_NUMBER ,CASE WHEN B.DISCOUNT<>'0.0' THEN B.LIST_PRICE-B.LIST_PRICE*B.DISCOUNT ELSE B.LIST_PRICE END  AS DISCOUNT,(Select SUM(CASE WHEN B.DISCOUNT<>'0.0' THEN (B.LIST_PRICE-B.LIST_PRICE*B.DISCOUNT) ELSE B.LIST_PRICE END) from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER and A.ITEM_NUMBER in %s ) AS Total_price,(Select count(B.ITEM_NUMBER) from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B  where A.ITEM_NUMBER=B.ITEM_NUMBER and A.ITEM_NUMBER in %s) as no_of_item  from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER and A.ITEM_NUMBER in %s",
            (totalproduct, totalproduct, totalproduct))
        if res > 0:
            productData = cur.fetchall()
            totalprice = productData[0][3]
            no_of_item = productData[0][4]
            return render_template("cart.html", Itemdata=productData, totalprice=totalprice, noOfItems=no_of_item,
                                           totalItems=totalproduct)
        else:
            error = "Cart is empty"
            return render_template("error.html", error=error)
    except Exception as e:
        return str(e)




@application.route("/removeFromCart")
def removeItem():
    productId = request.args.get('productId')
    itemnumber = request.args.get('itemnum')
    ls = list(itemnumber.rstrip(')').lstrip('(').split(","))
    listitem = []
    if len(ls) == 2 and ls[1] == '':
        listitem.append(ls[0].strip("'"))
    else:
        for val in ls:
            listitem.append(val.lstrip(' ').strip("'"))
    listitem.remove(productId)
    noofitems = len(listitem)
    print("remove",listitem)
    return redirect(url_for('about', noofitem=noofitems, productId=listitem,pagename='removecart'))


@application.route("/checkout",methods=['GET','POST'])
def checkout():
    if request.method =='POST':
        return '<html><body><h1>Thank you for shopping with us!!!!</h1></body></html>'
    return render_template("checkout.html")

if __name__ == "__main__":
    application.run()
