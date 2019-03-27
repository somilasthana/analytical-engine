import syslog


def print_me_log(statement="""insight for user""", tag="<>"):
    try:
        print('%s: %s' % (tag, statement))
        syslog.syslog(syslog.LOG_INFO, '%s: %s' % (tag, statement))
    except:
        print("Nothing to print")
        syslog.syslog(syslog.LOG_INFO, "Nothing to print")