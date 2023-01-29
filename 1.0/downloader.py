from pytube import YouTube
from tkinter import Tk, filedialog, ttk, StringVar, IntVar
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


def downloadVideo (url: str, quality: str, path: str, filename: str, isMp3: bool) :
    video = YouTube(url)

    if isMp3 :
        videoStreams = video.streams.filter(only_audio=True).get_by_itag(itags[quality])
        videoStreams.download(filename=f'{filename}.mp3', output_path=path)
    else :
        videoStreams = video.streams.filter(file_extension='mp4').get_by_itag(itags[quality])
        videoStreams.download(filename=f'{filename}.mp4', output_path=path)



class Application :
    def __init__ (self) :
        self.root = Tk()
        self.root.title('Youtube downloader')
        self.root.resizable(0, 0)

        self.resolutionOptions = ['720p / 192kbps',
            '3072p / 192kbps',
            '1080p / 192kbps',
            '720p / 192kbps',
            '480p / 128kbps',
            '320p / 128kbps',
            '240p / 64kbps',
            '144p / 24kbps']


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

        self.isMp3 = IntVar()
        Checkbutton(self.root, text='only sound', variable=self.isMp3, onvalue=True, offvalue=False).grid(row=3, column=0, padx=15, pady=15)

        # download button
        Button(self.root, text='Download', command=lambda: downloadVideo(self.url.get(), self.res.get(), filedialog.askdirectory(), self.filename.get(), self.isMp3.get())).grid(row=3, column=2, padx=15, pady=15)

        self.root.mainloop()
        #downloadVideo('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '720p', 'test')

Application().run()