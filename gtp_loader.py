#!/usr/bin/env python
#
# gtp_loader.py -- load a postscript file to be used by graphtecprint

import re, sys, os, string
import subprocess

# taken from http://bugs.python.org/file8185/find_in_path.py
def find_in_path(file, path=None):
  """find_in_path(file[, path=os.environ['PATH']]) -> list

  Finds all files with a specified name that exist in the operating system's
  search path (os.environ['PATH']), and returns them as a list in the same
  order as the path.  Instead of using the operating system's search path,
  the path argument can specify an alternative path, either as a list of paths
  of directories, or as a single string seperated by the character os.pathsep.

  If you want to limit the found files to those with particular properties,
  use filter() or which()."""

  if path is None:
    path = os.environ.get('PATH', '')
  if type(path) is type(''):
    path = string.split(path, os.pathsep)
  return filter(os.path.exists,
                map(lambda dir, file=file: os.path.join(dir, file), path))

class loader:
  def __init__(self):  
    all = find_in_path('pstoedit')
    if len(all) < 1:
      raise IOError, "pstoedit not found. Check your installation"
    self.pstoedit = all[0]

  def load(self, file_in):
    if type(file_in) == type(' '):
      file_in = open(file_in, 'r')
    ####
    # pstoedit -dt -f 'hpgl:-pen -pencolors 255'
    # can distinguish 255 colors
    ####
    # pstoedit -dt -f tgif
    # has easily parsable polygons, and colors associated with them.
    ####
    # pic is monochrom.
    ####
    p2 = subprocess.Popen([self.pstoedit,'-dt','-f','tgif'], 
        stdin=file_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (child_out,child_err) = p2.communicate()
    child_err = re.sub('^pstoedit: .*', '', child_err, re.M)
    if not re.match('\s*$', child_err, re.S):
      raise IOError, child_err + "\n\npstoedit failed. Not a postscipt file?"

    self.mstrokes = []   # all, for compat...
    self.cstrokes = {}  # by color
    scale = 3.96
    m = re.search('state\((.*?)\)\.', child_out, re.S)
    state = m.group(1).split(',')
    self.xceil = float(state[36])*scale
    self.yceil = float(state[37])*scale

    for stmt in re.findall('(box|polygon|poly)\((.*?)\)\.', child_out, re.S):
      if stmt[0].startswith('poly'):
        ## both poly and polygon have this format:
        #  color             x1,y1           x2,y2           x3,y3
        # '#0000ff',3,[ 958.485,19.7345,1057.46,1.63843,1037.94,186.666],0,1....
        (color,n,vector) = stmt[1].split(',',2)
        color = color.strip("'")
        vector = re.sub('[\[\s]+','', vector, 0, re.S)  # zap leading [ and any whitespace
        vector = re.sub('\].*$','', vector, 1, re.S)    # zap ] and any remainder.
        vector = [float(i)*scale for i in vector.split(',')]  # convert to double
        vector = zip(                  vector[ ::2], 
                     [self.yceil-v for v in vector[1::2]])   # convert to pairs and flip
        self.mstrokes.append(vector)
        if self.cstrokes.has_key(stmt[0]): self.cstrokes[stmt[0]].append(vector)
        else:                              self.cstrokes[stmt[0]] = [ vector ]
        # print "XXXXX" + repr(vector)

      else:
        ## box has this format:
        #  color        llx,lly         urx,ury   , ignore ...
        # '#0000ff',958.958,186.389,1037.82,19.9229,0,1.87244,1,41,0,0,0,
        (color,llx,lly,urx,ury,dummy) = stmt[1].split(',',5)
        color = color.strip("'")
        llx =            float(llx)*scale
        lly = self.yceil-float(lly)*scale
        urx =            float(urx)*scale
        ury = self.yceil-float(ury)*scale
        vector = [ (llx,lly), (llx,ury), (urx,ury), (urx,lly), (llx,lly) ]
        self.mstrokes.append(vector)
        if self.cstrokes.has_key(stmt[0]): self.cstrokes[stmt[0]].append(vector)
        else:                              self.cstrokes[stmt[0]] = [ vector ]
        # print "yyyyy" + repr(vector)

  def strokes(self, color=None):
    if color is not None:
      return self.cstrokes[color]
    else:
      return self.mstrokes

  def colors(self):
    return self.cstrokes.keys()
  def bbox(self):
    return (0,0,self.xceil,self.yceil)

if __name__ == '__main__':
  print "gtp_loader started"
  l = loader()
  if sys.argv[1] is not None:
    l.load(sys.argv[1])
  else:
    l.load(sys.stdin)
  print "bbox: " + repr(l.bbox())
  sys.exit(0)
