

TEMPLATE_CONTEXT_PROCESSORS = (
    "telecaster.context_processors.host",
)

TELECASTER_MASTER_SERVER = 'teleforma.parisson.com'

TELECASTER_CONF = [{'type':'mp3','server_type':'icecast','conf':'/etc/telecaster/deefuzzer/telecaster_mp3_default.xml', 'port':'8000'},
                   {'type':'webm','server_type':'stream-m','conf':'/etc/telecaster/deefuzzer/telecaster_webm_default.xml', 'port':'8080'}, ]

TELECASTER_RSYNC_SERVER = 'telecaster@jimi.parisson.com:archives/'

TELECASTER_RSYNC_LOG = '/var/log/telecaster/rsync.log'


