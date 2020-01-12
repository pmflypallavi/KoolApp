from flask import *
from flask_mysqldb import MySQL

application = Flask(__name__)

application.config['MYSQL_HOST'] = '127.0.0.1'
application.config['MYSQL_USER'] = 'xxuser'
application.config['MYSQL_PASSWORD'] = 'welcome1'
application.config['MYSQL_DB'] = 'sampledb'
mysql = MySQL(application)
total = []


@application.route("/")
def home():
    return render_template("home.html")


@application.route("/about")
def about():
    no_of_item = request.args.get('noofitem')
    cart_product_id = request.args.get('productId')

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


@application.route("/displayCategory")
def displayCategory():
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
        try:
            cur = mysql.connection.cursor()
            res = cur.execute(
                "Select DISTINCT A.DESCRIPTION,B.ITEM_NUMBER,B.LIST_PRICE,CASE WHEN B.DISCOUNT='0.0' or B.DISCOUNT IS NULL THEN 'No Discount' else CONCAT(substring_index(DISCOUNT*100,'.',1),'%%') end as  DISCOUNT,CASE WHEN B.IN_STOCK='Yes' THEN 'IN STOCK' ELSE 'OUT OF STOCK' END AS STOCK,A.SKU_ATTRIBUTE_VALUE1 from sampledb.XXIBM_PRODUCT_SKU A , sampledb.XXIBM_PRODUCT_PRICING B where A.ITEM_NUMBER=B.ITEM_NUMBER  and (A.DESCRIPTION like %s or A.SKU_ATTRIBUTE_VALUE1 like %s or A.SKU_ATTRIBUTE_VALUE2 like %s)",
                (categoryId, categoryId, categoryId))
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


@application.route("/brandCategory")
def brandCategory():
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


@application.route("/Cart")
def cart():
    productId = request.args.get('productId')
    name = request.args.get('page')
    if (name == 'aboutpage'):
        total.clear()
        ls = []
        ls = list(productId.rstrip(')').lstrip('(').split(","))
        if len(ls) == 2 and ls[1] == '':
            total.append(ls[0].strip("'"))
        else:
            for val in ls:
                total.append(val.lstrip(' ').strip("'"))
    else:
        total.append(productId)
    try:
        totalproduct = tuple(total)
        print(totalproduct)
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
    return redirect(url_for('about', noofitem=noofitems, productId=listitem))


@application.route("/checkout")
def checkout():
    return '<html><body><h1>Thank you for shopping with us!!!!</h1></body></html>'


if __name__ == "__main__":
    application.run()
