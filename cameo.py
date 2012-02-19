#
# graphtecprint extension for silhouette cameo
#
# (C) 2012 Juergen Weigert (jnweiger@gmail.com)
#

from graphtec_generic import graphtec_dialog

class cameo_dialog(graphtec_dialog):
   # inherit all.
   def __init__(self, datadir):
       print "cameo __init__ BaseClass"
       BaseClass.__init__(self, datadir)

