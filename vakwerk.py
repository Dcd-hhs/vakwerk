import PySimpleGUI as sg


def main():
    def snap_to(figure):
        bbfig = graph.get_bounding_box(figure)
        point=(bbfig[0][0]+bbfig[1][0])/2,(bbfig[0][1]+bbfig[1][1])/2
        return point
    sg.theme('Dark Blue')
    
    keuzes = sg.Col([[sg.Text('Knooppunten en staven', enable_events=True)],
              [sg.Radio('knooppunt',1,key='-KNP-', enable_events=True),
              sg.Radio('staaf',1,key='-STV-', enable_events=True)],
              [sg.Radio('balk',1,key='-BLK-', enable_events=True)],
              [sg.Radio('Wis',1,key='-WIS-', enable_events=True)]
             ],key='-kze-')
    
    werk = [[sg.Graph(
                canvas_size=(600,400),
                graph_bottom_left=(0,0),
                graph_top_right=(60,40),
                key = '-grf-',
                enable_events=True,
                background_color='DarkGreen',
                drag_submits=True,
                right_click_menu=[['tisditdan?'],['Wissen',]])
             ],
             [sg.T('asdf',key='-nfo-',size=(40,1))]]
            
    layout=[[keuzes,werk]]
    window = sg.Window("Teken en reken", layout, finalize=True)
    window.move(50,80)
    graph= window['-grf-'] # in window, get the graphobject handle
    
    dragging = False
    start_point = end_point = prior_fig = attempt = None
    obj_dict = {}
    
    while True:
        event, values = window.read()
        print(f'{event=},{values=}')
        if event in ('sg.WIN_CLOSED',None):
            break
        if event == '-grf-':
            x, y = values['-grf-']
            if not dragging: #new click
                start_point=(x,y)
                figs_at_cursor = graph.get_figures_at_location(start_point)
                dragging = True
            window['-nfo-'].update(value=f'mouse {x},{y}')
            if prior_fig:
                graph.delete_figure(prior_fig) #we're still dragging, so clear up
            cur_point=(x,y)
            dx = cur_point[0] - start_point[0]
            dy = cur_point[1] - start_point[1]
            if values['-STV-']:
                prior_fig = graph.draw_line(start_point, cur_point, width =4, color = 'black')
            if values['-BLK-']:
                prior_fig = graph.draw_line(start_point, cur_point, width =6, color = 'red')
            if values['-KNP-']:
                prior_fig = graph.draw_point(cur_point,size=2)
            if values['-WIS-']:
                for figure in figs_at_cursor:
                    graph.delete_figure(figure)
            
        elif event.endswith('+UP'):
            that = [this for this in values if values[this]==True]
            print(that)
            if len(that) >0:
                obj_dict[prior_fig] = that[0]
                print(obj_dict)
            if values['-STV-']:
                for figure in graph.get_figures_at_location(start_point):
                    if obj_dict[figure] == '-KNP-':
                        start_point=snap_to(figure)
                        attempt = 'OK'
                for figure in graph.get_figures_at_location(cur_point):
                    if obj_dict[figure] == '-KNP-' and attempt == 'OK':
                        print(f'knooppunt {figure} gevonden')
                        cur_point=snap_to(figure)
                        graph.delete_figure(prior_fig) #we're still dragging, so clear up
                        graph.draw_line(start_point, cur_point, width =4, color = 'black')
                if attempt == None:
                    graph.delete_figure(prior_fig)
                    del obj_dict[figure]
                attempt = None
                        
            print(f'{prior_fig=}')   
            prior_fig = start_point = end_point = None
            dragging = False
            
    window.close()

main()