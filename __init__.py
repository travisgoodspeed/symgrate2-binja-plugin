from binaryninja import *

from .Symgrate2 import Symgrate2

def do_nothing(bv,function):
	show_message_box("Do Nothing", "Congratulations! You have successfully done nothing.\n\n" +
					 bv,
                         MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)

PluginCommand.register_for_address("Symgrate2 Plugin", "Basically does nothing", do_nothing)


