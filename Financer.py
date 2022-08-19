from calendar import different_locale
from mimetypes import init
import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
from PIL import Image
import numpy as np # np mean, np random 
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 

def main():

    image = Image.open('logo.png')

    st.image(image, use_column_width=True)

    st.title("Financer")

    menu = ["Intro","Stocks Dashboard","Real-Time Dashboard", "MPG Dashboard", "Data Visualizer"]
    choice = st.sidebar.selectbox("Select Activity", menu)
    if choice == "Intro":
        st.subheader("Your Personal Finace Analyzer")

    elif choice == "Stocks Dashboard":
        @st.cache
        def load_data():
            """Function for loading data"""
            df = pd.read_csv("data/all_stocks_5yr.csv", index_col="date")

            numeric_df = df.select_dtypes(['float','int'])
            numeric_cols = numeric_df.columns

            text_df = df.select_dtypes(['object'])
            text_cols = text_df.columns

            stock_column = df['Name']

            unique_stocks = stock_column.unique()

            return df, numeric_cols, text_cols, unique_stocks


        df, numeric_cols, text_cols, unique_stocks = load_data()


        # Title of dashboard
        st.title("Stock Dashboard")
        st.subheader("A dashboard for the imformation related to 5yrs of stock data")

        # add checknob to sidebar
        check_box = st.sidebar.checkbox(label="Display dataset")

        if check_box:
            # lets show the dataset
            st.write(df)

        # give sidebar a title
        st.sidebar.title("Settings")
        st.sidebar.subheader("Timeseries settings")
        feature_selection = st.sidebar.multiselect(label="Features to plot",
                                                options=numeric_cols)

        stock_dropdown = st.sidebar.selectbox(label="Stock Ticker",
                                            options=unique_stocks)

        print(feature_selection)

        df = df[df['Name']==stock_dropdown]
        df_features = df[feature_selection]

        plotly_figure = px.line(data_frame=df_features,
                                x=df_features.index,y=feature_selection,
                                title=(str(stock_dropdown) + ' ' +'timeline')
                                )

        st.plotly_chart(plotly_figure)

    elif choice == "Real-Time Dashboard":
        st.subheader("Real-Time / Live Dashboard")

        # read csv from a github repo
        df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")


        #st.set_page_config(
            #page_title = 'Financer',
            #layout = 'wide'
        #)

        # dashboard title

        st.title("Real-Time / Live Data Dashboard")

        # top-level filters 

        job_filter = st.selectbox("Select the Job", pd.unique(df['job']))


        # creating a single-element container.
        placeholder = st.empty()

        # dataframe filter 

        df = df[df['job']==job_filter]

        # near real-time / live feed simulation 

        for seconds in range(200):
        #while True: 
            
            df['age_new'] = df['age'] * np.random.choice(range(1,5))
            df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

            # creating KPIs 
            avg_age = np.mean(df['age_new']) 

            count_married = int(df[(df["marital"]=='married')]['marital'].count() + np.random.choice(range(1,30)))
            
            balance = np.mean(df['balance_new'])

            with placeholder.container():
                # create three columns
                kpi1, kpi2, kpi3 = st.columns(3)

                # fill in those three columns with respective metrics or KPIs 
                kpi1.metric(label="Age ⏳", value=round(avg_age), delta= round(avg_age) - 10)
                kpi2.metric(label="Married Count 💍", value= int(count_married), delta= - 10 + count_married)
                kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)

                # create two columns for charts 

                fig_col1, fig_col2 = st.columns(2)
                with fig_col1:
                    st.markdown("### First Chart")
                    fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
                    st.write(fig)
                with fig_col2:
                    st.markdown("### Second Chart")
                    fig2 = px.histogram(data_frame = df, x = 'age_new')
                    st.write(fig2)
                st.markdown("### Detailed Data View")
                st.dataframe(df)
                time.sleep(1)
            #placeholder.empty()   

    elif choice == "MPG Dashboard":
        st.subheader("MPG Dashboard")
        # set the style for seaborn
        sns.set_style('darkgrid')

        # Title of the dashboard
        st.title('Dashboard for Autompg dataset.')


        @st.cache
        def load_data():
            """ Utility function for loading the autompg dataset as a dataframe."""
            df = pd.read_csv("data/clean_auto_mpg.csv")

            return df


        # load dataset
        data = load_data()
        numeric_columnss = data.select_dtypes(['float64', 'float32', 'int32', 'int64']).columns

        # checkbox widget
        checkbox = st.sidebar.checkbox("Reveal data.")

        if checkbox:
            # st.write(data)
            st.dataframe(data=data)

        # create scatterplots
        st.sidebar.subheader("Scatter plot setup")
        # add select widget
        select_box1 = st.sidebar.selectbox(label='X axis', options=numeric_columnss)
        select_box2 = st.sidebar.selectbox(label="Y axis", options=numeric_columnss)
        sns.relplot(x=select_box1, y=select_box2, data=data)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        # create histograms
        st.sidebar.subheader("Histogram")
        select_box3 = st.sidebar.selectbox(label="Feature", options=numeric_columnss)
        histogram_slider = st.sidebar.slider(label="Number of Bins",min_value=5, max_value=100, value=30)
        sns.distplot(data[select_box3], bins=histogram_slider)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        # create jointplot
        st.sidebar.subheader("Joint plot")
        select_box3 = st.sidebar.selectbox(label='x', options=numeric_columnss)
        select_box4 = st.sidebar.selectbox(label="y", options=numeric_columnss)
        sns.jointplot(x=select_box3, y=select_box4, data=data)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    elif choice == "Data Visualizer":

        # configuration
        st.set_option('deprecation.showfileUploaderEncoding', False)

        # title of the app
        st.title("Data Visualizer")
        st.subheader("A place to vizualize all of your csv data")
        # Add a sidebar
        st.sidebar.subheader("Visualization Settings")

        # Setup file upload
        uploaded_file = st.sidebar.file_uploader(
                                label="Upload your CSV or Excel file. (200MB max)",
                                type=['csv', 'xlsx'])

        global dff
        if uploaded_file is not None:
            print(uploaded_file)
            print("hello")

            try:
                dff = pd.read_csv(uploaded_file)
            except Exception as e:
                print(e)
                dff = pd.read_excel(uploaded_file)

        global numeric_columns
        global non_numeric_columns
        try:
            st.write(dff)
            numeric_columns = list(dff.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(dff.select_dtypes(['object']).columns)
            non_numeric_columns.append(None)
            print(non_numeric_columns)
        except Exception as e:
            print(e)
            st.write("Please upload file to the application.")

        # add a select widget to the side bar
        chart_select = st.sidebar.selectbox(
            label="Select the chart type",
            options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
        )

        if chart_select == 'Scatterplots':
            st.sidebar.subheader("Scatterplot Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
                y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
                color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
                plot = px.scatter(data_frame=dff, x=x_values, y=y_values, color=color_value)
                # display the chart
                st.plotly_chart(plot)
            except Exception as e:
                print(e)

        if chart_select == 'Lineplots':
            st.sidebar.subheader("Line Plot Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
                y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
                color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
                plot = px.line(data_frame=dff, x=x_values, y=y_values, color=color_value)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)

        if chart_select == 'Histogram':
            st.sidebar.subheader("Histogram Settings")
            try:
                x = st.sidebar.selectbox('Feature', options=numeric_columns)
                bin_size = st.sidebar.slider("Number of Bins", min_value=10,
                                            max_value=100, value=40)
                color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
                plot = px.histogram(x=x, data_frame=dff, color=color_value)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)

        if chart_select == 'Boxplot':
            st.sidebar.subheader("Boxplot Settings")
            try:
                y = st.sidebar.selectbox("Y axis", options=numeric_columns)
                x = st.sidebar.selectbox("X axis", options=non_numeric_columns)
                color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
                plot = px.box(data_frame=dff, y=y, x=x, color=color_value)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    main()