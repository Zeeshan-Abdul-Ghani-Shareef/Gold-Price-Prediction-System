
from .models import Customer
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category,Customer,Shipping_Address,Cart,Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from .forms import customerRegistrationForm
#------------------ml/ai--------------------
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from django.conf import settings

#---paggination------------------
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse

#-------grouped data--------------
from collections import defaultdict

#---basic search------------------
"""
def realEstateSearch(request):
    excel_file_path = os.path.join('media', 'world_real_estate_data.xls')
    data = pd.DataFrame()
    results_list = []

    try:
        # Load excel file
        data = pd.read_excel(excel_file_path)

        if request.method=="POST":
            NAME = request.POST.get('country', '').strip() # Get name, strip whitespace
            # Select required columns & limit first 1000 records
            results = data[['country', 'location', 'building_construction_year', 
                        'apartment_total_area', 'price_in_USD']][data['country'].astype(str).str.contains(NAME, case=False, na=False)]
        else:
            results = data[['country', 'location', 'building_construction_year', 
                        'apartment_total_area', 'price_in_USD']][0:1000]

        # Convert dataframe to list of dictionaries
        results_list = results.astype(str).to_dict(orient='records')

    except Exception as e:
        return HttpResponse(f"error occurred: {e}", status=500)

    # --- PAGINATION ---
    page = request.GET.get('page', 1)   # Get page number from query params (default 1)
    paginator = Paginator(results_list, 20)  # Show 20 records per page

    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        results_page = paginator.page(1)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)

    context = {
        'results_page': results_page
    }

    return render(request, "myshop/realEstate.html", context)
"""
#---advanse search with price field------------------

"""
def realEstateSearch(request):
    excel_file_path = os.path.join('media', 'world_real_estate_data.xls')
    data = pd.DataFrame()
    results_list = []

    try:
        # Load excel file
        data = pd.read_excel(excel_file_path)

        # Get search filters from POST or GET (so pagination works too)
        country = request.POST.get('country', '') if request.method == "POST" else request.GET.get('country', '')
        min_price = request.POST.get('min_price') if request.method == "POST" else request.GET.get('min_price')
        max_price = request.POST.get('max_price') if request.method == "POST" else request.GET.get('max_price')

        # Select columns
        results = data[['country', 'location', 'building_construction_year',
                        'apartment_total_area', 'price_in_USD']]

        # Apply country filter
        if country:
            results = results[results['country'].astype(str).str.contains(country, case=False, na=False)]

        # Apply price filter
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                results = results[(results['price_in_USD'] >= min_price) & (results['price_in_USD'] <= max_price)]
            except ValueError:
                pass  # Ignore if price inputs are invalid

        # Limit large dataset to first 1000 for performance
        results = results[0:1000]

        # Convert to list of dictionaries
        results_list = results.astype(str).to_dict(orient='records')

    except Exception as e:
        return HttpResponse(f"error occurred: {e}", status=500)

    # --- PAGINATION ---
    page = request.GET.get('page', 1)
    paginator = Paginator(results_list, 20)  # 20 per page

    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        results_page = paginator.page(1)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)

    context = {
        'results_page': results_page,
        'country': country,
        'min_price': min_price or '',
        'max_price': max_price or ''
    }

    return render(request, "myshop/realEstate.html", context)
"""
#---advanse search with price field and country list------------------


def realEstateSearch(request,country_name=None):
    excel_file_path = os.path.join('media', 'world_real_estate_data.xls')
    data = pd.DataFrame()
    results_list = []
    country_list = []

    try:
        # Load excel file
        data = pd.read_excel(excel_file_path)

        # Get search filters from POST or GET (so pagination works too)
        country = request.POST.get('country', '') if request.method == "POST" else request.GET.get('country', '')
        min_price = request.POST.get('min_price') if request.method == "POST" else request.GET.get('min_price')
        max_price = request.POST.get('max_price') if request.method == "POST" else request.GET.get('max_price')

        # Select columns
        results = data[['country', 'location', 'building_construction_year',
                        'apartment_total_area', 'price_in_USD']]

        # Apply country filter
        if country:
            results = results[results['country'].astype(str).str.contains(country, case=False, na=False)]

        # Apply price filter
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                results = results[(results['price_in_USD'] >= min_price) & (results['price_in_USD'] <= max_price)]
            except ValueError:
                pass  # Ignore if price inputs are invalid

        # Limit large dataset to first 1000 for performance
        results = results[0:1000]

        # Convert to list of dictionaries
        results_list = results.astype(str).to_dict(orient='records')

    except Exception as e:
        return HttpResponse(f"error occurred: {e}", status=500)
    
    # --- Build country list with counts ---
    country_counts = results['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'noofcountry']
    country_list = country_counts.to_dict(orient='records')

    # --- PAGINATION ---
    page = request.GET.get('page', 1)
    paginator = Paginator(results_list, 20)  # 20 per page

    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        results_page = paginator.page(1)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)

    context = {
        'results_page': results_page,
        'country': country,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'country_list': country_list,
        'selected_country': country_name
    }

    return render(request, "myshop/realEstate.html", context)



def index(request):
    return render(request, "myshop/index.html")

def about(request):
    return render(request, "myshop/about.html")

def contact(request):
    return render(request, "myshop/contact.html")


def logout_user(request):
    logout(request)
    return render(request, "myshop/login.html")

def login_user(request):
    msg=""

    if request.method == "POST":
        username=request.POST.get("uname")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            msg="Valid Login"
            next_param=request.GET.get('next')

            if next_param:
                if '://' not in next_param and next_param.startswith('/'):
                    return redirect(next_param)
                else:
                    return redirect(reverse('index'))
            else:
                return redirect(reverse('checkout'))
        else:
             msg="In Valid username/password"

             context={
                'msg':msg
            }
             return render(request, "myshop/login.html",context)

    return render(request, "myshop/login.html")

def signup(request):
    Msg=""
    F=False

    if request.method=="POST":

        full_name = request.POST['full_name']
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        confirmPass= request.POST['confirmPass']

        if password != confirmPass:
            Msg="Password and confirm password must be same"
            F=True
        
        if User.objects.filter(username=username).exists():
            Msg="Username already exists in database plz choose different"
            F=True

        if F==False:
            user=User.objects.create_user(first_name=first_name,username=username,
                                          email=email,password=password)
            user.save()

            Customer.objects.create(full_name=full_name,first_name=first_name,
                              username=username,email=email,password=password,address=address,
                              city=city,state=state,country=country,zip_code=zip_code,user=user)

            Msg="Your Registration has been completed plz signin"
    
    context={
        'Msg':Msg
    }

    return render(request, "myshop/signup.html",context)

@login_required(login_url='login_user')
def checkout(request):
          
     cart_items=[]
     cart=request.session.get('cart',{})
     cart_total=0
     order_total=0

     user_r=request.user

     for item in cart.values():
        product=Product.objects.get(pk=item['product_id'])
        
        total=int(item['quantity'])*product.price
        
        cart_total = cart_total + total

        cart_items.append(
            {
                'product':product,
                'total':total,
                'quantity':item['quantity']
            }
        )
     
        order_total= cart_total+17
     
     context={
        'cart_items':cart_items,
        'cart_total':cart_total,
        'order_total':order_total,
        'user_r':user_r
    }    

     return render(request, "myshop/checkout.html",context)

def product(request,id):
    
    products = Product.objects.all()
    category = Category.objects.all()

    if id!=0:
        if request.method=='POST':
            pname=request.POST.get('pname')
            cat = get_object_or_404(Category,pk=id)
            products = Product.objects.filter(product_category=cat,product_name__icontains=pname)
        else:
            cat = get_object_or_404(Category,pk=id)
            products = Product.objects.filter(product_category=cat)  

    context={
        'id':id,
        'products':products,
        'category':category
    }

    return render(request, "myshop/product.html",context)

def productDetail(request,id):
     
     products = get_object_or_404(Product,pk=id)    

     context={
        'products':products
      
    }

     return render(request, "myshop/productDetail.html",context)

def cart(request):
    cart_items=[]
    cart=request.session.get('cart',{})
    cart_total=0
    i=0
    for item in cart.values():
        
        product=Product.objects.get(pk=item['product_id'])        
        total=int(item['quantity'])*product.price        
        cart_total += total
        
        if i==0:
            cart_items.append(
            {
                'Display': False,
                'product':product,
                'total':total,
                'quantity':item['quantity']
            })

            cart_items.append(
            {
                'Display': True,
                'product':product,
                'total':total,
                'quantity':item['quantity']
            })
        else:
            cart_items.append(
            {
                'Display': True,
                'product':product,
                'total':total,
                'quantity':item['quantity']
            })
        
        i=i+1

    context={
        'cart_items':cart_items,
        'cart_total':cart_total
    }    

    return render(request, "myshop/cart.html",context)


def add_to_cart(request,product_id):
    quantity=request.POST.get('qty',0)
    product=Product.objects.get(pk=product_id)

    cart_item={
        'product_id':product_id,
        'quantity': quantity
    }

    if request.session.get('cart'):
        cart=request.session['cart']

        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id]=cart_item

        request.session.modified=True    
    else:
        cart={
            product_id:cart_item
        }
        request.session['cart']=cart          

    return redirect('cart')


def remove_from_cart(request,product_id):   
    product_id=str(product_id)
    cart=request.session.get('cart',{})
    if product_id in cart:
        del cart[product_id]
        request.session['cart']=cart

    return redirect('cart')


def update_to_cart(request,product_id):

    product_id=str(product_id)
    quantity=request.POST.get('qty',0)
    cart=request.session.get('cart',{}) 

    cart[product_id]['quantity'] = quantity
    request.session['cart']=cart       
    request.session.modified=True    
   
    return redirect('cart')

def calculator(request):
          
     r=0
     msg=""

     if request.method == "POST":
         A=int(request.POST.get("A"))
         B=int(request.POST.get("B"))
         O=request.POST.get("O")

         if (O=="+"):
             r=A+B
         elif (O=="-"):
             r=A-B
         elif (O=="*"):
             r=A*B
         elif (O=="/"):
             r=A/B
         else:
             r=0

         msg="success"

     context={
         'r':r,
         'msg':msg
     }
   
     return render(request, 'myshop/calculator.html', context)


def marksheet(request):
          
     P=0
     G=""
     msg=""

     if request.method == "POST":
         O=float(request.POST.get("O"))
         T=float(request.POST.get("T"))
        
         P=(O/T)*100

         if (P>=80):            
            G="A-1"
         elif (P>=70):
            G="A"
         elif (P>=60):
            G="B"
         elif (P>=50):
            G="C"
         else:
            G="FAIL"

         msg="success"
                 
     context={
         'P':P,
         'G':G,
         'msg':msg
     }
   
     return render(request, 'myshop/marksheet.html', context)


def tablegen(request):               
     T=0
     msg=""
     Table_List=[]
     F=False
     if request.method == "POST":         
         T=int(request.POST.get("T"))
         R=range(1,11)

         for i in R:
             
             M=T*i
             Table_List.append(
                 {
                 'T':T,
                 'i':i,
                 'M':M
                 }
                 )        
         F=True
         msg="success"
     context={
         'T':T,         
         'msg':msg,
         'Table_List':Table_List,
         'F':F
     }
   
     return render(request, 'myshop/tablegen.html', context)

#-------------------form based registration--------------------
def Register_Customer(request):
    msg=""
   

    if request.method=="POST":

        form=customerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            msg="Your Registration has been completed"
    else:
        form=customerRegistrationForm()

    context={
        'msg':msg,
        'form':form
    }    

    return render(request, "myshop/register.html",context)

@login_required(login_url='login_user')
def place_order(request):
    Msg=""
    F=False

    if request.method=="POST":
       
        contact = request.POST['contact']
        shipping_address=request.POST['address']
        shipping_city=request.POST['city']
        shipping_state=request.POST['state']
        shipping_country=request.POST['country']
        shipping_zip=request.POST['zip']

        user=request.user
       
        shiped=Shipping_Address.objects.create(contact=contact,shipping_address=shipping_address,
                              shipping_city=shipping_city,shipping_state=shipping_state,
                              shipping_country=shipping_country,shipping_zip=shipping_zip,user=user)
        #-----------------order--------------------
        cart_items=[]
        cart=request.session.get('cart',{})
        cart_total=0
        cart_qty=0

        for item in cart.values():
            product=Product.objects.get(pk=item['product_id'])        
            total=int(item['quantity'])*product.price        
            cart_total = cart_total + total
            cart_qty = cart_qty + int(item['quantity'])
        
        order=Order.objects.create(user=user,shiped=shiped,total_quantity=cart_qty,total_price=cart_total)
        
        #-----------------order--------------------

        cart=request.session.get('cart',{})
        cart_total=0
        cart_qty=0

        for item in cart.values():
            product=Product.objects.get(pk=item['product_id'])        
            total=int(item['quantity'])*product.price
            qty=int(item['quantity'])    
            Cart.objects.create(cart_product=product,user=user,order=order,quantity=qty)

        Msg="Your Order has been placed successfully"
    
    context={
        'Msg':Msg
    }

    return render(request, "myshop/thanks.html",context)



#----------machine learning dash board ----------------
def realEstateGraph(request):
    import os
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import plotly.offline as opy
    import plotly.graph_objects as go
    import plotly.express as px
    from django.http import HttpResponse
    from django.shortcuts import render

    excel_file_path = os.path.join('media', 'world_real_estate_data.xls')

    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        return HttpResponse(f"error occured: {e}", status=500)

    # ===== Clean dataset =====
    useful_columns = [
        'country',
        'location',
        'price_in_USD'
    ]
    df = df[[col for col in useful_columns if col in df.columns]]
    df = df.dropna()

    # ===== Line Chart: Average Price by Country =====
    if "country" in df.columns:
        avg_country = df.groupby("country")["price_in_USD"].mean().reset_index()
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=avg_country["country"],
            y=avg_country["price_in_USD"],
            mode='lines+markers',
            name='Average Price'
        ))
        fig_line.update_layout(
            title="Average Real Estate Prices by Country",
            xaxis_title="Country",
            yaxis_title="Average Price (USD)"
        )
        LineChart_div = opy.plot(fig_line, auto_open=False, output_type='div')
    else:
        LineChart_div = "<p>No country data available for line chart</p>"

    # ===== Map Chart: Choropleth of Prices =====
    if "country" in df.columns:
        avg_country_map = df.groupby("country")["price_in_USD"].mean().reset_index()
        fig_map = px.choropleth(
            avg_country_map,
            locations="country",
            locationmode="country names",
            color="price_in_USD",
            hover_name="country",
            color_continuous_scale="Viridis",
            title="Real Estate Prices by Country"
        )
        MapChart_div = opy.plot(fig_map, auto_open=False, output_type='div')
    else:
        MapChart_div = "<p>No country data available for map chart</p>"

    # ===== Regression (as before) =====
    # One-hot encode categorical columns
    categorical_cols = []
    if "country" in df.columns:
        categorical_cols.append("country")
    if "location" in df.columns:
        categorical_cols.append("location")

    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Features and target
    X = df_encoded.drop("price_in_USD", axis=1)
    y = df_encoded["price_in_USD"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    linear = LinearRegression().fit(X_train, y_train)
    y_pred = linear.predict(X_test)

    # Actual vs Predicted
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=list(range(len(y_test))),
        y=y_test,
        mode='lines',
        name='Actual Price'
    ))
    fig_pred.add_trace(go.Scatter(
        x=list(range(len(y_pred))),
        y=y_pred,
        mode='lines',
        name='Predicted Price'
    ))
    PredictionPlot_div = opy.plot(fig_pred, auto_open=False, output_type='div')

    # ===== Model formula =====
    coefficients = dict(zip(X.columns, linear.coef_))
    RegressionModelFormula = f"Price = {coefficients} + {linear.intercept_:.2f}"

    context = {
        'LineChart_div': LineChart_div,         # Graph 1
        'MapChart_div': MapChart_div,           # Graph 2
        'PredictionPlot_div': PredictionPlot_div, # Graph 3 (regression)
        'ModelFormula': RegressionModelFormula,
        'R2_Score': round(linear.score(X_test, y_test) * 100, 2),
    }

    return render(request, "myshop/realEstateGraph.html", context)


def realEstateGraph2(request):
    import os
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import plotly.offline as opy
    import plotly.graph_objects as go
    import plotly.express as px
    from django.http import HttpResponse
    from django.shortcuts import render

    excel_file_path = os.path.join('media', 'world_real_estate_data.xls')

    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        return HttpResponse(f"error occured: {e}", status=500)

    # ===== Clean dataset =====
    useful_columns = [
        'country',
        'location',
        'price_in_USD',
        'building_construction_year'
    ]
    df = df[[col for col in useful_columns if col in df.columns]]
    df = df.dropna()

    # ===== One-hot encode categorical columns =====
    categorical_cols = []
    if "country" in df.columns:
        categorical_cols.append("country")
    if "location" in df.columns:
        categorical_cols.append("location")

    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Features and target
    X = df_encoded.drop("price_in_USD", axis=1)
    y = df_encoded["price_in_USD"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    linear = LinearRegression().fit(X_train, y_train)

    # ===== Defaults if no input provided =====
    country_input = request.GET.get("country", "Pakistan")
    location_input = request.GET.get("location", "Karachi")
    year_input = int(request.GET.get("year", 2025))  # default year

    ForecastPlot_div = None
    predicted_prices = []

    try:
        # Build input row with base year
        input_data = {"building_construction_year": year_input}

        # Add all one-hot encoded columns with 0
        for col in X.columns:
            if col not in input_data:
                input_data[col] = 0

        # Activate chosen country/location dummy column
        country_col = f"country_{country_input}"
        if country_col in input_data:
            input_data[country_col] = 1

        location_col = f"location_{location_input}"
        if location_col in input_data:
            input_data[location_col] = 1

        input_df = pd.DataFrame([input_data])

        # Predict base price
        base_price = linear.predict(input_df)[0]

        # Assume yearly growth (5%)
        growth_rate = 0.05
        years = list(range(year_input, year_input + 10))  # actual years
        predicted_prices = [base_price * ((1 + growth_rate) ** i) for i in range(1, 11)]

        # Plot forecast
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=years,
            y=predicted_prices,
            mode='lines+markers',
            name='Forecasted Price'
        ))
        fig_forecast.update_layout(
            title=f"10-Year Price Forecast for {location_input}, {country_input} (from {year_input})",
            xaxis_title="Year",
            yaxis_title="Predicted Price (USD)"
        )
        ForecastPlot_div = opy.plot(fig_forecast, auto_open=False, output_type='div')

    except Exception as e:
        ForecastPlot_div = f"<p>Error in prediction: {e}</p>"

    # ===== Line Chart: Average Price by Country =====
    LineChart_div = "<p>No country data available for line chart</p>"
    if "country" in df.columns:
        avg_country = df.groupby("country")["price_in_USD"].mean().reset_index()
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=avg_country["country"],
            y=avg_country["price_in_USD"],
            mode='lines+markers',
            name='Average Price'
        ))
        fig_line.update_layout(
            title="Average Real Estate Prices by Country",
            xaxis_title="Country",
            yaxis_title="Average Price (USD)"
        )
        LineChart_div = opy.plot(fig_line, auto_open=False, output_type='div')

    # ===== Map Chart: Choropleth =====
    MapChart_div = "<p>No country data available for map chart</p>"
    if "country" in df.columns:
        avg_country_map = df.groupby("country")["price_in_USD"].mean().reset_index()
        fig_map = px.choropleth(
            avg_country_map,
            locations="country",
            locationmode="country names",
            color="price_in_USD",
            hover_name="country",
            color_continuous_scale="Viridis",
            title="Real Estate Prices by Country"
        )
        MapChart_div = opy.plot(fig_map, auto_open=False, output_type='div')

    # ===== Actual vs Predicted Plot =====
    y_pred = linear.predict(X_test)
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=list(range(len(y_test))),
        y=y_test,
        mode='lines',
        name='Actual Price'
    ))
    fig_pred.add_trace(go.Scatter(
        x=list(range(len(y_pred))),
        y=y_pred,
        mode='lines',
        name='Predicted Price'
    ))
    PredictionPlot_div = opy.plot(fig_pred, auto_open=False, output_type='div')

    # ===== Model Formula =====
    coefficients = dict(zip(X.columns, linear.coef_))
    RegressionModelFormula = f"Price = {coefficients} + {linear.intercept_:.2f}"

    context = {
        'LineChart_div': LineChart_div,
        'MapChart_div': MapChart_div,
        'PredictionPlot_div': PredictionPlot_div,
        'ForecastPlot_div': ForecastPlot_div,
        'PredictedPrices': predicted_prices,
        'ModelFormula': RegressionModelFormula,
        'R2_Score': round(linear.score(X_test, y_test) * 100, 2),
    }

    return render(request, "myshop/realEstateGraph2.html", context)


#-----------------Gold Prices--------------------------------
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login


#========== IMPORT LIBRARIES ==========
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
# Turn off pandas warning
pd.set_option('mode.chained_assignment', None)

# For Getting Dataset From YahooFinance
import yfinance as yf


# Get today's date
from datetime import datetime, timedelta
import pytz
today = datetime.now(tz=pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')

# For Graphs
import plotly.offline as opy
from plotly.graph_objs import Scatter
import plotly.graph_objects as go

#========== READ DATA ==========
Df = yf.download('GLD', '2023-10-01', today, auto_adjust=True)
# Only keep close columns
Df = Df[['Close']]
# Drop rows with missing values
Df = Df.dropna()

print(Df.head())

# Plot the closing price of GLD
x_data = Df.index
y_data = Df['Close']
ClosingPricePlot_div = opy.plot({
    'data': [Scatter(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green')],
    'layout': {'title': 'Gold ETF Price Series', 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Gold ETF price (in $)'}}
}, output_type='div')

#========== DEFINE EXPLANATORY VARIABLES ==========
Df['S_3'] = Df['Close'].rolling(window=3).mean()
Df['S_9'] = Df['Close'].rolling(window=9).mean()
Df['next_day_price'] = Df['Close'].shift(-1)

Df = Df.dropna()
X = Df[['S_3', 'S_9']]

# Define dependent variable
y = Df['next_day_price']

#========== TRAIN AND TEST DATASET ==========
t = .8
t = int(t*len(Df))

# Train dataset
X_train = X[:t]
y_train = y[:t]

# Test dataset
X_test = X[t:]
y_test = y[t:]

#========== LINEAR REGRESSION MODEL ==========
linear = LinearRegression().fit(X_train, y_train)
RegressionModelFormula = "Gold ETF Price (y) = %.2f * 3 Days Moving Average (x1) + %.2f * 9 Days Moving Average (x2) + %.2f (constant)" % (linear.coef_[0], linear.coef_[1], linear.intercept_)

#========== PREDICTING GOLD ETF PRICES ==========
predicted_price = linear.predict(X_test)
predicted_price = pd.DataFrame(predicted_price, index=y_test.index, columns=['price'])
# Attach y_tese series to dataframe
predicted_price['close'] = y_test
# Plot graph
x_data = predicted_price.index
y_data_predicted = predicted_price['price']
y_data_actual = predicted_price['close']
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_data, y=y_data_predicted,
                    mode='lines',
                    name='Predicted Price'))
fig.add_trace(go.Scatter(x=x_data, y=y_data_actual,
                    mode='lines',
                    name='Actual Price'))
PredictionPlot_div = opy.plot({
    'data': [Scatter(x=x_data, y=y_data_predicted, mode='lines', name='Predicted Price', opacity=0.8),
    Scatter(x=x_data, y=y_data_actual, mode='lines', name='Actual Price', opacity=0.8)],
    'layout': {'title': 'Predicted VS Actual Price', 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Gold ETF price (in $)'}}
}, auto_open=False, output_type='div')

#========== CUMULATIVE RETURNS ==========
gold = pd.DataFrame()

gold['price'] = Df[t:]['Close']
gold['predicted_price_next_day'] = predicted_price['price']
gold['actual_price_next_day'] = y_test
gold['gold_returns'] = gold['price'].pct_change().shift(-1)
    
gold['signal'] = np.where(gold.predicted_price_next_day.shift(1) < gold.predicted_price_next_day,1,0)
    
gold['strategy_returns'] = gold.signal * gold['gold_returns']
x_data = gold.index
y_data = ((gold['strategy_returns']+1).cumprod()).values
CumulativeReturns_div = opy.plot({
    'data': [Scatter(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green')],
    'layout': {'title': 'Cumulative Returns', 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Cumulative Returns (X 100%)'}}
}, output_type='div')

#========== PREDICT DAILY MOVES ==========
data = yf.download('GLD', '2023-10-01', today, auto_adjust=True)
data['S_3'] = data['Close'].rolling(window=3).mean()
data['S_9'] = data['Close'].rolling(window=9).mean()
data = data.dropna()
data['predicted_gold_price'] = linear.predict(data[['S_3', 'S_9']])
data['signal'] = np.where(data.predicted_gold_price.shift(1) < data.predicted_gold_price,"Buy","No Position")


# Return to Context functions
def PlotClosingPrice():
    return ClosingPricePlot_div

def RegressionModel():
    return RegressionModelFormula

def PredictionPlot():
    return PredictionPlot_div

def r2_scoreCalculate():
    # R square
    r2_score = linear.score(X[t:], y[t:])*100
    r2_score = float("{0:.2f}".format(r2_score))
    return r2_score

def CumulativeReturns():
    return CumulativeReturns_div

def SharpeRatioCalculate():
    return '%.2f' % (gold['strategy_returns'].mean()/gold['strategy_returns'].std()*(252**0.5))

def MovingAverage_S3():
    return round(data['S_3'].iloc[-1], 2)

def MovingAverage_S9():
    return round(data['S_9'].iloc[-1], 2)

def GetSignal():
    return data['signal'].iloc[-1]

def GetPredictedPrice():
    return round(data['predicted_gold_price'].iloc[-1], 2)

def GetNextDay():
    NextDate = (data.index[-1].date() + timedelta(days=1)).strftime('%d/%m/%Y')
    return NextDate

def GetClosingPrice():
    return round(data["Close"].iloc[-1], 2)

def GetClosingPriceDate():
    return data.index[-1].strftime("%d/%m/%y")

def GoldDashBoard(request):
    #Added

    context = {
        'ClosingPricePlot_div' : PlotClosingPrice(),
        'PredictionPlot_div' : PredictionPlot(),
        'CumulativeReturns_div' : CumulativeReturns(),
        'SharpeRatio' : SharpeRatioCalculate(),
        'S_3' : MovingAverage_S3(),
        'S_9' : MovingAverage_S9(),
        'Signal' : GetSignal(),
        'PredictedPrice' : GetPredictedPrice(),
        'NextDate' : GetNextDay(),
        'ClosingPrice' : GetClosingPrice(),
        'ClosingDate' : GetClosingPriceDate(),
    }

    #Ended
    return render(request, 'myshop/dashboard.html', context)


#----------machine learning chat bot ----------------
import os
import json
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from google import genai

# ⚠️ Use env variable in production
client = genai.Client(api_key="AIzaSyAb4OWFMpbUGF3g9CYSuIqbz_0NH69yHP0")

# ---- Price Formatter (PKR only) ----
def format_price_in_pkr(value):
    try:
        value = float(value)
        if value >= 10_000_000:  # Convert to Crore
            return f"{value/10_000_00:.2f} Crore PKR"
        elif value >= 1_000_000:  # Convert to Million
            return f"{value/1_000_000:.2f} Million PKR"
        else:
            return f"{int(value):,} PKR"
    except:
        return "N/A"
    
import os
import json
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

@csrf_exempt
def chatbot(request):
    user_input = ""
    bot_response = ""

    excel_file_path = os.path.join("media", "Gold1.xls")

    df = None
    try:
        df = pd.read_excel(excel_file_path)

        # Keep only useful columns
        useful_columns = ["Date", "Open", "High", "Low", "Close"]
        df = df[[col for col in useful_columns if col in df.columns]].dropna()

        # Convert Date to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        # Sort by Date
        df = df.sort_values("Date")

    except Exception as e:
        print(f"⚠️ Excel load failed: {e}")

    if request.method == "POST":
        try:
            if request.headers.get("Content-Type") == "application/json":
                data = json.loads(request.body)
                user_input = data.get("message", "")
            else:
                user_input = request.POST.get("message", "")
        except Exception:
            return JsonResponse({"response": "Invalid request."})

        if user_input and df is not None:

            # Prepare data for prediction
            df["Day"] = np.arange(len(df))  # numerical index for regression
            X = df[["Day"]]
            y = df["Close"]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

            model = LinearRegression()
            model.fit(X_train, y_train)

            # Last known price
            latest_price = df["Close"].iloc[-1]
            latest_date = df["Date"].iloc[-1].strftime("%Y-%m-%d")

            # Predict next day's price
            next_day = [[df["Day"].iloc[-1] + 1]]
            predicted_price = model.predict(next_day)[0]

            # Decide response based on user input
            if "today" in user_input.lower():
                bot_response = f"Today ({latest_date}), the gold closing price is PKR {latest_price:,.2f}"
            elif "tomorrow" in user_input.lower() or "next" in user_input.lower():
                bot_response = f"Predicted gold price for tomorrow is around PKR {predicted_price:,.2f}"
            elif "price" in user_input.lower() or "gold" in user_input.lower():
                bot_response = (
                    f"Latest gold closing price ({latest_date}) is PKR {latest_price:,.2f}.\n"
                    f"Predicted next day price: PKR {predicted_price:,.2f}"
                )
            else:
                bot_response = "I can provide gold prices (today, tomorrow, future trend). Please ask me about gold."

            if request.headers.get("Content-Type") == "application/json":
                return JsonResponse({"response": bot_response})

    return render(request, "myshop/chatbot.html", {
        "user_input": user_input,
        "bot_response": bot_response
    })

from django.http import JsonResponse

def get_city_location(request):
    import pandas as pd, os

    excel_file_path = os.path.join('media', 'world_real_estate_data.xls')
    df = pd.read_excel(excel_file_path)

    country = request.GET.get("city")

    cities, locations = [], []
    if country and "city" in df.columns:
        filtered = df[df["city"] == country]
        if "city" in filtered.columns:
            cities = sorted(filtered["city"].dropna().unique().tolist())
        if "location" in filtered.columns:
            locations = sorted(filtered["location"].dropna().unique().tolist())

    return JsonResponse({"cities": cities, "locations": locations})
