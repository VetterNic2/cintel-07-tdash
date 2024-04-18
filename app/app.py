import seaborn as sns
from faicons import icon_svg
import plotly.express as px
from shinywidgets import render_plotly
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
from shinyswatch import theme

# Importing necessary libraries
theme.united()  # Applying the 'united' theme from shinyswatch to the Shiny.express app

# Loading the penguins dataset
df = palmerpenguins.load_penguins()

# Creating a Title with page_opts function
ui.page_opts(title="Penguins dashboard", fillable=True)

# Creating the sidebar with filters. The user can adjust these and the data will change with the input.
with ui.sidebar(title="Filter controls"):
    # Adding input controls for filtering by mass and species
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Personal and Template Links
    ui.hr()  # Horizontal line for separation
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/VetterNic2/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://VetterNic2.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/VetterNic2/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Creating value boxes for showing data
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Creating cards for showing charts and df
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        # Rendering a scatter plot of bill length vs. bill depth
        @render_plotly
        def length_depth():
            return px.scatter(
                filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        # Creating stats summary data frame
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Reactive function for filtering the dataset based on input controls that user selects in the sidebar
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

