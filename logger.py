__author__ = 'JordSti'



class logger:
    (Normal, Verbose, Debug) = (0, 1, 2)
    def __init__(self, level=Normal):
        self.level = level

    def message(self, msg):
        pass

    def debug(self, msg):
        pass

    def error(self, msg):
        pass


global_output_level = logger.Normal

def set_output_level(level):
    global global_output_level
    global_output_level = level

def get_output_level():
    global global_output_level
    return global_output_level

class console_logger(logger):

    def __init__(self, level=get_output_level()):
        logger.__init__(self, level)


    def message(self, msg):
        if self.level == logger.Verbose or self.level == logger.Debug:
            print msg

    def error(self, msg):
        print "[Error] %s" % msg

    def debug(self, msg):
        if self.level == logger.Debug:
            print "[Debug] %s" % msg

class file_logger(logger):

    def __init__(self, path='log', level=get_output_level()):
        logger.__init__(self, level)
        self.console = console_logger(level)
        self.path = path

    def message(self, msg):
        self.console.message(msg)
        if self.level == logger.Verbose or self.level == logger.Debug:
            fp = open(self.path, 'wa')
            fp.write("%s\n" % msg)
            fp.close()

    def error(self, msg):
        self.console.error(msg)
        fp = open(self.path, 'wa')
        fp.write("[Error] %s\n" % msg)
        fp.close()

    def debug(self, msg):
        self.console.debug(msg)
        if self.level == logger.Debug:
            fp = open(self.path, 'wa')
            fp.write("[Debug] %s\n" % msg)
            fp.close()

class named_file_logger(file_logger):

    def __init__(self, name='Unnamed', path='log', level=get_output_level()):
        file_logger.__init__(self, level, path)
        self.name = name

    def message(self, msg):
        file_logger.message(self, "(%s) %s" % (self.name, msg))

    def error(self, msg):
        file_logger.error(self, "(%s) %s" % (self.name, msg))

    def debug(self, msg):
        file_logger.debug(self, "(%s) %s" % (self.name, msg))
