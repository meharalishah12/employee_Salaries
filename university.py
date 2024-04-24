import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# @st.cache
def load_data():
    return pd.read_csv('higher_ed_employee_salaries.csv')

data = load_data()

# Page configurations
st.set_page_config(
    page_title="Higher Education Analysis",
    page_icon=":chart_with_downwards_trend:",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
}
.sidebar{
    background-color: #fff;
}
.desc{
border: 2px solid white;
// width = 50px;
padding: 0 20px;
margin: 0px 20px 20px 10px;
border-radius: 20px;
}
.footer {
        position: fixed;
        bottom: 0;
        width: 100vw;
        color: white;
        background: black;
        text-align: center;
        z-index: 10000;
        left: -1px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_option('deprecation.showPyplotGlobalUse', False)
# Create navigation bar
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "EDA", 'Visualization'])
    page = page.split(" ")[0]
    data = pd.read_csv('higher_ed_employee_salaries.csv')
    df = data.copy()
    if page == "Home":
        st.title("Welcome to Higher Education Employee Analysis App")
        st.write("This app helps you analyze education employee data.")
        st.markdown("""
#### Information about columns
* **Name:** The name of the employee \n
* **School:**  The name of the school where the employee works\n
* **Job Description:** Description of the job or position held by the employee\n
* **Department:** The department within the school where the employee works\n
* **Earnings:** The earnings of the employee\n
* **Year:** The year associated with the earnings data\n
                    
#### Preferred Payment Method
* **Preferred Payment Method:** Cash, Credit/Debit Card, Mobile Payment App\n
""")

    elif page == "EDA":
        st.title("Exploratory Data Analysis")
        st.markdown("""
<p class="desc">This section provides an overview of the dataset through various analytical components. It includes descriptive statistics, data types, and the shape of the dataset. Use the sections below to explore different aspects of the dataset.</p>
""",unsafe_allow_html=True)
        # Add your data analysis components here
        st.header("Data Set")
        st.dataframe(df.head())
        st.markdown("#### Shape of Data")
        st.markdown("""
<p class="desc">Here, you can see the dimensions of the dataset represented as rows and columns. This information gives you an understanding of the dataset's size and structure.</p>
""",unsafe_allow_html=True)
        st.write(df.shape)
        st.markdown("### Data Types")
        st.markdown("""
<p class="desc">
                    Explore the data types of each column in the dataset. Understanding the data types is crucial for data preprocessing and analysis.
                    </p>
""",unsafe_allow_html=True)
        st.write(df.dtypes)

        st.markdown("## Descriptive Statistic of Data")
        st.markdown("""
<p class="desc">
                    Get insights into the central tendencies and spread of numerical features in the dataset. These descriptive statistics help in understanding the distribution and variability of the data.
                    </p>
""",unsafe_allow_html=True)
        st.write(df.describe())

        st.markdown("")
        
        
    elif page == "Visualization": 
        # Pie Chart
        catigories = ['Name','School','Job Description','Department','Year']
        st.title("Pie Chart")
        cat = st.selectbox("Select Categories ",catigories)
        # Add your visualization components
        st.markdown(f"""
        <h3>Distribution of {cat.capitalize().replace('_'," ")} in the Data Set </h3>
        """,unsafe_allow_html=True)
        st.markdown(f"""
        <p class="desc">The Pie Chart Vizualize the Distribution of {cat.capitalize().replace('_'," ")} among  the total employee in the Data Set. It provides insigts into the portions of different {cat.capitalize().replace('_'," ")} values, allowing for the quick understanding of the dataset's composition. Use the dropdown menu to select different categories to explore </p>
        """,unsafe_allow_html=True)
        fig, ax_pie = plt.subplots()
        major_counts = data[cat].value_counts()
        plt.figure(figsize=(4, 8))
        ax_pie.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', startangle=140)
        ax_pie.axis('equal')
        ax_pie.legend(title="Legend", loc="upper right", fontsize="small", fancybox=True,bbox_to_anchor=(2, 1))
        ax_pie.set_title(f"{cat.capitalize().replace('_',' ')} Percentage in Data set.")
        sns.scatterplot(x='Year', y='Earnings', data=df)
        plt.title('Relationship between Earnings and Year')
        plt.xlabel('Year')
        plt.ylabel('Earnings')
        plt.grid(True)  
        st.pyplot(fig)
        #Bar Chart
        fig, ax_pie = plt.subplots()
        st.title("Bar Chart")
        expenses_columns = ('School', 'Department','Earnings','Year') 
        cate = st.selectbox("Select ",expenses_columns)
        num_bin = 10
        num_bin = int(st.selectbox("No of School",range(10,1000,5)))
        fig, ax = plt.subplots()
        ax.bar(df.head(num_bin).index, df[cate].head(num_bin))
        ax.legend([cate], title="Legend", loc="upper right", fontsize="small", fancybox=True, bbox_to_anchor=(1.9, 1))
        plt.figure(figsize=(4, 8))
        sns.barplot(x='Year', y='Earnings', data=df)

        st.markdown(f"""
        <h3>Top  {num_bin} Students {cate.capitalize().replace("_"," ")} Earnings</h3>

        <p class="desc"> This bar plot displays the earning distribution of the top {num_bin} employee in the dataset across different categories. It offers insights into how the spending varies across categories for the selected group of students. Use the dropdown menus to select the spending category and the number of students to analyze.</p>

        """,unsafe_allow_html=True)
        ax.set_xlabel('Category')
        ax.set_ylabel('Earning ($)')
        ax.set_title(f'{cate.capitalize().replace("_"," ")} for top {num_bin} students')
        st.pyplot(fig)
        del fig, ax
        st.pyplot(fig)

        

    st.markdown("<footer class='footer'>© 2024 @meharali </footer>",unsafe_allow_html=True)




if __name__ == "__main__":
    
    main()