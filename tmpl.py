#!/usr/bin/env python3
################################################################################
# File: %%FILEBIG%%
# Date: %%DATE%%
# Author: %%AUTHOR%%
################################################################################
import sys, os, logging, inspect, stat
from functools import partial, wraps
################################################################################

################################################################################
# Global Inits - logging
################################################################################

log_dir=os.path.join( os.path.dirname(os.path.abspath(__file__)).replace('scripts/',''), 'logs' )
if not os.path.isdir( log_dir ): os.mkdir(log_dir)
log_path=os.path.join(log_dir, '%s.log'%(os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]) )
logging.basicConfig(filename=log_path, filemode='w', level=logging.DEBUG)
os.chmod(log_path,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

def pLog(msg, printit=True, logit=True, loglevel='info'):
  'Logger Function'
  if logit: logging.getLogger().__getattribute__(loglevel)(msg)
  if printit:
      sys.stdout.flush()
      sys.stdout.write('%s\n'%msg)

pLog('Writing to logfile: %s'%(log_path))
################################################################################
# Helper Static Functions
################################################################################
def getLines(filename):
    """Return list of lines from file"""
    with open(filename, 'r', errors='ignore') as ff:
        return ff.readlines()


def getopt(clf, ret_val, isbool=False):
    """ Command Line Option input parser"""
    found = []
    def getCLO(flag):
        iindx = sys.argv.index(flag)
        sys.argv.pop(iindx)
        return sys.argv.pop(iindx)
    if isbool: return (clf in sys.argv)
    while clf in sys.argv: found.append(getCLO(clf))
    if found: ret_val = [found, found[0]][int(len(found) == 1)]
    return ret_val


def exit_gracefully(exc, *args, **kwargs):
    """Default Try/Catch Function"""
    ii = inspect.currentframe()
    caller_locals=ii.f_back.f_locals
    func=caller_locals.get('func', None)
    func_args=caller_locals.get('args', None)
    func_kwargs=caller_locals.get('kwargs', None)
    func_name='%s::%s::%s'%(func.__module__,func.__class__,func.__name__)
    pLog('Exception "%s" running "%s" with args:"%s" and kwargs:"%s" '%(exc,func_name,func_args, func_kwargs), loglevel='error')


################################################################################
# Decorators - magic happens if environment variable "DEBUG" is present, try it!
################################################################################
def try_with_fn(func, *args, **kwargs):
  'Try/Catch Function Decorator'
  @wraps(func)
  def wrapper(*args, **kwargs):
    except_fn = kwargs.pop('except_fn', None)
    try:
      return func(*args, **kwargs)
    except Exception as e:
      if except_fn:
          except_fn(e, *args, **kwargs)
      else:
          raise
  return wrapper

def debugMethods(cls):
 'Debug Class Decorator'
 for name, val in vars(cls).items():
   if hasattr(val, '__call__'):
     setattr(cls, name, debug(val))
 return cls

def debug(func=None, *args ):
  'Debug Function Decorator'
  if func is None: return partial(debug)
  if 'DEBUG' not in os.environ: return func
  log = logging.getLogger(func.__module__)
  @wraps(func)
  def wrapper(*args, **kwargs):
    #if len(args)>0:

    prefix='%s:'%(func.__name__)
    try:
        if args[0].__class__.__name__ != 'list':
            prefix='%s::%s:'%(args[0].__class__.__name__,func.__name__)
    except: 
        pass
    msg="Calling: %s: args: %s kwargs: %s"%(prefix,repr(args),repr(kwargs))
    pLog(msg, loglevel='debug')
    retVal=func(*args, **kwargs)
    msg="Returned: %s: %s"%(prefix,retVal)
    return retVal #func(*args, **kwargs)
  return wrapper



def main():
    _usage='Usage: %s -f filename'%(__file__) 
    filename=getopt('-f',None)
    run=%%FILE%%(filename=filename, except_fn=exit_gracefully)
  
################################################################################
class Obj:
  def __init__(self, _name):
    self._name=_name
################################################################################
@debugMethods
class %%FILE%%:
    """%%FILE%% to do stuff"""
    def __init__(self, *args, **kwargs):
        self._handle_args(*args)
        self._handle_kwargs(**kwargs)
        self.run(except_fn=exit_gracefully)


    def __getattr__(self, name):
        """Return class property if it exists, else return None, do not error out"""
        return self.__dict__.get(name, None)


    def _handle_args(self, *args):
        """Placeholder for argument handling"""
        pass


    def _handle_kwargs(self, **kwargs):
        """Update class dict with specified kwargs"""
        self.__dict__.update(kwargs)
  

    @try_with_fn
    def run(self, *args, **kwargs):
        pass
    

################################################################################
if __name__ == '__main__':
   main()
################################################################################
# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
