from pytube    import YouTube
from threading import Thread
from os        import remove
from tkinter   import Tk, filedialog, ttk, StringVar, IntVar, PhotoImage
from moviepy.editor import AudioFileClip

Label  = ttk.Label
Button = ttk.Button
Entry  = ttk.Entry
OptionMenu = ttk.OptionMenu
Checkbutton = ttk.Checkbutton



itags = {
    '3072p / 192kbps': 38,
    '1080p / 192kbps': 37,
    '720p / 192kbps' : 22,
    '480p / 480p'    : 35,
    '320p / 128kbps' : 18,
    '240p / 64kbps'  : 5,
    '144p / 24kbps'  : 17
}


def downloadVideo (url: str, quality: str, path: str, filename: str, isMp3: bool, status, downloadButton) :
    downloadButton['state'] = 'disabled'

    status['text'] = 'Status: Searching for video'
    video = YouTube(url)

    status['text'] = 'Status: Getting video file'
    videoStreams = video.streams.filter(file_extension='mp4').get_by_itag(itags[quality])
    if videoStreams :
        status['text'] = 'Status: Downloading'
        videoStreams.download(filename=f'{filename}.mp4', output_path=path)

        if isMp3 :
            status['text'] = 'Status: Converting to .mp3'
            MP4toMP3(f'{path}\\{filename}.mp4', f'{path}\\{filename}.mp3')

        status['text'] = 'Status: Done'

    else :
        status['text'] = 'Status: No file with your preferences found'

    downloadButton['state'] = 'normal'



def MP4toMP3(mp4, mp3):
    file = AudioFileClip(mp4)
    file.write_audiofile(mp3)
    file.close()

    remove(mp4)


class Application :
    def __init__ (self) :
        self.root = Tk()
        self.root.title('Youtube downloader | V1.1')
        self.root.resizable(0, 0)
        self.root.iconphoto(0, PhotoImage(file='icon.png'))

        self.root.tk.call('source', 'theme.tcl')
        self.root.tk.call('set_theme', 'light')

        self.resolutionOptions = ['720p / 192kbps',
            '3072p / 192kbps',
            '1080p / 192kbps',
            '720p / 192kbps',
            '480p / 128kbps',
            '320p / 128kbps',
            '240p / 64kbps',
            '144p / 24kbps']


    def download (self) :
        Thread(target=downloadVideo, args=(self.url.get(), self.res.get(), filedialog.askdirectory(), self.filename.get(), self.isMp3.get(), self.status, self.downloadButton,)).start()


    def run (self) :
        # URL
        Label(self.root, text='URL:').grid(row=0, column=0, padx=15, pady=15)
        self.url = Entry(self.root, width=43)
        self.url.grid(row=0, column=1, columnspan=2, padx=15, pady=15)

        # filename
        Label(self.root, text='Filename:').grid(row=1, column=0, padx=15, pady=15)
        self.filename = Entry(self.root, width=25)
        Label(self.root, text='.mp4').grid(row=1, column=2, padx=15, pady=15)
        self.filename.grid(row=1, column=1, padx=15, pady=15)

        # resolution
        self.res = StringVar()
        OptionMenu(self.root, self.res, *self.resolutionOptions).grid(row=3, column=1, padx=15, pady=15)

        # is mp3
        self.isMp3 = IntVar()
        Checkbutton(self.root, text='Only sound', variable=self.isMp3, onvalue=True, offvalue=False).grid(row=3, column=0, padx=15, pady=15)

        self.status = Label(text='Status: awaiting')
        self.status.grid(row=4, column=0, columnspan=3, padx=15, pady=15)

        # download button
        self.downloadButton = Button(self.root, text='Download', command=self.download)
        self.downloadButton.grid(row=3, column=2, padx=15, pady=15)

        self.root.mainloop()



Application().run()