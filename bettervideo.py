from datetime import datetime
import yt_dlp
import time
import os

# getpath, clearconsole, title =>
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)


def clearConsole(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')
#===========================================#


# helpfunctions - txttime, log =>
t = time.localtime


def txttime():
    return datetime.now().strftime("%Y. %m. %d. - %H:%M:%S")


def vlogToFile(dlink, dtitle, dformat):
    try:
        f = open('log.txt', 'a')
        f.write(f"[{txttime()}] video link: {dlink}\n")
        f.write(f"[{txttime()}] video title: {dtitle}\n")
        f.write(f"[{txttime()}] format: {dformat}\n\n")
        f.close()
    except:
        f.write(f"[{txttime()}] video link: {dlink}\n")
        f.write(f"[{txttime()}] format: {dformat}\n\n")


def plogToFile(dlink, dtitle, dformat):
    f = open('log.txt', 'a')
    f.write(f"[{txttime()}] playlist link: {dlink}\n")
    f.write(f"[{txttime()}] playlist title: {dtitle}\n")
    f.write(f"[{txttime()}] playlist video format: {dformat}\n\n")
    f.close()


asciilogo = """
 /$$                   /$$     /$$                                    /$$       /$$
| $$                  | $$    | $$                                   |__/      | $$
| $$$$$$$   /$$$$$$  /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$  /$$    /$$ /$$  /$$$$$$$  /$$$$$$   /$$$$$$
| $$__  $$ /$$__  $$|_  $$_/|_  $$_/   /$$__  $$ /$$__  $$|  $$  /$$/| $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$  \ $$| $$$$$$$$  | $$    | $$    | $$$$$$$$| $$  \__/ \  $$/$$/ | $$| $$  | $$| $$$$$$$$| $$  \ $$
| $$  | $$| $$_____/  | $$ /$$| $$ /$$| $$_____/| $$        \  $$$/  | $$| $$  | $$| $$_____/| $$  | $$
| $$$$$$$/|  $$$$$$$  |  $$$$/|  $$$$/|  $$$$$$$| $$         \  $/   | $$|  $$$$$$$|  $$$$$$$|  $$$$$$/
|_______/  \_______/   \___/   \___/   \_______/|__/          \_/    |__/ \_______/ \_______/ \______/"""
#===========================================#


def DVideo():
    os.system("title " + "@fema3832")
    isPlaylist = False

    clearConsole()
    print(f"{asciilogo}\n\n")
    ulink = input("link: ")
    if ulink.startswith('https://www.youtube.com/') or ulink.startswith('https://youtu.be/'):
        if ulink.startswith('https://www.youtube.com/playlist?list='):
            isPlaylist = True
            # playlist
            uformat = input("playlist format (v/a): ")

            if uformat in ['video', 'vid', 'v']:
                ydl_opts = {
                    'outtmpl': f'{path}/playlists/%(playlist_title)s/%(title)s.mp4',
                    'format': 'mp4'
                }

            elif uformat in ['audio', 'aud', 'a']:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': f'{path}/playlists/%(playlist_title)s/%(title)s.%(ext)s',
                }

            else:
                ydl_opts = {
                    'outtmpl': f'{path}/playlists/%(playlist_title)s/%(title)s.%(ext)s',
                }
                print(
                    "=== next time, enter a format type, now it will be a video automatically ===")
                time.sleep(5)

        else:
            uformat = input("format (v/a/va/p): ")

            # video
            if uformat in ['v', 'video', 'vid']:
                ydl_opts = {
                    'outtmpl': f'{path}/video/%(title)s.%(ext)s',
                    'format': 'mp4'
                }

            # audio
            elif uformat in ['a', 'audio', 'aud']:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': f'{path}/audio/%(title)s.mp3',
                }

            # audio and video
            elif uformat in ['va', 'audiovideo', 'all', 'av']:
                ydlv = yt_dlp.YoutubeDL(
                    {'outtmpl': f'{path}/video/%(title)s.%(ext)s', 'format': 'mp4'})
                ydla = yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'postprocessors': [
                                        {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192', }], 'outtmpl': f'{path}/audio/%(title)s.%(ext)s'})
                with ydlv:
                    result = ydlv.extract_info(
                        ulink,
                        download=False
                    )
                video = result
                vtitle = video['title']
                vlogToFile(ulink, vtitle, uformat)

                starttime = datetime.now()
                ydlv.download([ulink])
                ydla.download([ulink])
                endtime = datetime.now()

                etime = str(endtime - starttime)
                print(f"\nEstimated time: {etime[:-7]}")
                print("== the function is restarting in 10 seconds ==")
                time.sleep(10)
                clearConsole()
                return DVideo()

            # not valid format
            else:
                print("\nvalid formats: v/a/va/p")
                time.sleep(1)
                return DVideo()

        # video info
        try:
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            with ydl:
                result = ydl.extract_info(
                    ulink,
                    download=False
                )
        except:
            clearConsole()
            print("=== the video or playlist is private or does not exist ===")
            time.sleep(5)
            return DVideo()

        # log section
        video = result
        vtitle = video['title']

        if isPlaylist == False:
            vlogToFile(ulink, vtitle, uformat)
        else:
            plogToFile(ulink, vtitle, uformat)

        starttime = datetime.now()
        ydl.download([ulink])
        endtime = datetime.now()

        etime = str(endtime - starttime)
        print(f"\n\nEstimated time: {etime[:-7]}")
        print("== The function is restarting in 5 seconds ==")
        time.sleep(5)
        clearConsole()
        return DVideo()

    # not valid link
    else:
        print("enter valid link")
        time.sleep(1)
        return DVideo()


DVideo()
