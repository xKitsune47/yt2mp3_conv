import PySimpleGUI as sg
import os
from pytube import YouTube
import sys
import subprocess

if not os.path.isdir('Downloaded'):
    os.mkdir('Downloaded')
if not os.path.isfile("TBDownloaded.txt"):
    downloadLinks = open("TBDownloaded.txt", "x").close()

listDownloadedFiles = os.listdir(sys.path[0]+'\Downloaded')
listDownloadedLinks = []
topHeaderColor = '#424C55'
blockColor = '#D1CCDC'
windowColor = '#F5EDF0'
defaultFontBanner = 'Lato 20'
defaultFontElse = 'Lato 14'
banner = [
    [sg.Text("YouTube -> MP3", font=defaultFontBanner,
             background_color=topHeaderColor, text_color='#D1CCDC')]
]
block = [
    [sg.Text("Paste the URL here:", font=defaultFontElse, background_color=blockColor,
             text_color='#424C55')],
    [sg.InputText(size=70, key='-INPUT-', enable_events=True),
     sg.Button("ADD", font='Lato 10', button_color='#424C55')],
    [sg.Listbox(listDownloadedLinks, size=(70, 12), key='-LIST-')]
]
footer = [
    [sg.Button("START CONVERTING", font='Lato 13', button_color='#424C55'),
     sg.Button("EXIT", font='Lato 13', button_color='#424C55'),
     sg.Button("CLEAR LIST", font='Lato 13', button_color='#424C55'),
     sg.Button("OPEN DIRECTORY", font='Lato 13', button_color='#424C55')]
]
layout = [
    [sg.Column(banner, background_color=topHeaderColor, size=(600, 60))],
    [sg.Column(block, background_color=blockColor, size=(600, 300))],
    [sg.Column(footer, background_color=blockColor, size=(600, 40))]
]

window = sg.Window("YT -> MP3", layout, background_color=windowColor, size=(630, 437))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "ADD":
        vidTitle = str(YouTube(values['-INPUT-']).title+'.mp3')
        if values['-INPUT-'] in listDownloadedLinks or vidTitle in os.listdir(sys.path[0]+'\Downloaded'):
            sg.popup("ALREADY ADDED/DOWNLOADED")
        else:
            listDownloadedLinks.append(values['-INPUT-'])
            downloadLinks = open("TBDownloaded.txt", "a")
            downloadLinks.write(values['-INPUT-'] + "\n")
            downloadLinks.close()
        window['-LIST-'].update(listDownloadedLinks)
    elif event == "START CONVERTING":
        for URL in listDownloadedLinks:
            video = YouTube(URL).streams.filter(only_audio=True).first()
            destination = 'Downloaded'
            outFile = video.download(output_path=destination)
            base, ext = os.path.splitext(outFile)
            newFile = base+'.mp3'
            os.rename(outFile, newFile)
        sg.popup("FILES DOWNLOADED")
    elif event == "CLEAR LIST":
        warningPopup = sg.popup_ok_cancel("ARE YOU SURE?")
        if warningPopup == "OK":
            listDownloadedLinks.clear()
            window['-LIST-'].update(listDownloadedLinks)
        elif warningPopup == "Cancel":
            pass
    elif event == "OPEN DIRECTORY":
        path = sys.path
        subprocess.Popen(r'explorer "{}"'.format(path[0]+'\Downloaded'))

window.close()
