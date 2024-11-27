from nicegui import ui
import pandas as pd

###############################################################################
def create_bar_highchart(df, x_col, y_col, title, x_axis_title, y_axis_title):
    chart_data = [{'name': row[x_col], 'y': row[y_col]} for _, row in df.iterrows()]
    
    ui.highchart({
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'type': 'category', 'title': {'text': x_axis_title}}, 
        'yAxis': {'title': {'text': y_axis_title}},
        'legend': {'enabled': False},
        'series': [{
            'name': y_axis_title,
            'data': chart_data,
            'colorByPoint': True,
        }],
        'plotOptions': {
            'column': {
                'dataLabels': {'enabled': True}
            }
        },
    })
    
########################
def create_bar_highchart(df, x_col, y_col, title, x_axis_title, y_axis_title):
    chart_data = [{'name': row[x_col], 'y': row[y_col]} for _, row in df.iterrows()]
    
    ui.highchart({
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'type': 'category', 'title': {'text': x_axis_title}}, 
        'yAxis': {'title': {'text': y_axis_title}},
        'legend': {'enabled': False},
        'series': [{
            'name': y_axis_title,
            'data': chart_data,
            'colorByPoint': True,
        }],
        'plotOptions': {
            'column': {
                'dataLabels': {'enabled': True}
            }
        },
    })
def create_line_highchart(df, x_col, y_col, title, x_axis_title, y_axis_title):
    chart_data = [{'name': row[x_col], 'y': row[y_col]} for _, row in df.iterrows()]
    
    ui.highchart({
        'chart': {'type': 'line'},
        'title': {'text': title},
        'xAxis': {'type': 'category', 'title': {'text': x_axis_title}}, 
        'yAxis': {'title': {'text': y_axis_title}},
        'legend': {'enabled': False},
        'series': [{
            'name': y_axis_title,
            'data': chart_data,
            'colorByPoint': True,
        }],
        'plotOptions': {
            'line': {
                'dataLabels': {'enabled': True},
                'enableMouseTracking': True,
                'connectNulls': True  # Connects points even if there's a gap
            }
        },
    })
    
########################### 
def create_pie_chart(df, title):
    total_touchdowns = int(df['rush_Tds'].sum() + df['rec_Tds'].sum())

    chart_data = [{
        'name': 'Rushing Touchdowns',
        'y': df['rush_Tds'].sum()
    }, {
        'name': 'Receiving Touchdowns',
        'y': df['rec_Tds'].sum()
    }]
    
    ui.highchart({
        'chart': {'type': 'pie'},
        'title': {'text': title},
        'plotOptions': {
                'series': {
                    'cursor': 'pointer',
                    'dataLabels': [{
                        'enabled': True,
                        'distance': 20,
                        'format': '{point.name} {point.percentage:.1f}%',

                    }, {
                        'enabled': True,
                        'distance': -40,
                        'format': '{point.y}',

                        'style': {
                            'fontSize': '1.2em',
                            'textOutline': 'none',
                            'opacity': 0.7,
                            'color': 'white'

                        },
                        'filter': {
                            'operator': '>',
                            'property': 'percentage',
                            'value': 10
                        }
                    }]
                }
            },
        'series': [{
            'name': 'Touchdowns',
            'colorByPoint': True,
            'data': chart_data
        }],
        'subtitle': {
        'text': f'{total_touchdowns}',
        'verticalAlign': 'middle',
        'floating': True,
        'style': {
            'fontSize': '36px',
            'fontWeight': 'bold',
            'color': 'black'

            }
        }
    })
  
#####################
def create_stacked_bar_chart(df, title, x_axis_title, y_axis_title):
    df = df[(df['rush_Tds'] != 0) | (df['rec_Tds'] != 0)]
    
    # Sort the DataFrame by 'rush_Tds' for initial display
    #df = df.sort_values(by=['rush_Tds', 'rec_Tds'], ascending=[False, False])
    df = df.sort_values(by='All_TDs', ascending=False)

    
    chart_data = [{
        'name': 'Rushing Touchdowns',
        'data': df['rush_Tds'].tolist()
    }, {
        'name': 'Receiving Touchdowns',
        'data': df['rec_Tds'].tolist()
    }]
    
    ui.highchart({
        'chart': {'type': 'bar'},
        'title': {'text': title},
        'xAxis': {
            'categories': df['Player'].tolist(),
            'title': {'text': x_axis_title}
        },
        'yAxis': {
            'min': 0,
            'title': {'text': y_axis_title},
            'allowDecimals': False,  # Ensure only whole numbers are used
            'tickInterval': 1      # Set the interval between ticks to 1
        },
        'plotOptions': {
            'series': {
                'stacking': 'normal'
            }
        },
        'series': chart_data
    })
    
######################
def create_stacked_chart(df, title):
    df = df[(df['rush_Yds'] != 0) | (df['rec_Yds'] != 0) | (df['rush_Att'] != 0) | (df['rec_Tgt'] != 0)].copy()

    # Calculate total production for sorting
    df['Total_Production'] = df['rush_Yds'] + df['rec_Yds'] + df['rush_Att'] + df['rec_Tgt']
    df = df.sort_values(by='Total_Production', ascending=False)     
    
    categories = df['Player'].tolist()
    data_series = {
        'Rushing Yards': df['rush_Yds'].tolist(),
        'Receiving Yards': df['rec_Yds'].tolist(),
        'Rushing Attempts': df['rush_Att'].tolist(),
        'Receiving Targets': df['rec_Tgt'].tolist()
    }
    
    filtered_series = []
    for name, data in data_series.items():
        if any(val != 0 for val in data):  # Only add series if there is at least one non-zero value
            filtered_data = [val if val != 0 else None for val in data]  # Replace 0s with None to hide them in the chart
            filtered_series.append({'name': name, 'data': filtered_data})
    
    ui.highchart({
        'chart': {
            'type': 'column'
        },
        'title': {
            'text': title
        },
        'xAxis': {
            'categories': categories,
            'title': {
                'text': 'Players'
            }
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Total Production'
            },
            'stackLabels': {
                'enabled': True,
                'style': {
                    'fontWeight': 'bold',
                    'color': 'gray'
                }
            }
        },
        'legend': {
            'align': 'right',
            'x': -30,
            'verticalAlign': 'top',
            'y': 25,
            'floating': True,
            'backgroundColor': 'white',
            'borderColor': '#CCC',
            'borderWidth': 1,
            'shadow': False
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True
                }
            }
        },
        'series': filtered_series
    })

#####################
def create_pie_chart_by_position(df, title):
    # Grouping data by position and summing the total yards
    pos_total_yards = df.groupby('Pos')['All_Yds'].sum().reset_index()
    total_yards = int(df['All_Yds'].sum())

    
    # Preparing data for Highcharts
    chart_data = [{'name': row['Pos'], 'y': row['All_Yds']} for _, row in pos_total_yards.iterrows()]
    
    ui.highchart({
        'chart': {'type': 'pie'},
        'title': {'text': title},
        'plotOptions': {
                'series': {
                    'cursor': 'pointer',
                    'dataLabels': [{
                        'enabled': True,
                        'distance': 20,
                        'format': '{point.name} {point.percentage:.1f}%',

                    }, {
                        'enabled': True,
                        'distance': -40,
                        'format': '{point.y}',

                        'style': {
                            'fontSize': '1.2em',
                            'textOutline': 'none',
                            'opacity': 0.7,
                            'color': 'white'

                        },
                        'filter': {
                            'operator': '>',
                            'property': 'percentage',
                            'value': 10
                        }
                    }]
                }
            },
        'series': [{
            'name': 'Total Yards',
            'colorByPoint': True,
            'data': chart_data
        }],
        'subtitle': {
        'text': f'{total_yards}',
        'verticalAlign': 'middle',
        'floating': True,
        'style': {
            'fontSize': '32px',
            'fontWeight': 'bold',
            'color': 'black'

            }
        }
    })
    
###############################################################################

### add hyper link columns in HTML
def add_hyperlink_columns(df):
    df['XTm'] = df['Tm'].apply(lambda x: f'<a href="/team/{code_to_team_mapping.get(x)}">{x}</a>')
    df['XPlayer'] = df['Player'].apply(lambda x: f'<a href="/player/{x.replace(" ", "_")}">{x}</a>')
    return df

###############

def fix_date(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%m-%d')
    return df
    
###### TEMPLATES FOR PAGES ####################################################
def template_html(label_val):
    with ui.header().classes("bg-gray-800 text-white py-4 px-6"):
        ui.label(f"{label_val}").classes("text-3xl font-semibold")
        
        # Navbar links
        with ui.row().classes("space-x-4 ml-6"):
            ui.link("Stat Leaders", state_leaders_page)
            ui.link("Player Stats", '/player/Trey_McBride')
            ui.link("Teams", teams_page)
            ui.link("Teams Compare", team_compare_page)
            ui.link("About", about_page)
    
    # Footer
    with ui.footer():
        ui.label("proplayermetrics © 2024").classes("text-sm text-center")   

##########################################

def create_grid(df, link_cols):
    df1 = df.copy()

    for col in link_cols:
        html_col = f'X{col}'
        if html_col in df1.columns:
            df1[col] = df1[html_col]  # Replace the original column's values with the HTML values
            df1.drop(columns=[html_col], inplace=True)  # Drop the HTML column after copying


    # Create column definitions, setting :cellRenderer only for the specified link columns
    column_defs = [
        {
            'headerName': col,
            'field': col,
            ':cellRenderer': LinkRenderer if col in link_cols else None  # Apply renderer for link columns
        }
        for col in df1.columns
    ]

    # removes the ':cellRendered' element from dict with None value
    for col_def in column_defs:
        if col_def[':cellRenderer'] is None:
            del col_def[':cellRenderer']

    grid_options = {
        'domLayout': 'autoHeight',
        'columnDefs': column_defs,
    }
    
    #return column_defs
    return ui.aggrid.from_pandas(df1, options=grid_options).style('height: auto; width: -webkit-fill-available;')

################################################################################
### args list options, initiale value, container obj
def template_dropdown(soptions, current_df, current_team_filter, link_cols):
    
    with ui.row().style('align-items: center;'):
        ui.label('Selected Type: ')
        selected_stat = ui.select(list(soptions), value="Rushing").classes("my-4")
        ui.label('Selected Team: ')
        selected_stat.on('update:modelValue', lambda e: update_grid(e))
        team_sel = ui.select(teams, clearable=True, multiple=True).classes("my-4")
        team_sel.on('update:modelValue', lambda e: team_update(e))
        
    #########################################################################
    grid_container = ui.element('div').style('width: 100%; display: flex; justify-content: center;')
    
    with grid_container:
        grid = create_grid(current_df, link_cols)


    # Function to update the grid
    def update_grid(e):
        nonlocal current_df, current_team_filter, grid  # Allow modification of these variables
        current_df = soptions[e.args["label"]]  # Update current_df based on selected stat type
        
        # Apply team filter if there is a selected team
        if current_team_filter:
            filtered_df = current_df[current_df['Tm'].isin(current_team_filter)]
        else:
            filtered_df = current_df
            
        grid.delete()  
        with grid_container:
            grid = create_grid(filtered_df, link_cols)
                    
    #########################
    def team_update(e):
        nonlocal current_team_filter, current_df, grid

        if e.args is None:
            current_team_filter = None
            filtered_df = current_df
            
        else:
            labels = [item['label'] for item in e.args]
            current_team_filter = [team_code_mapping[label] for label in labels if label in team_code_mapping]   
            
            filtered_df = current_df[current_df['Tm'].isin(current_team_filter)]
            
        grid.delete()  
        with grid_container:
            grid = create_grid(filtered_df, link_cols)
     
##############################################################################
def display_grids_barchart(data_list, grid_container, link_cols):
        for index in range(0, len(data_list), 2):    
            with grid_container:
                data, chart_column, title, y_label = data_list[index]
                data1, chart_column1, title1, y_label1 = data_list[index+1]
            
                create_grid(data, link_cols)
                create_grid(data1, link_cols)

                create_bar_highchart(data, 'Player', chart_column, f"{title}", 'Player', y_label)
                create_bar_highchart(data1, 'Player', chart_column1, f"{title1}", 'Player', y_label1)
                
###############################################################################
### SHOULD ONLY LINK TEAM
def display_grids_and_charts(data_list, grid_container, link_cols):
        for index in range(0, len(data_list), 2):    
            with grid_container:
                data, chart_column, avg, title, y_label = data_list[index]
                data1, chart_column1, avg1, title1, y_label1 = data_list[index+1]
                
                create_grid(data, link_cols)
                create_grid(data1, link_cols)

                create_line_highchart(data, 'Date', chart_column, f"{avg} {title}", 'Date', y_label)
                create_line_highchart(data1, 'Date', chart_column1, f"{avg1} {title1}", 'Date', y_label1)
                        
################################################################################
def process_player_stats(player_data, cols_and_titles, data_list):
    for cols, column, title, y_label in cols_and_titles:
        data = player_data[cols].sort_values(by='Date', ascending=False)
        avg = round(data[column].mean(), 2)
        data[column] = round(data[column], 2)  # Optional: rounding the column
        data_list.append((data, column, avg, title, y_label))
    return data_list

###############################################################################
def display_player_stats(player_data, postype, grid_container, button):
    data_list = []
    button.disable()

    if postype == 'Pass':
        data_list = process_player_stats(player_data, player_pass_cols_and_titles, data_list)
        
    elif postype == 'Rush':
        data_list = process_player_stats(player_data, player_rush_cols_and_titles, data_list)

    elif postype == 'Rec':
        data_list = process_player_stats(player_data, player_rec_cols_and_titles, data_list)

    display_grids_and_charts(data_list, grid_container, ['Tm'])
    
#################################################################################
################################################################################
def merge_dfs_with_shared_columns(df1, df2, df3, shared_columns):
    # Add prefixes to each DataFrame's columns, excluding the shared columns
    df1_prefixed = df1.add_prefix('rush_').rename(columns={f'rush_{col}': col for col in shared_columns})
    df2_prefixed = df2.add_prefix('rec_').rename(columns={f'rec_{col}': col for col in shared_columns})
    df3_prefixed = df3.add_prefix('pass_').rename(columns={f'pass_{col}': col for col in shared_columns})

    # Merge the DataFrames on the shared columns
    combined_df = df1_prefixed.merge(df2_prefixed, on=shared_columns, how='outer')
    combined_df = combined_df.merge(df3_prefixed, on=shared_columns, how='outer')

    return combined_df

#################################################################################
def prepare_team_stats(filtered_data, cols_and_titles, special_column, data_list):
        for cols, column, title, y_label in cols_and_titles:
            data = filtered_data[cols].sort_values(by=column, ascending=False)
            total_value = int(data[column].sum()) if column != special_column else round(data[column].mean(), 2)
            data[f'{column} Ratio'] = round(data[column] / total_value, 2) if total_value != 0 else 0
            data[column] = round(data[column], 2)
            data_list.append((data, column, f"{total_value} {title}", y_label))
        return data_list

#################################################################################
# Define pages for each section
### PLAYER AND TM LINKS
@ui.page('/stat_leaders')
def state_leaders_page():
    ui.label("Select your filters")
    template_html('NFL Stat Leaders')
    ui.page_title('NFL Stat Leaders')

    lrush_stats = latest_rush[lrush_stats_cols].sort_values(by='Att', ascending=False)
    lrec_stats = latest_rec[lrec_stats_cols].sort_values(by='Tgt', ascending=False)
    pass_df = latest_pass[lpass_stats_cols].sort_values(by='Att', ascending=False)
                
    stat_options = {'Rushing': lrush_stats, 'Receiving': lrec_stats, 'Passing': pass_df}
            
    current_df = stat_options["Rushing"]  # Start with "Rushing" as default
    current_team_filter = None
        
    template_dropdown(stat_options, current_df, current_team_filter, ['Player', 'Tm'])

###############################################################################
### TM LINKS
@ui.page('/player/{player_name}')
def player_page(player_name: str):
    player_name = player_name.replace('_', ' ')

    ### go to players specific url
    def player_update(e):
        selected_player = e.args["label"]
        # Replace spaces with underscores for the URL
        player_url = f"/player/{selected_player.replace(' ', '_')}"
        ui.navigate.to(player_url)
        
    ui.add_head_html(button_styles)
    template_html(f'{player_name} Stats')
    ui.page_title(f'{player_name} Stats')


    player_data = all_current_df[all_current_df['Player'] == player_name]
    player_pos = player_data['Pos'].iloc[0]

    for category, positions in position_map.items():
        if player_pos in positions:
            postype = category
            

    with ui.row().style('align-items: center;'):
        ui.label('Selected Player: ')
        player_sel = ui.select(list(unique_players), with_input=True, value=player_name).classes("my-4")
        player_sel.on('update:modelValue', lambda e: player_update(e))
        
        pass_button = ui.button("Show Passing Stats").classes('Pass').style('margin-right: 10px;')
        rush_button = ui.button("Show Rushing Stats").classes('Rush').style('margin-right: 10px;')
        rec_button = ui.button("Show Receiving Stats").classes('Rec').style('margin-right: 10px;')

        pass_button.on('click', lambda: display_player_stats(player_data, 'Pass', grid_container, pass_button))
        rush_button.on('click', lambda: display_player_stats(player_data, 'Rush', grid_container, rush_button))
        rec_button.on('click', lambda: display_player_stats(player_data, 'Rec', grid_container, rec_button))


    grid_container = ui.grid(columns=2).style("width: -webkit-fill-available;")
    
    button_position_map = {
        'Pass': pass_button,
        'Rush': rush_button,
        'Rec': rec_button 
    }
    
    display_player_stats(player_data, postype, grid_container, button_position_map[postype])    

################################################################################

# Player LINKS
@ui.page('/team/{team_name}')
def team_page(team_name: str):
    template_html(f'{team_name}')
    ui.page_title(f'{team_name} Team Stats')

    team_code = team_code_mapping.get(team_name)
    data_list = []

    grid_container = ui.grid(columns = 2).style("width: -webkit-fill-available;")
    
    # Filter data for the team
    latest_rush_filtered = latest_rush[latest_rush['Tm'] == team_code]
    latest_rec_filtered = latest_rec[latest_rec['Tm'] == team_code]
    latest_pass_filtered = latest_pass[latest_pass['Tm'] == team_code]
    
    data_list = prepare_team_stats(latest_rush_filtered, rush_cols_and_titles, 'Yds/Att', data_list)
    data_list = prepare_team_stats(latest_rec_filtered, rec_cols_and_titles, 'Cum_Mean_ADOT', data_list)

    display_grids_barchart(data_list, grid_container, ['Player'])

    
    pass_df = latest_pass_filtered[latest_pass_filtered['Tm'] == team_code][team_pass_cols].sort_values(by='Att', ascending=False)
    create_grid(pass_df, ['Player'])

    combined_df1 = merge_dfs_with_shared_columns(latest_rush_filtered, latest_rec_filtered, latest_pass_filtered, shared_columns)
    combined_df1['All_TDs'] = combined_df1['rush_Tds'].fillna(0) + combined_df1['rec_Tds'].fillna(0) #+ combined_df1['pass_Tds'].fillna(0)
    combined_df1['All_Yds'] = combined_df1['rush_Yds'].fillna(0) + combined_df1['rec_Yds'].fillna(0) #+ combined_df1['pass_Yds'].fillna(0)
    combined_df1['All_Att'] = combined_df1['rush_Att'].fillna(0) + combined_df1['rec_Tgt'].fillna(0) #+ combined_df1['pass_Att'].fillna(0)
    #############################
    
    # Group by 'Player' and aggregate relevant columns
    combined_df2 = combined_df1.groupby('Player', as_index=False).agg({
        'Pos': 'first',  
        'All_TDs': 'sum',
        'All_Yds': 'sum',
        'All_Att': 'sum',
        'rush_Tds': 'sum',
        'rec_Tds': 'sum',
        'rush_Yds': 'sum',
        'rec_Yds': 'sum',
        'rush_Att': 'sum',
        'rec_Tgt': 'sum'
    })

    with ui.grid(columns = 2).style("width: -webkit-fill-available;"):
        create_stacked_chart(combined_df2, 'Rushing + Receiving Production of Players')
        create_pie_chart(combined_df2, 'Distribution of Rushing and Receiving Touchdowns')
        create_pie_chart_by_position(combined_df2, 'Rushing + Receiving Yards by Position')
        create_stacked_bar_chart(combined_df2, 'Player Touchdown Contributions', 'Players', 'Total Touchdowns')

###############################################################################

@ui.page('/teams')
def teams_page():
    template_html('NFL Teams')
    ui.page_title('NFL Teams')


    with ui.grid(columns=8, rows=4).style("width: -webkit-fill-available; height: 600px;"):
        for team in teams:
            # Each team name is a clickable link to its specific page
            ui.link(team, f'/team/{team}').classes("text-lg font-medium text-center")
        
################################################################################
## TEAM LINKS
@ui.page('/team_compare')
def team_compare_page():
    ui.label("Select Filters")
    template_html('Team Compare')
    ui.page_title('Team Compare')


    # Select and aggregate rush stats
    lrush_stats = latest_rush[[col for col in lrush_stats_cols if col != 'XPlayer']].copy()
    lrush_stats = lrush_stats.groupby('Tm').agg({
        'Att': 'sum', 'Yds': 'sum', 'Tds': 'sum', 'Yds/Att': 'mean', 'XTm': 'first'
    }).reset_index().sort_values(by='Yds', ascending=False)
    lrush_stats['Yds/Att'] = round(lrush_stats['Yds/Att'], 2)
    
    # Select and aggregate receiving stats
    lrec_stats = latest_rec[[col for col in lrec_stats_cols if col != 'XPlayer']].copy()
    lrec_stats = lrec_stats.groupby('Tm').agg({
        'Tgt': 'sum', 'Rec': 'sum', 'Yds': 'sum', 'Tds': 'sum', 'Drop': 'sum', 'Cum_Mean_ADOT': 'mean', 'XTm': 'first'
    }).reset_index().sort_values(by='Yds', ascending=False)
    lrec_stats['Cum_Mean_ADOT'] = round(lrec_stats['Cum_Mean_ADOT'], 2)

    
    # Select and aggregate passing stats
    lpass_stats = latest_pass[[col for col in lpass_stats_cols if col != 'XPlayer']].copy()
    lpass_stats = lpass_stats.groupby('Tm').agg({
        'Cmp': 'sum', 'Att': 'sum', 'Yds': 'sum', 'YA_Catch': 'sum', 'Tds': 'sum', 'Drops': 'sum',
        'Sk': 'sum', 'Bltz': 'sum', 'Yds/Att': 'mean', 'Cum_Mean_QB_Rate': 'mean', 'XTm': 'first'
    }).reset_index().sort_values(by='Yds', ascending=False)
    lpass_stats[['Cum_Mean_QB_Rate', 'Yds/Att']] = round(lpass_stats[['Cum_Mean_QB_Rate', 'Yds/Att']], 2)
            
    stat_options = {'Rushing': lrush_stats, 'Receiving': lrec_stats, 'Passing': lpass_stats}
    current_df = stat_options["Rushing"]  # Start with "Rushing" as default
    current_team_filter = None
        
    template_dropdown(stat_options, current_df, current_team_filter, ['Tm'])

################################################################################

@ui.page('/about')
def about_page():
    template_html('About Me')
    ui.page_title('About Me')

    ui.html('''
    <h1>ABOUT THIS WEBSITE</h1>
    <p>Welcome to <strong>proplayermetrics.com</strong>, your go-to platform for comprehensive visual analysis of NFL data! Our goal is to offer an engaging, user-friendly experience that makes exploring and understanding the intricacies of football more accessible than ever.</p>
    
    <h2>ABOUT ME</h2>
    <p>My name is Alex, and I have a strong background in business data analytics and software development. With a Bachelor of Science in Business Data Analytics from Arizona State University and experience in roles that blend data processing and programming, I am passionate about creating tools that bridge the gap between raw data and insightful analysis. My expertise in Python, SQL, machine learning, and data visualization drives my commitment to delivering engaging, data-driven experiences for NFL fans and analysts alike.</p>

    <h2>WHAT WE DO</h2>
    <p>At <strong>proplayermetrics</strong>, we believe in the power of data to tell compelling stories. Our website is dedicated to showcasing NFL statistics through interactive and dynamic graphs and visuals that offer unique insights into team and player performance and season trends.</p>
    
    <h2>WHERE DOES THE DATA COME FROM?</h2>
    <p>The NFL data is extracted from various free sources throughout the internet.</p>
    
    <h2>KEY FEATURES</h2>
    <ul>
      <li><strong>Interactive Visuals</strong>: Dive into detailed visualizations that allow you to explore team statistics and player performances in just a few clicks.</li>
      <li><strong>Customizable Data Views</strong>: Tailor your data experience by selecting specific teams, and data types to view stats that matter most to you.</li>
      <li><strong>Up-to-Date Information</strong>: Stay informed with regularly updated data that reflects the latest NFL data.</li>
      <li><strong>User-Friendly Interface</strong>: Our easy to navigate site makes it simple for both casual fans and data enthusiasts to enjoy deep dives into NFL statistics.</li>
    </ul>
    
    <h2>WHY CHOOSE US?</h2>
    <p>Our platform is designed for those who love football and data in equal measure. Whether you're a fantasy football player looking for an edge, a sports analyst, or just a curious fan, <strong>proplayermetrics</strong> provides a visual, straightforward way to understand the game beyond the numbers.</p>
    
    <p>Explore the data, uncover trends, and elevate your understanding of NFL football with <strong>proplayermetrics</strong>. We’re committed to continuously enhancing our offerings, so stay tuned for more exciting features!</p>
    
    
    <h2>QUESTIONS OR CONCERNS?</h2>
    <p>codelockcrusaders@gmail.com</p>

    ''').style('text-align: left;')

################################################################################
LinkRenderer = """
class LinkRenderer {
    init(params) {
        this.eGui = document.createElement('div');
        this.eGui.innerHTML = params.value;  // Render HTML directly
    }
    getGui() {
        return this.eGui;
    }
}
"""

button_styles = """
<style>
    .Rush {
        /* Add your Rush-specific styles here */
        background-color: lightblue;
        color: black;
        border: 2px solid #007BFF;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .Rec {
        /* Add your Rec-specific styles here */
        background-color: lightgreen;
        color: black;
        border: 2px solid #28A745;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .Pass {
        /* Add your Pass-specific styles here */
        background-color: lightcoral;
        color: black;
        border: 2px solid #DC3545;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
"""

# Define lists for teams and their codes
teams = [
    '49ers', 'Bears', 'Bengals', 'Bills', 'Broncos', 'Browns', 'Buccaneers',
    'Cardinals', 'Chargers', 'Chiefs', 'Colts', 'Commanders', 'Cowboys',
    'Dolphins', 'Eagles', 'Falcons', 'Giants', 'Jaguars', 'Jets', 'Lions',
    'Packers', 'Panthers', 'Patriots', 'Raiders', 'Rams', 'Ravens', 'Saints',
    'Seahawks', 'Steelers', 'Texans', 'Titans', 'Vikings'
]

codes = [
    'SFO', 'CHI', 'CIN', 'BUF', 'DEN', 'CLE', 'TAM', 'ARI', 'LAC', 'KAN', 
    'IND', 'WAS', 'DAL', 'MIA', 'PHI', 'ATL', 'NYG', 'JAX', 'NYJ', 'DET', 
    'GNB', 'CAR', 'NWE', 'LVR', 'LAR', 'BAL', 'NOR', 'SEA', 'PIT', 'HOU', 
    'TEN', 'MIN'
]

# Create a mapping dictionary from teams to codes
team_code_mapping = dict(zip(teams, codes))
code_to_team_mapping = {v: k for k, v in team_code_mapping.items()}


# Load your data
latest_rush = pd.read_csv(r'website_nfl_rush_2024.csv')
latest_rec = pd.read_csv('website_nfl_rec_2024.csv')
latest_pass = pd.read_csv('website_nfl_pass_2024.csv')

all_rush = pd.read_csv('website_nfl_all_rush_2024.csv')
all_rec = pd.read_csv('website_nfl_all_rec_2024.csv')
all_pass = pd.read_csv('website_nfl_all_pass_2024.csv')

latest_rush = latest_rush.rename(columns={'Rushing_TDs': 'Tds'})
latest_rec = latest_rec.rename(columns={'Receiving_TDs': 'Tds'})
latest_pass = latest_pass.rename(columns={'Pass_TDs': 'Tds'})

all_rush = all_rush.rename(columns={'Rushing_TDs': 'Tds'})
all_rec = all_rec.rename(columns={'Receiving_TDs': 'Tds'})
all_pass = all_pass.rename(columns={'Pass_TDs': 'Tds'})

latest_rush = add_hyperlink_columns(latest_rush)
latest_rush = fix_date(latest_rush)

latest_rec = add_hyperlink_columns(latest_rec)
latest_rec = fix_date(latest_rec)

latest_pass = add_hyperlink_columns(latest_pass)
latest_pass = fix_date(latest_pass)

#####
all_rush = fix_date(all_rush)
all_rec = fix_date(all_rec)
all_pass = fix_date(all_pass)

a = all_rush.Player.unique()
b = all_rec.Player.unique()
c = all_pass.Player.unique()

unique_players = set(a).union(b, c)

shared_columns = ['Player', 'Tm', 'Pos', 'Date', 'Link', 'season', 
                  'Num', 'Pct', 'Num.1', 'Pct.1', 'Num.2', 'Pct.2',
                  'Off_Fmb_Lost', 'Off_Fmb']

combined_df = merge_dfs_with_shared_columns(all_rush, all_rec, all_pass, shared_columns)

combined_df['All_TDs'] = combined_df['rush_Tds'].fillna(0) + combined_df['rec_Tds'].fillna(0) + combined_df['pass_Tds'].fillna(0)
combined_df['All_Yds'] = combined_df['rush_Yds'].fillna(0) + combined_df['rec_Yds'].fillna(0) + combined_df['pass_Yds'].fillna(0)
combined_df['All_Att'] = combined_df['rush_Att'].fillna(0) + combined_df['rec_Tgt'].fillna(0) + combined_df['pass_Att'].fillna(0)

all_current_df = combined_df
all_current_df = add_hyperlink_columns(all_current_df)

postype = None

### constants for @ui.page('/stat_leaders')
lrush_stats_cols = ['Player', 'XPlayer', 'Tm', 'XTm', 'Pos', 'Att', 'Yds', 'Tds', 'Yds/Att']
lrec_stats_cols = ['Player','XPlayer', 'Tm', 'XTm','Pos', 'Tgt', 'Rec', 'Yds', 'Tds', 'Drop', 'Cum_Mean_ADOT']
lpass_stats_cols = ['Player', 'XPlayer', 'Tm', 'XTm', 'Pos', 'Cmp', 'Att', 'Yds','YA_Catch' ,'Tds' ,'Drops' ,'Sk' ,'Bltz' ,'Yds/Att' ,'Cum_Mean_QB_Rate']


### constants for @ui.page('/player/{player_name}')
position_map = {
    'Pass': ['QB'],
    'Rush': ['RB', 'FB'],
    'Rec': ['WR', 'TE'] 
}


### contants for @ui.page('/team/{team_name}')
rush_cols_and_titles = [
    (['Player', 'XPlayer', 'Pos', 'Att'], 'Att', "Total Rushing Attempts", "Rushing Attempts"),
    (['Player', 'XPlayer','Pos', 'Yds'], 'Yds', "Total Rushing Yards", "Rushing Yards"),
    (['Player', 'XPlayer','Pos', 'Tds'], 'Tds', "Total Rushing Touchdowns", "Rushing Touchdowns"),
    (['Player', 'XPlayer','Pos', 'Yds/Att'], 'Yds/Att', "Avg Rushing Yds/Att", "Yards/Attempt")
]

# Prepare column configurations for receiving data
rec_cols_and_titles = [
    (['Player','XPlayer', 'Pos', 'Tgt'], 'Tgt', "Total Receiving Targets", "Targets"),
    (['Player','XPlayer', 'Pos', 'Rec'], 'Rec', "Total Receiving Receptions", "Receptions"),
    (['Player','XPlayer', 'Pos', 'Yds'], 'Yds', "Total Receiving Yards", "Yards"),
    (['Player','XPlayer', 'Pos', 'Tds'], 'Tds', "Total Receiving Touchdowns", "Touchdowns"),
    (['Player','XPlayer', 'Pos', 'Drop'], 'Drop', "Total Receiving Drops", "Drops"),
    (['Player','XPlayer', 'Pos', 'Cum_Mean_ADOT'], 'Cum_Mean_ADOT', "Avg Receiving ADOT", "ADOT")
]

team_pass_cols = ['Player', 'XPlayer', 'Pos', 'Cmp', 'Att', 'Yds' ,'YA_Catch','Tds','Drops' , 'Sk','Bltz' ,'Y ds/Att' , 'Cum_Mean_QB_Rate']


#### constants for def display_player_stats
player_pass_cols_and_titles = [
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Cmp'], 'pass_Cmp', "Passing Avg Completions", "Completions"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Att'], 'pass_Att', "Passing Avg Attempts", "Attempts"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Yds'], 'pass_Yds', "Passing Avg Yards", "Yards"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_YA_Catch'], 'pass_YA_Catch', "Passing Avg YAC", "Yards After Catch"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Tds'], 'pass_Tds', "Passing Avg Touchdowns", "Touchdowns"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Drops'], 'pass_Drops', "Passing Avg Drops", "Drops"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Sk'], 'pass_Sk', "Passing Avg Sacks", "Sacks"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Bltz'], 'pass_Bltz', "Passing Avg Blitzes", "Blitzes"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_Yds/Att'], 'pass_Yds/Att', "Passing Avg Yds/Att", "Yards/Attempt"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'pass_QB_Rate'], 'pass_QB_Rate', "Passing Avg QB Rate", "QB Rating"),
]

player_rush_cols_and_titles = [
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rush_Att'], 'rush_Att', "Rushing Avg Attempts", "Rushing Attempts"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rush_Yds'], 'rush_Yds', "Rushing Avg Yards", "Rushing Yards"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rush_Tds'], 'rush_Tds', "Rushing Avg Touchdowns", "Rushing Touchdowns"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rush_Yds/Att'], 'rush_Yds/Att', "Rushing Avg Yds/Att", "Yards/Attempt")
]

player_rec_cols_and_titles = [
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rec_Tgt'], 'rec_Tgt', "Receiving Avg Targets", "Targets"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rec_Rec'], 'rec_Rec', "Receiving Avg Receptions", "Receptions"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rec_Yds'], 'rec_Yds', "Receiving Avg Yards", "Receiving Yards"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rec_Tds'], 'rec_Tds', "Receiving Avg Touchdowns", "Touchdowns"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rec_Drop'], 'rec_Drop', "Receiving Avg Drops", "Drops"),
    (['Player', 'XTm', 'Tm', 'Pos', 'Date', 'rec_ADOT'], 'rec_ADOT', "Receiving Avg ADOT", "Average Depth of Target"),
]
    
teams_page()
ui.run(host='0.0.0.0', port=443, ssl_certfile='/etc/letsencrypt/live/proplayermetrics.com/fullchain.pem', ssl_keyfile='/etc/letsencrypt/live/proplayermetrics.com/privkey.pem')
