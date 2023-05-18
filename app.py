from unicodedata import category
import streamlit as st
import json
from Classifier import KNearestNeighbours
from operator import itemgetter

# Load data and movies list from corresponding JSON files
with open(r'data.json','r+',encoding='utf-8') as f:
    data = json.load(f)
with open(r'Model.json','r+',encoding='utf-8') as f:
    laptop_models = json.load(f)
with open(r'Category.json','r+',encoding='utf-8') as f:
    category = json.load(f)

def knn(test_point, k):
    # create dummy variables for the KNN classifier
    target = [0 for item in laptop_models]
    # Instantiate object for the classifier
    model = KNearestNeighbours(data,target,test_point,k=k)
    # Run the algorithum
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key = itemgetter(0))[-1]
    # Print list of 10 recommendations
    table = list()
    for i in model.indices:
        # Return back laptop model 
        table.append([laptop_models[i][0],laptop_models[i][2]])
    return table

if __name__ == '__main__':
    Manufacturer = ['Acer','Apple','Asus','Chuwi','Dell','Fujitsu','Google','HP','Huawei','LG','Lenovo',
    'MSI','Mediacom','Microsoft','Razer','Samsung','Toshiba','Vero','Xiaomi']
    laptops = [model[0] for model in laptop_models]
    st.header('Laptop Recommendation System')
    apps = ['---Select---','Company based', 'Category based' ]
    app_options = st.selectbox('Select application :',apps)
    super1 = ['Workstation',
 'Netbook',
 'Ultrabook',
 '2 in 1 Convertible',
 'Notebook',
 'Gaming']
    if app_options == 'Category based':
        laptop_select = st.selectbox('Select Category :',['--Select--'] + super1)
        if laptop_select == '--Select--':
            st.write('Select a Category')
        else:
            n = st.number_input('Number of laptops :',min_value = 5 , max_value=20,step=1)
            Manufacturer = data[category.index(laptop_select)]
            test_point = Manufacturer
            table = knn(test_point, n)
            for laptop, CPU in table:
                # Display model name with ram
                st.markdown(f"[{laptop}]({CPU})")

    elif app_options == apps[1]:
        options = st.multiselect('Select Manufactuere :',Manufacturer)
        if options:
            RAM = st.slider('RAM :',4 , 64, 8)
            n = st.number_input('Number of laptops :', min_value=5, max_value=20, step=1)
            test_point = [1 if manufacturer in options else 0 for manufacturer in Manufacturer ]
            test_point.append(RAM)
            table = knn(test_point,n)
            for laptop , CPU in table:
                # Display laptop model with CPU
                st.markdown(f"[{laptop}]({CPU})")

        else:
            st.write(" ")

    else:
        st.write('Select option')
        



