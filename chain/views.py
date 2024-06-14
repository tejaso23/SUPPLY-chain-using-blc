from email.policy import default
from django.shortcuts import render, HttpResponse, redirect
from audioop import add
from .forms import SignUpForm, LoginForm, ImageForm
from distutils.command.build import build
from itertools import chain
from math import ceil
from PayTm import Checksum
import json
from operator import index
from web3 import Web3
from chain.models import cropImage, ChainUser, Orders, OrderUpdate, Product
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login, logout

from statistics import multimode
import numpy as np
import pandas as pd
from collections import OrderedDict

import csv
import matplotlib.pyplot as plt
import sys
from statistics import multimode
from collections import OrderedDict

# Create your views here.
# from brownie import Crop


web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

print(web3.isConnected())

privateaddress = Web3.toChecksumAddress(
    "0x0188F076ccbE70fB53078432C7DE6454CDBF6215")

privateabi = [
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "prod_id",
          "type": "uint256"
        }
      ],
      "name": "retreive_distributor_details",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "prod_id",
          "type": "uint256"
        }
      ],
      "name": "retreive_prod_details",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "prod_id",
          "type": "uint256"
        }
      ],
      "name": "retreive_retailer_details",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_prod_id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_distributorname",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_dkycid",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_daddress",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_dcontact",
          "type": "uint256"
        }
      ],
      "name": "store_distributor_details",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_prod_id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_cropname",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_fname",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_faddress",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_prodname",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_prodprice",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_manudate",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_processnames",
          "type": "string"
        }
      ],
      "name": "store_prod_details",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_prod_id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_retailername",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_rkycid",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_raddress",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_rcontact",
          "type": "uint256"
        }
      ],
      "name": "store_retailer_details",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]

web3.eth.defaultAccount = web3.eth.accounts[0]

privatecontract = web3.eth.contract(address=privateaddress, abi=privateabi)


def index(request):
    crop_context = None
   
    if 'addrecordbtn' in request.POST:
        prod_id = int(request.POST.get('prodid'))
        cropname = request.POST.get('cropname')
        fname = request.POST.get('farmername')
        faddress = request.POST.get('farmeraddress')
        prodname = request.POST.get('productname')
        prodprice = int(request.POST.get('productprice'))
        prodcat = request.POST.get('productcategory')
        prodsubcat = request.POST.get('productsubcategory')
        prodqt = int(request.POST.get('productquantity'))
        proddesc = request.POST.get('productdesc')
        prodimg = request.FILES['upload_img']
        # product_details=Product()
        # product_details.save(prodimage.name,prodimage)
        manudate = request.POST.get('manudate')
        processnames = request.POST.get('processname')
        # if request.method == 'POST':
        #     form = ImageForm(request.POST, request.FILES)
        #     form.save()
        # if request.method == request.FILES:
        #     prodimage = request.FILES['upload_img']
        #     Product.objects.create(image=prodimage).save()
        #     print(prodimage)
        #     return prodimage
        product_details = Product(image = prodimg,product_id=prod_id, cropused=cropname, farmer_name=fname, farmer_address=faddress, product_name=prodname, product_price=prodprice,
                                  manu_date=manudate, process_used=processnames, product_category=prodcat, subcategory=prodsubcat, product_qt=prodqt, desc=proddesc)
        # prodimg = Product.objects.create(image=prodimage)
        product_details.save()
        prodrecord = privatecontract.functions.store_prod_details(
            prod_id, cropname, fname, faddress, prodname, prodprice, manudate, processnames).transact()
        web3.eth.waitForTransactionReceipt(prodrecord)

        # dname = request.POST.get('distributorname')
        # dkycid = int(request.POST.get('dkycid'))
        # dcity = request.POST.get('dcity')
        # dstate = request.POST.get('dstate')
        # dpincode = int(request.POST.get('dpincode'))
        # dcontact = int(request.POST.get('dcontact'))

        # distributorrecord=privatecontract.functions.store_distributor_details(fid,dname,dkycid,dcity,dstate,dpincode,dcontact).transact()
        # web3.eth.waitForTransactionReceipt(distributorrecord)

        # rname = request.POST.get('retailername')
        # rkycid = int(request.POST.get('rkycid'))
        # rcity = request.POST.get('rcity')
        # rstate = request.POST.get('rstate')
        # rpincode = int(request.POST.get('rpincode'))
        # rcontact = int(request.POST.get('rcontact'))

        # distributorrecord=privatecontract.functions.store_retailer_details(fid,rname,rkycid,rcity,rstate,rpincode,rcontact).transact()
        # web3.eth.waitForTransactionReceipt(distributorrecord)

        # croppic = request.FILES['imgfile']
        # cropImage = cropImage.objects.create(image=croppic)
        # cropImage.save()
        allcroppic = cropImage.objects.all()
        # allcroppic.save()
        context = {'allcroppic': allcroppic}
        # print(fid,fname,cname,qt,price,gender)
        # CropImage = cropImage(fid=fid, cname=cname, croppic=croppic)

        render(request, 'index.html', context)
    elif 'searchbtn' in request.POST:
        prod_id = int(request.POST.get('s_farmerid'), False)
        outputvalue = privatecontract.functions.retreive_prod_details(
            prod_id).call()
        print(outputvalue)
        outputdistributor = privatecontract.functions.retreive_distributor_details(
            prod_id).call()
        print(outputdistributor)
        outputretailer = privatecontract.functions.retreive_retailer_details(
            prod_id).call()
        print(outputretailer)
        crop_context = {
            'Oprodid': outputvalue[0],
            'Ocropname': outputvalue[1],
            'Ofname': outputvalue[2],
            'Ofaddress': outputvalue[3],
            'Oprodname': outputvalue[4],
            'Oprodprice': outputvalue[5],
            'Omanudate': outputvalue[6],
            'Oprocessname': outputvalue[7],





            'Odistributorname': outputdistributor[1],
            'Odkycid': outputdistributor[2],
            'Odaddress': outputdistributor[3],
            # 'Odstate' : outputdistributor[4],
            # 'Odpincode' : outputdistributor[5],
            'Odcontact': outputdistributor[4],


            'Oretailername': outputretailer[1],
            'Orkycid': outputretailer[2],
            'Oraddress': outputretailer[3],
            # 'Orstate' : outputretailer[4],
            # 'Orpincode' : outputretailer[5],
            'Orcontact': outputretailer[4],

        }
        # farmer_context = {
        #     'Ofarmername' : outputfarmer[1],
        #     'Ofkycid' : outputfarmer[2],
        #     'Ofcity' : outputfarmer[3],
        #     'Ofstate' : outputfarmer[4],
        #     'Ofpincode' : outputfarmer[5],
        #     'Ofcontact' : outputfarmer[6],
        # }
        # distributor_context = {
        #     'Odistributorname' : outputdistributor[1],
        #     'Odkycid' : outputdistributor[2],
        #     'Odcity' : outputdistributor[3],
        #     'Odstate' : outputdistributor[4],
        #     'Odpincode' : outputdistributor[5],
        #     'Odcontact' : outputdistributor[6],
        # }
        # retailer_context = {
        #     'Oretailername' : outputretailer[1],
        #     'Orkycid' : outputretailer[2],
        #     'Orcity' : outputretailer[3],
        #     'Orstate' : outputretailer[4],
        #     'Orpincode' : outputretailer[5],
        #     'Orcontact' : outputretailer[6],
        # }
        # render(request, 'index.html', context)
        # print())
        # print(outputvalue[1])
        # print(outputvalue[2])
        # print(type(outputvalue))
        # print(outputvalue)
        # return context
    return render(request, 'index.html', crop_context)

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
def userHome(request):
  # Load the data from the CSV file
 
  
  data = pd.read_csv("C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//media//Product-1.csv")
  # Define the independent and dependent variables
  X = data[['Product_id', 'Product_Name', 'Crop_Used', 'Location', 'Purchased_Or_Not']]
  y = data['Crop_demand']
  X = pd.get_dummies(X, columns=['Product_Name', 'Crop_Used','Location'], drop_first=True)

  # Split the data into training and test sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Create a LinearRegression object
  model = LinearRegression()

  # Fit the model to the training data
  model.fit(X_train, y_train)

  # Make predictions on the test data
  y_pred = model.predict(X_test)

  # Plot the predicted values against the actual values
  plt.scatter(y_test, y_pred)
  plt.xlabel('Actual Values')
  plt.ylabel('Predicted Values')
  # plt.show()

  # Calculate the mean squared error
  mse = mean_squared_error(y_test, y_pred)

  # Calculate the mean absolute error
  mae = mean_absolute_error(y_test, y_pred)

  # Print the mean squared error and mean absolute error
  print('Mean Squared Error:', mse)
  print('Mean Absolute Error:', mae)

  
  # Create a Lasso object with a regularization parameter of 0.1
  lasso = Lasso(alpha=0.1)

  # Fit the Lasso model to the training data
  lasso.fit(X_train, y_train)

  # Make predictions on the test data
  y_pred_lasso = lasso.predict(X_test)

  # Plot the predicted values against the actual values
  plt.scatter(y_test, y_pred_lasso)
  plt.xlabel('Actual Values')
  plt.ylabel('Predicted Values')
  # plt.show()

  # Group the data by crop and sum the demand
  crop_demand = data.groupby('Crop_Used')['Crop_demand'].sum()

  # Find the crop with the highest demand
  high_demand_crop = crop_demand.idxmax()

  # Print the crop with the highest demand
  print('Crop with highest demand:', high_demand_crop)


  # Filter the data to only show the high-demand crop
  high_demand_data = crop_demand[crop_demand.index == high_demand_crop]

  # Create a line graph showing the demand for the high-demand crop
  plt.plot(high_demand_data)

  # Add axis labels
  plt.xlabel('Year')
  plt.ylabel('Demand')

  # Show the graph
  # plt.show()

  # Group the data by crop and sum the demand
  crop_demand = data.groupby('Crop_Used')['Crop_demand'].sum()

  # Sort the data in descending order of demand
  crop_demand = crop_demand.sort_values(ascending=False)

  # Select the top 5 crops with the highest demand
  top_5_crops = crop_demand.head(5)
  crop_demand_list=crop_demand.index.tolist()
  print(crop_demand_list)

  # Plot the top 5 crops and their demand using a bar graph
  top_5_crops.plot(kind='bar')
  plt.xlabel('Crop')
  plt.ylabel('Demand')
  # plt.show()
  # Save the figure as an image file
  plt.savefig("C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//media//graph.png")
  plt.savefig("C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//static//Graph//graph.png")


# 
  # plt.show()
  crop=None
  prod_id = None
        
  # data = pd.read_csv('C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//media//Product-1.csv')
  # A = data['Crop_Used'].values
  # frequency = {}

  # for item in A:
  #   if item in frequency:
  #       frequency[item] += 1
  #   else:
  #       frequency[item] = 1

  # # print(frequency)


  # keys = list(frequency.keys())
  # values = list(frequency.values())
  # sorted_value_index = np.argsort(values)
  # sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

  # # print(sorted_dict)

  # sort_data = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
  # sort_data_dict = dict(sort_data)
  # sort_data_dict.keys()

  # print(*A, sep = "\n")


  # print("This is the crops ")
  # print(A)





  # crop = {
  #   'crop_output1' : crops[0],
  #   'crop_output2' : crops[1],
  #   'crop_output3' : crops[2],
  #   'crop_output4' : crops[3],
  #   'crop_output5' : crops[4],
  #   'crop_output6' : crops[5],
  # }
  

  # data = pd.read_csv('C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//media//Product.csv')
  # A = data['cropused'].values
  # frequency = {}


  # for item in A:
  #   if item in frequency:
  #       frequency[item] += 1
  #   else:
  #       frequency[item] = 1

  # print(frequency)


  # keys = list(frequency.keys())
  # values = list(frequency.values())
  # sorted_value_index = np.argsort(values)
  # sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

  # # print(sorted_dict)

  # sort_data = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
  # sort_data_dict = dict(sort_data)
  # sort_data_dict.keys()


  # # Line Graph Code
  # graph_names = list(sort_data_dict.keys())
  # graph_values = list(sort_data_dict.values())
  # plt.plot(graph_names,graph_values)
  # plt.savefig("C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//static//Graph//graph.png", dpi=550)
  # plt.show()//
        #prod_id=None



  if 'searchrecordbtn' in request.POST:
  # if  request.method == 'POST':
      prod_id = request.POST.get('search_input')
      # global searchs_fid

      # print(type(prod_id))
      print(prod_id)

  #   request.session['search'] = s_fid
  #   print(request.session['search_input'])
      
      return redirect(request, 'search/<prodid>', prod_id)
        
  return render(request,  'User/Userhome.html', {'prod_id':prod_id, 'crop_demand_list':crop_demand_list})


def userSearch(request, prodid):
  print(prodid)
  temp_prod = int(prodid)

  crop_context = None
  # if request.method == 'POST':
    # print(type(prod_id))
    # print(prod_id)
    # prod_id= int(param)
    
    
  outputvalue = privatecontract.functions.retreive_prod_details(temp_prod).call()
  print(outputvalue)

  outputdistributor = privatecontract.functions.retreive_distributor_details(
      temp_prod).call()
  print(outputdistributor)
  outputretailer = privatecontract.functions.retreive_retailer_details(
      temp_prod).call()
  print(outputretailer)

  crop_context = {
      'Oprodid': outputvalue[0],
      'Ocropname': outputvalue[1],
      'Ofname': outputvalue[2],
      'Ofaddress': outputvalue[3],
      'Oprodname': outputvalue[4],
      'Oprodprice': outputvalue[5],
      'Omanudate': outputvalue[6],
      'Oprocessname': outputvalue[7],





      'Odistributorname': outputdistributor[1],
      'Odkycid': outputdistributor[2],
      'Odaddress': outputdistributor[3],
      # 'Odstate' : outputdistributor[4],
      # 'Odpincode' : outputdistributor[5],
      'Odcontact': outputdistributor[4],


      'Oretailername': outputretailer[1],
      'Orkycid': outputretailer[2],
      'Oraddress': outputretailer[3],
      # 'Orstate' : outputretailer[4],
      # 'Orpincode' : outputretailer[5],
      'Orcontact': outputretailer[4],
  }
  # return s_fid
  # render(request,  'User/search.html', s_fid,  crop_context)
  return render(request, 'User/search.html', crop_context)
  


# def addrecord(request):
    # if request.method == "POST":
    #     fid = int(request.POST.get('farmerid'), False)
    #     fname = request.POST.get('farmername')
    #     cname = request.POST.get('cropname')
    #     qt = int(request.POST.get('cropqt'))
    #     price = int(request.POST.get('cropprice'))
    #     gender = request.POST.get('gender')
    # fid = int(request.GET['farmerid'])
    # fname = request.GET['farmername']
    # cname = request.GET['cropname']
    # qt = int(request.GET['cropqt'])
    # price = int(request.GET['cropprice'])
    # gender = request.GET['gender']
    #     print(fid,fname,cname,qt,price,gender)

    # privaterecord=privatecontract.functions.store_crop_details(fid,fname,cname,qt,price,gender).transact()
    # web3.eth.waitForTransactionReceipt(privaterecord)

    # return render(request, 'index.html')


# def handleSignUp(request):
#     if request.method=="POST":
#         # Get the post parameters
#         username=request.POST['username']
#         email=request.POST['email']
#         # fname=request.POST['fname']
#         # lname=request.POST['lname']
#         pass1=request.POST['pass1']
#         pass2=request.POST['pass2']

#         # check for errorneous input
#         if len(username) > 10:
#             messages.error(request, " Your user name must be under 10 characters")
#             return redirect('userhome')

#         if not username.isalnum():
#             messages.error(request, " User name should only contain letters and numbers")
#             return redirect('userhome')

#         if (pass1!= pass2):
#              messages.error(request, " Passwords do not match")
#              return redirect('userhome')

#         # Create the user
#         myuser = User.objects.create_user(username, email, pass1)
#         # myuser.first_name= fname
#         # myuser.last_name= lname
#         myuser.save()
#         messages.success(request, " Your MetaBlog Account has been successfully created")
#         return redirect('userhome')

#     else:
#         return HttpResponse("404 - Not found")


def register(request):
    msg = None
    userdoc = None
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            print(user)

            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
        userdoc = ChainUser.objects.all()
    return render(request, 'register.html', {'form': form, 'msg': msg, 'userimg': userdoc})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_purchaser:
                login(request, user)

                return redirect('admin')
            elif user is not None and user.is_distributor:
                login(request, user)
                return redirect('distributor')
            elif user is not None and user.is_retailor:
                login(request, user)
                return redirect('retailor')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


# def admin(request):
#     return render(request,'admin.html')


# ***************************************Authentication APIS****************************************


# def handeLogin(request):
#     if request.method=="POST":
#         # Get the post parameters
#         loginusername=request.POST['loginusername']
#         loginpassword=request.POST['loginpassword']

#         user=authenticate(username= loginusername, password= loginpassword)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Successfully Logged In")
#             return redirect("userpanel")
#         else:
#             messages.error(request, "Invalid credentials! Please try again")
#             return redirect("userhome")

#     return HttpResponse("404- Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('login_view')


def userPanel(request):
    return render(request, 'User/userPanel.html')


def Distributor(request):
    crop_context = None
    allProds = []
    catprods = Product.objects.values('product_category', 'id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    render(request, "Admin/Distributor.html", params)

    if 'searchrecordbtn' in request.POST:

        prod_id = int(request.POST.get('search_input'), False)
        outputvalue = privatecontract.functions.retreive_prod_details(prod_id).call()
        print(outputvalue)
        

        crop_context = {

            'Oprodid': outputvalue[0],
            'Ocropname': outputvalue[1],
            'Ofname': outputvalue[2],
            'Ofaddress': outputvalue[3],
            'Oprodname': outputvalue[4],
            'Oprodprice': outputvalue[5],
            'Omanudate': outputvalue[6],
            'Oprocessname': outputvalue[7],
        }
        return render(request, 'Admin/Distributor.html', crop_context)
    return render(request, 'Admin/Distributor.html', params, crop_context)

    # elif 'addrecordbtn' in request.POST:
    #     prod_id = int(request.POST.get('prodid'))
    #     # dname = request.POST.get('distributorname')
    #     dname = request.user.first_name + " " + request.user.last_name

    #     dkycid = int(request.user.user_kyc)

    #     daddress = request.user.user_address
    #     # daddress = request.POST.get('daddress')
    #     # dstate = request.POST.get('dstate')
    #     # dpincode = int(request.POST.get('dpincode'))
    #     # dcontact = int(request.POST.get('dcontact'))
    #     dcontact = int(request.user.phoneno)
    #     # dcontact = int(request.POST.get(user.))

    #     distributorrecord = privatecontract.functions.store_distributor_details(prod_id, dname, dkycid, daddress, dcontact).transact()
    #     web3.eth.waitForTransactionReceipt(distributorrecord)



def Retailor(request):
    crop_context = None
    allProds = []
    catprods = Product.objects.values('product_category', 'id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    render(request, "Admin/Retailor.html", params)

    if 'searchrecordbtn' in request.POST:
        s_fid = int(request.POST.get('search_input'), False)
        outputvalue = privatecontract.functions.retreive_crop_details(
            s_fid).call()
        print(outputvalue)
        outputfarmer = privatecontract.functions.retreive_farmer_details(
            s_fid).call()
        print(outputfarmer)
        outputdistributor = privatecontract.functions.retreive_distributor_details(
            s_fid).call()
        print(outputdistributor)

        crop_context = {
            'Ofarmerid': outputvalue[0],
            'Ocropname': outputvalue[1],
            'Ocropqt': outputvalue[2],
            'Ocropprice': outputvalue[3],
            'Osdate': outputvalue[4],

            'Ofarmername': outputfarmer[1],
            'Ofkycid': outputfarmer[2],
            'Ofaddress': outputfarmer[3],
            # 'Ofstate' : outputfarmer[4],
            # 'Ofpincode' : outputfarmer[5],
            'Ofcontact': outputfarmer[4],

            'Odistributorname': outputdistributor[1],
            'Odkycid': outputdistributor[2],
            'Odaddress': outputdistributor[3],
            # 'Odstate' : outputdistributor[4],
            # 'Odpincode' : outputdistributor[5],
            'Odcontact': outputdistributor[4],

        }
        return render(request, 'Admin/Retailor.html', crop_context)

    elif 'addrecordbtn' in request.POST:
        fid = int(request.POST.get('farmerid'))
        rname = request.user.first_name + " " + request.user.last_name
        rkycid = int(request.user.user_kyc)
        raddress = request.user.user_address
        # rstate = request.POST.get('rstate')
        # rpincode = int(request.POST.get('rpincode'))
        rcontact = int(request.user.phoneno)

        distributorrecord = privatecontract.functions.store_retailer_details(
            fid, rname, rkycid, raddress, rcontact).transact()
        web3.eth.waitForTransactionReceipt(distributorrecord)

    return render(request, 'Admin/Retailor.html', params)


# def Verified(request):
#     if 'addrecordbtn' in request.POST:
#         prod_id = int(request.POST.get('prodid'))
#         # dname = request.POST.get('distributorname')
#         dname = request.user.first_name + " " + request.user.last_name

#         dkycid = int(request.user.user_kyc)

#         daddress = request.user.user_address
#         # daddress = request.POST.get('daddress')
#         # dstate = request.POST.get('dstate')
#         # dpincode = int(request.POST.get('dpincode'))
#         # dcontact = int(request.POST.get('dcontact'))
#         dcontact = int(request.user.phoneno)
#         # dcontact = int(request.POST.get(user.))

#         distributorrecord = privatecontract.functions.store_distributor_details(
#             prod_id, dname, dkycid, daddress, dcontact).transact()
#         web3.eth.waitForTransactionReceipt(distributorrecord)
#         return 

def productView(request, myid):
    if 'addrecordbtn' in request.POST:
        if request.user.is_distributor == True:
            prod_id = int(request.POST.get('prodid'))
            print(prod_id)
            # dname = request.POST.get('distributorname')
            dname = request.user.first_name + " " + request.user.last_name

            dkycid = int(request.user.user_kyc)

            daddress = request.user.user_address
            # daddress = request.POST.get('daddress')
            # dstate = request.POST.get('dstate')
            # dpincode = int(request.POST.get('dpincode'))
            # dcontact = int(request.POST.get('dcontact'))
            dcontact = int(request.user.phoneno)
            # dcontact = int(request.POST.get(user.))

            distributorrecord = privatecontract.functions.store_distributor_details(
                prod_id, dname, dkycid, daddress, dcontact).transact()
            web3.eth.waitForTransactionReceipt(distributorrecord)
            product = Product.objects.filter(id=myid)
            return render(request, 'Admin/prodView.html', {'product': product[0]})
        elif request.user.is_retailor == True:
            prod_id = int(request.POST.get('prodid'))
            rname = request.user.first_name + " " + request.user.last_name
            rkycid = int(request.user.user_kyc)
            raddress = request.user.user_address
            # rstate = request.POST.get('rstate')
            # rpincode = int(request.POST.get('rpincode'))
            rcontact = int(request.user.phoneno)

            retailorrecord = privatecontract.functions.store_retailer_details(
                prod_id, rname, rkycid, raddress, rcontact).transact()
            web3.eth.waitForTransactionReceipt(retailorrecord)
            product = Product.objects.filter(id=myid)
            return render(request, 'Admin/prodView.html', {'product': product[0]})
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'Admin/prodView.html', {'product': product[0]})


MERCHANT_KEY = 'x8M5lZ0HDk!Ho%mQ'


def checkout(request):
    prod_id = ""
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        prod_id = request.POST.get('prodid')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # Request paytm to transfer the amount to your account after payment by user

        # prod_id = int(request.POST.get('prodid'))
        # dname = request.POST.get('distributorname')
        # dname = request.user.first_name + " " + request.user.last_name

        # dkycid = int(request.user.user_kyc)

        # daddress = request.user.user_address
        # # daddress = request.POST.get('daddress')
        # # dstate = request.POST.get('dstate')
        # # dpincode = int(request.POST.get('dpincode'))
        # # dcontact = int(request.POST.get('dcontact'))
        # dcontact = int(request.user.phoneno)
        # dcontact = int(request.POST.get(user.))

        # distributorrecord = privatecontract.functions.store_distributor_details(
        #     prod_id, dname, dkycid, daddress, dcontact).transact()
        # web3.eth.waitForTransactionReceipt(distributorrecord)
        render(request, 'Admin/Distributor.html', {'thank':thank, 'id': id, 'product_id':prod_id})


    return render(request, 'Admin/checkout.html', {'product_id':prod_id})








def recomendation(request):
  data = pd.read_csv('C://Users//USER//Desktop//FOOD-Chain//FOOD_SUPPLY//media//Product-2022-12-16.csv')
  A = data['cropused'].values
  frequency = {}


  for item in A:
    if item in frequency:
        frequency[item] += 1
    else:
        frequency[item] = 1

  # print(frequency)


  keys = list(frequency.keys())
  values = list(frequency.values())
  sorted_value_index = np.argsort(values)
  sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

  # print(sorted_dict)

  sort_data = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
  sort_data_dict = dict(sort_data)
  sort_data_dict.keys()


  print(A)

  #def most_crop():
  #    print(pd.Series(A).value_counts())

  #def most_crop_multimode():
  #    return multimode(A)

  #print(most_crop())

  #print(most_crop_multimode())

  #print(list(most_crop()))
  return HttpResponse('Working')