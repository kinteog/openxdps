from numpy import poly1d
import streamlit as st
import pandas as pd
# Data Viz Pkgs
import plotly.express as px 

import csv

from db_fxns import add_data, create_table, view_all_data, get_name, view_unique_name, edit_patient_data, delete_data, create_usertable, add_userdata, login_user,view_allusers,view_unique_user,get_authname,edit_authstatus,delete_user

@st.cache
def load_data():
    diabetes_dataset=pd.read_csv('diabetes.csv')
    return diabetes_dataset
def load_data1():
    heart_dataset=pd.read_csv('heart.csv')
    return heart_dataset
def load_data2():
    parkinson_dataset=pd.read_csv('parkinsons.csv')
    return parkinson_dataset
def load_data4():
    new_diabetes_dataset=pd.read_csv('newdiabetes.csv')
    return new_diabetes_dataset
def load_data5():
    new_heart_dataset=pd.read_csv('newheart.csv')
    return new_heart_dataset
def load_data6():
    new_parkinson_dataset=pd.read_csv('newparkinsons.csv')
    return new_parkinson_dataset
def load_data3():
    review_dataset=pd.read_csv('review.csv')
    return review_dataset


def show_adminn_page():
    st.title("Explore Admin page")

    st.write("You need to be logged in as qualified admin personnel to access database services.")
    st.sidebar.write("___________________________________________________________")
    authmenu = ["Login","Logout"]
    auth = st.sidebar.selectbox("Admin Login or Logout",authmenu)
    
    if auth == "Login":
        st.sidebar.write(" # Login Here #")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password" ,type="password")
        authstatus = "admin"
        if st.sidebar.checkbox("Login"):
            create_usertable()
            resultss = login_user(username,password,authstatus)
            #if password == "1234":
            if resultss:
                st.success("Succesfully logged in as {}".format(username))
            

                st.write(
                    """
                ### View Admin Dashboard
                """
                )
                

                menu = ["Add New Users","View All Users Details","Verify And Update Users Details","Delete Users Account" , "Data Analysis"]
                choice = st.selectbox("Menu",menu)
                create_table()

                if choice == "Add New Users":
                    st.subheader("Add User Details")
                    col1,col2 = st.columns(2)
                    col3,col4,col5 = st.columns(3)
                  

                    with col1:
                        new_username = st.text_input("User Full Name")
                    with col2:
                        new_email = st.text_input("User Email")
                    with col3:
                        new_regnumber = st.text_input("User Registration Number")
                        
                    with col4:
                        auth_status = st.selectbox("Authorization Status" , ("Pending","verified", "unverified", "admin"))
                    with col5:
                        new_password = st.text_input("Enter User Default Password" ,type="password")


                    add = st.button("Add User to database")
                    if add:
                        create_usertable()
                        add_userdata(new_username,new_password,new_email,new_regnumber,auth_status)
                        st.success("Successfully Signed Up New User")
                        
                        st.info("sucessfully added :: {} :: to auth database".format(new_username))
                elif choice == "View All Users Details":
                    st.subheader("View Database")
                    result = view_allusers()
                    #st.write(result)
                    df = pd.DataFrame(result,columns=['Name of User' ,'User Email','RegID Number.','Auth Status'])
                    with st.expander("View all User Data"):
                        st.dataframe(df)
                    with st.expander("Authentication Distribution  Summary"):
                        diabetis_df= df['Auth Status'].value_counts().to_frame()
                        diabetis_df = diabetis_df.reset_index()
                        st.dataframe(diabetis_df)
                        p1 = px.pie(diabetis_df,names='index',values='Auth Status')
                        st.plotly_chart(p1,use_container_width=True)
                    result3 = load_data3()
                    review_table = result3.drop(columns= 'User Email' , axis=1)
                            
                    with st.expander("View all Reviews"):
                            st.dataframe(review_table)

                        


                elif choice == "Verify And Update Users Details":
                    st.subheader("Edit / Update User Details")
                    with st.expander("View User Current Data"):
                        result = view_allusers()
                        df = pd.DataFrame(result,columns=['Name of User' ,'User Email','RegID Number.','Auth Status'])
                        st.dataframe(df)

                    list_of_name = [i [0] for i in view_unique_user()]
                    selected_name = st.selectbox("Choose User's Detail To Edit By Email",list_of_name)
                    selected_result = get_authname(selected_name)

                    st.subheader("View User Profile")

                    if selected_result:
                        

                        name = selected_result[0][0]
                        id = selected_result[0][1]
                        user_email = selected_result[0][2]
                        user_regno = selected_result[0][3]
                        auth_reference = selected_result[0][4]


         
                       

                        
                        
                        st.text (f"User Full Name: {name}")
                    
                        st.text(f"User Password : {id}")

                        st.text(f"User Email : {user_email}")

                        st.text(f"User Reg No. : {user_regno}")

                        st.text(f"User Auth Status : {auth_reference}")
            
                        update_authstatus = st.selectbox("User Auth Status" , ["pending","verified", "unverified","admin"])

                        
                    add = st.button("Update User details")
                    if add:
                        edit_authstatus(update_authstatus,auth_reference)
                        st.success("sucessfully updated :: {}'s :: user authentication status from :: {} :: to :: {} ::".format(name,auth_reference,update_authstatus))
                
                    with st.expander("View User Updated Data"):
                        result2 = view_allusers()
                        df2 = pd.DataFrame(result2,columns=['Name of User' ,'User Email','RegID Number.','Auth Status'])
                        st.dataframe(df2)
                elif choice == "Delete Users Account":
                    st.subheader("Delete User Profile")
                    with st.expander("View Users' Current Data"):
                        result = view_allusers()
                        df = pd.DataFrame(result,columns=['Name of User','User Email','RegID Number','Auth Status'])
                        st.dataframe(df)

                    list_of_name = [i [0] for i in view_unique_user()]
                    selected_name = st.selectbox("Select User's Detail To Delete",list_of_name)
                    st.warning("Do You Want To Delete  :: {}'s User Profile?".format(selected_name))
                    if st.button("Delete User Profile And Account"):
                        delete_user(selected_name)
                        st.success("User Profile Successfully deleted")
                    with st.expander("View Updated User Data"):
                        result3 = view_allusers()
                        df2 = pd.DataFrame(result3,columns=['Name of User' ,'User Email','RegID Number','Auth Status'])
                        st.dataframe(df2)
                elif choice == "Data Analysis":

                    st.write( """ ### more info on data used to train the models and project documentations""")
                    if st.button("View Diabetes Model Data Analysis"):
                        st.subheader("Dataset Used To Train And Test The Model")

                        result = load_data()
            
                        with st.expander("View all Data Used To Train And Test The Diabetes Model"):
                            st.dataframe(result)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset")
                        with st.expander("View The Distribution Of The Labelled Data"):
                            diabetis_df= result['Outcome'].value_counts().to_frame()
                            diabetis_df = diabetis_df.reset_index()
                            st.dataframe(diabetis_df)
                            p1 = px.pie(diabetis_df,names='index',values='Outcome')
                            st.plotly_chart(p1,use_container_width=True)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Age")
                        with st.expander("View The Distribution Of The Labelled Data Based on Age"):
                            data = result.groupby(["Age"])["Outcome"].mean().sort_values(ascending=True)
                            st.bar_chart(data)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Blood Pressure")
                        with st.expander("View The Distribution Of The Labelled Data Based on Blood Pressure"):

                            data = result.groupby(["BloodPressure"])["Outcome"].mean().sort_values(ascending=True)
                            st.line_chart(data)
                    if st.button("View heart Disease Model Data Analysis"):
                        st.subheader("Dataset Used To Train And Test The Model")


                        result = load_data1()
            
                        with st.expander("View all Data Used To Train And Test The Diabetis Model"):
                            st.dataframe(result)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset")
                        with st.expander("View The Distribution Of The Labelled Data"):
                            heart_df= result['target'].value_counts().to_frame()
                            heart_df = heart_df.reset_index()
                            st.dataframe(heart_df)
                            p1 = px.pie(heart_df,names='index',values='target')
                            st.plotly_chart(p1,use_container_width=True)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Chest Pain Type")
                        with st.expander("View The Distribution Of The Labelled Data Based on Chest Pain Type"):
                            data = result.groupby(["cp"])["target"].mean().sort_values(ascending=True)
                            st.bar_chart(data)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Age")
                        with st.expander("View The Distribution Of The Labelled Data Based on Age"):

                            data = result.groupby(["age"])["target"].mean().sort_values(ascending=True)
                            st.line_chart(data)
                    if st.button("View Parkinson's Disease Model Data Analysis"):
                        st.subheader("Dataset Used To Train And Test The Model")

                        result = load_data2()
            
                        with st.expander("View all Data Used To Train And Test The Diabetis Model"):
                            st.dataframe(result)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset")
                        with st.expander("View The Distribution Of The Labelled Data"):
                            parkinson_df= result['status'].value_counts().to_frame()
                            parkinson_df = parkinson_df.reset_index()
                            st.dataframe(parkinson_df)
                            p1 = px.pie(parkinson_df,names='index',values='status')
                            st.plotly_chart(p1,use_container_width=True)
                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On MDVP:Jitter(Abs)")
                        with st.expander("View The Distribution Of The Labelled Data Based on MDVP:Jitter(Abs)"):
                            data = result.groupby(["MDVP:Jitter(Abs)"])["status"].mean().sort_values(ascending=True)
                            st.bar_chart(data)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On MDVP:Jitter(%)")
                        with st.expander("View The Distribution Of The Labelled Data Based on Blood MDVP:Jitter(%)"):

                            data = result.groupby(["MDVP:Jitter(%)"])["status"].mean().sort_values(ascending=True)
                            st.line_chart(data)

                    if st.button("View New Diabetes Dataset Analysis"):
                        st.subheader("Dataset Collected From Patients To Train And Test The Model")

                        result = load_data4()
            
                        with st.expander("View all Data Used To Train And Test The Diabetes Model"):
                            st.dataframe(result)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset")
                        with st.expander("View The Distribution Of The Labelled Data"):
                            diabetis_df= result['Outcome'].value_counts().to_frame()
                            diabetis_df = diabetis_df.reset_index()
                            st.dataframe(diabetis_df)
                            p1 = px.pie(diabetis_df,names='index',values='Outcome')
                            st.plotly_chart(p1,use_container_width=True)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Age")
                        with st.expander("View The Distribution Of The Labelled Data Based on Age"):
                            data = result.groupby(["Age"])["Outcome"].mean().sort_values(ascending=True)
                            st.bar_chart(data)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Blood Pressure")
                        with st.expander("View The Distribution Of The Labelled Data Based on Blood Pressure"):

                            data = result.groupby(["BloodPressure"])["Outcome"].mean().sort_values(ascending=True)
                            st.line_chart(data)
                    if st.button("View New heart Disease Dataset Analysis"):
                        st.subheader("Dataset Used To Train And Test The Model")


                        result = load_data5()
            
                        with st.expander("View all Data Used To Train And Test The Diabetis Model"):
                            st.dataframe(result)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset")
                        with st.expander("View The Distribution Of The Labelled Data"):
                            heart_df= result['target'].value_counts().to_frame()
                            heart_df = heart_df.reset_index()
                            st.dataframe(heart_df)
                            p1 = px.pie(heart_df,names='index',values='target')
                            st.plotly_chart(p1,use_container_width=True)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Chest Pain Type")
                        with st.expander("View The Distribution Of The Labelled Data Based on Chest Pain Type"):
                            data = result.groupby(["cp"])["target"].mean().sort_values(ascending=True)
                            st.bar_chart(data)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On Age")
                        with st.expander("View The Distribution Of The Labelled Data Based on Age"):

                            data = result.groupby(["age"])["target"].mean().sort_values(ascending=True)
                            st.line_chart(data)
                    if st.button("View New Parkinson's Disease Dataset Analysis"):
                        st.subheader("Dataset Used To Train And Test The Model")

                        result = load_data6()
            
                        with st.expander("View all Data Used To Train And Test The Diabetis Model"):
                            st.dataframe(result)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset")
                        with st.expander("View The Distribution Of The Labelled Data"):
                            parkinson_df= result['status'].value_counts().to_frame()
                            parkinson_df = parkinson_df.reset_index()
                            st.dataframe(parkinson_df)
                            p1 = px.pie(parkinson_df,names='index',values='status')
                            st.plotly_chart(p1,use_container_width=True)
                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On MDVP:Jitter(Abs)")
                        with st.expander("View The Distribution Of The Labelled Data Based on MDVP:Jitter(Abs)"):
                            data = result.groupby(["MDVP:Jitter(Abs)"])["status"].mean().sort_values(ascending=True)
                            st.bar_chart(data)

                        st.subheader("The Distribution Of The Labelled Data On The Dataset Based On MDVP:Jitter(%)")
                        with st.expander("View The Distribution Of The Labelled Data Based on Blood MDVP:Jitter(%)"):

                            data = result.groupby(["MDVP:Jitter(%)"])["status"].mean().sort_values(ascending=True)
                            st.line_chart(data)


                    if st.button("View Project Documentation"):
                        st.subheader("About This Project")
                        with st.expander("View Project Documentation"):
                            st.subheader("about the project")
                            st.write("about the project")
                            st.write("about the project")
                        st.subheader("Disclaimer")
                        with st.expander("View View Disclaimer Documentation"):
                            st.subheader("project disclaimer")
                            st.write("project disclaimer")
                            st.write("project disclaimer")
                        st.subheader("Terms And Conditions")
                        with st.expander("View View Terms And Conditions Documentation"):
                            st.subheader("project Terms And Conditions")
                            st.write("project Terms And Conditions")
                            st.write("project Terms And Conditions")

                    
            else:  
                st.warning("Incorrect Username/Password Combination Or You Do Not Have Admin Authorization")    
    elif auth == "Signup":
        st.sidebar.write(" # SignUp Here #")
        new_username = st.sidebar.text_input("User Name")
        new_email = st.sidebar.text_input("Email Address")
        new_regnumber = st.sidebar.text_input("Registration Number")
        confirm_password = st.sidebar.text_input("Password" ,type="password")
        new_password = st.sidebar.text_input("Confirm Password" ,type="password")
        if st.sidebar.checkbox("SignUp"):
            if confirm_password == new_password:
                create_usertable()
                add_userdata(new_username,new_password,new_email,new_regnumber)
                st.success("Successfully Signed Up")
                st.info("Go to Login Tab to Login to the service")
            else:
                st.warning("SignUp Unsuccessful!")
                st.info("Make sure the passwords entered match each other")
    elif auth == "Logout":
        st.info("Successfully Logged out")
        st.write("You are currently logged out")