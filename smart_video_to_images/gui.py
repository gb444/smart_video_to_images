import PySimpleGUI as sg

from .smart_video_to_images import video_to_images



def process_resolution(inp):
    if inp == 'original':
        return None
    else:
        return tuple(map(int, inp.split('x')))

def main():
    sg.theme("SystemDefaultForReal")
    settings = sg.UserSettings._default_for_function_interface
    try:
        settings.get('-last input-', '')
    except AttributeError:
        settings = {}
    # All the stuff inside your window.
    layout = [  [sg.Text('Input file:'), sg.InputText(default_text=settings.get('-last input-', '') ), sg.FileBrowse("Select input")],
                [sg.Text('Target frames: '), sg.InputText(default_text=settings.get('-last frames-', ''))],
                [sg.Text('Target resolution: '), 
                    sg.OptionMenu(['1920x1080','2560x1440', '3840x2160', 'original'],
                                    default_value='original', s=(15,2))],
                [sg.Text('Export location: '), sg.InputText(default_text=settings.get('-last output-', '')), sg.FolderBrowse("Select output folder")],
                [sg.Button('Export Start', key='start'), sg.Button('Close')] ]

    # Create the Window
    window = sg.Window('Smart Video-to-images', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        if event == 'start':
            errors = []
            input_path = values[0]
            if len(input_path) == 0:
                errors.append("Missing input path")
            if len(values[1]) == 0:
                errors.append("Missing target frames")
            else:
                try:
                    target_frames = int(values[1])
                except e:
                    errors.append("Error parsing target frames: "+str(e))
            try:
                target_resolution = process_resolution(values[2])
            except e:
                errors.append("Error parsing target resolution")
            output_dir = values[3]
            if len(output_dir) == 0:
                errors.append("Missing output dir")
            if len(errors) > 0:
                sg.popup_error('\n'.join(errors), title="Input errors")
            else:
                try:
                    sg.user_settings_set_entry('-last input-', input_path)
                    sg.user_settings_set_entry('-last frames-', target_frames)
                    sg.user_settings_set_entry('-last output-', output_dir)
                except AttributeError:
                    print("Cannot save user settings when not invoked directly")

                print(f"Openning {input_path}")
                err = video_to_images(input_path=input_path, 
                                target_frames=target_frames, 
                                target_resolution=target_resolution, 
                                output_dir=output_dir,
                                sg=sg)
                if not err:
                    sg.popup("Finished export")
                else:
                    sg.popup("Stopped export early")

    window.close()


if __name__=='__main__':
    main()