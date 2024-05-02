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
        #Pie Chart
        categories = ['School','Year']
        st.title("Pie Chart")
        cat = st.selectbox("Select Category", categories)


        st.markdown(f"""
    <h3>Distribution of {cat.capitalize().replace('_'," ")} in the Data Set</h3>
    <p class="desc">The Pie Chart visualizes the distribution of {cat.capitalize().replace('_'," ")} among the total employees in the data set. 
    It provides insights into the portions of different {cat.capitalize().replace('_'," ")} values, allowing for a quick understanding of the dataset's composition. 
    Use the dropdown menu to select different categories to explore.</p>
""", unsafe_allow_html=True)

        category_counts = data[cat].value_counts()
        sorted_categories = category_counts.sort_values(ascending=False)
        filtered_categories = sorted_categories.iloc[5:]
        fig, ax_pie = plt.subplots()
        ax_pie.pie(filtered_categories, labels=filtered_categories.index, autopct='%1.1f%%', startangle=140)
        ax_pie.axis('equal')
        ax_pie.legend(title="Legend", loc="upper right", fontsize="small", fancybox=True, bbox_to_anchor=(2, 1))
        ax_pie.set_title(f"{cat.capitalize().replace('_',' ')} Percentage Against Total Employees.",color="darkblue")
        st.pyplot(fig)
        # Bar Chart
        st.title("Bar Chart")
        expenses_columns = ('School', 'Department')
        cate = st.selectbox("Select Category", expenses_columns)
        num_bin = int(st.selectbox("Number of School", range(5, len(df['School']) + 1)))
        fig, ax = plt.subplots()
        sns.barplot(y='Earnings', data=df)
        ax.set_xlabel(cate.capitalize())
        ax.set_ylabel('Earnings ($)')
        ax.set_title(f'Employee Earnings for Top {num_bin} {cate.capitalize()}', color='darkgreen')
        ax.legend(title="Year", loc="upper right", fontsize="small", fancybox=True, bbox_to_anchor=(1.5, 1))
        colors = plt.cm.viridis(np.linspace(0, 1, len(df['Year'].unique()))) 
        if cate == 'School':
            columns = ['School']
        else:
            columns = ['Department']
        top_schools = df.groupby(columns)['Earnings'].sum().nlargest(num_bin).index
        df_filtered = df[df[columns[0]].isin(top_schools)]
        for index,row in df_filtered.iterrows():
                ax.bar(row[columns[0]], row['Earnings'], color=colors[row['Year'] - df['Year'].max()], label=str(row['Year']))

            
        st.markdown(f"""
    <h3>Top {num_bin} Employee {cate.capitalize().replace("_", " ")} Earnings</h3>
    <p class="desc">This bar plot displays the earnings distribution of the top {num_bin} {cate.lower()}s in the dataset. 
    It offers insights into how the earnings vary across {cate.lower()}s for the selected group of employees. 
    Use the dropdown menus to select the {cate.lower()} category and the number of {cate.lower()}s to analyze.</p>
""", unsafe_allow_html=True)

        plt.xticks(rotation=30)
        st.pyplot(fig)
        del fig, ax
     # Histogram Chart
        fig, ax = plt.subplots()
        st.title("Histogram Charts")
        expenses_columns = ['School', 'Year']
        cate_hist = st.selectbox("Select Hist ",expenses_columns)
        hist_bin = int(st.selectbox("No of Bins",range(5,1000,5)))
        plt.figure(figsize=(8, 6))
        plt.xlabel('School')
        plt.ylabel('Earnings ($)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
       
        st.markdown(f"""
        <h3>Distribution of {cate_hist.capitalize().replace("_"," ")} Data Earnings</h3>

        <p class="desc"> This histogram displays the distribution of {cate_hist.capitalize().replace("_"," ")} data among the students in the dataset. It offers insights into the spread and density of values within the selected category. Use the dropdown menus to select the category and adjust the number of bins for the histogram.</p>

        """,unsafe_allow_html=True)
        plt.title(f'Distrubution of {cate_hist.capitalize().replace("_"," ")} data',color='brown')
        sns.histplot(df[cate_hist],bins=hist_bin,kde=True, color='darkblue', alpha=0.8)
        plt.legend([cate_hist], title="Legend", loc="upper right", fontsize="large", fancybox=True, bbox_to_anchor=(1.3, 1))
        plt.xticks(rotation=35, fontsize=8)
        st.pyplot()
        
        # Boxplot Chart
        st.title("Boxplot Chart")
        expenses_columns = ['School', 'Year']
        cate_box = st.selectbox("Select Boxplot Category", expenses_columns)
        hist_bin = int(st.selectbox("Number of Bins", range(5, 1000, 5)))
    
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=cate_box, y='Earnings', data=data, color='darkblue')
        plt.xlabel(cate_box.capitalize())
        plt.ylabel('Earnings ($)')
        plt.title(f'Boxplot of Earnings by {cate_box.capitalize()}', color='brown')
        plt.xticks(rotation=30, fontsize=8)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend([cate_box], title="Legend", loc="upper right", title_fontsize="large", fontsize="large", fancybox=True, bbox_to_anchor=(1.5, 1))
        legend = plt.legend([cate_box], title="Legend", loc="upper right", title_fontsize="large", fontsize="large", fancybox=True, bbox_to_anchor=(1.5, 1))
        legend.get_title().set_color('darkred')
       
        st.pyplot()
        # Correlation Heatmap
        st.title("Correlation Heatmap")
        expenses_columns = ['Earnings', 'Year']
        cate_box = st.selectbox("Select Heatmap Category", expenses_columns)
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[['Earnings', 'Year']].corr(), annot=True, cmap='coolwarm', fmt=".1f", linewidths=0.5)
        plt.title("Correlation Heatmap", fontsize=2)
        plt.xticks(rotation=40, ha='right', fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        plt.title('Heatmap Correlation of Earnings and Year')
        st.pyplot()

    


        


        st.markdown("<footer class='footer'>© 2024 @meharali </footer>",unsafe_allow_html=True)




if __name__ == "__main__":
    main()