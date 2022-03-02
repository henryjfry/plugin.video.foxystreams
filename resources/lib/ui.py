from .router import router

import xbmc
import xbmcgui
import xbmcplugin


def build_listitems(names, videos=False):
    listitems = []
    for name in names:
        li = xbmcgui.ListItem(name)
        if videos:
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {
                'title': name,
                'mediatype': 'video',
            })
        listitems.append(li)
    return listitems


def get_user_input(title='Search'):
    return xbmcgui.Dialog().input(title)


def directory_view(names_urls, contexts=False, videos=False, folders=False,
                   more=False, cache=True):
    if names_urls:
        if contexts:
            names, urls, contexts = zip(*names_urls)
        else:
            names, urls = zip(*names_urls)
            contexts = []
        true_list = [folders] * len(names)
        listitems = build_listitems(names, videos=videos)
        for li, context in zip(listitems, contexts):
            li.addContextMenuItems(context)

        items = zip(urls, listitems, true_list)
        #xbmc.log(str(items)+'===>PHIL', level=xbmc.LOGINFO)
        xbmcplugin.addDirectoryItems(handle=router.handle,
                                     items=list(items))
    if videos:
        xbmcplugin.setContent(router.handle, 'videos')
    if more:
        return
    xbmcplugin.endOfDirectory(handle=router.handle, cacheToDisc=cache)


def dialog_select(names):
    listitems = build_listitems(names)
    return xbmcgui.Dialog().select('Select', listitems)


def notify(message):
    xbmc.executebuiltin('Notification(FoxyStreams, {})'.format(message))


def add_torrent(user_debrid, magnet, fn_filter=None):
    dialog = xbmcgui.DialogProgressBG()
    dialog.create('Adding To Debrid')
    status = user_debrid.grab_torrent(magnet, fn_filter=fn_filter)
    dialog.close()
    if status:
        notify('Added Torrent to Debrid')
    else:
        notify('Failed to add to Debrid')
       
def metadata_from(args):
    clearlogo = ''
    if args.get('clearlogo', '') == '' or args.get('clearlogo', '') == None:
        clearlogo = xbmcgui.Window(10000).getProperty('tmdbhelper_clearlogo')
    else:
        clearlogo = args.get('clearlogo', '')

    metadata = {
        'info': {
            'title': args.get('title', ''),
            'plot': args.get('plot', ''),
            'genres': args.get('genre', ''),
            'votes': args.get('votes', ''),
            'rating': args.get('rating', ''),
            'year': args.get('year', ''),
            'mpaa': args.get('mpaa', ''),
            'imdb': args.get('imdb', ''),
            'name': args.get('name', ''),

        },
        'art': {
            'poster': args.get('poster', ''),
            'fanart': args.get('fanart', ''),
            'clearlogo': clearlogo,

        },
    }
    info = metadata['info']
#    xbmc.log(str(args['mode'])+'===>FOXY_STREAMS', level=xbmc.LOGNOTICE)
    if args['mode'] == 'movie':
        info['mediatype'] = 'movie'
        info['movietitle'] = args.get('title', '')
        info['originaltitle'] = args.get('original_title', '')
        info['premiered'] = args.get('premiered', '')
    elif args['mode'] == 'tv':
        info['mediatype'] = 'episode'
        info['episode'] = args.get('episode', '')
        info['season'] = args.get('season', '')
        info['tvshowtitle'] = args.get('showname', '')
        info['originaltitle'] = args.get('showname', '')
        info['aired'] = args.get('aired', '')
    return metadata

